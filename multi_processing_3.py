#! /usr/bin/env python3
from multiprocessing import Pool
import subprocess
import sys
args = sys.argv



###multi processでnamas_bashを起動する



#which_analysis
WHAL=args[1]

#multi_processの数
MPN=args[2]

#出力ディレクトリを指定
MPT_DIR=args[3]

#TREFILEの指定
TREFILE=args[4]

#尤度比検定の有意水準を指定
PLRTV=args[5]

#raxml用のスレッドを用意
THREADS=args[6]

##並列処理させる関数

#MPNの数値化
MPN=int(MPN)

#定義
if WHAL=='selected_genes_search':
    #namas_paml_3をbashで起動させる、という関数を定義し、引数にTEMP_DIRを読み込ませる
    def namas_bash(x):
        subprocess.run(f'namas_paml_3 {MPT_DIR}/TEMPO_{x} {TREFILE} {PLRTV}', shell=True)

elif WHAL=='phylogenetic_analysis':
    #namas_phylogenetic_analysis_3をbashで起動させる、という関数を定義し、引数にTEMP_DIRを読み込ませる
    def namas_bash(x):
        SPECIESFILE=TREFILE
        BOOTSTRAP=PLRTV
        subprocess.run(f'namas_phylogenetic_analysis_3 {MPT_DIR}/TEMPO_{x} {SPECIESFILE} {BOOTSTRAP} {THREADS}', shell=True)


##並列処理します！
if __name__ == "__main__":
    #プロセス数を設定
    p=Pool(MPN)

    #MPN個の並列演算
    p.map(namas_bash, range(0, MPN)) 
