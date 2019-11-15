# coding=utf-8
import re
import json
def getInputJson():
    f = open('G:\School\git\info.csv',mode='r',encoding='utf-8')
    index = 0;
    linenum=0;
    for line in f:
        if index==0:
            index = 1
            continue;
        infos = line.split("\t")
        name = infos[0]

        if "/" in infos[9]:
            alias = infos[9].split("/")
            alias = [x.strip() for x in alias]
        else:
            alias = infos[9].strip()

        id = infos[12]

        data = {
            'name' : name,
            'alias' : alias
        }

        idline = {
            'index' : {'_id' : id}
        }
        idj = json.dumps(idline,ensure_ascii=False)
        #print(idline)
        #infoline = "{\"name\":\""+ name +"\",\"director\":\""+director+ "\""+"\",\"writer\":\""+writer+"\",\"actor\":\""+actor+"\",\"type\":\""+type+"\",\"country\":\""+country+"\",\"alias\":\""+alias+"\",\"brief\":\""+brief+"\",\"score\":\""+score+"\",\"cnum\":\""+cnum+'}'
        #print(infoline)
        json_str = json.dumps(data,ensure_ascii=False)
        #print(idj)
        #print(json_str)
        linenum=linenum+1

        with open("D:\suggest", 'a') as json_file:
            json.dump(idline,json_file,ensure_ascii=False)
            json_file.write("\n")
            json.dump(data, json_file,ensure_ascii=False)
            json_file.write("\n")
        if linenum%100 == 0:
            print("line: ",linenum)
    print(linenum)


def test():
    S = "这是 / 一个 / 测试"
    l = S.split("/")
    for i in l:
        print (i)
if __name__ == '__main__':
    getInputJson()
    #test()