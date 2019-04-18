# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import re
import sys

def simple_array_compare(arrA,arrB,prefix):
    for itemA in arrA:
        if itemA in arrB:
            arrB.remove(itemA)
        else:
            print "多下发数组元素"+str(item)
    if len(arrB) != 0:
        print "漏下发以下数组元素"+prefix
        print arrB

def compare_arr(arrA,arrB,prefix):
    if len(arrA) > 0 and len(arrB) > 0:
        if type(arrA[0]) == type(arrB[0]):
            #json数组比对
            if isinstance(arrA[0],dict):
                key='id'
                length=len(arrA)
                for i in xrange(length):
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
                            print "多下发数组元素 "+prefix+str(i)+"["+key+"]="+arrA[i][key]+",值为："+json.dumps(arrA[i]).decode("unicode-escape")[0:500]+"..."
                    else:
                        print "数组"+prefix+"元素不含id"
                        return
                for item in arrB:
                    print "漏下发数组元素 "+prefix+"["+key+"]="+arrB[i][key]+"[],值为："+json.dumps(item).decode("unicode-escape")[0:500]+"..."            
            #普通数组比对
            elif isinstance(arrA[0],int) or isinstance(arrA[0],str) or isinstance(arrA[0],unicode):
                simple_array_compare(arrA,arrB,prefix)
            else:
                print "暂不支持的数组元素类型 "+prefix+' '+str(type(arrA[0]))
                
        else:
            print "数组元素类型不一致 "+prefix+' '+str(type(arrA[0])) + "!=" +str(type(arrB[0]))
    else:
        if len(arrA) != len(arrB):
            print "key内容不一致 "+prefix+str(arrA)[0:500]+" != "+str(arrB)[0:500]

def json_compare(jsonA,jsonB,prefix):
    for item in jsonA:
        #判断是否存在
        if item in jsonB:
            #判断类型是否一致
            if type(jsonA[item]) == type(jsonB[item]):
                #case：数组类型处理
                if isinstance(jsonA[item],list):
                    compare_arr(jsonA[item],jsonB[item],prefix+item+'/')
                    del jsonB[item]
                #case:对象类型处理
                elif isinstance(jsonA[item],dict):
                    json_compare(jsonA[item],jsonB[item],prefix+item+'/')
                    del jsonB[item]
                #default:非集合类值直接进行比对
                else:
                    if jsonA[item] != jsonB[item]:
                        print "key内容不一致：\t"+prefix+item+"\t"+str(jsonA[item])+" != " + str(jsonB[item])
                    del jsonB[item]
            else:
                print "类型不一致"+prefix+str(type(jsonA[item]))+"!="+str(type(jsonB[item]))
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
    urlB=url.replace('10.18.217.220','home-launcher-old.')
    url_response_compare(url,urlB)

if __name__ == '__main__':
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8') 
    json_compare(jsonA,jsonB,'/')
    #url_response_compare(urlA,urlB)
    #url_check(urlA)
    if len(sys.argv)>1:
        url_check(sys.argv[1])
    else:
        print "Expmple:\n"+sys.argv[0] + " " + url
