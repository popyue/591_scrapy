<h1> 591 Scrapy </h1>

- Language : python
- Library : 
	- BeautifulSoup (bs4)
	- re
	- requests 

<h3> How to use </h3>

# go to the dir which the 591_scrapy is in
```
python 591_scrapy.py
```

<h3> Content </h3>

- It will parse the 591 租屋網's website (https://rent.591.com.tw/?kind=1&order=money&orderType=desc&region=1&section=5&rentprice=5&pattern=3)
- with the data we get, we will save it to the text file
- we will compare the file everytime we parse and find which data is new and which one is deleted
- Line will notify when data is change

<h3>TO DO LIST</h3>

1. [FUNCTION]Add an argument to let user can key the condition from command line(使用者輸入條件)
2. [BUG]now just parse the 1 page (30 item), we need to parse add data from 591 in the future(讓爬蟲能往後爬其他的頁面但不會有資料重複)
3. [SYSTEM]Deploy to server and run it automatically(需用無限回銓重覆執行)
4. [FUNCTION]修改成更有效率的資料檢查方式(新舊資料比較方式修改)
5. [BUG]Try to parse 591 map site, it will ignore the bug#2, it won't have the page reload problem.

<h3> Reference </h3>

- [python 2個文件內容比對](https://blog.csdn.net/MiaoDaLengShui/article/details/52037473)
- [python 去除空白字串](https://www.delftstack.com/zh-tw/howto/python/how-to-remove-whitespace-in-a-string/)
- [Line Notify API Doc](https://notify-bot.line.me/doc/en/)
- [Line Sticker ID](https://devdocs.line.me/files/sticker_list.pdf)
- [python 并集union, 交集intersection, 差集difference(set檢查內容)](https://blog.csdn.net/lanyang123456/article/details/77596349)
- [puyhon duplicates 清除重複資料](https://ithelp.ithome.com.tw/questions/10189254)
- [使用python讀取txt檔案的內容,並刪除重複的行數方法](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/357800/)
- [Python tutorial to remove duplicate lines from a text file](https://www.codevscolor.com/python-remove-duplicate-lines-text-file/)
- [tuple 操作](https://www.jb51.net/article/47986.htm)
- [591 爬蟲實戰(影片)](https://www.youtube.com/watch?v=zzMRbrOHlrk)
- [Python 使用 Beautiful Soup 抓取與解析網頁資料，開發網路爬蟲教學](https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/2/)
- [BeautifulSoup 提取某个tag标签里面的内容](https://blog.csdn.net/willib/article/details/52246086)
	- ![](/591_scrapy/pic/parsehtmltag.png)
- [Compare two different files line by line in python](https://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python)
- [lib-filecmp](https://docs.python.org/2/library/filecmp.html)
- [lib-beautifulsoup](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)
- [Python爬蟲學習筆記(一) - Requests, BeautifulSoup, 正規表達式](https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%80-beautifulsoup-1ee011df8768)
- [Python 元组](http://www.runoob.com/python/python-tuples.html)
- [python中的全局变量,出现referenced before assignment的解决方案](https://zhouzaibao.iteye.com/blog/559381)
- [Python: BeautifulSoup - get an attribute value based on the name attribute
](https://stackoverflow.com/questions/11205386/python-beautifulsoup-get-an-attribute-value-based-on-the-name-attribute)
	- ![](/591_scrapy/pic/gettag.png)