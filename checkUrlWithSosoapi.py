# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import re
import sys
def copy_json(source):
    return json.loads(json.dumps(source))
    #if isinstance(source,list):
    #    target=[]
    #    length=len(source)
    #    for i in range(0,length):
    #        target.append(copy_json(source[i]))
    #elif isinstance(source,dict):
    #    target={}
    #    for item in source:
    #        target[item]=copy_json(source[item])
    #else:
    #    target=source
    #return target


def check_json_ergodic(obj,objStruct,prefix):
    if isinstance(objStruct,dict) == False:
        objStruct = json.loads(objStruct)
    if isinstance(obj,dict) == False:
        obj = json.loads(obj)
    for item in obj:
        if item in objStruct:
            #存在bug，暂时规避
            if obj[item] == None:
                print item+"返回None"
                continue
            #item在objStruct中
            #如果值是非空数组对象且元素为dict类型，递归回调方法check_json_ergodic
            if isinstance(obj[item],list):
                #print "array"+item
                #判断是否是空数组
                if len(obj[item])>0:                        
                    if isinstance(obj[item][0],dict):
                        if isinstance(objStruct[item],dict):
                            #dict包含''字段
                            if '' in objStruct[item]:
                                i=0
                                for subitem in obj[item]:
                                    copyStruct=copy_json(objStruct[item][''])
                                    check_json_ergodic(subitem,copyStruct,prefix+item+'/'+str(i)+'/')
                                    i=i+1
                                del objStruct[item]['']
                            else:
                                #print "ergodic test array:"+item
                                i=0
                                for subitem in obj[item]:
                                    copyStruct=copy_json(objStruct[item])
                                    check_json_ergodic(subitem,copyStruct,prefix+item+'/'+str(i)+'/')
                                    i=i+1
                                del objStruct[item]
                                #print "ergodic test array:%s finished" % item
                        elif isinstance(objStruct[item],list) and len(objStruct[item])>0 and isinstance(objStruct[item][0],dict):
                            #print "ergodic test array:"+item
                            i=0
                            for subitem in obj[item]:
                                copyStruct=copy_json(objStruct[item][0])
                                check_json_ergodic(subitem,copyStruct,prefix+item+'/'+str(i)+'/')
                                i=i+1
                            del objStruct[item][0]
                            #print "ergodic test array:%s finished" % prefix+item
                        else:
                            print "无法递归测试数组"+prefix+item
                    else:
                        print "%s 数组元素非对象为%s" % (prefix+item,type(obj[item][0]),)
                else:
                    print item+"数组为空"
                #del objStruct[item]
            elif isinstance(obj[item],dict):
                #print "object %s" % item
                #print "ergodic test object:"+item
                #loginfo在icd中存储的是在""字段中
                if "" in objStruct[item] and isinstance(objStruct[item][""],dict):
                    check_json_ergodic(obj[item],objStruct[item][""],prefix+item+'/')
                    del objStruct[item][""]
                elif isinstance(objStruct[item],dict):                
                    check_json_ergodic(obj[item],objStruct[item],prefix+item+'/')
                    del objStruct[item]
                #print "ergodic test object:%s finished" % item
            elif isinstance(obj[item],int):
                #print "integer"+item
                matchIntObj = re.match(r'integer',objStruct[item],re.I)
                matchLongObj = re.match(r'long',objStruct[item],re.I)
                matchBooleanObj = re.match(r'boolean',objStruct[item],re.I)
                if matchBooleanObj:
                    if obj[item] not in [0,1]:
                        print "!!!"+prefix+item+" = "+str(obj[item])+"(int or long),But sosoapi:"+objStruct[item]
                else:
                    if matchIntObj == None and matchLongObj == None:
                        print "!!!"+prefix+item+" = "+str(obj[item])+"(int or long),But sosoapi:"+objStruct[item]
                del objStruct[item]
            elif isinstance(obj[item],str) or isinstance(obj[item],unicode):
                #print "string:"+item
                matchObj = re.match(r'string',objStruct[item],re.I)
                if matchObj == None:
                    print "!!!"+prefix+item+" = "+str(obj[item])+"(string),But sosoapi:"+objStruct[item]
                del objStruct[item]
            else:
                print "!!! "+prefix+item+"类型为"+type(obj[item])+",请在工具中补充"
        else:
            print "!!! "+prefix+item+"字段未在sosoapi中录入" 
    for item in objStruct:
        if isinstance(objStruct[item],str) or isinstance(objStruct[item],unicode):
            print "漏下发字段：\t"+prefix+item+"\t"+objStruct[item]
        else:
            print "漏下发字段：\t"+prefix+item+"\t"+json.dumps(objStruct[item]).decode('unicode_escape')

