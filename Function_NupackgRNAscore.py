# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:37:24 2017

@author: wangq
"""

def Nupack_gRNA_score(final_Nupack_gRNA_list):
    Nupack_gRNA_score_list = []
    for each_gRNA_data in final_Nupack_gRNA_list:
        temp_list = each_gRNA_data[-(len(tracrRNA_seq)+gRNA_length):]  # Get the range of -50: ---> all containing individual probabilities of stem loop
        temp_product = 1
    
        for subset in temp_list:
            if (subset[1]=="-1"):
                prob = float(subset[2])
            else:
                prob = 0.001
    
            temp_product *= prob
            
        Nupack_gRNA_score_list.append(temp_product)
    
    return Nupack_gRNA_score_list

Nupack_gRNA_final_score = Nupack_gRNA_score(gRNA_stats_list)
