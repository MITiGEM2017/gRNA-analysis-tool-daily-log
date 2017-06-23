# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:48:16 2017

@author: wangq
"""

#Factors of the System
# 1. Secondary Structure of intron and gRNA
# 2. Off-target binding
# 3. CG distribution
# 4. location on Cas13a
# 5. Competition of proteins at the site
# 6. Location of activator/repressor


#User input intron sequence
# 5' GU 
# 3' AG
# Polyprimidine 
# AUCG

t = True
AUCG_test = True
while t and AUCG_test:
    seq = input('Please input your intron sequence...   ')
    if (seq[:2]!="GU" or seq[len(seq)-2:]!="AG"):
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
            

#CG distribution