def check_url(url):
    #获取url的接口名
    searchObj=re.search(r'/\w+\?',url)
    target=searchObj.group()[1:-1]
    with open("sosoapi/"+target,'r') as load_f:
        jsonStruct=json.load(load_f)
    r=requests.get(url)
    obj=json.loads(r.text)
    check_json_ergodic(obj,jsonStruct,"/")

def jsoncompare():
    print 'hello'

if __name__ == '__main__':
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8') 
    url='http://10.18.217.13:30350/onlineApi/columns?appVersionName=2018.5.0.2.28.1&deviceId=86100300900000100000060a48766326&languageId=0&appVersionCode=1500002029&mac=a8%3Aa6%3A48%3A76%3A63%3A26&accessToken=1Z-lehYbOvt7WSpUbacGt590TvBfOyUNvqpD2IIquHXUlXumS1Jo6x-NpqJu8I28q9uTG-2-3Qs-0brGS&logParams=%7B%22eventType%22%3A%22208%22%2C%22appversionname%22%3A%222018.5.0.2.28.1%22%2C%22apiversion%22%3A%2201.102.040%22%2C%22eventcode%22%3A%22208001%22%2C%22license%22%3A%22wasu%22%2C%22deviceid%22%3A%2286100300900000100000060a48766326%22%2C%22appversioncode%22%3A%221500002029%22%2C%22eventPos%22%3A%22001%22%2C%22productcode%22%3A%228%22%2C%22sessionid%22%3A%224a79ffb641424b57b2a99ba7e8c7924e%22%2C%22logstamp%22%3A%2262%22%2C%22requesttime%22%3A%221539841273773%22%2C%22subscriberid%22%3A%22129416980%22%2C%22version%22%3A%222.3%22%2C%22ip%22%3A%22192.168.137.180%22%2C%22devicemsg%22%3A%22LED55MU7000U%22%2C%22customerid%22%3A%225989126%22%7D&timestamp=2522560593000&tabId=252&license=1015&appPackageName=com.jamdeo.tv.vod&appVersion=01.102.040&customerId=599999&area=%25E5%25B1%25B1%25E4%25B8%259C-%25E9%259D%2592%25E5%25B2%259B&metaInfo=&model_id=0&sidebarId=631&subscriberId=129416980&deviceExt=LED55MU7000U&forceRefresh=1&md5=aa47bebcdb69ee6c90e47d8a8262f821&'
    if len(sys.argv)>1:
        check_url(sys.argv[1])
    else:
        print "Expmple:\n"+sys.argv[0] + " " + url
    #jsonStruct1={"resultCode":1}
    #正向测试
    #异常测试1：String-->integer
    #异常测试2：integer-->String
    #异常测试3：子对象元素错误
    #异常测试4：数组子对象元素错误
    #jsonStruct={"resultCode1":"integer,操作结果： 0，操作成功 1，操作失败(操作失败的情况参见统一错误处理)","metaInfo":"string,下一页地址","columns":{"index":"integer,位置号"}}
    #obj={"resultCode":"aaa","metaInfo":"metainfo","columns":{"index":1}}
    #check_json_ergodic(obj,jsonStruct,"")
    #jsonStructObj=json.loads(jsonStruct)
    #print jsonStruct['resultCode']
    
    #check_url(url)
    #r=requests.get(url)
    #response = json.loads(r.text)
    #print response['columns']
    #response = urllib2.urlopen(url)
    #html = response.read()
    #print response
