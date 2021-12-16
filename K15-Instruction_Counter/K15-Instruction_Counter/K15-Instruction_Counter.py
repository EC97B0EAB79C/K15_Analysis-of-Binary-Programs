import sys

prefix=["es","cs","ss","ds","fs","gs","opsize","adsize","lock","repne","rep","repz"]

def format(f_name):
    file=open(f_name)
    lines = file.readlines()
    data=[]
    for line in lines:
        data.append(line.split('\t'))
    return data

def print_dic(data):
    data=dict(sorted(data.items(), key=lambda item: item[1],reverse=True))
    for i in data:
        print("\t\t{}\t{}".format(i,data[i]))

# print count of instructions per function
def INTS_rank(data):
    print("INT rank:")
    dic_total={}
    dic_func={}
    for i in data:
        if i==['\n']:
            pass
        else:
            if len(i)==1:
               print_dic(dic_func)
               dic_func={}
               temp=i[0].split(' ')
               if(temp[0]=="Disassembly"):
                   print("\tsection:\t{}".format(temp[-1][:-1]))
               elif(len(temp)==2):
                   print("\tfucntion:\t{}".format(temp[-1][:-1]))
            elif len(i)>2:
                temp=i[2].split(' ')
                INTS=''
                for ints in temp:
                    INTS=ints.replace('\n','',1)
                    if INTS not in prefix and INTS[:3]!='rex':
                        break

                if INTS in dic_func:
                    dic_func[INTS]+=1
                else:
                    dic_func[INTS]=1
                if INTS in dic_total:
                    dic_total[INTS]+=1
                else:
                    dic_total[INTS]=1

    print_dic(dic_func)
    print("\tTotal:")
    print_dic(dic_total)

def print_rel(name,data):
    print_string=''
    for i in data:
        print_string=print_string+', '+i
    if(print_string!=''):
        print("\t{} {}".format(name, print_string[1:]))

# print functions called per function
def call_rel(data):
    relation=[]
    name=""
    print("call relation:")
    for i in data:

        if i==['\n']:
            pass
        else:
            if len(i)==1:
               temp=i[0].split(' ')
               if(len(temp)==2):
                   print_rel(name, relation)
                   relation=[]
                   name=temp[-1][:-1]

            elif len(i)>2:
                if (i[2].split(' ')[0]).replace("\n","",1)=="callq":
                    temp=i[2].split("<")
                    if len(temp)>1:
                        if temp[-1].split(">")[0] not in relation:
                            relation.append(temp[-1].split(">")[0])

def print_INTS(data):
    for i in data:
        print(i)

# print branch and loop base on jmp 
def branch_rel(data, mode_branch):
    if mode_branch:
        print("\nbranch:")
    else:
        print("\nloop")
    start=[]
    last=0
    for i in data:
        if i==['\n']:
            pass
        elif(len(i)==1):
            temp=i[0].split(' ')
            if(temp[0]!="Disassembly") and(len(temp)==2):
                start.append(int('0x'+temp[0],16))
        elif len(i)>2:
            temp=i[0].split(':')
            last=int('0x'+temp[0].replace(" ",""),16)
    start.append(last)

    stack_branch_in=[]
    stack_branch_out=[]
    stack_while_in=[]
    stack_while_out=[]
    
    index=-1;
    jmp=["je","jne","jg","jge","jl","jle","ja","jae","jb","jbe","jxcz","jc","jnc","jo","jno","jp","jnp","js","jns","jmp"]
    for i in data:
        if i==['\n']:
            pass
        elif(len(i)==1):
            temp=i[0].split(' ')
            if(temp[0]!="Disassembly") and(len(temp)==2):
                index+=1;
        elif len(i)>2:
            temp=i[2].split(' ')
            INTS=temp[0]
            if INTS in jmp:
                add_target=int('0x'+temp[-2],16)
                add_here=int('0x'+i[0].split(':')[0].replace(" ",""),16)
                if(add_target>=start[index] and add_target<=start[index+1]):
                    if(add_here>add_target):
                        stack_while_in.append(add_target)
                        stack_while_out.append(add_here)
                    else:
                        stack_branch_in.append(add_here)
                        stack_branch_out.append(add_target)

    stack_branch_in.sort()
    stack_branch_out.sort()
    stack_while_in.sort()
    stack_while_out.sort()
    stack_branch_in.append(0)
    stack_branch_out.append(0)
    stack_while_in.append(0)
    stack_while_out.append(0)

    tab=0;
    for i in data:
        if i==['\n']:
            pass
        elif(len(i)==1):
            temp=i[0].split(' ')
            if(temp[0]!="Disassembly") and(len(temp)==2):
                print("\n\tfucntion:\t{}".format(temp[-1][:-1]))
        elif len(i)>2:
            add=int('0x'+i[0].split(':')[0].replace(" ",""),16)

            if mode_branch:
                while(add==stack_branch_out[0]):
                    tab-=1
                    stack_branch_out.pop(0)
            else:
                while(add==stack_while_in[0]):
                    print('\t\t'+'\t'*tab+'{')
                    tab+=1
                    stack_while_in.pop(0)
                while(add==stack_while_out[0]):
                    tab-=1
                    print('\t\t'+'\t'*tab+'}')
                    stack_while_out.pop(0)

            print('\t{}\t'.format(i[0])+'\t|'*tab+'{}'.format(i[2].replace("\n","",1)))

            if mode_branch:
                while(add==stack_branch_in[0]):
                    tab+=1
                    stack_branch_in.pop(0)
            
            

def main():
    file_path=""
    if "--file" in sys.argv:
        file_path=sys.argv[sys.argv.index("--file")+1]
        data=format(file_path)
        INTS_rank(data)
        call_rel(data)
        branch_rel(data,True)
        branch_rel(data,False)
    else:
        print("usage:\tK15-Instruction_Counter.py --file [file]")





if __name__=="__main__":
    main()
