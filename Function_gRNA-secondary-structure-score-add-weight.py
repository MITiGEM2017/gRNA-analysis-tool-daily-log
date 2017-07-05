# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 10:40:19 2017

@author: wangq
"""
import math

secondary_structure_score_prob_target = 0.951 #constant used in function: gRNA_secondary_structure_score_weight  range:[0.949,0.951]

def gRNA_secondary_structure_score_weight(gRNA_2_score_list):
    maximum_score = max(gRNA_2_score_list)
    print(math.log(maximum_score,secondary_structure_score_prob_target))
    print((math.log10(maximum_score)))
    weight_power = -(math.log(maximum_score,secondary_structure_score_prob_target))*(math.log10(maximum_score))
    print(weight_power)
    final_gRNA_secondary_score_list = []
    for gRNA_2_score in gRNA_2_score_list:
        temp_score = gRNA_2_score**(-math.log10(gRNA_2_score)/weight_power)
        final_gRNA_secondary_score_list.append(temp_score)

    return final_gRNA_secondary_score_list

a=gRNA_secondary_structure_score_weight(Nupack_gRNA_final_score)
    
