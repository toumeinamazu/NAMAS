#! /usr/bin/env python3
import scipy.stats as sps
import re
import sys
args = sys.argv


PAMLRESULTDIR=args[1]
NAME=args[2]
TESTMODEL=args[3]
LRTV=args[4]


##altとnullのtxtファイルからlnl値を取得し、尤度比検定を実行
kuma=[]
for MODE in 'alternative', 'null':

    RESULTFILE=f'{PAMLRESULTDIR}/{NAME}/{TESTMODEL}/{NAME}_{MODE}.txt'

    with open(RESULTFILE, mode='r') as f:
        for uma in f:
            if 'lnL(ntime:' in uma:
                lnlvalue=uma
                lnlvalue=lnlvalue.split('):')[1].rsplit(' ', 1)[0].strip()
        kuma.append(lnlvalue)

#文字列から数値に変換
altlnl=float(kuma[0])
nulllnl=float(kuma[1])

#有意水準の指定と数値化
LRTV=float(LRTV)

#尤度比検定
CHI2=(altlnl - nulllnl)*2-sps.chi2.ppf(q=LRTV, df = 1)
PVALUE=1-sps.chi2.cdf(x=(altlnl - nulllnl)*2, df = 1)

#勝ったか負けたか教えてね
if CHI2 > 0:
    MESSAGE=f'{NAME}, YOU WIN, pvalue={PVALUE}'
else:
    MESSAGE=f'{NAME}, YOU LOSE, pvalue={PVALUE}'

#結果はDECISION.txtでお知らせするね
with open(f'{PAMLRESULTDIR}/{NAME}/{TESTMODEL}/{NAME}_{TESTMODEL}_DECISION.txt', mode="w") as f:
    for zo in MESSAGE:
        f.write(zo)
