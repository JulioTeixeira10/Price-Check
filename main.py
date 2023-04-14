import requests
from configparser import ConfigParser
import xml.etree.ElementTree as ET

dirDados = "C:\\Bancamais\\Fastcommerce\\DadosLoja"

#Administração do arquivo .cfg
config_object = ConfigParser()
config_object.read(f"{dirDados}\\StoreData.cfg")
STOREINFO = config_object["STOREINFO"]
StoreName = STOREINFO["StoreName"]
StoreID = STOREINFO["StoreID"]
Username = STOREINFO["Username"]
password = STOREINFO["password"]

#Request
url = "https://www.rumo.com.br/sistema/adm/APILogon.asp"
payload= (f"""StoreName={StoreName}&StoreID={StoreID}&Username={Username}&
          method=ReportView&password={password}&ObjectID=425&Fields=IDProduto, Preco""")
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, headers=headers, data=payload)
resposta = response.text

with open("C:\\Users\\Usefr\\Desktop\\Integração[Bmais - FC ]\\Stock-Check\\output.xml","w+") as f:
    f.write(resposta)
    f.close()

#Extrai os elementos do xml do fc
root = ET.fromstring(response.text)
produtos_fc = {}

for record in root.findall('Record'):
    id_produto = record.find('Field[@Name="IDProduto"]').attrib['Value']
    estoque = record.find('Field[@Name="Preco"]').attrib['Value']
    produtos_fc[id_produto] = estoque


#Extrai os elementos do txt do b+
with open("C:\\Users\\Usefr\\Desktop\\Integração[Bmais - FC ]\\Price-Check\\Input1B+.txt", "r") as r:
    file_contents = r.read()

produtos_bmais = {}

for line in file_contents.split('\n'):
    line = line.strip() 
    if not line:  
        break
    id_produto = line[0:8].strip() 
    estoque = line[8:].strip() 
    produtos_bmais[id_produto] = estoque

if len(produtos_bmais) != len(produtos_fc):
    print(f"DIVERGÊNCIA ENCONTRADA: A quantidade de produtos entre sistemas não é a mesma: [FC = {len(produtos_fc)} <-> B+ {len(produtos_bmais)}]")

c = 0

for key in produtos_bmais:
    if produtos_bmais[key] != produtos_fc[key]:
        print(f"Diferença de preço encontrada: ID = {key} // B+ = R$ {produtos_bmais[key]} <-> FC = R$ {produtos_fc[key]}")
        c += 1

if c == 0:
    print("Nenhuma diferença encontrada.")
else:
    if c == 1:
        print("\n")
        print(f"Foi encontrada apenas {c} diferença de preço em total.")
        print("\n")
    else:
        print("\n")
        print(f"Foram encontradas {c} diferenças de preço em total.")
        print("\n")