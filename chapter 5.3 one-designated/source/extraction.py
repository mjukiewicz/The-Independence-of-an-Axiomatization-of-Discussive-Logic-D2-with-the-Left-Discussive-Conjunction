order = [('0','0'),('0','1'),('0','2'),('1','0'),('1','1'),('1','2'),('2','0'),('2','1'),('2','2')]
neg_order = [('0|'),('1|'),('2|')] + ["  "]*6
counter = 0

file_number = str(1)

with open("step"+file_number+"_simplified.txt","w") as output_data: pass

with open("v3_step"+file_number+".txt","r") as input_data:
    for line in input_data:
        imp, con, neg, dis = [int(element) for element in line[1:-2].split(", ")][:9],\
                            [int(element) for element in line[1:-2].split(", ")][9:18], \
                            [int(element) for element in line[1:-2].split(", ")][18:21], \
                            [int(element) for element in line[1:-2].split(", ")][21:]
        with open("step"+file_number+"_simplified.txt","a") as output_data:
            output_data.write("p|q|p>q p|q|p^q p|~p p|q|pvq \n")
            output_data.write("------- ------- ---- -------\n")
            for index, element in enumerate(order):
                fragment = element[0]+"|"+element[1]+"| "
                to_write = fragment+str(imp[index])+"  "
                if len(con):
                    to_write += fragment+str(con[index])+"  "
                    if len(neg):
                        neg = neg + [" "]*6
                        to_write += neg_order[index]+str(neg[index])+"  "
                        if len(dis):
                            to_write += fragment+str(dis[index])+"  "
                output_data.write(to_write+"\n")
            output_data.write("\n")
            counter += 1

print(counter)