# -*- coding: utf-8 -*-
import json
import urllib2
import requests
import re
import sys
def copy_json(source):
    if isinstance(source,list):
        target=[]
        length=len(source)
        for i in range(0,length):
            target.append(copy_json(source[i]))
    elif isinstance(source,dict):
        target={}
        for item in source:
            target[item]=copy_json(source[item])
    else:
        target=source
    return target


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
                                copyStruct=copy_json(objStruct[item][''])
                                i=0
                                for subitem in obj[item]:
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
    jsonStruct={"resultCode":"integer,操作结果： 0，操作成功 1，操作失败(操作失败的情况参见统一错误处理)","metaInfo":"string,下一页地址","columns":{"index":"integer,位置号","title":"string,栏目的标题","id":"integer,各聚栏目id","thirdId":"string,第三方栏目id：=15京东秒杀","type":"integer,1-我的应用,2-公共栏目,4-影视自动生成栏目,5-教育自动生成栏目,6-应用自动生成栏目,7-游戏自动生成栏目,8-购物自动生成栏目,9-虚拟栏目,10-混合栏目,11-推荐栏目, 12-京东栏目,99-瀑布流","subType":"integer,type=6或7： 2-下载，3-好评榜，4-游戏榜，5-软件榜，6-新秀榜，7-猜你喜欢  type=9： 91-教育通知区 92-教育频道定制区 93-一键优化 94-我的应用(定制)  95-历史记录(会员中心)-1.2.3新增 type=12： 121-京东购物透传栏目 122-京东家居透传栏目 ","visible":"integer,是否显示栏目（用于控制独家频道是否显示） 1显示，0不显示","titleVisible":"integer,是否显示栏目标题（默认显示） 1显示，0不显示","mediaTitleVisible":"integer,是否显示推荐位主标题（默认显示） 1显示，0不显示","mediaSubTitleVisible":"integer,是否显示推荐位副标题（默认显示） 1显示，0不显示","templateId":"integer,模板id,参考UXD-栏目模板 -1表示动态模板","templateType":"integer,模板类型 1-固定模板、2-普通自定义模板、3-圆形自定义模板、4-动态模板","minColumnRecCount":"integer,栏目推荐媒资数量，默认为0，大于0时生效","sloganVisible":"integer,Slogon是否显示，1显示，0不显示","eduChannelId":"integer,仅type=5时，有效","colHeight":"integer,栏目的高度","recWidth":"integer,推荐位宽度","tiles":[{"index":"integer,位置号","productCode":"string,所属产品,1-影视2-教育3-购物4-应用5-游戏 6-轮播7-直播8-Launcher 9-其他 10-广告 14-嗨唱 16-手机聚好看 18-BOS","typeCode":"string,见公共返回值typeCode说明","subTypeCode":"string,用于存放二级页在业务中的typeCode（OP编排二级页列表中的id）","id":"long,媒资id，不全局唯一","adPosId":"string,如果此推荐位是广告会下发此字段","h5Url":"string,h5跳转url","params":"string,跳转参数json","original":"integer,媒资来源 0-运营编排 1-智能推荐","showInfo":{"title":"string,主标题","subTitle":"string,副标题","voiceTitle":"string,直达词","slogan":"string,在聚享购/聚好用/聚好玩中表示卖点","frontPic":"string,海报","postPic":"string,竖海报","frontPicSmall":"string,小海报","focusPic":"string,获取焦点海报","isSpecialPic":"integer,是否异形图：0-否，1-是","width":"integer,宽度","height":"integer,高度","desc":"string,更多说明（目前主要用于私人影院最下面的文字）","price":"long,价格,单位为厘，vod根据区分单点，1-非单点，0-单点视频","priceVisible":"integer,价格是否显示，1显示，0不显示","score":"string,分数","mark":[{"pos":"integer,1,左上 2,右上 3,左下 4,右下","picUrl":"string,角标url"}],"bgColor1":"string,收藏等特殊推荐位使用的背景色","bgColor2":"string,收藏等特殊推荐位使用的背景色","showMark":"integer,是否显示角标 0-不显示，1-显示","caroPlayMode":"integer,轮播窗/轮播起播模式，0-直接播放，1-点击播放。轮播默认是1，轮播窗默认0","caroSource":"integer,轮播内容来源方式，0-轮播窗口(运营配置)  1-聚看点(猜你喜欢接口，top20)","caroPlainText":"integer,是否纯文本，默认否，0-否 1-是","topHotVisible":"integer,控制近期热点是否展示，默认否，当该值为1时，显示，其他情况均不显示；1.2.2新增","caroMaskMapSource":"integer,1，取推荐位大海报tile.showInfo.frontPic遍历存放到carousel.tile.[i].showInfo.frontPic；默认0"},"appInfo":{"appIcon":"string,应用或游戏icon","downloads":"long,下载次数","packageName":"string,App名称","exParam":"string,应用跳转json","appUrl":"string,h5跳转url","md5Sign":"long,套餐id","versionCode":"long,版本code","categoryName":"string,应用分类,UI没有展示需确认"},"goodsInfo":{"marketPrice":"long,原价，单位为厘","sellPercent":"string,商品已售百分比，不带%"},"vodInfo":{"doubanScore":"string,豆瓣评分","showDetail":"integer,是否直接播放，1是进入详情，0是直接播放","total":"integer,总集数","current":"integer,当前集数","updateMark":"string,更新至第XX集","subColumnId":"string,聚好看二级栏目ID","venderId":"integer,供应商id","vendorName":"string,提供商名称","vipId":[{}],"cardParentRemind":"string,点卡标题","cardRemind":"string,点卡提示","cardDesc":"string,点卡描述图片","episodeIndex":"integer,海报跳转视频的集数","timeLength":"integer,时长","is_fee":"integer,是否付费，1-付费 0-不付费"},"mvodInfo":{"thirdChannelId":"string,手机聚好看直播频道第三方频道","thirdTvChannelId":"string,手机聚好看直播频道第三方电视频道","filters":"string,分类筛选条件  1.2.3新增"},"channel":{"thirdId":"integer,第三方频道id","type":"integer,频道类型，1-轮播，2-直播","subType":"integer,频道子类型， 轮播：0-暂无子类型 直播：1-现场直播，2-电台直播","categoryId":"string,频道所属轮播分类id","vendor":"string,直播间归属运营商，0000-海信,1001-搜狐,1002-爱奇艺,1003-聚享购,1004-CNTV,1005-聚联播,1006-PPTV,1007-优酷,1008-优朋,1009-乐视,1011-腾讯,1012-微信电视,1013-芒果,1014-聚好玩,1015-华数,1016-明流,1017-4k花园","provider":"string,内容提供商","free":"integer,0-收费，1-免费","tollAlone":"long,单点价格id，没有单点价格id在返回值中去掉该段","price":"long,价格，单位是厘（人民币）","priceVaildPeriod":"long,价格有效期，单位小时","isShowChannelInfo":"integer,是否显示频道信息，默认1 枚举值：0-否、1-是, ","channelProductId":"integer,轮播所属产品，默认0 枚举值：0-通用、1-视频、2-教育、3-购物、4-游戏、5-应用, "},"eduInfo":{"total":"integer,总集数","current":"integer,当前集数","updateMark":"string,更新至第XX集"},"carousel":[{}],"carouselInfo":{"videoUrl":"string,视频url","playParams":{"id":"integer,id","name":"string,name","fee":"integer,fee","video_play_url":"string,video_play_url","video_play_param":"string,video_play_param","video_quality":"string,video_quality"},"isJump":"integer,点击小图标后是否跳转： 0-否 1-是","jumpParams":"string,跳转参数（适用于跳转到第三方应用的场景）","buttonMarkWord":"string,按钮提示语，如“点击OK键查看详情”","categoryId":"integer,聚好看媒资分类ID（多个取第一个）","channelId":"integer,聚好学媒资所属频道ID（多个取第一个）","jumpMode":"integer,轮播窗推荐位--跳转模式，默认1  1-大屏播放模式、2-直接跳转模式"},"vipInfo":{"packageVipId":"string,套餐包ID","vipId":"integer,套餐ID","vipWillPass":"integer,即将过期天数","vipDesc":"string,描述"},"topicInfo":{"type":"integer,专题类型, 5-带tab专题、6-翻页专题, 0-其他","desc":"string,专题推荐位描述","descPic":"string,专题推荐位描述图片","star":"string,专题推荐位推荐指数"},"couponInfo":{"useRangeDesc":"string,使用范围描述","useDesc":"string,使用描述","horizontalPic":"string,横版背景图","verticalPic":"string,竖版背景图","remainingNum":"integer,剩余总数量","validStartTime":"long,生效时间（类型：utc时间，单位s）","validEndTime":"long,失效时间（类型：utc时间，单位s）","account":"string,面额","limitNum":"integer,每个用户限领数量","receiveNum":"integer,当前用户已领数量"},"shortMediaInfo":[{"shortMediaId":"long,短视频集锦ID","videoId":"long,Video ID","title":"string,短视频标题","frontPic":"string,海报","frontPicSmall":"string,小海报","focusPic":"string,获取焦点海报"}],"sportsInfo":{"tournamentId":"integer,id","roundType":"integer,比赛阶段： 0-小组赛、1-淘汰赛、2-其他","seasonId":"integer,赛季类型","resource":"integer,赛事内容： 1-赛事预告、2-积分榜、3-射手榜"},"displayMode":"integer,显示模式（1-默认模式、2-会员价模式、3-纯图模式）","gotoInfo":{"gotoType":"integer,0 – 本地； 1 – {htType==single_vip:h5跳转参数；h5Type==user_right_vip:h5会员权益跳转地址}","h5Type":"string,‘’-未选；’all_vip’-全部套餐；’single_vip’-单个套餐；’user_right_vip’-会员权益","jumpParams":"string,跳转参数或地址"},"jdInfo":{"action":"string,拉起跳转时填入的action Intent appIntent = new Intent(action);","data":"string,拉起跳转时填入的data appIntent.setData(Uri.parse(data));"},"naviId":"long,导航id，当typeCode=8008时生效","logInfo":{"":{"curpageid":"string,当前页面id","curpagetype":"string,当前页面类型","objectid":"string,内容id","objecttype":"string,内容类型标识-typeCode","posindex":"string,推荐位index","columnid":"string,栏目id","rowindex":"string,栏目index","original":"string,媒资来源 0 运营 1 推荐 2 搜索 3 用户 4 优惠券 5 外部应用","algid":"string,original为1推荐时相应的算法id，original为其他时此字段为空"}},"songList":[{"index":"integer,索引","id":"long,id","title":"string,歌曲名","singer":[{}],"frontPic":"string,海报","definition":[{}],"thirdPartySongId ":"long,第三方歌曲id，终端用此参进行播放","scoreFlag":"integer,分数标识 1.2.3新增"}],"hcInfo":{},"myExtInfo":{},"showType":"integer,推荐位UI样式，1.2.3新增；0-模板(与模板样式保持一致) 9-个人信息 \t10-卡券相关 \t12-商品(单个商品，商品分类) \t17-全部商品 \t13-权益活动(礼包) \t14-权益海报 \t15-联系我们 \t16-已购套餐 \t20-应用版本 24-推荐套餐","jumpSubTypeCode":"string,1.2.3新增，标记会员中心媒资跳转的subtypecode，系统端内部使用","displaySource":"string,业务优先字段，系统端内部使用"}],"algId":"string,智能推荐栏目算法ID","moreInfo":{},"columnBackImage":"string,栏目背景图","isVodVip":"integer,是否VOD VIP栏目（0-否；1-是） 如果是，则终端会对已购用户强制替换前面三个推荐位数据为VOD已购套餐","backColor1":"string,栏目背景色-渐变色1（本版本仅适用于京东栏目）","backColor2":"string,栏目背景色-渐变色2（本版本仅适用于京东栏目）","orientation":"integer,栏目自定义模板样式， 1-横向 从左到右，2-纵向 从上到下","colMaxSize":"integer,自定义模板：orientation =1时栏目宽度，orientation =2时栏目高度","templateGroup":"string,栏目组合模板","isShowPubdate":"integer,是否显示期数(0-否，1-是)","isShowScore":"integer,是否显示评分(0-否，1-是)","isLineWrap":"boolean,栏目是否换行，默认false，1.2.3新增","colPurpose":"integer,栏目用途colPurpose为“1-付费”时，下发付费视频单片，当栏目用途为“2-单点”时，下发单点视频单片，其他资源类型不做处理。"},"channelrequestid":"string,日志曝光用"}
    obj={"columns":[{"mediaTitleVisible":1,"id":725,"mediaSubTitleVisible":1,"isVodVip":0,"subType":"","templateType":1,"index":4,"isShowPubdate":1,"colHeight":0,"isShowScore":1,"templateId":25,"isLineWrap":0,"tiles":[{"displaySource":"","showType":-1,"subTypeCode":"80062","original":0,"id":"80062","vipInfo":{"vipId":0},"topicInfo":{"desc":"","star":""},"sportsInfo":{"roundType":1,"seasonId":10872,"resource":1,"tournamentId":295},"productCode":"8","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","title":"体育赛事","isSpecialPic":0,"bgColor2":"","voiceTitle":"体育赛事","height":0,"showMark":1,"width":0},"logInfo":{"objecttype":"8006","original":"0","posindex":"1","channelid":"624","objectid":"80062","rowindex":"4","columnid":"725","navid":"92"},"typeCode":"8006","index":1},{"displaySource":"","showType":-1,"subTypeCode":"80062","original":0,"id":"80062","vipInfo":{"vipId":0},"topicInfo":{"desc":"","star":""},"sportsInfo":{"roundType":2,"seasonId":10872,"resource":2,"tournamentId":295},"productCode":"8","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","title":"体育赛事","isSpecialPic":0,"bgColor2":"","voiceTitle":"体育赛事","height":0,"showMark":1,"width":0},"logInfo":{"objecttype":"8006","original":"0","posindex":"2","channelid":"624","objectid":"80062","rowindex":"4","columnid":"725","navid":"92"},"typeCode":"8006","index":2},{"displaySource":"","showType":-1,"subTypeCode":"80062","original":0,"id":"80062","vipInfo":{"vipId":0},"topicInfo":{"desc":"","star":""},"sportsInfo":{"roundType":0,"seasonId":9602,"resource":3,"tournamentId":290},"productCode":"8","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"topHotVisible":0,"subTitle":"","priceVisible":1,"bgColor1":"","title":"体育赛事","isSpecialPic":0,"bgColor2":"","voiceTitle":"体育赛事","height":0,"showMark":1,"width":0},"logInfo":{"objecttype":"8006","original":"0","posindex":"3","channelid":"624","objectid":"80062","rowindex":"4","columnid":"725","navid":"92"},"typeCode":"8006","index":3}],"colPurpose":0,"title":"体育赛事栏目","minColumnRecCount":0,"visible":1,"sloganVisible":1,"titleVisible":1,"recWidth":0,"type":2},{"mediaTitleVisible":1,"id":8949,"mediaSubTitleVisible":1,"isVodVip":0,"subType":"","templateType":4,"index":5,"isShowPubdate":1,"colHeight":360,"isShowScore":1,"templateId":-1,"isLineWrap":0,"tiles":[{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":1,"topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"frontPic":"https:\/\/img-launcher.hismarttv.com\/epgdata\/jhkLauncher\/column\/2018101808133856399365.jpg","subTitle":"","priceVisible":1,"bgColor1":"","isSpecialPic":0,"title":"动漫追番","topHotVisible":0,"bgColor2":"","showMark":1,"height":0,"voiceTitle":"动漫追番","width":0},"logInfo":{"objecttype":"15000","original":"0","posindex":"1","channelid":"624","objectid":"1","rowindex":"5","columnid":"8949","navid":"92"},"typeCode":"15000","index":1},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":2,"topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"frontPic":"https:\/\/img-launcher.hismarttv.com\/epgdata\/jhkLauncher\/column\/2018101808134270651462.jpg","subTitle":"","priceVisible":1,"bgColor1":"","isSpecialPic":0,"title":"动漫追剧-跨平台","topHotVisible":0,"bgColor2":"","showMark":1,"height":0,"voiceTitle":"动漫追剧-跨平台","width":0},"logInfo":{"objecttype":"15000","original":"0","posindex":"2","channelid":"624","objectid":"2","rowindex":"5","columnid":"8949","navid":"92"},"typeCode":"15000","index":2},{"displaySource":"","showType":-1,"subTypeCode":"0","original":0,"id":9,"topicInfo":{"desc":"","star":""},"vipInfo":{"vipId":0},"productCode":"1","vodInfo":{"subColumnId":"0"},"appInfo":{"packageName":""},"showInfo":{"frontPic":"https:\/\/img-launcher.hismarttv.com\/epgdata\/jhkLauncher\/column\/2018101808134739083603.jpg","subTitle":"","priceVisible":1,"bgColor1":"","isSpecialPic":0,"title":"动漫追剧123","topHotVisible":0,"bgColor2":"","showMark":1,"height":0,"voiceTitle":"动漫追剧123","width":0},"logInfo":{"objecttype":"15000","original":"0","posindex":"3","channelid":"624","objectid":"9","rowindex":"5","columnid":"8949","navid":"92"},"typeCode":"15000","index":3}],"colPurpose":0,"title":"动漫追番栏目","minColumnRecCount":0,"visible":1,"sloganVisible":1,"titleVisible":1,"recWidth":240,"type":2},{"mediaTitleVisible":1,"index":6,"id":1472,"isShowScore":1,"isLineWrap":0,"isShowPubdate":1,"minColumnRecCount":0,"title":"聚看点","titleVisible":1,"visible":1,"mediaSubTitleVisible":1,"type":2,"subType":"","sloganVisible":1}],"resultCode":0,"metaInfo":"frontpageNum=3,recpageNum=0","md5": "3ca32a854decb3af89c84ff829e28875", "channelrequestid":"3775dbde-6a98-4b70-95e2-62740c19a56b","signatureServer": "E1F73jN3O7IGzsOGe0mCe9u/7OA2LiVztPAs9KFgKfEPQLmvoIicBA6RdjCDlpSK/5h8IMGx56y8+dwJ4xh4/Q=="}
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
