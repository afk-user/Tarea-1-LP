import re

txt = "1245 // 10  +           12"
ope = '(\+|\-|\*|\/\/)'
ope_space = "\s*"+ope+"\s*"

print(ope_space)
x = re.search("\d+"+ope_space+"\d+",txt).group()
print(x)
x = re.sub(" ","",x)
print(x)
x1,x2=re.split(ope,x)
xope = str(int(x1)*int(x2))
print(xope)
txt=re.sub("\d+"+ope_space+"\d+",xope,txt)
print(txt)