import re

special_functions = "(ANS|CUPON\(X\)|CUPON\(X,Y\))"
parentheses = "(\(|\))"
mult_div_ops = "\s*(\*|\/\/)\s*"
add_sub_ops = "\s*(\+|\-)\s*"

def CUPON(word,percent):
    return

curr_ans = 0
last_ans = 0

def par_check(line):
    if len(re.findall("\(",line)) == len(re.findall("\)",line)):
        return True
    return False

def calculate(exercise):
    solved_line=exercise; aux_line=""
    while re.search("("+special_functions+"|"+parentheses+"|"+mult_div_ops+"|"+add_sub_ops+")",solved_line) != None:

        search_sf = re.search(special_functions,solved_line)
        search_parentheses = re.search(parentheses,solved_line)
        search_mult_div = re.search(mult_div_ops,solved_line)
        search_add_sub = re.search(add_sub_ops,solved_line)

        aux1=0;aux2=0;operation=0

        if search_sf != None:
            if last_ans == 0:
                print("sin resolver")
            else:
                solved_line = re.sub("ANS",str(last_ans),solved_line)

        elif search_parentheses != None:
            x = re.search("\w+\s*\)",solved_line) 
            print(x.group())
            #calculate(lo que está dentro del paréntesis)
        
        elif search_mult_div != None:
            aux_line = re.search("\d+"+mult_div_ops+"\d+",solved_line).group()
            aux_line = re.sub(" ","",aux_line)

            if r"*" in solved_line:
                aux1,aux2 = re.split("\*",aux_line)
                operation=str(int(aux1)*int(aux2))

            elif r"//" in solved_line:
                aux1,aux2 = re.split("\/\/",aux_line)
                operation=str(int(aux1)//int(aux2))

            solved_line=re.sub("\d+"+mult_div_ops+"\d+",operation,solved_line)
        
        elif search_add_sub != None:
            aux_line = re.search("\d+"+add_sub_ops+"\d+",solved_line).group()
            aux_line = re.sub(" ","",aux_line)

            if r"+" in solved_line:
                aux1,aux2 = re.split("\+",aux_line)
                operation=str(int(aux1)+int(aux2))

            elif r"-" in solved_line:
                aux1,aux2 = re.split("\-",aux_line)
                operation=str(int(aux1)-int(aux2))

            solved_line=re.sub("\d+"+add_sub_ops+"\d+",operation,solved_line)

    return solved_line

def add_sub(num1,num2):
    return int(num1)+int(num2)


# main
questions_file=open("/home/nine/Documents/Informagia/LP/Tarea 1/problemas (EJEMPLO).txt","r")
for line in questions_file:
    line=re.sub("–","-",line.strip("\n"))
    par_flag=par_check(line)
    if line == "\n":
        curr_ans = 0
        last_ans = 0
    else:
        curr_ans = calculate(line)
        print(line+" = "+curr_ans)
        last_ans = curr_ans
questions_file.close()

#answers_file=open("/home/nine/Documentos/Informagia/LP/Tarea 1/desarrollo.txt","w")
#answers_file.close