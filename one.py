#coding: utf-8
 
import string
import urllib2
import re

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
    # 申明相关的属性
    def __init__(self,url):  
        self.myUrl = url + ''
        self.datas = []
        self.myTool = HTML_Tool()
        print u'已经启动ONE爬虫'
  
    # 初始化加载页面并将其转码储存
    def one_content(self):
        # 读取页面的原始信息并将其从gb2313转码
        myPage = urllib2.urlopen(self.myUrl).read().decode("gb2313")
        # 获取该帖的标题
        title = self.find_title(myPage)
        print u'文章名称：' + title
        # 获取最终的数据
        self.save_data(self.myUrl,title,endPage)

    # 用来寻找该帖的标题
    def find_title(self,myPage):
        # 匹配 <h1 class="tit" id="onebd" >XXXX</h1>找出标题
        myMatch = re.search(r'<h1 class="tit" id="onebd" >(.*?)</h1>', myPage, re.S)
        title = u'暂无标题'
        if myMatch:
            title  = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
        return title


    # 用来存储楼主发布的内容
    def save_data(self,url,title,endPage):
        # 加载页面数据到数组中
        self.get_data(url,endPage)
        # 打开本地文件
        f = open(title+'.txt','w+')
        f.writelines(self.datas)
        f.close()
        print u'爬虫报告：文件已下载到本地并打包成txt文件'
        print u'请按任意键退出...'
        raw_input();

    # 获取页面源码并将其存储到数组中
    def get_data(self,url,endPage):
        url = url + '&pn='
        for i in range(1,endPage+1):
            print u'爬虫报告：爬虫%d号正在加载中...' % i
            myPage = urllib2.urlopen(url + str(i)).read()
            # 将myPage中的html代码处理并存储到datas里面
            self.deal_data(myPage.decode('gbk'))
            

    # 将内容从页面代码中抠出来
    def deal_data(self,myPage):
        myItems = re.findall('id="post_content.*?>(.*?)</div>',myPage,re.S)
        for item in myItems:
            data = self.myTool.Replace_Char(item.replace("\n","").encode('gbk'))
            self.datas.append(data+'\n')




# 以某小说贴吧为例子
# bdurl = 'http://tieba.baidu.com/p/2296712428?see_lz=1&pn=1'

print u'请输入贴吧的地址最后的数字串：'
bdurl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/')) 

#调用
mySpider = Baidu_Spider(bdurl)
mySpider.baidu_tieba()

