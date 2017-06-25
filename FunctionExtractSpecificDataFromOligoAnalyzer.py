# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 16:59:11 2017

@author: wangq
"""
import re
def oligoAnalyzer_extract_specific_info(final_hp_list,index):
    result = []    
    for hp_each_list in final_hp_list:
        #temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        temp = re.findall("\d+\.\d+", hp_each_list[index])
        if (len(temp)==0):
            temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        result.append(temp)
        
    return result