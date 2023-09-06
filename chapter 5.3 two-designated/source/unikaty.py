import os, ast
impl_list, eq_list, conj_list, dis_list, neg_list=[],[],[],[],[]
counter=0
with open("v3_step6.txt") as file2:
    for line2 in file2:
        counter+=1
        line2=ast.literal_eval(line2)
        if not str(line2[0:9]) in impl_list:
            impl_list.append(str(line2[0:9]))
        if not str(line2[9:18]) in conj_list:
            conj_list.append(str(line2[9:18]))
        if not str(line2[21:30]) in dis_list:
            dis_list.append(str(line2[21:30]))
        if not str(line2[18:21]) in neg_list:
            neg_list.append(str(line2[18:21]))

        if counter%10000==0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Implication:", len(impl_list))
            print("Conjunction:", len(conj_list))
            print("Disjunction:", len(dis_list))
            print("Negation:", len(neg_list))

os.system('cls' if os.name == 'nt' else 'clear')
print("Implication:", len(impl_list))
print("Conjunction:", len(conj_list))
print("Disjunction:", len(dis_list))
print("Negation:", len(neg_list))
print(counter)
