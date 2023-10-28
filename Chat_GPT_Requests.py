
# key: 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

import requests
import json
key = "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"
headers = {"Authorization":"Bearer " + key,"Content-Type":"application/json"}
linkGetModelos = "https://api.openai.com/v1/models"
linkPostCriarChat = "https://api.openai.com/v1/chat/completions"
linkPostGerarImagem = "https://api.openai.com/v1/images/generations"
#id_modelo = "gpt-3.5-turbo-16k-0613"
#
#body_msg = {
#    "model":id_modelo,
#    "messages":[{"role":"user","content":"você é um professor de física. me explique de forma simples como o sol foi formado."}]
#
#}
#body_msg = json.dumps(body_msg)
#requisicao = requests.post(linkPostCriarChat,headers = headers,data = body_msg)

#print(requisicao)
#print(requisicao.text)
#resposta = requisicao.json()
#gpt_Respondeu = resposta["choices"][0]["message"]["content"]
#print(gpt_Respondeu)



#body_Imag = {
#    "prompt":"marceline de hora de aventura tocando flauta",
#    "n": 2,
#    "size":"1024x1024"
#}
#body_Imag = json.dumps(body_Imag)

#requisicao = requests.post(linkPostGerarImagem,headers = headers,data = body_Imag)
#print(requisicao)
#print(requisicao.text)

img = open('imagem.png')

body_ImagEdit = {
    "image": img,
    "prompt":"Flores coloridas e vagalumes ",
    "n": 1,
    "size":"1024x1024"
}
body_ImagEdit = json.dumps(body_ImagEdit)

requisicao = requests.post(linkPostGerarImagem,headers = headers,data = body_ImagEdit)
print(requisicao)
print(requisicao.text)

#Pegar Modelos da openIa
#requisicao = requests.get(linkGetModelos,headers = headers)
#print(requisicao)
#print(requisicao.text)

