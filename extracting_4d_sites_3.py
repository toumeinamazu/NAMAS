#! /usr/bin/env python3

import re
import sys
args = sys.argv



#遺伝子とfastaの指定
gene_fasta=args[1]

#出力ファイルの指定
extraced_4d_fasta=args[2]



## 4_degenerate_site になる アミノ酸
#leucine
LEU='CT'
#valine
VAL='GT'
#serine
SER='TC'
#proline
PRO='CC'
#threonine
THR='AC'
#alanine
ALA='GC'
#Arginine
ARG='CG'
#glycine
GLY='GG'
#リストに格納
C4D=[LEU, VAL, SER, PRO, THR, ALA, ARG, GLY]



fsnm=[]
fssq=[]
flag=0
num=0
with open(f'{gene_fasta}', mode='r') as f:
    for uma in f:
        if '>' in uma:
            flag=1
            fsnm.append(uma)

        if flag==1:
            num+=1      

        if num==2:
            fssq.append(uma)
            flag=0
            num=0

#fsnmに名前を格納
#fssqに配列を格納
    
#fssqに格納された各配列をコドンずつに区切る
cossq=[]
for j in range(len(fssq)):
    shika=re.split('(...)', fssq[j])[1::2]
    cossq.append(shika)

#コドン数
#晴れて4dとなった3塩基目達を格納する部屋
seq4d=[]
for k in range(len(cossq[0])):
    
    theme=cossq[0][k]
    all_codon=[]
    
    #種数
    for l in range(len(cossq)):
        #そもそも含まれてる？
        if l==0:
            if not theme[:2].upper() in C4D:
                break
            else:
                all_codon.append(theme)
        #皆一緒？
        if l>0:
            if not theme[:2]==cossq[l][k][:2]:
                break
            else:
                all_codon.append(cossq[l][k])

    #クリアした者たちの世界
    if len(all_codon)==len(fsnm):
        temp_seq4d=[]
        for m in range(len(all_codon)):
            #0ならリストに追加してね
            if not len(seq4d)==len(fsnm):
                seq4d.append(all_codon[m][2:])
            #もう誰かいるなら後ろに追記してね
            else:
                tempseq=seq4d[m]
                tempseq+=all_codon[m][2:]
                temp_seq4d.append(tempseq)

                if m==len(all_codon)-1:
                    seq4d=temp_seq4d

#出力ファイルに名前を書き込む
with open(f'{extraced_4d_fasta}', mode='w') as g:
    for h in range(len(fsnm)):
        g.write(fsnm[h])
        g.write(seq4d[h])
        g.write('\n')

