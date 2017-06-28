# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:19:06 2017

@author: wangq
"""

def downstream_exon_input():
    t = True
    ATCG_test = True
    while t and ATCG_test:
        down_ex_seq = input('Please input your upstream exon sequence...   ')
        down_ex_seq = down_ex_seq.upper()
        if len(down_ex_seq)>30:
            print("Invalid input. [Length of the intron invalid]")
        else:
            num = 0
            while num<len(down_ex_seq):
                if down_ex_seq[num] not in 'ATCG':
                    print("Invalid input. [Nucleotides other than A,T,C,G]")
                    print("First Invalid base position:",num)
                    num=100000
                else:
                    num+=1

            if num != 100000:
                print("Your input exon upstream sequence is",down_ex_seq)
                t=False
                ATCG_test = False
    return down_ex_seq

