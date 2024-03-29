# -*- coding:utf8 -*-
from __future__ import with_statement
import urllib.request as req
from bs4 import BeautifulSoup
import bs4
import requests
import re
import json
import datetime
import os
from lxml import html
import hashlib
import pandas as pd
import line_notify

#class house_parser():
# Check system time (get date)
currenttime = str(datetime.datetime.now().strftime("%d-%m-%Y")) 
postID = []
price = []
new_postID = []
new_price = []
delete_postID = []
delete_price = []
flag = 0

# Read Line token from file
with open("token.txt", 'r') as tokenfile:
	token=tokenfile.read()
tokenfile.close()

def main():
	# Start Parse 591
	global flag
	# Site be parsed
	url = "https://rent.591.com.tw/?kind=1&order=money&orderType=desc&region=1&section=5&rentprice=5&pattern=3"
	session_requests = requests.session()
	res = session_requests.get(url)
	res.encoding = 'utf-8'

	soup_Daan = BeautifulSoup(res.text,'html.parser')
	tag_Daan_csrfval = soup_Daan.find("meta" , {"name":"csrf-token"})['content']
	tag_Daan_total = soup_Daan.find("div" , {"class":"pull-left hasData"})
	totalitem = int(tag_Daan_total.find('i').string)
	print(totalitem)

	# limit item number in 30 
	# If totalitem bigger than 30, page will change(Every page's item limit in 30)
	# If the page change the data will reload
	# This may cause the same item will apper again and again 
	# And we will parse the duplicate data
	if totalitem > 30:
		totalitem = 30

	# Get json Response
	# this url is the query url that 591 site will send to backend and get a json response back 
	url_search = "https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=1&searchtype=1&order=money&orderType=desc&region=1&section=5&rentprice=5&pattern=3"
	headers = {"X-Requested-With": "XMLHttpRequest","X-CSRF-TOKEN":tag_Daan_csrfval}
	res2 = session_requests.get(url_search, headers=headers)
	data = json.loads(res2.text)
	house_detail_all = data['data'] #get house data
	for house in range(totalitem):
		postID.append(house_detail_all.get('data')[house].get('id'))
		price.append(house_detail_all.get('data')[house].get('price'))

	# Check file exist or not
	# 爬完的資料儲存進檔案
	# 目前採用絕對路徑
	## Best Solution: 改成相對路徑
	filepath =r"C:\\Users\\user\\Desktop\\python\\591_scrapy\\postID_%s.txt" % currenttime
	if os.path.isfile(filepath):
		print("The file postID_%s.txt is here" % currenttime)
		duplicatefilecreate()
		filecompare_newitem()
		filecompare_deleteitem() 
	else:
		print("The file postID_%s.txt isn't here, plz create one" % currenttime)
		filecreate()
	
	# Find new_item and delete_item
	#differnt function 會 return tuple
	different_info=different()
	# new item count
	newitem_size = len(different_info[0])
	# delete item count
	deleteitem_size = len(different_info[2])
	
	print('flag: %d' % flag)
	# Call Line Notify API
	if flag == 0:
		print("Data isn't update")
	elif flag == 1:
		linenotification=line_notify.LineNotify(token)
		for newitemnumber in range(newitem_size):
			detail_url = "https://rent.591.com.tw/rent-detail-%s.html" % different_info[0][newitemnumber]
			detail_price = re.sub(r"^\s+","",different_info[1][newitemnumber])
			linenotification.notify("New House : \n Price is: %s\n URL:\n %s "% (detail_price ,detail_url))
		for deleteitemnumber in range(deleteitem_size):
			detail_url2 = "https://rent.591.com.tw/rent-detail-%s.html" % different_info[2][deleteitemnumber]
			detail_price2 = re.sub(r"^\s+","",different_info[3][deleteitemnumber])
			linenotification.notify("Delete House : \n Price is: %s\n URL:\n %s "% (detail_price2 ,detail_url2))
	else:
		pass

# Create a file to store postID
def filecreate():
	f = open("postID_%s.txt" % currenttime , "w+")
	for postwrite in range(len(postID)):
		f.write("%s price is %s\r\n" % (postID[postwrite],price[postwrite]))
	f.close()

# repeat file exist, create and rename new file 
def duplicatefilecreate():
	f = open("postID_%s_new.txt" % currenttime , "w+")
	for duplicatedata in range(len(postID)):
		f.write("%s price is %s\r\n" % (postID[duplicatedata],price[duplicatedata]))
	f.close()


# Read Different Data
def different():
	# 判斷是否又新的房子等待出租
	# 首先開啟紀錄新房子的檔案
	with open("New_item.txt" , "r") as f1 :
		content = f1.readlines()
		for newhouse in range(len(content)):
			detail_line = content[newhouse]
			detail_post_ID = re.split(' price is ', detail_line)[0] # 取得新房子ID
			detail_price = re.split(' price is ', detail_line)[1]	# 取得新房子price	
			new_postID.append(detail_post_ID) # 將新房子的ID 寫進 new_postID 陣列
			new_price.append(detail_price) # 將新房子的價錢 寫進 new_price 陣列
	f1.close()
	
	with open("Delete_item.txt", "r") as f_readdel:
		content = f_readdel.readlines()
		for deletehouse in range(len(content)):
			detail_line = content[deletehouse]
			detail_post_ID = re.split(' price is ',detail_line)[0] # 取得被刪除的房子ID
			detail_price = re.split(' price is ', detail_line)[1]  # 取得被刪除的房子price
			delete_postID.append(detail_post_ID) # 將被刪除的房子的ID 寫進delete_postID 陣列
			delete_price.append(detail_price)    # 將被刪除的房子的ID 寫進delete_price 陣列
	f_readdel.close()
	# return 四個陣列(tuple)
	return new_postID, new_price, delete_postID, delete_price
	
# 比較新舊檔案的差別，並找出新增的房子
def filecompare_newitem():
	global flag
	# List new item and write to file 
	with open("postID_%s.txt" % currenttime, "r") as file_old:
		old = file_old.readlines()
	file_old.close()
	with open("postID_%s_new.txt" % currenttime, "r") as file_new:
		new = file_new.readlines()
	file_new.close()		
	with open("New_item.txt", 'w') as write_new:
		for line in new:
			if line not in old:
				write_new.write(line)
		write_new.close()
		flag = 1
	return flag
# 比較新舊檔案的差別，並找出刪除的房子
def filecompare_deleteitem():
	global flag
	#print("filecompare_delete: {}".format(flag))	
	with open("postID_%s.txt" % currenttime, "r") as file_old:
		old = file_old.readlines()
	file_old.close()
	with open("postID_%s_new.txt" % currenttime, "r") as file_new:
		new = file_new.readlines()
	file_new.close()
	# List delete item and write to file
	with open("Delete_item.txt", 'w') as write_delete:
		for line in old:
			if line not in new:
				write_delete.write(line)
		write_delete.close()
		flag = 1
	return flag

if __name__ == '__main__':
	#while(1):
	main()
	# Delete old file and rename new file
	filepath2 =r"C:\\Users\\user\\Desktop\\python\\591_scrapy\\postID_%s_new.txt" % currenttime
	if os.path.isfile(filepath2): 
		os.remove("postID_%s.txt" % currenttime)
		print("File Delete!!!")
		os.rename("postID_%s_new.txt" % currenttime,"postID_%s.txt" % currenttime)	
		print("File Rename Finish!!!")
	else:
		pass