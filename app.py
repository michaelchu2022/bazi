
from flask import Flask
from flask import request
from flask import render_template
from markupsafe import Markup
from flask import jsonify


import sxtwl
import datetime
import collections
from bidict import bidict
from datas import *
from sizi import summarys
from common import *
from helper import *
from baziModel import BaziModel

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get("/")
def home():
    return render_template('index.html')


@app.post('/')
def processData():
    birthday = request.form['birthday']
    birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    year = birthday.year
    month = birthday.month
    day = birthday.day
    hour = request.form['hour']
    sex = request.form['sex']
    print(birthday, year, month, day, hour, sex)

    result, nft_file = getResult(year, month, day, hour, int(sex))

    return render_template('index.html', result=Markup(result.__str__()), nft_file=nft_file, birthday=birthday, hour=hour, sex=sex)


@app.post('/api/bazi')
def processApi():
    # error = None
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    hour = request.form['hour']
    print(year, month, day, hour)

    result = getResult(year, month, day, hour)

    return result.toJson()

def getResult(year, month, day, hour, sex):
    Gans = collections.namedtuple("Gans", "year month day time")
    Zhis = collections.namedtuple("Zhis", "year month day time")
    day = sxtwl.fromSolar(
            int(year), int(month), int(day))

    gz = day.getHourGZ(int(hour))
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG = day.getDayGZ()

    if day.hasJieQi():
        print('节气：%s'% jqmc[day.getJieQi()])
        #获取节气的儒略日数
        jd = day.getJieQiJD()
        # 将儒略日数转换成年月日时秒
        t = sxtwl.JD2DD(jd)

        print(t.h, t.m)
        # roundedHour = int(t.h) + 1 if (int(t.m) > 30) else int(t.h)
        # if ( int(hour) < roundedHour ):
        if (int(hour) <= t.h):
            previousDay = day.before(1)
            mTG = previousDay.getMonthGZ()
            if (jqmc[day.getJieQi()] == '立春'):
                yTG = previousDay.getYearGZ()

    gans = Gans(year=Gan[yTG.tg], month=Gan[mTG.tg], 
                day=Gan[dTG.tg], time=Gan[gz.tg])
    zhis = Zhis(year=Zhi[yTG.dz], month=Zhi[mTG.dz], 
                day=Zhi[dTG.dz], time=Zhi[gz.dz])

    (countZhi1, countZhi2) = getCountZhi(zhis)

    (wuxiScore, tenDeities, strong, sameValue, diffValue) = getWuxiScore(gans, zhis)

    print(" ".join(gans))
    print(" ".join(zhis))

    # 藏干
    hiddenGan = hideGan(gans, zhis)

    # getBaziStrongness(gans, zhis)

    (ganShens, zhiShens) = majorStar(gans, zhis)

    # 神煞
    shenSha = getShenSha(gans, zhis, sex)

    # 格局
    geguk = getGeguk(gans, zhis)

    geguk2 = getGeguk2(gans, zhis)
    print("格局2： ", geguk2)

    # 天干五合
    gan5hap = tinGan5hap(gans)

    # 地支六合
    zhi6hap = deizhi6hap(zhis)

    (heiShens, keiShens) = getHeiShenKeiShen(gans, zhis)

    (luckyColor, luckyNumber, luckyDirection) = getLuckyAttributes(gans, zhis)

    nft_file = getNFT(gans, zhis)
    nft_file = nft_file.removeprefix('static/')
    print("nft_file: ",nft_file)
    
    baziModel = BaziModel(gans, zhis, countZhi1, countZhi2, wuxiScore, tenDeities, strong, sameValue, diffValue, 
        hiddenGan, ganShens, zhiShens, shenSha, heiShens, keiShens, 
        geguk, geguk2, gan5hap, zhi6hap, luckyColor, luckyNumber, luckyDirection)
    # print(baziModel)
    return baziModel, nft_file
