#---+---+---+---+---+---+---+---+---+---+---+---] Global Variables [---+---+---+---+---+---+---+---+---+---+---+---#

import re

coupon_pattern = "CUPON\((\s*(\d+|ANS)\s*(,\s*(\d+|ANS)\s*)?)\)"
couponception = "CUPON\((\s*"+coupon_pattern+"\s*(,\s*\d+\s*)?|\s*\d+\s*,\s*"+coupon_pattern+"\s*|\s*"+coupon_pattern+"\s*,\s*"+coupon_pattern+"\s*)\)"
not_two_arg_coupon = "CUPON\(\s*\w*\s*((,\s*\w*\s*){2,}(,\s*)?|,\s*\w*\s*,|,\s*)\)|CUPON\(\s*,\s*\w+\s*\)"
coupon_twice = "CUPONCUPON\(?"
parentheses = "(\(|\))"
mult_div_ops = "\s*(\*|\/\/)\s*"
add_sub_ops = "\s*(\+|\-)\s*"
zero_as_divider = "\/\/\s*0"

curr_ans = "0"
last_ans = "0"
last_line = ""
question_array = [[]]
error_flag = True

#---+---+---+---+---+---+---+---+---+---+---+---] Error Checkers [---+---+---+---+---+---+---+---+---+---+---+---#

def error_check(line):
    '''
    ***
    * line: string
    
    ***

    Función que engloba todas las verificaciones de errores, para no tener que estar llamandolas por separado.
    Retorna True cuando todo está en orden y False cuando una de las subfunciones encuentra un error.
    '''
    coupon_check = coupon_in_coupon(line) and more_than_hundred_coupon(line) and coupon_arg_count(line) and repeated_coupon(line)
    operation_check = div_by_zero(line) and wrong_operations(line)
    par_check = par_count(line) and par_operation(line)
    if coupon_check and operation_check and par_check and keyword_check(line):
        return True
    return False

