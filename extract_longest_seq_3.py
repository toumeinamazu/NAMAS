#! /usr/bin/env python3
# coding: utf-8

# 230123 ver.4.2


# Import modules
from argparse import ArgumentParser
from Bio.Seq import Seq
from Bio import SeqIO
import sys
import re


def get_option():

	argparser = ArgumentParser(usage = "extract_longest_seq.py in.fasta > out.fasta",
							   description = "A pipeline for extracting the longest sequences")
	argparser.add_argument("-v", action="version", version="ver.4.2 (230208)")
	argparser.add_argument("fasta", metavar="in.fasta", type = str, help="Input sequences in fasta format")
	argparser.add_argument("--split", action="store_true", help="If this option added, sequence files will be seperated")
	argparser.add_argument("--source", metavar="STR", type = str, help="Sequence source (refseq, ensembl, other) [refseq]", default="refseq", choices=['refseq', 'ensembl', 'genbank', 'other'])
	argparser.add_argument("--delimiter", metavar="STR", type = str, help="Delimiter letters for detecting isoforms. For this option, use '--source other'", default="geneID=")
	argparser.add_argument("--prefix", metavar="STR", type = str, help="Prefix for output sequences")

	return(argparser.parse_args())


if __name__ == "__main__":

	# Parse options
	args = get_option()

	len_dict = {}
	name_dict = {}

	# delimiterを定義
	if args.source == "refseq":
		args.delimiter = r"(?<=GeneID:)\d+"
	elif args.source == "ensembl":
		args.delimiter = r"(?<=gene:)[\w\.]+"
	elif args.source == "genbank":
		args.delimiter = r"(?<=;Name=)[\w\.]+"
	else:
		args.delimiter = rf"(?<={args.delimiter})[\w\.]+"

	delimiter = re.compile(args.delimiter)

	for seq_record in SeqIO.parse(args.fasta, "fasta"):

		if not delimiter.search(seq_record.description):
			sys.exit(f"ERROR: '{args.delimiter}' does not exist at {seq_record.description}")

		else:
			gene_name = delimiter.search(seq_record.description).group(0)

		if gene_name not in len_dict or len(seq_record) > len_dict[gene_name]:

			len_dict[gene_name] = len(seq_record)
			name_dict[gene_name] = seq_record.description

	# name_dictのキーとバリューを入れ替え
	name_dict_swap = {value: key for key, value in name_dict.items()}

	for seq_record in SeqIO.parse(args.fasta, "fasta"):

		if args.split:

			if seq_record.description in name_dict_swap:

				if len(seq_record) == len_dict[name_dict_swap[seq_record.description]]:

					gene_name = delimiter.search(seq_record.description).group(0)

					with open(f"{gene_name}.fa", "w") as f:
						print(f">{seq_record.description}\n{seq_record.seq}", file = f)

					del name_dict_swap[seq_record.description]

		else:

			if seq_record.description in name_dict_swap:

				if len(seq_record) == len_dict[name_dict_swap[seq_record.description]]:

					gene_name = delimiter.search(seq_record.description).group(0)

					if args.prefix:
						gene_name = f"{args.prefix}_{gene_name}"

					print(f">{gene_name} {seq_record.description}")
					print(seq_record.seq)

					del name_dict_swap[seq_record.description]
