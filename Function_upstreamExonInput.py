# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:19:06 2017

@author: wangq
"""

def upstream_exon_input():
    t = True
    ATCG_test = True
    while t and ATCG_test:
        up_ex_seq = input('Please input your upstream exon sequence...   ')
        up_ex_seq = up_ex_seq.upper()
        if len(up_ex_seq)>30:
            print("Invalid input. [Length of the intron invalid]")
        else:
            num = 0
            while num<len(up_ex_seq):
                if up_ex_seq[num] not in 'ATCG':
                    print("Invalid input. [Nucleotides other than A,T,C,G]")
                    print("First Invalid base position:",num)
                    num=100000
                else:
                    num+=1

            if num != 100000:
                print("Your input exon upstream sequence is",up_ex_seq)
                t=False
                ATCG_test = False
    return up_ex_seq

