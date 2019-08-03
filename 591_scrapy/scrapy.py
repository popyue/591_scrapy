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
# Read Line token from file
with open("token.txt", 'r') as tokenfile:
	token=tokenfile.read()
tokenfile.close()

def main():
	#flag = 0
	url = "https://rent.591.com.tw/?kind=1&order=money&orderType=desc&region=1&section=5&rentprice=6&pattern=3"
	session_requests = requests.session()
	res = session_requests.get(url)
	res.encoding = 'utf-8'

	soup_Daan = BeautifulSoup(res.text,'html.parser')
	#print(soup_Daan)
	tag_Daan_csrfval = soup_Daan.find("meta" , {"name":"csrf-token"})['content']
	tag_Daan_total = soup_Daan.find("div" , {"class":"pull-left hasData"})
	totalitem = int(tag_Daan_total.find('i').string)
	print(totalitem)
	if totalitem > 30:
		totalitem = 30

	# Get json Response
	url_search = "https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=1&searchtype=1&order=money&orderType=desc&region=1&section=5&rentprice=6&pattern=3"
	headers = {"X-Requested-With": "XMLHttpRequest","X-CSRF-TOKEN":tag_Daan_csrfval}
	res2 = session_requests.get(url_search, headers=headers)
	data = json.loads(res2.text)
	#print(data.keys())
	house_detail_all = data['data'] #get house data
	for house in range(totalitem):
		print('index house: %d' % house)
		postID.append(house_detail_all.get('data')[house].get('id'))
		price.append(house_detail_all.get('data')[house].get('price'))

	# Check file exist or not
	filepath =r"C:\\Users\\user\\Desktop\\postID_%s.txt" % currenttime
	if os.path.isfile(filepath):
		print("The file postID_%s.txt is here" % currenttime)
		duplicatefilecreate()
		filecompare_newitem()
		filecompare_deleteitem() 
	else:
		print("The file postID_%s.txt isn't here, plz create one" % currenttime)
		filecreate()
	d_info=different()
	# Generate house detail url
	print(d_info)
	print('flag: %d' % flag)
	#detail_price_message = "This House Price is %s" % detail_price # Get House Price
	#print(detail_price_message)
	# Call Line Notify API
	if flag == 0:
		print("Data isn't update")
	elif flag == 1:
		linenotification=line_notify.LineNotify(token)
		for newpost,pricenew in range(len(d_info[0])):
			detail_url = "https://rent.591.com.tw/rent-detail-%s.html" % d_info[0][newpost]
			detail_price = re.sub(r"^\s+","",d_info[1][pricenew])
			linenotification.notify("New House : \n Price is: %s\n URL:\n %s "% (detail_price ,detail_url))
		for delete_post,pricedelete in range(len(d_info[2])):
			detail_url2 = "https://rent.591.com.tw/rent-detail-%s.html" % d_info[2][delete_post]
			detail_price2 = re.sub(r"^\s+","",d_info[3][pricedelete])
			linenotification.notify("Delete House : \n Price is: %s\n URL:\n %s "% (detail_price2 ,detail_url2))
	else:
		pass
# Read Different Data
def different():
	with open("New_item.txt" , "r") as f1 :
		content = f1.readlines()
		for newhouse in range(len(content)):
			detail_line = content[newhouse]
			detail_post_ID = re.split(' price is ', detail_line)[0]
			detail_price = re.split(' price is ', detail_line)[1]
			#print(detail_line)
			new_postID.append(detail_post_ID)
			new_price.append(detail_price)
			#print(type(detail_line))
			#new_info = re.split(' price is ', detail_new[1])
	f1.close()
	
	with open("Delete_item.txt", "r") as f_readdel:
		content = f_readdel.readlines()
		for deletehouse in range(len(content)):
			detail_line = content[deletehouse]
			detail_post_ID = re.split(' price is ',detail_line)[0]
			detail_price = re.split(' price is ', detail_line)[1]
			delete_postID.append(detail_post_ID)
			delete_price.append(detail_price)
	f_readdel.close()

	return new_postID, new_price, delete_postID, delete_price
	

# Create a file to store postID
def filecreate():
	f = open("postID_%s.txt" % currenttime , "w+")
	for postwrite in range(len(postID)):
		#f.write("Post ID is %s\r\n" % postID[j])
		f.write("%s price is %s\r\n" % (postID[postwrite],price[postwrite]))
		filedata = re.findall("postID_%s.txt" % currenttime)
	f.close()
def duplicatefilecreate():
	f = open("postID_%s_new.txt" % currenttime , "w+")
	for duplicatedata in range(len(postID)):
		#f.write("Post ID is %s\r\n" % postID[k])
		f.write("%s price is %s\r\n" % (postID[duplicatedata],price[duplicatedata]))
	f.close()

def filecompare_newitem():
	print("filecompare_new: {}".format(flag))
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

def filecompare_deleteitem():
	print("filecompare_delete: {}".format(flag))	
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
	global flag
	flag = flag + 0
	#while(1):
	main()
	# Delete old file and rename new file
	os.remove("postID_%s.txt" % currenttime)
	print("File Delete!!!")
	os.rename("postID_%s_new.txt" % currenttime,"postID_%s.txt" % currenttime)	
	print("File Rename Finish!!!")