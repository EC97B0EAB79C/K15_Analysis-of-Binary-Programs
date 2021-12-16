import re
import sys
import random

def read_cfile(f_name):
    file=open(f_name)
    code=file.readlines()
    return code

def add_nhm(file):
    temp=open("NHM.c")
    file.writelines(temp.readlines())

def export_code(f_name,result):
    file=open(f_name,"w")
    add_nhm(file)
    file.writelines(result)

def obfusscate_c(code):
    result=[]
    for line in code:
        instruction=str(line).lstrip().replace("\t","").replace("\n","")
        words=instruction.split(" ")
        re_sult=re.search(r"\((\d+)\)",line)
        if words[0]=="int":
            if "=" in instruction:
                temp=re.search(r"\=(\d+)\;",line)
                key=random.randrange(1<<32)
#                print(line[:temp.span()[0]+1]+"nhm("+str(-(int(temp.group(0)[1:-1])^key))+","+str(key)+")"+line[temp.span()[1]-1:])
                result.append(line[:temp.span()[0]+1]+"nhm("+str(-(int(temp.group(0)[1:-1])^key))+","+str(key)+")"+line[temp.span()[1]-1:])
            else:
                result.append(line)
        elif re_sult:
#            print(re_sult)
#            print(instruction[:re_sult.span()[0]+1]+str(int(re_sult.group(0)[1:-1])+(2<<31)*random.randint(-5,5))+instruction[re_sult.span()[1]-1:])
            result.append(line[:re_sult.span()[0]+1]+str(int(re_sult.group(0)[1:-1])+(2<<31)*random.randint(-5,5))+line[re_sult.span()[1]-1:])
        else:
            result.append(line)
#    print(result)
    return result

def main():
    code=read_cfile("test1.c")
    result=obfusscate_c(code)
    export_code("result.c",result)

if __name__=="__main__":
    main()
