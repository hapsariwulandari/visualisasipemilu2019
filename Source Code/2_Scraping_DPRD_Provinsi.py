import json
import pandas as pd
import csv
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from itertools import chain

url = "https://pemilu2019.kpu.go.id/static/json/wilayah/0.json"
resp = requests.get(url,verify = False)
data = resp.json()

try:
    table = data
    listdapil = [ k for k in table ]
    print(listdapil)

    for i in range(0, len(listdapil)):
        tabdapil = data[listdapil[i]]['dapil']
        listprovinsi = [ k for k in tabdapil ]
        print(listprovinsi)
        f=open("dprdprovinsi.csv", "a+")

        for i in range(0, len(listprovinsi)):
            if len(str(listprovinsi[i])) >= 5:
                urlprov = "https://pemilu2019.kpu.go.id/static/json/pc/"+str(tabdapil[i])+".json"
                #urlprov = "https://pemilu2019.kpu.go.id/static/json/pc/11704.json"
                print(urlprov)
                resp = requests.get(urlprov,verify = False)
                if len(resp.content) < 1:
                    continue
                #print(len(resp.content))
                dataprov = resp.json()
                tabprov = dataprov['table']
                time.sleep(3)
                print(dataprov)
                            
                if len(dataprov) > 0:
                    for i in range(0, len(dataprov)):
                       nama = dataprov['table'][i]['nama']
                       suara = dataprov['table'][i]['suara']
                       partai = dataprov['table'][i]['partai']
                       ranking = dataprov['table'][i]['ranking']
                       nomor_urut = dataprov['table'][i]['nomor_urut']
                       hasil = str(nama)+";"+str(suara)+";"+str(partai)+";"+str(ranking)+";"+str(nomor_urut)
                       #hasil = str(nama)
                       f.write(hasil + "\r\n")
                       f.flush()

    f.close()    
                
except:
    print("error guys")

