from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
import socket
from threading import Thread
import time
import requests

global mutado
global ounvindo
global online
global ouviuIsso
global respostasClientes
global usandoGPT

ouviuIsso = "Vazio"
online = True
mutado = False
ounvindo = False
usandoGPT =  False


#preparando requestes pro chat gpt
key = "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"
headers = {"Authorization":"Bearer " + key,"Content-Type":"application/json"}
linkGetModelos = "https://api.openai.com/v1/models"
linkPostCriarChat = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo-16k-0613"


#preparando server local
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.1.110", 5252))



#Preparando Locutor
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 15)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + volume + 0.50)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Preparando o microfone para captura
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

# Apontando o algoritmo para ler o m odelo treinado na pasta "model-br"
# Validacao da pasta de modelo
# Eh necessario criar a pasta model-br a partir de onde estiver este fonte
if not os.path.exists("model-br"):
    print ("Modelo em portugues nao encontrado.")
    exit (1)

model = Model("model-br")
rec = KaldiRecognizer(model, 16000)


#Funcão para Falar texto. thread
def Falar(texto):
    global mutado
    print("Thread [Falar] Inicializada!")
    if len(texto) > 0:
        mutado = True
        time.sleep(0.3)
        engine.say(texto)
        engine.runAndWait()
        time.sleep(0.3)
        mutado = False
    
    print("Thread [Falar] Finalizada!")


#Funcão para Mandar Requisicao ao Chat GPT. thread
def PerguntasGPT(pergunta):
    global mutado
    global usandoGPT
    
    print("Thread [PerguntasGPT] Inicializada!")
    usandoGPT = True
    if len(pergunta) > 0:
        #pergunta = "você é um professor de física. me explique de forma simples como o sol foi formado."
        body_msg = {
            "model":id_modelo,
            "messages":[{"role":"user","content": pergunta}]
        }
        body_msg = json.dumps(body_msg)

        mutado = True
        time.sleep(0.1)
        engine.say("Enviando Pergunta ao GPT.")
        engine.runAndWait()
        requisicao = requests.post(linkPostCriarChat,headers = headers,data = body_msg)
        resposta = requisicao.json()
        print(requisicao.text)
        gpt_Respondeu = resposta["choices"][0]["message"]["content"]
        engine.say("O Chat GPT Respondeu: " + gpt_Respondeu)
        engine.runAndWait()
        time.sleep(0.1)
        mutado = False
    
    print("Thread [PerguntasGPT] Finalizada!")
    usandoGPT = False
    
#Função para ouvir e transformar em texto. thread loop
def OuvirAmbiente():
    global mutado
    global ounvindo
    global ouviuIsso
    global online
    print("Thread [Ouvir Ambiente] Iniciada.")
    while online:
        if mutado == False:
            # Lendo audio do microfone
            ounvindo = True
            data = stream.read(4096)
            # Convertendo audio em texto
            if rec.AcceptWaveform(data):
                ounvindo = False
                #Fazendo a leitura do JSON para extrair apenas o texto capturado
                finalResult = json.loads(rec.Result())
                texto = finalResult.get("text")
                if len(texto) > 0 :
                    #Verifica se chamou o nome da assistente
                    chamou = False
                    indexCarol = 0;
                    palavrasDitas = texto.split()
                    for x in palavrasDitas: 

                      if x == "dezoito":
                        chamou = True
                        break
                      else:
                        indexCarol += 1
                    if chamou == True:  
                        #Inicia pergunta GPT Request thread
                        thread_GPT = Thread(target=PerguntasGPT,args=[texto[7:]])
                        thread_GPT.start()

                        
                    else:
                        #Fazendo a leitura do JSON para extrair apenas o texto capturado
                        print("Result: " + texto)
                        ouviuIsso = texto
                        #print( "PartialResult: " + rec.PartialResult())
        else:
            time.sleep(0.1)
    print("Thread [Ouvir Ambiente] Finalizada!")



#Função para aceitar conexoes. thread loop
def AceitarConexoes(soquete):
    global ouviuIsso
    global online
    global respostasClientes
    recebeu = "null"
    print("Thread [Aceitar Conexoes] Iniciada.")
    serversocket.listen(100)
    while online == True:
        
      #  print("Esperando pedido de conexão...")
        conexao, address = soquete.accept()  # accept new connection

        #Receber e Enviar Pacotes
        data = ouviuIsso
        conexao.send(data.encode())  # send data to the client
        i = 10000
        while i > 0:
            i += -1
            data = conexao.recv(1024).decode()
            if len(data) > 0:
                recebeu = str(data)
                if recebeu == "OK":
                   print(".") 
                else:
                    print("Respota: " + recebeu)
                    #Responder em Fala
                    thread_aceitarConexoes = Thread(target=Falar,args=[recebeu])
                    thread_aceitarConexoes.start()
                    
                break
            
        conexao.close()  # close the connection
        ouviuIsso = "vazio"
       # print("Conexao de : " + str(address) +", Recebeu: " + recebeu)


    print("Thread [Aceitar Conexoes] Finalizada!")

#Iniciando threads
print("Instanciando threads...")

#Fala em texto 
thread_OuvirAmbiente = Thread(target=OuvirAmbiente,args=[])
thread_OuvirAmbiente.start()

#Receber Conexoes
thread_aceitarConexoes = Thread(target=AceitarConexoes,args=[serversocket])
thread_aceitarConexoes.start()







    






