import sys
import math
import matplotlib.pyplot as plt

def get_histogram(filename):
    histro=[0]*256
    file=open(filename,'rb')
    data=bytearray(file.read())
    for d in data:
        histro[d]+=1
    return histro

def entrophy_cal(histro):
    entropy=0
    prob=sum(histro)
    for h in histro:
        if h!=0:
            entropy-=(h/prob)*math.log2(h/prob)
    return entropy

def plot(histro, name='temp'):
    x=[]
    for i in range(256):
        x.append(i)
    plt.clf()
    plt.bar(x,histro)
    plt.xlabel("byte value")
    plt.ylabel("quant.")
    plt.savefig("img/"+(name.replace('.','')).replace(' ','')+".png")
    print("saved img/"+(name.replace('.','')).replace(' ','')+".png")
def main():
    file_offset=1
    MODE_COMPARE    = False
    MODE_HISTOGRAM  = False
    MODE_ENTROPHY   = False
    if "-h" in sys.argv:
        MODE_HISTOGRAM=True
        file_offset+=1
    if "-e" in sys.argv:
        MODE_ENTROPHY=True
        file_offset+=1
    if "-c" in sys.argv:
        MODE_COMPARE=True
        file_offset+=1

    if file_offset==1 or len(sys.argv)==1:
        print('''usage:\tFileHistogram.py {options} [file name list]
        \n\t\t-h\tcreate histogram plot of binary(created in ./img/.)
        \n\t\t-e\tprint entrophy of binary
        \n\t\t-c\tcompare mode(read files from ./original/. and ./packed/.)''')

    program=sys.argv[file_offset:]
    if MODE_COMPARE:
        if MODE_ENTROPHY:
            print("============================================================")
            print("             file               origin -> packed (increment)")
            print("------------------------------------------------------------")
            for p in program:
                histro_p=get_histogram('packed/'+p)
                histro_o=get_histogram('original/'+p)
                entrophy_o=entrophy_cal(histro_o)
                entrophy_p=entrophy_cal(histro_p)
                print("{:>30}: {:.4f} -> {:.4f} ({:.4f}%)".format(p,entrophy_o,entrophy_p,entrophy_p/entrophy_o*100-100))
        if MODE_HISTOGRAM:
            print("============================================================")
            print("creating histogram")
            print("------------------------------------------------------------")
            for p in program:
                histro_p=get_histogram('packed/'+p)
                histro_o=get_histogram('original/'+p)
                plot(histro_p,"p_"+p)
                plot(histro_o,"o_"+p)
    else:
        if MODE_ENTROPHY:
            print("========================================")
            print("             file               Entrophy")
            print("----------------------------------------")
            for p in program:
                histro=get_histogram(p)
                entrophy=entrophy_cal(histro)
                print("{:>30}: {:.4f}".format(p,entrophy))
        if MODE_HISTOGRAM:
            print("========================================")
            print("creating histogram")
            print("----------------------------------------")
            for p in program:
                histro_p=get_histogram(p)
                plot(histro_p,p)
    

if __name__=="__main__":
    main()