# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 10:15:17 2017

@author: wangq
"""
def intron_input():
    t = True
    AUCG_test = True
    while t and AUCG_test:
        seq = input('Please input your intron sequence...   ')
        seq = seq.upper()
        if len(seq)<26:
            print("Invalid input. [Length of the intron invalid]")
        elif (seq[:2]!="GU" or seq[len(seq)-2:]!="AG"):
                print("Invalid input. [Conserved sequence invalid]")
        else:
            num = 0
            while num<len(seq):
                if seq[num] not in 'AUCG':
                    print("Invalid input. [Nucleotides other than A,U,C,G]")
                    print("Invalid base position:",num)
                    num=100000
                else:
                    num+=1
                    
            if num != 100000:
                print("Your input intron sequence is",seq)
                t=False
                AUCG_test = False
    return seq

intron_input()