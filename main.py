import pyluog as pl
import requests
import time
from openpyxl import Workbook
def idtochr(vl):
    vl = vl - 1
    ret = ""
    while vl > 0:
        ret = chr('A' + (vl % 26) - 1) + ret
        vl = vl // 26
    return ret
uid=input("please input your uid:")
client_id=input("please input your client_id(cookie):")
hackid=input("pleaes input the name of the user you're going to get:")
endnm = input("please input the last Pid you're going to get(doesn't include):")

s=requests.session()
requests.utils.add_dict_to_cookiejar(s.cookies,{'__client_id':client_id,'_uid':str(uid)})
res=pl.User('*','*')
res.sess=s
res.client_id_=client_id
res.uid=uid

# settings finished
idx = 1
exl = Workbook()
sht = exl.active
ipc = 0
conti = 1
fis = {}
fia = {}
while conti:
    lst=res.getRecordList("581015",idx)["result"]
    # print(type(htmlback))
    # print(htmlback)
    # htmlback is a list
    for dc in lst:
        if str(dc["problem"]["pid"]) == endnm:
            conti = 0
            break
        if "score" in dc.keys():
            fis[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], str(dc["score"])+'/'+str(dc["problem"]["fullScore"]), dc["submitTime"], dc["id"]]
            if dc["status"] == 12:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], str(dc["score"])+'/'+str(dc["problem"]["fullScore"]), dc["submitTime"], dc["id"]]
        else:
            if dc["status"] == 12:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], "AC/AC", dc["submitTime"], dc["id"]]
            else:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], "UNAC/AC", dc["submitTime"], dc["id"]]
    idx = idx + 1
    print("page "+str(idx)+" finished!")
for sub in fis:
    pro = ""
    stat = ""
    atim = ""
    pro = fis[sub][0]
    stat = fis[sub][1]
    if sub in fia.keys():
        loctim = time.localtime(fia[sub][2])
        # loctim is time.structtime
        atim = atim + str(loctim.tm_year) + '/'
        atim = atim + str(loctim.tm_mon) + '/'
        atim = atim + str(loctim.tm_mday) + ' '
        atim = atim + str(loctim.tm_hour) + ':'
        atim = atim + str(loctim.tm_min)
    else:
        atim = "UNAC yet"
    print(pro+' '+stat+' '+atim)
    ipc = ipc + 1
    sht['A' + str(ipc)] = pro
    sht['B' + str(ipc)] = stat
    sht['D' + str(ipc)] = atim
exl.save(filename = 'Record.xlsx')
