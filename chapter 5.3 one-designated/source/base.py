conj=["^",">","v","="]


def prepare_elements(formula):
    letters=list(set([i for i in formula if i.isalpha() and not i=="v"]))
    list_elements=[formula]
    list_elements_to_divide=[formula]

    while True:
        lancuch=list_elements_to_divide[0]
        neg_flag=False
        for indx in range(len(lancuch)):
            if lancuch[indx] in conj:
                if lancuch[:indx].count("(")-lancuch[:indx].count(")")==0 and lancuch[indx:].count("(")-lancuch[indx:].count(")")==0:
                    neg_flag=True
        if lancuch[0]=="~" and lancuch[-1]==")" and lancuch.count("(") >= lancuch.count(conj[0])+lancuch.count(conj[1])+lancuch.count(conj[2])+lancuch.count(conj[3]) and not neg_flag:
            list_elements.append(lancuch[2:-1])
            list_elements_to_divide.append(lancuch[2:-1])
        else:
            for indx in range(len(lancuch)):
                if lancuch[indx] in conj:
                    if lancuch[:indx].count("(")-lancuch[:indx].count(")")==0 and lancuch[indx:].count("(")-lancuch[indx:].count(")")==0:
                        if len(lancuch[:indx-1])>2 and lancuch[0]=="~" and lancuch.count("(") >= lancuch.count(conj[0])+lancuch.count(conj[1])+lancuch.count(conj[2])+lancuch.count(conj[3]):
                            list_elements.append(lancuch[:indx-1])
                            list_elements.append(lancuch[2:indx-2])
                        elif len(lancuch[:indx-1])>2 and lancuch[0]=="~": list_elements.append(lancuch[:indx-1])
                        elif len(lancuch[:indx-1])>2: list_elements.append(lancuch[1:indx-2])
                        else: list_elements.append(lancuch[:indx-1])
                        if len(list_elements[-1])>2: list_elements_to_divide.append(list_elements[-1])
                        if len(lancuch[indx+2:])>2 and lancuch[indx+2]=="~" and lancuch.count("(") >= lancuch.count(conj[0])+lancuch.count(conj[1])+lancuch.count(conj[2])+lancuch.count(conj[3]):
                            list_elements.append(lancuch[indx+2:])
                            list_elements.append(lancuch[indx+4:-1])
                        elif len(lancuch[indx+2:])>2 and lancuch[indx+2]=="~": list_elements.append(lancuch[indx+2:])
                        elif len(lancuch[indx+2:])>2: list_elements.append(lancuch[indx+3:-1])
                        else: list_elements.append(lancuch[indx+2:])
                        if len(list_elements[-1])>2: list_elements_to_divide.append(list_elements[-1])
        list_elements_to_divide.remove(lancuch)
        if not list_elements_to_divide: break
    list_elements=list(set(list_elements+letters))
    list_elements.sort()
    list_elements.sort(key=len)
    return list_elements, letters

def negation(elements):
    return [negation_dic[element] for element in elements]
def conjunction(element1, element2):
    return [and_dic[(element1[i],element2[i])] for i in range(len(element1))]
def implication(element1, element2):
    return [implication_dic[(element1[i],element2[i])] for i in range(len(element1))]
def equivalence(element1, element2):
    return [eq_dic[(element1[i],element2[i])] for i in range(len(element1))]
def alternative(element1, element2):
    return [alt_dic[(element1[i],element2[i])] for i in range(len(element1))]

def assembling_sides(item, indx, elements_in_formula, values_list):
    if item[:indx-1] in elements_in_formula:
        left_side=values_list[elements_in_formula.index(item[:indx-1])]
    elif item[1:indx-2] in elements_in_formula:
        left_side=values_list[elements_in_formula.index(item[1:indx-2])]
    if item[indx+2:] in elements_in_formula:
        right_side=values_list[elements_in_formula.index(item[indx+2:])]
    elif item[indx+3:-1] in elements_in_formula:
        right_side=values_list[elements_in_formula.index(item[indx+3:-1])]
    return left_side, right_side

def prepare_values_list(elements_in_formula, letters, indx_list):
    values_list=[]
    for item in elements_in_formula:
        if item=='p': values_list.append([0,1,2]*3**(len(letters)-1))
        elif item=='q': values_list.append(([0]*3+[1]*3+[2]*3)*3**(len(letters)-2))
        elif item=='r': values_list.append([0]*(3**(len(letters)-1))+[1]*(3**(len(letters)-1))+[2]*(3**(len(letters)-1)))
        elif len(item)==2:
            neg=negation(values_list[elements_in_formula.index(item[-1])])
            values_list.append(neg)
        elif item[2:-1] in elements_in_formula and item[0]=="~":
            neg=negation(values_list[elements_in_formula.index(item[2:-1])])
            values_list.append(neg)
        else:
            for indx in range(len(item)):
                if item[indx] in conj and item[:indx].count("(")-item[:indx].count(")")==0 and item[indx:].count("(")-item[indx:].count(")")==0:
                    break
            left_side, right_side=assembling_sides(item, indx, elements_in_formula, values_list)
            if item[indx]=="^":
                result=conjunction(left_side, right_side)
            elif item[indx]=="v":
                result=alternative(left_side, right_side)
            elif item[indx]==">":
                result=implication(left_side, right_side)
            elif item[indx]=="=":
                result=equivalence(left_side, right_side)
            values_list.append(result)
    return values_list

def check_main_conj_indx(elements_in_formula):
    indx_list=[]
    for item in elements_in_formula:
        flag=False
        for indx in range(len(item)):
            if item[indx] in conj and item[:indx].count("(")-item[:indx].count(")")==0 and item[indx:].count("(")-item[indx:].count(")")==0:
                flag=True
                break
        if flag: indx_list.append(indx)
    return indx_list

def print_table(elements_in_formula, letters, result, display, indx_list, list_of_dic, n_deginated_val):
    #do poprawy
    global implication_dic, and_dic, alt_dic, negation_dic, eq_dic
    implication_dic=list_of_dic[0]
    and_dic=list_of_dic[1]
    alt_dic=list_of_dic[2]
    negation_dic=list_of_dic[3]
    eq_dic=list_of_dic[4]

    values_list=prepare_values_list(elements_in_formula, letters, indx_list)
    if display:# and elements_in_formula[-1]=="p > (~p > (~(~p) > q))":
        line_len=0
        for item in elements_in_formula:
            print("|", item, "|", end="")
            line_len+=(len(item)+4)
        print()
        print("-"*line_len)
        for i in range(3**len(letters)):
            for j in range(len(elements_in_formula)):
                n_char=len(elements_in_formula[j])
                if n_char%2==0:
                    print("| "+" "*int(-1+n_char/2)+str(values_list[j][i])+" "*int(n_char/2)+" |", end="")
                else:
                    print("| "+" "*int(n_char/2)+str(values_list[j][i])+" "*int(n_char/2)+" |", end="")
            print()
        print()

    if n_deginated_val==2:
        if result: #dwie desg wart
            if not 0 in values_list[-1]: return True
            else: return False
        else:
            if not 0 in values_list[-1]: return False
            else: return True

    elif n_deginated_val==1:
        if result: #jedna desg wart
            if not 0 in values_list[-1] and not 1 in values_list[-1]: return True
            else: return False
        else:
            if not 0 in values_list[-1] and not 1 in values_list[-1]: return False
            else: return True
