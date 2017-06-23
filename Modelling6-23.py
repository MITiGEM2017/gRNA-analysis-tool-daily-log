# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:48:16 2017

@author: wangq
"""

#Factors of the System
# 1. Secondary Structure of intron and gRNA
# 2. Off-target binding
# 3. GC content
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



#
#Skip silencer, enhancer, branchpoint
"""
temporary
for tiling test
"""
gRNA_len = 22
site=[]
pos = 3
while pos<(len(seq)-gRNA_len):
    site.append(pos)
    pos+=1
#return the available start site of guide RNA



"""
Worked
Produce gRNA in a list
Could be traced with position number
"""

#Tiling
gRNA_list = []
gRNA_len = 22  #Update later
for gRNA_pos in site:
    temp="CCACCCCAAUAUCGAAGGGGACUAAAAC"
    for num in range(gRNA_len):
        position = num+gRNA_pos-1
        base = seq[position]
        index = "AUCG".find(base)
        complement = "UAGC"[index]
        temp += complement
    gRNA_list.append(temp)
#return a list containing all the guide RNA sequences
print ("The number of guide RNA sequences is ",len(gRNA_list)) 
#Count the number of the gRNA sequences - for test use






#CG distribution
score_list = [] #the list containing all the numbers of hydrogen bonds
for gRNA in gRNA_list:
    score = 0    
    for base in gRNA:
        if (base=="C" or base=="G"):
            score += 3
        else:
            score += 2
    score_list.append(score)


