#! /usr/bin/env python3

import os
import sys
args = sys.argv



###multi processで処理する前準備



#multi_processの数
MPN=args[1]

#トリム済みのコドンアライメントIDが格納されてるディレクトリの指定
AGL_PATH=args[2]

#出力ディレクトリの指定
PAML_DIR=args[3]



##codemlを実行する遺伝子数とIDを取得
#全遺伝子のID取得
AGL=os.listdir(AGL_PATH)
AGL.sort()

#遺伝子数の取得
algnum=len(AGL)

#以下の式で遺伝子達をmulti_process用に分割したい
# algnum=(OPGN+1)*adgenum+OPGN*(MPN-adgenum)

#MPNの数値化
MPN=int(MPN)

OPGN=algnum//MPN
adgenum=algnum%MPN

#まずOPGN+1個に分けるリストとOPGN個に分けるリストで分割する（sepは区切りの位置）
sep=(OPGN+1)*adgenum

#リストの前側（一リストにOPGN+1個の要素×adgenum）
agl_at=AGL[:sep]

#リストの前側をadgenumに分割し、一つのリストにまとめる
AGLSL=list()
for i in range(0, len(agl_at), OPGN+1):
    AGLSL.append(agl_at[i:i+OPGN+1])


#リストの後側（一リストにOPGN個の要素×(MPN-adgenum)）
agl_ps=AGL[sep:]

#リストの後側をMPN-adgenumに分割し、一つのリストにまとめる
for i in range(0, len(agl_ps), OPGN):
    AGLSL.append(agl_ps[i:i+OPGN])


##作成したリストをtxtファイルとして各TEMP_DIRに投げる
for j in range(0, MPN):
    with open(f'{PAML_DIR}/TEMPO_{j}/temp_{j}_gene_list.txt', 'w') as f:
        for k in AGLSL[j]:
            f.write("%s\n" % k)