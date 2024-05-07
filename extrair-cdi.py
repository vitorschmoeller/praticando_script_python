import os
import json
from random import random
from datetime import datetime

import requests
#Padrão para declarar variáveis que não se alteram constante
URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

# Criando a variável data e hora

data_e_hora = datetime.now()
data = datetime.strftime(data_e_hora, '%Y/%m/%d')
hora = datetime.strftime(data_e_hora, '%H:%M:%S')

# Captando a taxa CDI do site da B3

try:
  response = requests.get(URL)
  response.raise_for_status()
except requests.HTTPError as exc:
  print("Dado não encontrado, continuando.")
  cdi = None
except Exception as exc:
  print("Erro, parando a execução.")
  raise exc
else:
  #Transformando a resposta da requisição com o get em um json através da biblioteca json.loads(get)
  dado = json.loads(response.text)
  cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5) 

# Verificando se o arquivo "taxa-cdi.csv" existe
#os é um pacote de interação com o sistema operacional
#path tem a função exists para verificar a existência do arquivo
if os.path.exists('./taxa-cdi.csv') == False:
  #Se não existir, criamos ele aqui
  with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
    fp.write('data,hora,taxa\n')

# Salvando dados no arquivo "taxa-cdi.csv"

with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
  fp.write(f'{data},{hora},{cdi}\n')

print("Sucesso")