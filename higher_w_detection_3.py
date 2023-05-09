#! /usr/bin/env python3

import re
import sys
args = sys.argv



CURRENT_DIR=args[1]
NAME=args[2]
OUTPUT=args[3]

MODE='alternative'
PAMLRESULTDIR=f'{CURRENT_DIR}/RESULTS/POSITIVE_SELECTED_GENES/BRANCH'
TREFILE_DIR=f'{CURRENT_DIR}/RESULTS/WHOLE_ORTHOLOGUES_PAML'



RESULTFILE=f'{PAMLRESULTDIR}/{NAME}/{NAME}_{MODE}.txt'
flag=0
num=0
with open(RESULTFILE, mode='r') as f:
    for uma in f:
        if 'w ratios as labels for TreeView:' in uma:
            flag=1
        if flag==1:
            num+=1
        if num==2:
            omegavalue=uma


TREFILE=f'{TREFILE_DIR}/{NAME}/ALLFISH_{NAME}.tre'
with open(TREFILE, mode='r') as f:
    for shika in f:
        # #1のついた種は誰
        shikatrim=re.search('\w+_\w+_\d+ #1', shika)
        shikatrim=shikatrim.group()
        shikatrim=shikatrim.split(' #1')[0]

# #1のついた種のomegaを抽出
shikaomega=omegavalue.split(f'{shikatrim} #')[1].split(' ')[0]
# print(shikaomega)


#その他の種のomegaを抽出
otheromegavalue=omegavalue.replace(f'{shikatrim} #{shikaomega}', '')
otheromega=otheromegavalue.split(f'#')[1].split(' ')[0]
# print(otheromega)

#勝ったら記入してあげるよ
if float(shikaomega) > float(otheromega):
    MESSAGE=f'\n{NAME},{shikaomega},{otheromega}'
    with open(f'{PAMLRESULTDIR}/{OUTPUT}', mode="a") as f:
        for zo in MESSAGE:
            f.write(zo)
