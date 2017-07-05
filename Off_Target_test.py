# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 21:20:54 2017

@author: wangq
"""
from timeit import default_timer as timer


def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )

def off_target_mismatch(mRNA_seq,gRNA_seq):
    crRNA_seq = gRNA_seq[-gRNA_length:]
    print(crRNA_seq)

    count = 0
    difference_list = []
    RNA_complement = ""
    for num in range(len(crRNA_seq)):
        base = crRNA_seq[num]
        index = "UAGC".find(base)
        complement = "ATCG"[index]
        RNA_complement += complement
    print(RNA_complement)
        
    start_pos = 0
    while start_pos < (len(mRNA_seq)-len(crRNA_seq)+1):
        DNA_seq = mRNA_seq[start_pos:(start_pos+len(crRNA_seq))]
        diff = diff_letters(RNA_complement, DNA_seq)
        if diff <= off_target_mismatch_threshold:
            count +=1
            difference_list.append(diff)
            start_pos += 1

        else:
            start_pos += (diff-off_target_mismatch_threshold)

        if (start_pos%100000 == 0):
            print("Currently at",start_pos,"th base.")

    return count, difference_list

file = open("human-cDNA.txt","r")
#file = open("test.txt","r")
#mRNA = file.readline()
off_target_mismatch_threshold = 4
gRNA_length = 22
start = timer()
print(off_target_mismatch(file.readline(),'CCACCCCAAUAUCGAAGGGGACUAAAACGUACAAGUAUGGAGAAUAGAAG'))
end = timer()
print("In total    ", end-start)
