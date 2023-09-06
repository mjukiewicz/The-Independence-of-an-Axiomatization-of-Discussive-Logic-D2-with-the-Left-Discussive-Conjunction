from base import *

formulas_set=[
['~(p ^ ~p)', True],
['(~p > p) > p', True],
['(p > ~p) > ~p', True],
['~(p > q) > p', True],
['~(p > q) > ~q', True],
['p > (~q > ~(p > q))', True],
['((p > ~p) ^ (~p > p)) > (p ^ ~p)', True],
]


def matrix_generator(first_element, second_element=0, third_element=0, fourth_element=0):
    # numbers_list=[0]*6
    with open("v3_step2.txt") as file1:
        for line1 in file1:
            line1=ast.literal_eval(line1)
            yield line1+first_element
    return

dataset=[]
for element in formulas_set:
    elements_in_formula, letters=prepare_elements(element[0])
    cmci=check_main_conj_indx(elements_in_formula)
    dataset.append([elements_in_formula, letters, element[1], cmci])
dataset=tuple(dataset)
# import os
# os.system("ulimit -n 10000")
def main(first_element, second_element=0, third_element=0, fourth_element=0):
    global negation_dic, implication_dic, and_dic, eq_dic, alt_dic
    z=0
    for i in matrix_generator(first_element, second_element, third_element, fourth_element):
        if z%1000000==0: print(z)
        # print(i)
        z+=1
        values_to_check=i
        implication_dic={(0,0):values_to_check[0], (0,1):values_to_check[1], (0,2):values_to_check[2],
                         (1,0):values_to_check[3], (1,1):values_to_check[4], (1,2):values_to_check[5],
                         (2,0):values_to_check[6], (2,1):values_to_check[7], (2,2):values_to_check[8]
                         }
        negation_dic={0:values_to_check[18], 1:values_to_check[19], 2:values_to_check[20],
                 }
        eq_dic={}
        alt_dic={}
        and_dic={(0,0):values_to_check[9], (0,1):values_to_check[10], (0,2):values_to_check[11],
                         (1,0):values_to_check[12], (1,1):values_to_check[13], (1,2):values_to_check[14],
                         (2,0):values_to_check[15], (2,1):values_to_check[16], (2,2):values_to_check[17]}
        list_of_dic=[implication_dic, and_dic, alt_dic, negation_dic, eq_dic]
        n_inccorect=0
        for indx, element in enumerate(dataset):
            # print(element)
            r=print_table(element[0], element[1], element[2], False, element[3], list_of_dic, n_deginated_val=2)
            # if not r: break
            if not r: n_inccorect+=1
            # if not r: print_table(element[0], element[1], element[2], True, element[3], list_of_dic, n_deginated_val=2)
            if n_inccorect>=1: break #do odkomentowania !!!!!!!!!!!!!!!
        if n_inccorect==0:
            f = open("v3_step4.txt", "a")
            # print_table(element[0], element[1], element[2], True, element[3], list_of_dic, n_deginated_val=2)
            f.write(str(values_to_check)+"\n")
            # f.write(str(1)+"\n")
            f.close()
            # print(z,len(formulas_set)-n_inccorect,n_inccorect, values_to_check)
            # print(str(values_to_check))
        # if r: print(z,values_to_check)

from multiprocessing import Pool, cpu_count, Process
import ast
if __name__ == '__main__':
    val_list=[]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                val_list.append([i,j,k])
    processes = []
    for element in val_list:
        p = Process(target=main, args=(element,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