def coupon_in_coupon(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que no hayan cupones dentro de cupones (hence, couponception).
    Retorna True cuando todo está en orden y False cuando encuentra cupones dentro de cupones.
    '''
    if re.search(couponception,line) == None: return True
    return False 

def more_than_hundred_coupon(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que el porcentaje de CUPON() no sobrepase el 100%.
    Retorna True cuando todo está en orden y False en caso de encontrar un CUPON(X,Y), Y > 100.
    '''
    search_coupon = re.search(coupon_pattern,line)
    if search_coupon != None:
        coupon_num = re.findall("\d+",search_coupon.group())
        if len(coupon_num) == 2:
            if int(coupon_num[1]) >= 100: return False
    return True

def coupon_arg_count(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que la cantidad de argumentos en la función CUPON() sean una o dos.
    Retorna True cuando todo está en orden y False en caso de encontrar un CUPON(X,) o CUPON(X,Y,Z...).
    '''
    if re.search(not_two_arg_coupon,line) == None: return True
    return False

def repeated_coupon(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que no exista CUPONCUPON(X[,Y]).
    Retorna True cuando todo está en orden y False en caso de encontrar un CUPONCUPON(X).
    '''
    if re.search(coupon_twice,line) == None:
        return True
    return False

def div_by_zero(line):
    '''
    ***
    * line: string
    
    ***

    Esta función se encarga de encontrar un caso de división sobre cero, incluyendo si el cero es resultado de un paréntesis.
    Retorna True cuando todo está en orden y False cuando encuentra una división sobre cero.
    '''
    div_by_par = re.search("\/\/\s*\(",line)
    new=""
    if re.search(zero_as_divider,line) == None and div_by_par == None: return True
    elif div_by_par != None:
        new = line[div_by_par.end():]
        new = new[:re.search("\)",new).start()]
        if calculate(new) != "0": return True
    return False

def wrong_operations(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que no hayan errores de operadores binarios o que no haya una operación de potencia.
    También verifica que exista por lo menos un operador.
    Retorna True cuando todo está en orden y False en caso de encontrar uno o más de los casos descritos anteriormente.
    '''
    ops = re.findall("("+add_sub_ops+"|"+mult_div_ops+")",line)
    op_args = re.findall("\d+|"+coupon_pattern+"|ANS",line)
    exponentials = re.search("\^",line)
    if len(op_args) == len(ops)+1 and len(ops) >= 1 and exponentials == None:
        return True
    return False

def par_count(line):
    '''
    ***
    * line: string
    
    ***

    Esta función verifica que la cantidad y orden de paréntesis sea la correcta para poder realizar operaciones con estos.
    Retorna True cuando todo está en orden y False cuando encuentra un error de paréntesis.
    '''
    par_array = re.findall(parentheses,line)
    counter = 0
    for par in par_array:
        if par == r"(":
            counter += 1
        elif par == r")":
            counter -= 1
        if counter < 0:
            return False
    if counter == 0: return True
    return False

def par_operation(line):
    '''
    ***
    * line: string
    
    ***

    Esta función verifica que no existan paréntesis con un solo número dentro de ellos, excepto si son los de CUPON(X).
    Retorna True cuando todo está en orden y False cuando encuentra un error de paréntesis.
    '''
    if len(re.findall("CUPON\(\s*(\d+|ANS)\s*\)",line)) == len(re.findall("\(\s*(\d+|ANS)\s*\)",line)):
        return True
    return False

def keyword_check(line):
    '''
    ***
    * line: string
    
    ***

    Esta función revisa que no se encuentren palabras aparte de la palabras clave.
    Retorna True cuando todo está en orden y False en caso de encontrar palabras distintas a las claves
    '''
    words = re.findall("[a-zA-Z]+",line)
    coupons = re.findall(coupon_pattern,line)
    answers = re.findall("ANS",line)
    if len(coupons)+len(answers) < len(words):
        return False
    return True

#---+---+---+---+---+---+---+---+---+---+---+---] Operation Functions [---+---+---+---+---+---+---+---+---+---+---+---#

def par_find(line):
    '''
    ***
    * line: string
    
    ***

    Función que ayuda a encontrar el par de paréntesis más externo.
    En caso de haber varios parentesis externos lado a lado, los encuentra de izquierda a derecha.
    Retorna un arreglo de dos datos, los cuales son la posición del paréntesis que abre y del paréntesis que cierra, respectivamente.
    '''
    counter1 = 0; counter2 = 0; char = 0
    init = re.search("\(",line).end()
    pos = [init,0]
    while char < len(line):
        if line[char] == r"(":
            counter1 += 1
        elif line[char] == r")":
            counter2 += 1
        if counter1 == counter2 and counter1 != 0:
            pos[1] = char
            break
        char += 1
    return pos

def cupon(value,percent):
    '''
    ***
    * value: string
    * percent: string
    
    ***

    Función que calcula un porcentaje percent del valor value.
    El valor se trunca para que sea un entero en caso de haber decimales.
    Retorna el valor multiplicado por el porcentaje.
    '''
    discount = int(value) * (int(percent) / 100)
    discount = str(discount)
    discount = re.sub("\.\d+","",discount)
    return discount

def operate(operation):
    '''
    ***
    * operation: string
    
    ***

    Función que realiza las cuatro operaciones binarias.
    Dependiendo del operador que se detecte la función realiza una operación.
    Si el número resultante es menor que 0, se iguala a 0.
    Retorna el resultado de la operación binaria que recibió.
    '''
    if "+" in operation:
        num1,num2 = re.split("\+",operation)
        operation = int(num1)+int(num2)
    elif "-" in operation:
        num1,num2 = re.split("\-",operation)
        operation = int(num1)-int(num2)
    elif "*" in operation:
        num1,num2 = re.split("\*",operation)
        operation = int(num1)*int(num2)
    elif "//" in operation:
        num1,num2 = re.split("\/\/",operation)
        operation = int(num1)//int(num2)
    
    if operation < 0: operation = 0
    return str(operation)

def calculate(exercise):
    '''
    ***
    * exercise: string
    
    ***

    Función "Esqueleto" que analiza el string en busca de las operaciones a realizar de acuerdo al PAPOMUDAS.
    Retorna el resultado de la expresión en formato string para que pueda implementarse sin tener que cambiar de formato int a str.
    '''
    operation=""
    while re.search("(ANS|"+coupon_pattern+"|"+parentheses+"|"+mult_div_ops+"|"+add_sub_ops+")",exercise) != None:

        search_ans = re.search("ANS",exercise)
        search_coupon = re.search(coupon_pattern,exercise)
        search_parentheses = re.search(parentheses,exercise)
        search_mult_div = re.search(mult_div_ops,exercise)
        search_add_sub = re.search(add_sub_ops,exercise)

        if search_ans != None:
            exercise = re.sub("ANS",last_ans,exercise)

        elif search_coupon != None:
            coupon_num = re.findall("\d+",search_coupon.group())
            if len(coupon_num) == 1:
                coupon = cupon(coupon_num[0],20)
            elif len(coupon_num) == 2:
                coupon = cupon(coupon_num[0],coupon_num[1])
            exercise = re.sub(coupon_pattern,coupon,exercise)

        elif search_parentheses != None:
            start,end = par_find(exercise) 
            operation = exercise[start:end]
            operation = calculate(operation)
            exercise = exercise.replace(exercise[start-1:end+1],operation)
        
        elif search_mult_div != None:
            operation = re.search("\d+"+mult_div_ops+"\d+",exercise).group()
            operation = re.sub(" ","",operation)
            operation = operate(operation)
            exercise=re.sub("\d+"+mult_div_ops+"\d+",operation,exercise,1)
        
        elif search_add_sub != None:
            operation = re.search("\d+"+add_sub_ops+"\d+",exercise).group()
            operation = re.sub(" ","",operation)
            operation = operate(operation)
            exercise=re.sub("\d+"+add_sub_ops+"\d+",operation,exercise,1)

    return exercise

#---+---+---+---+---+---+---+---+---+---+---+---] Main Function [---+---+---+---+---+---+---+---+---+---+---+---#

questions_file=open("./problemas.txt","r")

for line in questions_file:
    line=re.sub("–","-",line.strip("\n"))
    
    if line != "":
        question_array[-1].append(line)
        if not error_check(line):
            error_flag = False

    else:
        question_array[-1].append(error_flag)
        question_array.append(list())
        error_flag = True

question_array[-1].append(error_flag)
questions_file.close()
answers_file=open("./desarrollo.txt","w")

for question in question_array:
    if question[-1]:
        question.pop()
        for item in question:
            curr_ans = calculate(item)
            answers_file.write(item+" = "+curr_ans+"\n")
            last_ans = curr_ans
    
    else:
        question.pop()
        for item in question:
            if not error_check(item):
                answers_file.write(item+" = Error\n")
            else:
                answers_file.write(item+" = Sin resolver\n")
    
    curr_ans = "0"
    last_ans = "0"
    answers_file.write("\n")

answers_file.close()