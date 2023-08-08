import re

'''
operaciones binarias:
    suma: 1 + 2
    resta: 2 - 18
    multiplicación: 5 * 7
    división entera: 3 // 2

'''

digits_and_0 = '[0-9]+*'
special_functions = r"(ANS|CUPON|CUPON(X,Y)"
parentheses = r"((|))"
multiplication_division = r"(*|//)"
addition_substraction = r"(+|-)"

def CUPON(word,percent):
    return

curr_ans = 0
last_ans = 0

def par_check(line):
    if len(re.findall("\(",line)) == len(re.findall("\)",line)):
        return True
    return False

def calculate(exercise): 
    while re.search((special_functions|parentheses|multiplication_division|addition_substraction),exercise) != None:
        if re.search(special_functions,line) != None:
            if last_ans == 0:
                print("sin resolver")
            else:
                line = re.sub("ANS",str(last_ans),line)
                print(0)

        elif re.search(parentheses,line) != None:
            x = re.search("\w+\s*\)",line) 
            print(x.group())
        
        elif re.search(multiplication_division,line) != None:
            print(2)
        
        elif re.search(addition_substraction,line) != None:
            print(3)
    return

def sum(num1,num2):
    return int(num1)+int(num2)


# main
questions_file=open("/home/nine/Documents/Informagia/LP/Tarea 1/problemas.txt","r")
for line in questions_file:
    line=re.sub("–","-",line.strip("\n"))
    par_flag=par_check(line)
    if line == "\n":
        curr_ans = 0
        last_ans = 0
    else:
        '''
        print(re.search("(ANS|CUPON|CUPON\(X,Y\))",line))
        print(re.findall("(\(|\))",line))
        print(re.search("(\*|//)",line)) 
        print(re.search("(\+|-)",line)) 
        '''
        

        curr_ans = eval(line)
        print(curr_ans)
        last_ans = curr_ans
questions_file.close()

#answers_file=open("/home/nine/Documentos/Informagia/LP/Tarea 1/desarrollo.txt","w")
#answers_file.close