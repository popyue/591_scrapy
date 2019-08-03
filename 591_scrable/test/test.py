# Read Different Data
import re
with open("some_output_file.txt" , "r") as f1 :
	content =f1.readlines()
	#content.discard('\n')
	print(type(content))
	print(content)
	detail_info=content[0]
	detail_postID=re.split(' price is', detail_info)
	detail_url= "https://rent.591.com.tw/rent-detail-%s.html" % detail_postID[0]
	detail_price= "This House Price is %s" % detail_postID[1]
	print(detail_url)
	print(detail_price)

with open("token.txt", 'r') as tokenfile:
	token=tokenfile.read()
	print(type(token))