# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import re
import sys

def json_compare(jsonA,jsonB,prefix):
    for item in jsonA:
	if item in jsonB:
            if isinstance(jsonA[item],list):
                if len(jsonA[item]) == len(jsonB[item]):
                    length = len(jsonA[item])
                    for i in range(0,length):
                        if isinstance(jsonA[item][i],dict):
                            json_compare(jsonA[item][i],jsonB[item][i],prefix+item+'/'+str(i)+'/')
                        else:
                            if jsonA[item][i] != jsonB[item][i]:
                                print "warining: "+prefix+item+" 数组的元素类型非对象,且元素值不一致"
                    del jsonB[item]
                else:
                    print "数组长度不一致:\t"+prefix+item+"\t"+ str(len(jsonA[item]))+"!="+ str(len(jsonB[item]))
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
    urlB=url.replace('10.18.217.220','home-launcher.hismarttv.com')
    url_response_compare(url,urlB)

if __name__ == '__main__':
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8') 
    jsonA={"vodChanType":0,"columns":[{"mediaTitleVisible":1,"id":8953,"mediaSubTitleVisible":1,"isVodVip":0,"tiles":[{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"index":1,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1011,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"voiceTitle":"酷学习-小学数学","topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"酷学习-小学数学","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","showMark":1,"price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"1","channelid":"639","objectid":"1335856","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","id":1335856},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"index":2,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1003,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"voiceTitle":"慈禧身边的女人","topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"慈禧身边的女人","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","showMark":1,"price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"2","channelid":"639","objectid":"1335859","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","id":1335859},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"index":3,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1011,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"voiceTitle":"MAYA：奥迪TT制作全过程","topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"MAYA：奥迪TT制作全过程","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","showMark":1,"price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"3","channelid":"639","objectid":"1335863","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","id":1335863},{"displaySource":"title,subTitle","showType":-1,"subTypeCode":"0","original":0,"index":4,"showInfo":{"slogan":"","width":0,"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","voiceTitle":"测试复仇者联盟2钢铁侠","height":0,"title":"测试复仇者联盟2钢铁侠","mark":[{"pos":2,"markType":"2","picUrl":"https:\/\/pic-shop.hismarttv.com\/epgdata\/ShoppingCornerPic\/FM152059230646647684.png"}],"bgColor2":"","isSpecialPic":0,"score":"5","showMark":1,"price":99010},"topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"3","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"goodsInfo":{"marketPrice":0},"logInfo":{"objecttype":"3001","original":"0","posindex":"4","channelid":"639","objectid":"363","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"3001","id":363}],"templateType":1,"index":1,"titleVisible":1,"colHeight":0,"isShowScore":1,"templateId":7,"isLineWrap":0,"sloganVisible":1,"colPurpose":0,"title":"api0.1栏目推荐资源数量与模板要求一致","minColumnRecCount":4,"visible":1,"displayMode":1,"isShowPubdate":1,"recWidth":0,"type":2}],"resultCode":0,"metaInfo":"","md5": "334fe52724e63dffe1eaf08b7aaaea17", "channelrequestid":"4f8d1f45-e37b-4cd5-b244-ea86d7f3f0ff","signatureServer": "kzfqWcTgk7fAo39FYQ4ksqWaMgi3bjejLjUWlYYGBqNSFgfz0i6mYF7xhu4Ef3mXYNrplWm5Ke8+dkKVnIW1tA=="}
    jsonB={"columns":[{"mediaTitleVisible":1,"id":8953,"mediaSubTitleVisible":1,"isVodVip":0,"subType":"","templateType":1,"index":1,"isShowPubdate":1,"colHeight":0,"isShowScore":1,"templateId":7,"isLineWrap":0,"tiles":[{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":1335856,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1011,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"showMark":1,"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"酷学习-小学数学","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","voiceTitle":"酷学习-小学数学","price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"1","channelid":"639","objectid":"1335856","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","index":1},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":1335859,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1003,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"showMark":1,"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"慈禧身边的女人","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","voiceTitle":"慈禧身边的女人","price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"2","channelid":"639","objectid":"1335859","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","index":2},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":1335863,"params":"","topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"is_fee":0,"category_id":1011,"venderId":1015,"updateMark":"","current":None,"doubanScore":"","showDetail":1,"total":-1,"subColumnId":"0","preload_info":[],"vipId":[]},"appInfo":{"packageName":""},"showInfo":{"width":0,"showMark":1,"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","height":0,"frontPic":"","title":"MAYA：奥迪TT制作全过程","isSpecialPic":0,"bgColor2":"","mark":[],"score":"","voiceTitle":"MAYA：奥迪TT制作全过程","price":0},"logInfo":{"objecttype":"1001","original":"0","posindex":"3","channelid":"639","objectid":"1335863","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"1001","index":3},{"displaySource":"title,subTitle","showType":-1,"subTypeCode":"0","original":0,"id":363,"showInfo":{"slogan":"","width":0,"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","showMark":1,"height":0,"title":"测试复仇者联盟2钢铁侠","mark":[{"pos":2,"markType":"2","picUrl":"https:\/\/pic-shop.hismarttv.com\/epgdata\/ShoppingCornerPic\/FM152059230646647684.png"}],"bgColor2":"","isSpecialPic":0,"score":"5","voiceTitle":"测试复仇者联盟2钢铁侠","price":99010},"topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"3","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"goodsInfo":{"marketPrice":0},"logInfo":{"objecttype":"3001","original":"0","posindex":"4","channelid":"639","objectid":"363","rowindex":"1","columnid":"8953","navid":"252"},"typeCode":"3001","index":4}],"colPurpose":0,"title":"api0.1栏目推荐资源数量与模板要求一致","minColumnRecCount":4,"visible":1,"sloganVisible":1,"titleVisible":1,"recWidth":0,"type":2}],"resultCode":0,"metaInfo":"","md5": "b1e902ac6d60b30aa50795aa4ec9afab", "channelrequestid":"544ebad5-dd11-4fcb-a45b-114be8ccde1e","signatureServer": "gCjXwfXVx/uSjsNs9Iwy/iqdsSKUHHszXjKUlDYBnDEDFkPoDo27OMP3+N2/yyyBEyZwmkwCYxZEJjKMpTr68A=="}
    #json_compare(jsonA,jsonB,'/')
    urlA="http://10.18.217.220/api/columns?appVersionName=2018.5.0.2.28.1&deviceId=86100300900000100000060a48766326&languageId=0&appVersionCode=1500002029&mac=a8%3Aa6%3A48%3A76%3A63%3A26&accessToken=1DM_JNYZdlMqBAATBkHSfwLCcq1nXDq5NMrM__iEaieL7HP5Rep5jtE-8P8bUW2q81N1xpgALVHqvAbZk&logParams=%7B%22eventType%22%3A%22208%22%2C%22appversionname%22%3A%222018.5.0.2.28.1%22%2C%22apiversion%22%3A%2201.102.040%22%2C%22eventcode%22%3A%22208001%22%2C%22license%22%3A%22wasu%22%2C%22deviceid%22%3A%2286100300900000100000060a48766326%22%2C%22appversioncode%22%3A%221500002029%22%2C%22eventPos%22%3A%22001%22%2C%22productcode%22%3A%228%22%2C%22sessionid%22%3A%224a79ffb641424b57b2a99ba7e8c7924e%22%2C%22logstamp%22%3A%2262%22%2C%22requesttime%22%3A%221539841273773%22%2C%22subscriberid%22%3A%22129416980%22%2C%22version%22%3A%222.3%22%2C%22ip%22%3A%22192.168.137.180%22%2C%22devicemsg%22%3A%22LED55MU7000U%22%2C%22customerid%22%3A%225989126%22%7D&timestamp=2522560593000&tabId=252&license=1015&appPackageName=com.jamdeo.tv.vod&appVersion=01.102.040&customerId=599999&area=%25E5%25B1%25B1%25E4%25B8%259C-%25E9%259D%2592%25E5%25B2%259B&metaInfo=&model_id=0&sidebarId=639&subscriberId=129416980&deviceExt=LED55MU7000U&forceRefresh=1&md5=aa47bebcdb69ee6c90e47d8a8262f821&"
    urlB="http://home-launcher.hismarttv.com/api/columns?appVersionName=2018.5.0.2.28.1&deviceId=86100300900000100000060a48766326&languageId=0&appVersionCode=1500002029&mac=a8%3Aa6%3A48%3A76%3A63%3A26&accessToken=1DM_JNYZdlMqBAATBkHSfwLCcq1nXDq5NMrM__iEaieL7HP5Rep5jtE-8P8bUW2q81N1xpgALVHqvAbZk&logParams=%7B%22eventType%22%3A%22208%22%2C%22appversionname%22%3A%222018.5.0.2.28.1%22%2C%22apiversion%22%3A%2201.102.040%22%2C%22eventcode%22%3A%22208001%22%2C%22license%22%3A%22wasu%22%2C%22deviceid%22%3A%2286100300900000100000060a48766326%22%2C%22appversioncode%22%3A%221500002029%22%2C%22eventPos%22%3A%22001%22%2C%22productcode%22%3A%228%22%2C%22sessionid%22%3A%224a79ffb641424b57b2a99ba7e8c7924e%22%2C%22logstamp%22%3A%2262%22%2C%22requesttime%22%3A%221539841273773%22%2C%22subscriberid%22%3A%22129416980%22%2C%22version%22%3A%222.3%22%2C%22ip%22%3A%22192.168.137.180%22%2C%22devicemsg%22%3A%22LED55MU7000U%22%2C%22customerid%22%3A%225989126%22%7D&timestamp=2522560593000&tabId=252&license=1015&appPackageName=com.jamdeo.tv.vod&appVersion=01.102.040&customerId=599999&area=%25E5%25B1%25B1%25E4%25B8%259C-%25E9%259D%2592%25E5%25B2%259B&metaInfo=&model_id=0&sidebarId=639&subscriberId=129416980&deviceExt=LED55MU7000U&forceRefresh=1&md5=aa47bebcdb69ee6c90e47d8a8262f821&"
    #url_response_compare(urlA,urlB)
    #url_check(urlA)
    if len(sys.argv)>1:
        url_check(sys.argv[1])
    else:
        print "Expmple:\n"+sys.argv[0] + " " + url
