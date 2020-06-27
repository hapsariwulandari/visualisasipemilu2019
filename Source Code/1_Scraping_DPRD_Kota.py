import json
import pandas as pd
import csv
import requests
import time
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from itertools import chain

url = "https://pemilu2019.kpu.go.id/static/json/wilayah/0.json"
resp = requests.get(url,verify = False)
data = resp.json()

try:
    table = data
    listdata = [ k for k in table ]
    print(listdata)
    f=open("dprdkota.csv", "a+")
    
    for i in range (0, len(listdata)):
        urlprov = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+listdata[i]+".json"
        urlprov2 = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+listdata[i] 
        print(urlprov)
        resp = requests.get(urlprov,verify = False)
        if len(resp.content) < 1:
            continue
        dataprov = resp.json()
        tabprov = dataprov
        listkota = [ k for k in tabprov ]
        print(listkota)
        time.sleep(3)
            
        for i in range(0, len(listkota)):
            urlkota = urlprov2+"/"+str(listkota[i])+".json"
            print(urlkota)
            resp = requests.get(urlprov,verify = False)
            if len(resp.content) < 1:
                continue
            datakota = resp.json()
            tabkota = datakota[listkota[i]]['dapil']
            listkec = [ k for k in tabkota ]
            print(listkec)
            time.sleep(3)

            for i in range(0, len(listkec)):
                if len(str(listkec[i])) >= 7:
                    urlkec = "https://pemilu2019.kpu.go.id/static/json/pc/"+str(listkec[i])+".json"
                    #urlkec = "https://pemilu2019.kpu.go.id/static/json/pc/2127201.json"
                    print(urlkec)
                    resp = requests.get(urlkec,verify = False)
                    print(resp.content)
                    if len(resp.content) < 1:
                        continue
                    stringresp = str(resp.content)
                    #if re.search(['<title>Error</title>'], str(resp.content)) == True:
                    if (stringresp.find('error') > 0):
                        continue
                    print(resp.content)
                    datakec = resp.json()
                    tabkec = datakec['table']
                    #listtps = [ k for k in tabkec ]
                    #print(listtps)
                    time.sleep(3)
                    print(datakec)

                    if len(datakec) > 0:
                        for i in range(0, len(datakec)):
                           nama = datakec['table'][i]['nama']
                           suara = datakec['table'][i]['suara']
                           partai = datakec['table'][i]['partai']
                           ranking = datakec['table'][i]['ranking']
                           nomor_urut = datakec['table'][i]['nomor_urut']
                           hasil = str(nama)+";"+str(suara)+";"+str(partai)+";"+str(ranking)+";"+str(nomor_urut)
                           #hasil = str(nama)
                           f.write(hasil + "\r\n")
                           f.flush()
          
                    #if len(datakec) > 0:
                    #    hasil = str(datakec)
                    #    f.write(hasil)
                    #    f.flush()

    f.close()    
                
except:
    print("error guys")

