#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import wx #pip install wxPython
import time
import hashlib #pip install hashlib
import requests #pip install requests
import re
from urllib import parse

salt=int(time.time())
appid=
miyao=''  #百度翻译密钥

def md5(str1):
    a=hashlib.md5()
    a.update((str(str1)).encode(encoding='utf-8'))
    return a.hexdigest()

def tran(text):
    print (text)
    sign='%s%s%s%s'%(appid,str(text),salt,miyao)
    sign=md5(sign)  #MD5加密
    # text=str(text)
#    text=parse.quote(text)
    print (text)
    url='http://api.fanyi.baidu.com/api/trans/vip/translate?q=%s&from=auto&to=en&appid=20160727000025884&salt=%s&sign=%s'%(text,salt,sign)
    html=requests.get(url).content
    html = html.decode('utf8')
    text = re.findall('"dst":"([\s\S]*?)"',html)[0]
    
    
    if text:
        sign='%s%s%s%s'%(appid,str(text),salt,miyao)
        sign=md5(sign)
        url_fy='http://api.fanyi.baidu.com/api/trans/vip/translate?q=%s&from=auto&to=zh&appid=20160727000025884&salt=%s&sign=%s'%(text,salt,sign)
        html_fy=requests.get(url_fy).content
        html_fy = html_fy.decode('utf8')
        result=re.findall('"dst":"([\s\S]*?)"}]}',html_fy)[0]
        result = result.encode('utf-8').decode('unicode_escape')
        print (result)
        if result:
            contents2.AppendText(result+'\n')
            
        else:
            wx.MessageBox(u"出错了，请确认网络连接是否正常")
    # return result

def go(event):
    contents2.Clear()  #清空内容
    text=contents1.GetValue()  #获取contents1里的内容
    if text:
        text1=text+"\n"
        #text1=text1.replace("\n", "")
        #tran(text1)
        # abc = "在此之前，尽管CarPlay可以将iPhone的屏幕投射到车机屏幕上，使用手机内置的音乐播放器等功能，但地图依然只能局限于苹果原生地图，自然不如高德等第三方应用适合中国道路，体验也会大打折扣。"
        # tran(abc)
        # print (text1)
        text_list = re.findall('(.*?)\s+',text1)
        for text in text_list:
            tran(text)

    else:
        wx.MessageBox(u"错误提示，检测内容为空，请填入需要伪原创的文章内容")

if __name__=="__main__":
    app = wx.App()
    win = wx.Frame(None,title = "1", size=(1200,600))
    win.Show()
    contents1 = wx.TextCtrl(win, pos = (5,5),size = (500,600), style = wx.TE_MULTILINE | wx.TE_RICH)
    contents2 = wx.TextCtrl(win, pos = (650,5),size = (500,600), style = wx.TE_MULTILINE | wx.TE_RICH)
    loadButton = wx.Button(win, label = 'start>>',pos = (515,310),size = (120,40))
    loadButton.Bind(wx.EVT_BUTTON,go)  #这个按钮绑定 tran 这个函数
    app.MainLoop()
    
