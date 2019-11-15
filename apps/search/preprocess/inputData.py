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
        #print (infos[1])
        if "/" in infos[1]:
            director = infos[1].split("/")
            director = [x.strip() for x in director]
        else :director = infos[1].strip()

        if "/" in infos[2]:
            writer = infos[2].split("/")
            writer = [x.strip() for x in writer]
        else:
            writer = infos[2].strip()
        #print(infos[3])
        if "/" in infos[3]:
            actor = infos[3].split("/")
            actor = [x.strip() for x in actor]
        else:
            actor = infos[3].strip()


        if "/" in infos[4]:
            type = infos[4].split("/")
            type = [x.strip() for x in type]
        else:
            type = infos[4].strip()

        if "/" in infos[5]:
            country = infos[5].split("/")
            country = [x.strip() for x in country]
        else:
            country = infos[5].strip()

        if "/" in infos[9]:
            alias = infos[9].split("/")
            alias = [x.strip() for x in alias]
        else:
            alias = infos[9].strip()
        #alias = infos[9]
        brief = infos[11].lstrip("\"").rstrip("\"")
        id = infos[12]
        score = infos[13]
        cnum = infos[14].rstrip("\n")
        #print (name,director,writer,actor,type,country,alias,brief,id,score,cnum)

        data = {
            'name' : name,
            'director' : director,
            'writer' : writer,
            'actor' : actor,
            'type' : type,
            'country' : country,
            'alias' : alias,
            'brief' : brief,
            'score' : score,
            'cnum' : cnum
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
        with open("D:\movieinfo", 'a') as json_file:
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