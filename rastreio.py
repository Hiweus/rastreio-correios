from requests import Session
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    print("======================================")
    print("O codigo de rastreio não foi fornecido")
    print("======================================")
    exit(0)

codigo = sys.argv[1]

s = Session()

response = s.post("https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?", data={
    "acao": "track",
    "btnPesq": "Buscar",
    "objetos": codigo
})

site = response.text.replace("\r\n", "\n").replace("\t", "")

html = BeautifulSoup(site, "html.parser")

events = html.find_all("table", class_="listEvent sro")
if len(events) == 0:
    print("======================================================")
    print("Nenhum evento encontrado, verifique o codigo fornecido")
    print("   Ou aguarde a postagem da encomenda nos correios    ")
    print("======================================================")
    exit(0)


for i in events:
    print("===========================================")

    [datalocal, acao] = i.find_all("td")
    
    content = datalocal.text.split("\n")
    
    data = content[0]
    hora = content[1]
    local = content[2]


    content = acao.text.split("\n\n")

    acao = content[0].strip()
    depara = content[1].replace("\n", " ").strip().replace("  ", " ")

    
    print("Situação:",acao)
    print("Movimentação:", depara)

print("===========================================")
