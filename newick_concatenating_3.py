#! /usr/bin/env python3

import os

import sys
args = sys.argv


#ディレクトリの指定
PHY_DIR=args[1]
ALGEPHY=args[2]
ALGEBSP=args[3]


#遺伝子リストの取得
alge_list=os.listdir(f'{PHY_DIR}/GENE_PHYLOGENIES')

#all_genes_phylogeny.treに記入
with open(f'{ALGEPHY}', 'w') as agp:

    #all_genes_bootstrap_pathに記入
    with open(f'{ALGEBSP}', 'w') as agb:

        #各遺伝子ごとのnewickを入手
        for i in range(len(alge_list)):
            gene_name=alge_list[i]

            #なんか変なのを巻き込まないように
            if 'OG' in f'{gene_name}':
                gene_tre_file=f'{PHY_DIR}/GENE_PHYLOGENIES/{gene_name}/{gene_name}_codon_aligned_trimed.fasta.raxml.bestTree'
                gene_bootstrap_path=f'{PHY_DIR}/GENE_PHYLOGENIES/{gene_name}/{gene_name}_codon_aligned_trimed.fasta.raxml.bootstraps'

                #結合(all_genes_phylogeny.tre)
                with open(gene_tre_file) as f:
                    for line in f:
                        agp.write(line)

                #結合(all_genes_bootstrap_path)
                agb.write(gene_bootstrap_path)
                agb.write('\n')
