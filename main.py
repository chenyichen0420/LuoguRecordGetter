import pyluog as pl
import requests
import time
from openpyxl import Workbook
uid = input("please input your uid:")
client_id = input("please input your client_id(cookie):")
hackid = input("pleaes input the name of the user you're going to get:")
endnm = int(input("please input the last Pid you're going to get(doesn't include):"))

s = requests.session()
requests.utils.add_dict_to_cookiejar(s.cookies,{'__client_id':client_id,'_uid':str(uid)})
res = pl.User('*','*')
res.sess = s
res.client_id_ = client_id
res.uid = uid

# settings finished
idx = 1
exl = Workbook()
sht = exl.active
ipc = 0
conti = 1
fis = {}
fia = {}
while conti:
    lst=res.getRecordList(hackid, idx)["result"]
    # print(type(htmlback))
    # print(htmlback)
    # htmlback is a list
    for dc in lst:
        if dc["id"] == endnm:
            conti = 0
            break
        if "score" in dc.keys():
            fis[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], str(dc["score"])+'/'+str(dc["problem"]["fullScore"]), dc["submitTime"]]
            if dc["status"] == 12:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], str(dc["score"])+'/'+str(dc["problem"]["fullScore"]), dc["submitTime"]]
        else:
            if dc["status"] == 12:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], "AC/AC", dc["submitTime"]]
            else:
                fia[str(dc["problem"]["pid"])] = [str(dc["problem"]["pid"])+' '+dc["problem"]["title"], "UNAC/AC", dc["submitTime"]]
    print("page "+str(idx)+" finished!")
    idx = idx + 1
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
