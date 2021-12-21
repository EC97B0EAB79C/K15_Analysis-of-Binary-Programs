import hashlib, binascii
import os, sys
import re


db_loc="./db/"

def read_hdb():
    f=open(db_loc+"main.hdb")
    data=f.readlines()
    dic_hdb={}
    for d in data:
        temp=d.split(":")
        dic_hdb[temp[0]]=temp[1:]
    return dic_hdb

def read_ndb():
#    f=open(db_loc+"main.ndb")
    f=open(db_loc+"reduced.ndb")
    data=f.readlines()
    db_hex=[]
    for d in data:
        temp=d.split(":")

        #Transfer wildcard to RegEx
        temp[3]=temp[3].replace("\n","")
        temp[3]=temp[3].replace("?",".")
        temp[3]=temp[3].replace("*","(..)+")
        temp[3]=temp[3].replace("-",",")
        match=re.finditer("\{.+\}",temp[3])
        l=[]
        for r in match:
            l.append(r)
        for r in l:
            temp[3]=temp[3][:r.start()]+"(..)"+temp[3][r.start():]

        if temp[2]=="*":
            db_hex.append(temp)
        elif temp[2].isdigit():
            temp[2]=int(temp[2])*2
            db_hex.append(temp)
        elif "EOF" in temp[2]:
            temp[2]=int(temp[2][3:])*2
            db_hex.append(temp)

    return db_hex

def read_db():
    return read_hdb(), read_ndb()

def scan_hash(file_list, dic_hdb):
    print("\nStarting Hash Scan\n------------------")
    for f in file_list:
        print(f)
        f_hash=hashlib.md5(open(f,"rb").read()).hexdigest()
        if (f_hash in dic_hdb) and (int(dic_hdb[f_hash][0])==os.stat(f).st_size):
            print("\tdetected: {}".format(dic_hdb[f_hash][1][:-1]))
   
def scan_hex(file_list,db_hex):
    print("\nStarting Hex Signature Scan\n---------------------------")
    for f in file_list:
        print(f)
        file=open(f,'rb')
        data=str(binascii.hexlify(file.read()))[2:-1]
#        print(data)
        for d in db_hex:
            if d[2]=="*":
                if re.search(d[3],data):
                    print("\tdetected: {}".format(d[0]))
            else:
                if re.match(d[3],data[d[2]:]):
                    print("\tdetected: {}".format(d[0]))

def scan_yara(file_list,db_yara):
    print("\nStarting Yara Rule Scan\n-----------------------")
    pass

def main():
    file_list=["./eicar.com"]
    if "-f" in sys.argv:
        file_list=sys.argv[sys.argv.index("-f")+1:]
    elif "-d" in sys.argv:
        file_list=[os.path.join(sys.argv[sys.argv.index("-d")+1],f) for f in os.listdir(sys.argv[sys.argv.index("-d")+1]) if os.path.isfile(os.path.join(sys.argv[sys.argv.index("-d")+1],f))]
    else:
        print("usage:\n\t-f file1 file2 ...\n\t-d directory")
        #exit(0)

    dic_hdb,db_hex=read_db()
    scan_hash(file_list,dic_hdb)
    scan_hex(file_list,db_hex)
    scan_yara(file_list,)



if __name__=="__main__":
    main()