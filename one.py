#coding: utf-8
 
import string
import urllib2
import re
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),("&nbsp;"," ")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n    ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:  
            x = x.replace(t[0],t[1])  
        return x  
    
class One_Spider:

    def __init__(self):  
        self.datas = {}
        self.myTool = HTML_Tool()
        self.myUrl = {}
        to_vol = (datetime.date.today() - datetime.date(2013, 11, 24)).days + 413
        for i in range(177, to_vol):
            one_m = str(i)
            self.myUrl[one_m] = ('http://hanhan.qq.com/hanhan/one/one' + one_m + 'm.htm#page1')
        print u'已经启动ONE爬虫'
        print self.myUrl
  
    # 初始化加载页面并将其储存
    def one_content(self):
        for one_vol in sorted(self.myUrl.iterkeys()):
            try:
                # 读取页面的原始信息并将其从gbk转码
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                headers = { 'User-Agent' : user_agent } 
                req = urllib2.Request(self.myUrl[one_vol], None, headers)
                myPage = urllib2.urlopen(req, timeout = 5).read().decode("gbk")
                # 获取标题
                title = self.find_title(myPage)
                # 获取最终的数据
                self.deal_data(myPage, one_vol, title)    
            except urllib2.URLError, e:

                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
                else:
                    print 'No exception was raised.'
        self.save_data()

    # 用来寻找标题
    def find_title(self, myPage):
        # 匹配 <h1 class="tit" id="onebd" >XXXX</h1>找出标题
        myMatch = re.search(r'<h1 class="tit" id="onebd" >(.*?)</h1>', myPage, re.S)
        title = u'暂无标题'
        if myMatch:
            title  = myMatch.group(1)
        else:
            print u'无法加载文章标题！'
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
        print title
        return title


    # 用来存储内容
    def save_data(self):
        # 打开本地文件
        f = open('one_is_all.txt', 'a')
        for one_vol in sorted(self.datas.iterkeys()):
            f.write(one_vol)
            f.write(self.datas[one_vol])
        f.close()
        print u'爬虫报告：文件已下载到本地并打包成txt文件'
        print u'请按任意键退出...'
        raw_input();

    # 将内容从页面代码中抠出来
    def deal_data(self, myPage, one_vol, title):
        article = re.search(r'<div class="neirong" id="picIdbd" >(.*?)</div>',myPage,re.S).group(1)
        #print article, type(article)
        data = title + "\n" + self.myTool.Replace_Char(article.replace("\n",""))
        self.datas[one_vol] = data+'\n'
        print "已爬到vol{0}\n".format(one_vol)


#调用
mySpider = One_Spider()
mySpider.one_content()

