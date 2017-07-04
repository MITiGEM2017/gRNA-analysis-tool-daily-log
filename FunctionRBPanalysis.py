# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:49:10 2017

@author: wangq
"""

weighted_factor = 0.4
binding_prob_power = 2

def RBP_competition_score(site,gRNA_seq,gRNA_list,RBP_data_list,RBP_Kd_list):
    start_pos = site[gRNA_list.index(gRNA_seq)]
    end_pos = start_pos + gRNA_length -1
    potential_RBP_list = []
    partial_RBP_list = []

    for row in RBP_data_list:
        if (row[1]<=end_pos and row[1]>=start_pos):
            if(row[-1]<=end_pos):
                potential_RBP_list.append(row)
            else:
                partial_RBP_list.append(row)
        elif (row[-1]>=start_pos and row[1]<start_pos):
            partial_RBP_list.append(row)


    sum_RBP_interference_score = 0  # return value

    # For the score from RBPs that completely bind in the region
    sum_complete_bind = 0
    RBP_num_count = 0
    while RBP_num_count < len(potential_RBP_list):
        potential_info_list = potential_RBP_list[RBP_num_count]
        potential_start_pos = potential_info_list[1]
        potential_RBP_test = True
        power_count = 0
        base_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])
        complete_score_list = []
        complete_score_list.append(base_score)
        while (potential_RBP_test and (RBP_num_count+power_count+1)<len(potential_RBP_list)):
            if(potential_RBP_list[RBP_num_count+power_count+1][1] == potential_start_pos):
                power_count += 1
                potential_info_list = potential_RBP_list[RBP_num_count+power_count]
                additional_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])  #temporary score
                complete_score_list.append(additional_score)
            else:
                potential_RBP_test = False
                RBP_num_count += power_count


        if len(complete_score_list) > 1:
            while len(complete_score_list) > 1:
                minimum_score = min(complete_score_list)
                sum_complete_bind += minimum_score*(weighted_factor**power_count)
                power_count -= 1
                complete_score_list.remove(minimum_score)

        else:
            sum_complete_bind += base_score


        RBP_num_count += 1

    print(sum_complete_bind)



    # Score for partially bind RBPs in the region
    sum_partially_bind = 0
    RBP_num_count = 0
    while RBP_num_count < len(partial_RBP_list):
        potential_info_list = partial_RBP_list[RBP_num_count]
        potential_start_pos = potential_info_list[1]
        potential_RBP_test = True
        power_count = 0
        factor = min((potential_info_list[6]-start_pos+1),(end_pos-potential_info_list[1]+1))/potential_info_list[5]
        base_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])*factor
        complete_score_list = []
        complete_score_list.append(base_score)
        while (potential_RBP_test and (RBP_num_count+power_count+1)<len(partial_RBP_list)):
            if(partial_RBP_list[RBP_num_count+power_count+1][1] == potential_start_pos):
                power_count += 1
                potential_info_list = partial_RBP_list[RBP_num_count+power_count]
                factor = min((potential_info_list[6]-start_pos+1),(end_pos-potential_info_list[1]+1))/potential_info_list[5]
                additional_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])*factor  #temporary score
                complete_score_list.append(additional_score)
            else:
                potential_RBP_test = False
                RBP_num_count += power_count

        if len(complete_score_list) > 1:
            while len(complete_score_list) > 1:
                minimum_score = min(complete_score_list)
                sum_partially_bind += minimum_score*(weighted_factor**power_count)
                power_count -= 1
                complete_score_list.remove(minimum_score)
        else:
            sum_partially_bind += base_score

        RBP_num_count += 1

    print(sum_partially_bind)
    sum_RBP_interference_score = sum_partially_bind+sum_complete_bind


    return sum_RBP_interference_score


RBP_final_competition_score = RBP_competition_score(gRNA_start_site, 'CCACCCCAAUAUCGAAGGGGACUAAAACGAGUCCUAGCAAAAUCAAAGAA', gRNA_seq_list, RBP_data,kd_data_list)
