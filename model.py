#coding:utf-8
import matplotlib
import requests
import numpy as np
from matplotlib.font_manager import *
import matplotlib.pyplot as plt
import os
from multiprocessing.dummy import Pool as ThreadPool
import time
import urllib2,urllib
import re
'''
#解决负号'-'显示为方块的问题  
matplotlib.rcParams['axes.unicode_minus']=False
'''

myfont = FontProperties(fname='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')
class MM:
    def __init__(self):
        self.bing={}
        self.bing_num=[]
        self.zhu={}
        self.zhu_num=[]
        self.baseurl='https://mm.taobao.com/json/request_top_list.htm?page='
        self.pool = ThreadPool(10)
        self.headers={
                'Accept-Language':'zh-CN,zh;q=0.8',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Connection':'close',
                'Referer': 'https://www.baidu.com/'}
    def indexPage(self,index):
        try:
            indexpage=requests.get(self.baseurl+str(index),headers=self.headers)
        except Exception as e:
            print e
        return indexpage.content.decode('GBK')

    def getAlldetail(self,index):
        indexpage=self.indexPage(index)
        p=re.compile(r'class="lady-avatar".*?<img src="(.*?)".*?class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        alldetail=re.findall(p,indexpage)
        eachdetail=[]
        for eachmm in alldetail:
            eachdetail.append(['http:'+eachmm[0],eachmm[1],eachmm[2]+'years old',eachmm[3]])
        
        return eachdetail

    def getImg(self,filename,imgaddr):
        #f=open('mm/'+filename+'/'+filename+'.jpg','wb+') 
        urllib.urlretrieve(imgaddr,'mm/'+filename+'/'+filename+'.jpg')
        #f.write(requests.get(imgaddr,headers=self.headers).content)
        #f.close()

    def getContent(self,filename,content):     
        with open('mm/'+filename+'/'+filename+'.txt','w+') as f:
            for each in content:
                f.write((each.encode('utf-8'))+'\n')

    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            # 如果不存在则创建目录
            print u"新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True                 
        else:       
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建'
            return False

    def savePageInfo(self,index):
        alldetail=self.getAlldetail(index) 
        for eachdetail in alldetail:
            self.mkdir('mm/'+eachdetail[1])       
            self.getImg(eachdetail[1],eachdetail[0])
            self.getContent(eachdetail[1],eachdetail[1:])
    def bing_pic(self,index):
        alldetail=self.getAlldetail(index)
        for eachdetail in alldetail:
            if eachdetail[3] not in self.bing:
                self.bing[eachdetail[3]]=1
            else:
                self.bing[eachdetail[3]]+=1

    def zhu_pic(self,index):
        alldetail=self.getAlldetail(index)
        for eachdetail in alldetail:
            eachdetail=eachdetail[2].replace('years old','')
            if eachdetail not in self.zhu:
                self.zhu[eachdetail]=1
            else:
                self.zhu[eachdetail]+=1
    def start(self):
        while 1: 
            try:
                startpage=int(raw_input('开始查询的页数（整数）：'))
                endpage=int(raw_input('结束的页数（整数）：'))
            except Exception,e:
                print e
            else:
                break

        index=range(startpage,endpage+1)
        begin=time.time()
        try:
            results = self.pool.map(self.savePageInfo,index)
            self.pool.close()
            self.pool.join()
        except Exception as e:
            print e
            pass
        end=time.time()
        total=end-begin
        print '总共耗时：%lf秒' %total

        for i in range(startpage,endpage+1):
            self.zhu_pic(i)
            self.bing_pic(i)

        #柱状图
        for i in self.zhu:
            self.zhu_num.append(self.zhu[i])
        sorted(self.zhu)
        year=[]
        for i in self.zhu:
            year.append(int(i))
        #print year,self.zhu1
        plt.title(u'淘女郎年龄分布图',fontproperties=myfont,size=20)
        plt.xlabel(u'年龄',fontproperties=myfont,size=20)
        plt.ylabel(u'人数',fontproperties=myfont,size=20)
        
        plt.bar(year, self.zhu_num)
        plt.show()

        #饼状图
        for i in self.bing:
            self.bing_num.append(self.bing[i])
        #print self.bing_num
        group=[]
        for i in self.bing:
            group.append(i)
        plt.figure(num=1, figsize=(12, 12))
        plt.axes(aspect=1)
        plt.title(u'淘女郎居住地分布图',fontproperties=myfont,size=20)
        patches,l_text,p_text=plt.pie(self.bing_num,labels=group,autopct = '%3.1f%%',shadow=True, startangle=90) 
        for t in l_text: 
            t.set_fontproperties(matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf")) # 把每个文本设成中文字体
        plt.show()
if __name__=='__main__':
    mm=MM()
    mm.start()
