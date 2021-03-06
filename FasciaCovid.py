import re
import sys
import json
import requests
from bs4 import BeautifulSoup

govUrl = 'http://www.salute.gov.it/portale/nuovocoronavirus/dettaglioContenutiNuovoCoronavirus.jsp?area=nuovoCoronavirus^&id=5351^&lingua=italiano^&menu=vuoto'
govData = requests.get(govUrl)

if govData.status_code != 200:
    print('Errore. La pagina ha risposto con il codice ' + str(govData.status_code) + '. Termino l\'esecuzione.')
    raise SystemExit
else:
    govData = BeautifulSoup(govData.content, 'html.parser')

regioniArr = {}

regioniBianche = govData.find('div', style=re.compile(r'border: 1px solid #000;border-top:0*?')).get_text(separator="\n").strip()
regioniBianche = regioniBianche.split('\n')
regioniArr['regioniBianche'] = list(map(str.strip, filter(None, regioniBianche)))

regioniGialle = govData.find('div', style=re.compile(r'border: 1px solid #f8c300*?')).get_text(separator="\n").strip()
regioniGialle = regioniGialle.split('\n')
regioniArr['regioniGialle'] = list(map(str.strip, filter(None, regioniGialle)))

regioniArancioni = govData.find('div', style=re.compile(r'border: 1px solid #e78314*?')).get_text(separator="\n").strip()
regioniArancioni = regioniArancioni.split('\n')
regioniArr['regioniArancioni'] = list(map(str.strip, filter(None, regioniArancioni)))

regioniRosse = govData.find('div', style=re.compile(r'border: 1px solid #dd222a*?')).get_text(separator="\n").strip()
regioniRosse = regioniRosse.split('\n')
regioniArr['regioniRosse'] = list(map(str.strip, filter(None, regioniRosse)))

if(len(sys.argv) > 1):
    endFileName = sys.argv[1]
else:
    endFileName = 'fasceRegioni.json'

outFile = open(endFileName, 'w')
json.dump(regioniArr, outFile)
