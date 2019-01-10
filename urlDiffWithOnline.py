# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import re
import sys

def compare_arr(arrA,arrB,prefix):
    key='id'
    length=len(arrA)
    for i in xrange(length):
        if isinstance(arrA[i],dict) == False:
            print prefix+"该数组的元素非对象"
            return
        if key in arrA[i]:
            target=-1
            for j in xrange(len(arrB)):
                if key in arrB[j] and int(arrB[j][key])==int(arrA[i][key]):
                    target=j
                    itemB=json.loads(json.dumps(arrB[j]))
                    json_compare(arrA[i],itemB,prefix+str(i)+'/')
                    del arrB[j] 
                    break
            if target == -1:
                print "多下发数组元素 "+prefix+str(i)+"/,值为："+json.dumps(arrA[i]).decode("unicode-escape")[0:500]+"..."
        else:
            print "数组"+prefix+"元素不含id"
            return
    for item in arrB:
        print "漏下发数组元素 "+prefix+"[],值为："+json.dumps(item).decode("unicode-escape")[0:500]+"..."
        

def json_compare(jsonA,jsonB,prefix):
    for item in jsonA:
	if item in jsonB:
            if isinstance(jsonA[item],list):
                if len(jsonA[item]) == len(jsonB[item]):
                    compare_arr(jsonA[item],jsonB[item],prefix+item+'/')
                    #length = len(jsonA[item])
                    #for i in range(0,length):
                    #    if isinstance(jsonA[item][i],dict):
                    #        json_compare(jsonA[item][i],jsonB[item][i],prefix+item+'/'+str(i)+'/')
                    #    else:
                    #        if jsonA[item][i] != jsonB[item][i]:
                    #            print "warining: "+prefix+item+" 数组的元素类型非对象,且元素值不一致"
                    del jsonB[item]
                else:
                    print "数组长度不一致:\t"+prefix+item+"\t"+ str(len(jsonA[item]))+"!="+ str(len(jsonB[item]))
                    compare_arr(jsonA[item],jsonB[item],prefix+item+'/')
                    del jsonB[item]
            elif isinstance(jsonA[item],dict):
                json_compare(jsonA[item],jsonB[item],prefix+item+'/')
                del jsonB[item]
            else:
                if jsonA[item] != jsonB[item]:
                    print "key内容不一致：\t"+prefix+item+"\t"+str(jsonA[item])+" != " + str(jsonB[item])
                del jsonB[item]
        else:
            print "多下发字段：\t"+prefix+item+"\t"+"homeportal["+prefix+item+"] = "+str(jsonA[item])
    #遍历输出jsonB中的字段，即本次少下发的字段
    for item in jsonB:
        if jsonB[item] != [] and jsonB[item] != {}:
	    print "漏下发字段：\t"+prefix+item+"\t"+"老Online["+prefix+item+"] = "+str(jsonB[item])

def url_response_compare(urlA,urlB):
    rA=requests.get(urlA)
    jsonA=json.loads(rA.text)
    rB=requests.get(urlB)
    jsonB=json.loads(rB.text)
    json_compare(jsonA,jsonB,'/')

def url_check(url):
    urlB=url.replace('10.18.217.220','home-launcher-old')
    url_response_compare(url,urlB)

if __name__ == '__main__':
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8') 
    #json_compare(jsonA,jsonB,'/')
    urlA="http://10.18.217.220/api/columns?appVersionName=2018.5.0.2.28.1&deviceId=86100300900000100000060a48766326&languageId=0&appVersionCode=1500002029&mac=a8%3Aa6%3A48%3A76%3A63%3A26&accessToken=1DM_JNYZdlMqBAATBkHSfwLCcq1nXDq5NMrM__iEaieL7HP5Rep5jtE-8P8bUW2q81N1xpgALVHqvAbZk&logParams=%7B%22eventType%22%3A%22208%22%2C%22appversionname%22%3A%222018.5.0.2.28.1%22%2C%22apiversion%22%3A%2201.102.040%22%2C%22eventcode%22%3A%22208001%22%2C%22license%22%3A%22wasu%22%2C%22deviceid%22%3A%2286100300900000100000060a48766326%22%2C%22appversioncode%22%3A%221500002029%22%2C%22eventPos%22%3A%22001%22%2C%22productcode%22%3A%228%22%2C%22sessionid%22%3A%224a79ffb641424b57b2a99ba7e8c7924e%22%2C%22logstamp%22%3A%2262%22%2C%22requesttime%22%3A%221539841273773%22%2C%22subscriberid%22%3A%22129416980%22%2C%22version%22%3A%222.3%22%2C%22ip%22%3A%22192.168.137.180%22%2C%22devicemsg%22%3A%22LED55MU7000U%22%2C%22customerid%22%3A%225989126%22%7D&timestamp=2522560593000&tabId=252&license=1015&appPackageName=com.jamdeo.tv.vod&appVersion=01.102.040&customerId=599999&area=%25E5%25B1%25B1%25E4%25B8%259C-%25E9%259D%2592%25E5%25B2%259B&metaInfo=&model_id=0&sidebarId=639&subscriberId=129416980&deviceExt=LED55MU7000U&forceRefresh=1&md5=aa47bebcdb69ee6c90e47d8a8262f821&"
    #url_response_compare(urlA,urlB)
    #url_check(urlA)
    if len(sys.argv)>1:
        url_check(sys.argv[1])
    else:
        print "Expmple:\n"+sys.argv[0] + " " + url
