from common import *
import sxtwl
from nftTest import *

def gan_zhi_he(zhu):    #干支
    gan, zhi = zhu
    if ten_deities[gan]['合'] in zhi5[zhi]:
        return "|"
    return ""

def get_gong_kus(zhis):
    result = []
    for i in range(3):
        zhi1 = zhis[i]
        zhi2 = zhis[i+1]
        if abs(Zhi.index(zhi1) - Zhi.index(zhi2)) == 2:
            value = Zhi[(Zhi.index(zhi1) + Zhi.index(zhi2))//2]
            if value in ("丑", "辰", "未", "戌"):
                result.append(value)
    return result    

def showBazi(gans, zhis):
    baziList = [item[0]+item[1] for item in zip(gans, zhis)]
    print("八字:",' '.join(baziList))   # 八字: 辛丑 辛丑 丁亥 庚子
    print("日元：", gans.day)
    print("月令：", zhis.month)
    print("天干："," ".join(gans))
    print("地支："," ".join(zhis))

def getWuxiScore(gans, zhis):
    # 计算五行分数 http://www.131.com.tw/word/b3_2_14.htm

    scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
    gan_scores = {"甲":0, "乙":0, "丙":0, "丁":0, "戊":0, "己":0, "庚":0, "辛":0,
                "壬":0, "癸":0}   
    me = gans.day

    for item in gans:
        scores[gan5[item]] += 5  # 天干對應五行加5分
        gan_scores[item] += 5       #天干加5分
    # print(scores)

    for item in list(zhis) + [zhis.month]: # 地支加月柱（因為月柱分數雙倍，加兩次分） 戌戌午亥戌
        for gan in zhi5[item]:  # 地支轉天干
            # print(gan,end=' ')
            scores[gan5[gan]] += zhi5[item][gan]  # 天干轉五行
            gan_scores[gan] += zhi5[item][gan]

    # example from http://www.131.com.tw/word/b3_2_14.htm bazi.py 1981 5 24 22 -g

    # gans Gans(year='辛', month='癸', day='壬', time='辛')
    # zhis Zhis(year='酉', month='巳', day='寅', time='亥')

    # gan5 = {"甲":"木", "乙":"木", "丙":"火", "丁":"火", "戊":"土", "己":"土", 
    #         "庚":"金", "辛":"金", "壬":"水", "癸":"水"}

    # 天干分數：
    # 金 +5+5 = 10
    # 木
    # 水 +5+5 = 10
    # 火
    # 土

    # 地支＋月柱：酉巳寅亥巳
    # 地支藏干為 {"辛":8}，{ "丙":5, "戊":2, "庚":1,}，{"甲":5, "丙":2, "戊":1, }，{"壬":5, "甲":3, }，{ "丙":5, "戊":2, "庚":1,}
    # 金 +8+1+1 = 10
    # 木 +5+3 = 8
    # 水 +5 = 5
    # 火 +5+2+5 = 12
    # 土 +2+1+2 = 5

    # 總分：金 20 木 8 水 15 火 12 土 5 ＝ 60

    # 天干分數："甲":8, "乙":0, "丙":12, "丁":0, "戊":5, "己":0, "庚":2, "辛":8, "壬":5, "癸":0}

    me_attrs_ = ten_deities[me].inverse
    strong = gan_scores[me_attrs_['比']] + gan_scores[me_attrs_['劫']] \
        + gan_scores[me_attrs_['枭']] + gan_scores[me_attrs_['印']]

    tenDeitiesStr = ''
    for item in gan_scores:  
        print("{}[{}]-{} ".format(
            item, ten_deities[me][item], gan_scores[item]),  end='  ')
        tenDeitiesStr += "{}[{}]-{}  ".format(
            item, ten_deities[me][item], gan_scores[item])
        
    
    sameValue = 0
    diffValue = 0
    for item in gan_scores:
        if (ten_deities[me][item] in ['枭','印','比','劫']):
            sameValue += gan_scores[item]
        else:
            diffValue += gan_scores[item]
    
    print("五行分數:",scores)
    print("天干分數",gan_scores)
    print("十神", tenDeitiesStr)
    print("身強弱",strong,"(通常>29为强，需要参考月份、坐支等)")
    print('同類值',sameValue)
    print('異類值',diffValue)

    return (scores, tenDeitiesStr, strong, sameValue, diffValue)


def hideGan(gans, zhis):
    resultArr = []
    for item in list(zhis):
        temp=''
        for i in zhi5[item]:
            temp += i
        resultArr.append(temp)
    print('藏干: ', ", ".join(resultArr))
    return ", ".join(resultArr)

def getDeities(gans, zhis):
    gan_shens = []
    me = gans.day
    for seq, item in enumerate(gans):    
        if seq == 2:
            gan_shens.append('--')  # 日柱天干自己不計
        else:
            gan_shens.append(ten_deities[me][item])   # ten_deities[庚][庚]-> 比，ten_deities[庚][丙] -> 杀

    zhi_shens = []
    for item in zhis:
        d = zhi5[item]  # for 戌 return OrderedDict({"戊":5, "辛":2, "丁":1 })，for 午 return ({"丁":5, "己":3, })
        zhi_shens.append(ten_deities[me][max(d, key=d.get)]) 
        # ten_deities[庚][d.key with max value = 戊] -> 枭
        # ten_deities[庚][d.key with max value = 戊] -> 枭
        # ten_deities[庚][d.key with max value = 丁] -> 官

    # print(gan_shens)  # 比 杀 -- 官
    # print(zhi_shens)   # 枭 枭 官 食
    shens = gan_shens + zhi_shens
    # print(shens)
    return (gan_shens, zhi_shens)

def getBaziStrongness(gans, zhis):
    # 计算八字强弱
    weak = True
    me = gans.day
    shens = getDeities(gans, zhis)
    me_status = []
    for item in zhis:
        me_status.append(ten_deities[me][item])
        if ten_deities[me][item] in ('长', '帝', '建'):
            weak = False
    if weak:
        if shens.count('比') + me_status.count('库') >2:
            weak = False

    print('weak', weak)


def getShenSha(gans, zhis, sex):
    resultArr= []
    print("===========神煞==============")
    flag = False
    me = gans.day
    month = zhis.month
    alls = list(gans) + list(zhis)
    zhus = [item for item in zip(gans, zhis)]
    # print(me)
    for items in tianyis[me]:
        for item in items:
            if item in zhis:
                if not flag:
                    print("天乙贵人：", end=' ')
                    resultArr.append("天乙贵人")
                    flag = True
                print(item, end=' ')
            print('\n')
    
    # 玉堂贵人
    flag = False
    for items in yutangs[me]:
        for item in items:
            if item in zhis:
                if not flag:
                    print("| 玉堂贵人：", end=' ')
                    resultArr.append("玉堂贵人")
                    flag = True
                print(item, end=' ')            

    # 天德贵人
    if tiandes[month] in alls:
        print("| 天德贵人：{}".format(tiandes[month]), end=' ') 
        resultArr.append("天德贵人")

    # 月德贵人
    if yuedes[month] in zhis:
        print("| 月德贵人：{}".format(yuedes[month]), end=' ') 
        resultArr.append("月德贵人")

    # 驿马
    if mas[zhis.day] in zhis:
        for seq, item in enumerate(zhis):
            if item == mas[zhis.day]:
                print(ma_zhus[zhus[seq]], zhus[seq])
                resultArr.append(ma_zhus[zhus[seq]])

    # 天罗
    if  nayins[zhus[0]][-1] == '火':			
        if zhis.day in '戌亥':
            print("| 天罗：{}".format(zhis.day), end=' ') 
            resultArr.append("天罗")

    # 地网		
    if  nayins[zhus[0]][-1] in '水土':			
        if zhis.day in '辰巳':
            print("| 地网：{}".format(zhis.day), end=' ')
            resultArr.append("地网")

    # 三奇 (三奇贵人?)
    flag = False
    if ['乙','丙', '丁'] == list(gans[:3]) or ['乙','丙', '丁'] == list(gans[1:]):
        flag = True  
        print("三奇　乙丙丁", end=' ')
        resultArr.append("三奇")
    if ['甲','戊', '庚'] == list(gans[:3]) or ['甲','戊', '庚'] == list(gans[1:]):
        flag = True   
        print("三奇　甲戊庚", end=' ')
        resultArr.append("三奇")
    if ['辛','壬', '癸'] == list(zhis[:3]) or ['辛','壬', '癸'] == list(zhis[1:]):
        flag = True       
        print("三奇　辛壬癸", end=' ')
        resultArr.append("三奇")

    # 学堂分析
    statuses = [ten_deities[me][item] for item in zhis]
    for seq, item in enumerate(statuses):
        if item == '长':
            print("学堂:", zhis[seq], "\t", end=' ')
            resultArr.append("学堂")
            if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
                print("正学堂:", nayins[zhus[seq]], "\t", end=' ')

    # seq = Gan.index(gans.year)
    # if sex:
    #     if seq % 2 == 0:
    #         direction = -1
    #     else:
    #         direction = 1
    # else:
    #     if seq % 2 == 0:
    #         direction = 1
    #     else:
    #         direction = -1

    # for seq, item in enumerate(zhus):
    #     # 检查空亡 
    #     result = "{}－{}".format(nayins[item], '亡') if zhis[seq] == wangs[zhis[0]] else nayins[item]
    #     # 检查劫杀 
    #     result = "{}－{}".format(result, '劫杀') if zhis[seq] == jieshas[zhis[0]] else result
    #     # 检查元辰
    #     result = "{}－{}".format(result, '元辰') if zhis[seq] == Zhi[(Zhi.index(zhis[0]) + direction*-1*5)%12] else result    
    #     print("{1:{0}<15s}".format(chr(12288), result), end='')

    # 羊刃分析
    key = '帝' if Gan.index(me)%2 == 0 else '冠'

    if ten_deities[me].inverse[key] in zhis:
        print("羊刃:", me, ten_deities[me].inverse[key])
        resultArr.append("羊刃")

    # 将星分析
    me_zhi = zhis[2]
    other_zhis = zhis[:2] + zhis[3:]
    flag = False
    tmp_list = []
    if me_zhi in ("申", "子", "辰"):
        if "子" in other_zhis:
            flag = True
            tmp_list.append((me_zhi, '子'))
    elif me_zhi in ("丑", "巳", "酉"):
        if "酉" in other_zhis:
            flag = True   
            tmp_list.append((me_zhi, '酉'))
    elif me_zhi in ("寅", "午", "戌"):
        if "午" in other_zhis:
            flag = True     
            tmp_list.append((me_zhi, '午'))
    elif me_zhi in ("亥", "卯", "未"):
        if "卯" in other_zhis:
            flag = True   
            tmp_list.append((me_zhi, '卯'))

    if flag:
        print("将星: ",tmp_list)
        resultArr.append("将星")

    # 华盖分析
    flag = False
    if me_zhi in ("申", "子", "辰"):
        if "辰" in other_zhis:
            flag = True
    elif me_zhi in ("丑", "巳", "酉"):
        if "丑" in other_zhis:
            flag = True   
    elif me_zhi in ("寅", "午", "戌"):
        if "戌" in other_zhis:
            flag = True     
    elif me_zhi in ("亥", "卯", "未"):
        if "未" in other_zhis:
            flag = True   

    if flag:
        print("华盖 ")
        resultArr.append("华盖") 

    # 咸池 桃花
    print('桃花：',me_zhi, zhis[0])
    flag = False
    taohuas = []
    year_zhi = zhis[0]
    exclude_me_zhis = zhis[:2] + zhis[3:]
    exclude_year_zhis = zhis[1:]
    if me_zhi in ("申", "子", "辰"):
        if "酉" in exclude_me_zhis:
            flag = True
            taohuas.append("酉")
    elif me_zhi in ("丑", "巳", "酉"):
        if "午" in exclude_me_zhis:
            flag = True   
            taohuas.append("午")
    elif me_zhi in ("寅", "午", "戌"):
        if "卯" in exclude_me_zhis:
            flag = True    
            taohuas.append("卯")
    elif me_zhi in ("亥", "卯", "未"):
        if "子" in exclude_me_zhis:
            flag = True   
            taohuas.append("子")

    if year_zhi in ("申", "子", "辰"):
        if "酉" in exclude_year_zhis:
            flag = True
            taohuas.append("酉")
    elif year_zhi in ("丑", "巳", "酉"):
        if "午" in exclude_year_zhis:
            flag = True   
            taohuas.append("午")
    elif year_zhi in ("寅", "午", "戌"):
        if "卯" in exclude_year_zhis:
            flag = True    
            taohuas.append("卯")
    elif year_zhi in ("亥", "卯", "未"):
        if "子" in exclude_year_zhis:
            flag = True   
            taohuas.append("子")

    if flag:
        print("咸池(桃花): ",taohuas, zhis)
        for _ in taohuas:
            resultArr.append("桃花") 

    # 紅鸞 天喜
    if otherTuHua[year_zhi][0] in exclude_year_zhis:
        print("紅鸞：", otherTuHua[year_zhi][0])
        resultArr.append("紅鸞")

    if otherTuHua[year_zhi][1] in exclude_year_zhis:
        print("天喜：", otherTuHua[year_zhi][1])
        resultArr.append("天喜")

    # 禄分析 (禄神?)
    flag = False
    for item in zhus:
        if item in lu_types[me]:
            if not flag:
                print("禄神：",item,lu_types[me][item])
                resultArr.append("禄神") 

    # 文昌贵人
    if wenchang[me] in zhis:
        print("文昌贵人: ", me,  wenchang[me])
        resultArr.append("文昌贵人")   

    # 文星贵人
    if wenxing[me] in zhis:
        print("文星贵人: ", me,  wenxing[me])  
        resultArr.append("文星贵人")   

    # 天印贵人
    if tianyin[me] in zhis:
        print("天印贵人: 此号天印贵，荣达受皇封", me,  tianyin[me])  
        resultArr.append("天印贵人")   

    print("\n===========================")

    return ", ".join(resultArr)


def getGeguk(gans, zhis):
    print("===========格局============")
    ge = ''
    me = gans.day
    if (me, zhis.month) in jianlus:
        print(jianlu_desc)
        print("-"*120)
        print(jianlus[(me, zhis.month)]) 
        print("-"*120 + "\n")
        ge = '建'
        tempStr = '建' 
    #elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
        #print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
    elif (me, zhis.month) in (('甲','卯'), ('庚','酉'), ('壬','子')):
        ge = '月刃'
        tempStr = '月刃' 
    else:
        zhi = zhis[1]
        if zhi in wuhangs['土'] or (me, zhis.month) in (('乙','寅'), ('丙','午'),  ('丁','巳'), ('戊','午'), ('己','巳'), ('辛','申'), ('癸','亥')):
            for item in zhi5[zhi]:
                if item in gans[:2] + gans[3:]:
                    ge = ten_deities[me][item]
        else:
            d = zhi5[zhi]
            ge = ten_deities[me][max(d, key=d.get)]
        tempStr = ge
    print("格局:", ge, '\t', end='\n')
    return tempStr

def getGeguk2(gans, zhis):
    me = gans.day
    yueling = zhis[1]
    hiddenGans = zhi5[yueling]
    print('月令藏干：', hiddenGans)

    for hiddenGan in hiddenGans:
        # nextGan = ''
        firstGan = ''
        secondGan = ''
        for wuhang in wuhangs.values():        
            if hiddenGan[0] in wuhang:
                firstGan, secondGan = wuhang[0:2]
                print('two gans:', firstGan, secondGan)
                # index = wuhang.index(hiddenGan[0])
                # nextGan = wuhang[1-index]
                # print('nextGan :', nextGan)
        # if (hiddenGan[0] in gans) or (nextGan in gans):
        if (firstGan in gans) or (secondGan in gans):
            return ten_deities[me][hiddenGan[0]]
        # elif nextGan in gans:
        #     return ten_deities[me][nextGan]
    return ten_deities[me][list(hiddenGans)[0][0]]

# 甲己合化土　乙庚合化金　丙辛合化水　丁壬合化木　戊癸合化火
# 天干相沖：(+6 相沖)
# 甲庚相沖　乙辛相沖　丙壬相沖　丁癸相沖
# 天干相剋：（pair jump 相剋）
# 甲乙木剋戊己土　丙丁火剋庚辛金　戊己土剋壬癸水　庚辛金剋甲乙木　壬癸水剋丙丁火

def tinGan5hap(gans):
    tempArr = []
    ganList = " ".join(gans)
    print(ganList)
    for key, value in gan_5_hap.items():
        if (key[0] in ganList) and (key[1] in ganList):
            tempArr.append(value)
    if (tempArr == []):
        tempArr.append('無合的關係')
    return ", ".join(tempArr)
    

# 子丑合化土　寅亥合化木　卯戌合化火　辰酉合化金　巳申合化水　午未為陰陽中正合化土

def deizhi6hap(zhis):
    tempArr = []
    zhiList = " ".join(zhis)
    print(zhiList)
    for keys, value in zhi_6_hap.items():
        allTrue = True
        for key in keys:
            if key not in zhiList:
                allTrue = False
        if allTrue:
            tempArr.append(value)
        # if (key[0] in zhiList) and (key[1] in zhiList):
            # tempArr.append(value)

    # 自刑
    for item in zhi_zixings:
        if zhiList.count(item) >= 2:
            tempArr.append(item+'自刑')

    if (tempArr == []):
        tempArr.append('無合的關係')
    return ", ".join(tempArr)
    
    
    # for zhi_ in zhis:
    #     totalZhi = set()
    #     zhi__ = set()
    #     for item in zhis:
    #         for type_ in zhi_atts[zhi_]:
    #             if item in zhi_atts[zhi_][type_]:
    #                 zhi__.add(type_ + ":" + item)    
    #     zhiStr = '  '.join(zhi__)
    #     # print(zhiStr)
    #     totalZhi.add(zhi_+": "+zhiStr)
    #     print(totalZhi)
    # return ""
    

def majorStar(gans, zhis):
    gan_shens, zhi_shens = getDeities(gans, zhis)
    print("主星：",gan_shens)  # 比 杀 -- 官
    print("副星：",zhi_shens)   # 枭 枭 官 食
    return (gan_shens, zhi_shens)

def getHeiShenKeiShen(gans, zhis):
    me = gans.day
    meWuhang = gan5[me]
    (_, _, strong, _, _) = getWuxiScore(gans, zhis)

    if (strong > 29):
        heiShens = wuHangDifferentCategory[meWuhang]
        keiShens = wuHangSameCategory[meWuhang]
    else:
        heiShens = wuHangSameCategory[meWuhang]
        keiShens = wuHangDifferentCategory[meWuhang]

    print("日主五行：", meWuhang)
    print("喜神：", heiShens)
    print("忌神：", keiShens)
    
    return (heiShens, keiShens)


def getLuckyAttributes(gans, zhis):
    (heiShens, _) = getHeiShenKeiShen(gans, zhis)
    luckyColor = [color for shen in heiShens for color in wuHangColor[shen]]
    luckyNumber = [number for shen in heiShens for number in wuHangNumber[shen]]
    luckyNumber.sort()
    luckyDirection = [direction for shen in heiShens for direction in wuHangDirection[shen]]
    print("幸運顏色：", luckyColor)
    print("幸運數字：", luckyNumber)
    print("幸運方位：", luckyDirection)
    return (luckyColor, luckyNumber, luckyDirection)

def getCountZhi(zhis):
    group1 = {"子":0,"午":0,"卯":0,"酉":0}
    group2 = {"辰":0,"戌":0,"丑":0,"未":0}
    for zhi in zhis:
        if zhi in group1.keys():
            group1[zhi] += 1
        if zhi in group2.keys():
            group2[zhi] += 1
    return (group1, group2)

def calculate_attribute_map(gans, zhis):
    attribute_map = [0,0,0,0,0,0,0,0]
    idx = 0
    for gan in gans:
        # print(Gan.index(gan))
        attribute_map[idx] = Gan.index(gan) % 5
        idx += 1

    for zhi in zhis:
        # print(Zhi.index(zhi))
        attribute_map[idx] = Zhi.index(zhi) % 5
        idx += 1

    return attribute_map

def getNFT(gans, zhis):
    parse_config()
    # rt = generate_images("test", 1)
    # attribute_map = [3,1,2,1,2,1,1,1]
    attribute_map = calculate_attribute_map(gans, zhis)
    image_file_name = generate_images("test", 1, attribute_map)
    return image_file_name

def testSxtwl():
    day = sxtwl.fromSolar(2022, 4, 5)
    s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
    print(s)
    # 以春节为界的农历(注getLunarYear如果没有传参，或者传true，是以春节为界的)
    s = "农历:%d年%s%d月%d日" % (day.getLunarYear(), 
        '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
    print(s)
    # 以立春为界的农历
    s = "农历:%d年%s%d月%d日" % (day.getLunarYear(False), 
        '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
    print(s)
    # 以立春为界的天干地支 （注，如果没有传参，或者传false，是以立春为界的。刚好和getLunarYear相反）
    yTG = day.getYearGZ()
    print("以立春为界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
    print("以立春为界的生肖:", ShX[yTG.dz])

    # 当日是否有节气
    if day.hasJieQi():
        print('节气：%s'% jqmc[day.getJieQi()])
        #获取节气的儒略日数
        jd = day.getJieQiJD()
        # 将儒略日数转换成年月日时秒
        t = sxtwl.JD2DD(jd )

        # 注意，t.s是小数，需要四舍五入
        print("节气时间:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
    else:
        print("当天不是节气日")

