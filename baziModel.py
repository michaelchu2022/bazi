class BaziModel:
    def __init__(self, gans, zhis, countZhi1, countZhi2, wuxiScore, tenDeities, strong, sameValue, diffValue, \
        hiddenGan, ganShens, zhiShens, shenSha, heiShens, keiShens, geguk, geguk2, gan5hap, zhi6hap, luckyColor, luckyNumber, luckyDirection):
        self.gans = gans
        self.zhis = zhis
        self.baziList = [item[0]+item[1] for item in zip(gans, zhis)]
        self.renyun=gans.day
        self.yueling=zhis.month
        self.tingan=" ".join(gans)
        self.deizhi=" ".join(zhis)
        self.countZhi1 = countZhi1
        self.countZhi2 = countZhi2
        self.wuxiScore = wuxiScore
        self.tenDeities = tenDeities
        self.strong = strong
        self.sameValue = sameValue
        self.diffValue = diffValue
        self.hiddenGan = hiddenGan
        self.ganShens = ganShens
        self.zhiShens = zhiShens
        self.shenSha = shenSha
        self.heiShens = heiShens
        self.keiShens = keiShens
        self.geguk = geguk
        self.geguk2 = geguk2
        self.gan5hap = gan5hap
        self.zhi6hap = zhi6hap
        self.luckyColor = luckyColor
        self.luckyNumber = luckyNumber
        self.luckyDirection = luckyDirection
    
    def __str__(self):
        resultArray = []
        resultArray.append("八字："+' '.join(self.baziList))
        resultArray.append("日元：" + self.renyun)
        resultArray.append("月令：" + self.yueling)
        resultArray.append("天干：" + self.tingan)
        resultArray.append("地支：" + self.deizhi)
        resultArray.append("地支數1：" + str(self.countZhi1))
        resultArray.append("地支數2：" + str(self.countZhi2))
        resultArray.append("五行分數：" + str(self.wuxiScore))
        resultArray.append("身強弱：" + str(self.strong) + " (通常>29为强，需要参考月份、坐支等)")
        resultArray.append("同類值：" + str(self.sameValue))
        resultArray.append("異類值：" + str(self.diffValue))
        resultArray.append("藏干：" + str(self.hiddenGan))
        resultArray.append("主星：" + " ".join(self.ganShens))
        resultArray.append("副星：" + " ".join(self.zhiShens))
        resultArray.append("神煞：" + str(self.shenSha))
        resultArray.append("喜神：" + " ".join(self.heiShens))
        resultArray.append("忌神：" + " ".join(self.keiShens))
        resultArray.append("格局：" + str(self.geguk))
        resultArray.append("格局2：" + str(self.geguk2))
        resultArray.append("天干五合：" + str(self.gan5hap))
        resultArray.append("地支六合：" + str(self.zhi6hap))
        resultArray.append("十神：" + str(self.tenDeities))
        resultArray.append("咸池桃花數量：" + str(self.shenSha.count('桃花')+self.shenSha.count('紅鸞')+self.shenSha.count('天喜')))
        resultArray.append("幸運顏色：" + ", ".join(self.luckyColor))
        resultArray.append("幸運號碼：" + ", ".join(map(str, self.luckyNumber)))
        resultArray.append("幸運方位：" + ", ".join(self.luckyDirection))
        # resultString = "<br/>".join(resultArray)
        temp = [ "<tr><td>"+row+"</td></tr>" for row in resultArray ]
        resultString = "<table class='table table-striped'>"+"".join(temp)+"</table>"
        return resultString

    def toJson(self):
        return jsonify(
            bazi=' '.join(self.baziList),
            renyun=self.renyun,
            yueling=self.yueling,
            wuxingindex=str(self.wuxiScore),
            tiangan=self.tingan,
            dizhi=self.deizhi,
            canggan=str(self.hiddenGan),
            zhuxing=" ".join(self.ganShens),
            fuxing=" ".join(self.zhiShens),
            shensha=str(self.shenSha),
            


        )
