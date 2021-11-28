from base import *

formulas_set=[
['p > (~p > q)', False],
['p > (~p > ~q)', False],
['(p > q) > (~(p > q) > r)', False],
['((p > q) ^ (q > p)) > (~((p > q) ^ (q > p)) > r)', False],
['p > (~p > (~(~p) > q))', False],
['((p > ~p) ^ (~p > p)) > q', False],
['(p > ~p) > ((~p > p) > q)', False],
['~(p > p) > q', False],
['(p > q) > (~q > ~p)', False],
['(~p > ~q) > (q > p)', False],
['(p > q) > ((p > ~q) > ~p)', False],
['(~p > q) > ((~p > ~q) > p)', False],
['((p > q) ^ ~q) > ~p', False],
['((p > q) ^ (p > ~q)) > ~p', False],
]


def matrix_generator(first_element):
    with open("v3_step2.txt") as file1:
        for line1 in file1:
            line1=ast.literal_eval(line1)
            numbers_list=[0]*6
            yield line1+first_element+numbers_list
            for i in range(3**len(numbers_list)):
                if numbers_list==[2]*6: break
                numbers_list[-1]+=1
                for j in range(len(numbers_list)-1,-1,-1):
                    if numbers_list[j]==3:
                        numbers_list[j]=0
                        numbers_list[j-1]+=1
                yield line1+first_element+numbers_list
    return

def main(first_element, dataset):
    global negation_dic, implication_dic, and_dic, eq_dic, alt_dic
    for index, values_to_check in enumerate(matrix_generator(first_element)):
        if index%1000000==0: print(index)

        implication_dic={(0,0):values_to_check[0], (0,1):values_to_check[1], (0,2):values_to_check[2],
                         (1,0):values_to_check[3], (1,1):values_to_check[4], (1,2):values_to_check[5],
                         (2,0):values_to_check[6], (2,1):values_to_check[7], (2,2):values_to_check[8]
                         }
        negation_dic={0:values_to_check[18], 1:values_to_check[19], 2:values_to_check[20],
                 }
        eq_dic={}
        alt_dic={(0,0):values_to_check[21], (0,1):values_to_check[22], (0,2):values_to_check[23],
                         (1,0):values_to_check[24], (1,1):values_to_check[25], (1,2):values_to_check[26],
                         (2,0):values_to_check[27], (2,1):values_to_check[28], (2,2):values_to_check[29]}
        and_dic={(0,0):values_to_check[9], (0,1):values_to_check[10], (0,2):values_to_check[11],
                         (1,0):values_to_check[12], (1,1):values_to_check[13], (1,2):values_to_check[14],
                         (2,0):values_to_check[15], (2,1):values_to_check[16], (2,2):values_to_check[17]}
        list_of_dic=[implication_dic, and_dic, alt_dic, negation_dic, eq_dic]
        n_inccorect=0
        for indx, element in enumerate(dataset):
            r=print_table(element[0], element[1], element[2], False, element[3], list_of_dic, n_deginated_val=2)
            if not r: n_inccorect+=1
        if n_inccorect==0:
            f = open("v3_step3.txt", "a")
            f.write(str(values_to_check)+"\n")
            f.close()

from multiprocessing import Pool, cpu_count, Process
import ast
if __name__ == '__main__':
    val_list=[]
    dataset=[]
    for element in formulas_set:
        elements_in_formula, letters=prepare_elements(element[0])
        cmci=check_main_conj_indx(elements_in_formula)
        dataset.append([elements_in_formula, letters, element[1], cmci])
    dataset=tuple(dataset)


    for i in range(3):
        for j in range(3):
            for k in range(3):
                val_list.append([i,j,k])
    processes = []
    for element in val_list:
        p = Process(target=main, args=(element,dataset))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
