from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json

import socket
from threading import Thread

online = True

global msgEsp8266
# Validacao da pasta de modelo
# Eh necessario criar a pasta model-br a partir de onde estiver este fonte
if not os.path.exists("model-br"):
    print ("Modelo em portugues nao encontrado.")
    exit (1)

#preparando server local
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.1.110", 5252))
serversocket.listen(100)

clientes = []
msgEsp8266 = "Vazio"

#Preparando Locutor
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 10)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + volume + 0.50)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#engine.save_to_file('Olá Meu Criador, como posso lhe ser útil ?', "test.mp3")
#engine.runAndWait()

engine.say('Olá Meu Criador,estou acordada, qualquer coisa é so me chamar.')
engine.runAndWait()

# Preparando o microfone para captura
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Apontando o algoritmo para ler o m odelo treinado na pasta "model-br"
model = Model("model-br")
rec = KaldiRecognizer(model, 16000)

#Chaves de comandos
dispositivos = ["lâmpada","luz", "luzes", "ventilador","ventiladores"]
locais = ["quarto", "banheiro", "externa","sala"]
comandos = ["ligar", "desligar", "aumentar","diminuir","mudar","café","leite"]
#funcao de executar comandos
def executarComando(palavras,posicaoChamada):
    global msgEsp8266
    resposta = "Sua ordem é tudo, meu Senhor."
    print("posicao da chamada Carol" + str(posicaoChamada))
    print(str(len(palavras)) + " Palavras ditas")
    print("Executando comando: ")
    if len(palavras) > 1:
        comando = procurarComando(palavras)
        match comando:

            case "ligar":
                print ("Ligar")
                desp = procurarDispositivo(palavras)
                local = procurarLocais(palavras)

                if desp != "Erro" and local != "Erro":
                    resposta = "Ligando " + desp + " de " + local
                    msgEsp8266 = "LED ON"
                else:
                    resposta = "Algo deu errado ao ligar."
                
            case "desligar":
                print ("Desligar")
                desp = procurarDispositivo(palavras)
                local = procurarLocais(palavras)

                if desp != "Erro" and local != "Erro":
                    resposta = "Desligando " + desp + " de " + local
                    msgEsp8266 = "LED OFF"
                    
                else:
                    resposta = "Algo deu errado ao desligar."
                
            case "leite":
                print ("Leite")
                resposta = "Leite bem Gelado saindo."
            case "café":
                print ("Café")
                resposta = "Cafézinho Beeeeeeeeeeeem Quente saindo!!"

            case _:
                print ("Comando Inválido")
                resposta = "Comando Inválido meu Senhor..."
    else:
        print ("Você só falou o nome dela ?")
        resposta = "O senhor me chamou?"
    return resposta



def procurarLocais(palavras):
    print("Buscando Locais....")
    indexLoc = 0;
    indexPal = 0;
    for palavra in palavras:
        indexLoc = 0
        for local in locais:
            if local == palavra:
                print("[ "+ local + " ]existe na lista!")
                print("Index Local: " + str(indexLoc))
                print("Index Palavra: " + str(indexPal))
                return local
            indexLoc += 1
        indexPal +=1
    return "Erro"   

def procurarDispositivo(palavras):
    print("Buscando Dispositivos....")
    indexDisp = 0;
    indexPal = 0;
    for palavra in palavras:
        indexDisp = 0
        for disp in dispositivos:
            if disp == palavra:
                print("[ "+ disp + " ]existe na lista!")
                print("Index Dispositivo: " + str(indexDisp))
                print("Index Palavra: " + str(indexPal))
                return disp
            indexDisp += 1
        indexPal +=1
    return "Erro"

def procurarComando(palavras):
    print("Buscando Comandos....")
    indexcom = 0;
    indexPal = 0;
    for palavra in palavras:
        indexcom = 0
        for comando in comandos:
            if comando == palavra:
                print("[ "+ comando + " ]existe na lista!")
                print("Index Comando: " + str(indexcom))
                print("Index Palavra: " + str(indexPal))
                return comando
            indexcom += 1
        indexPal +=1
    return "Erro"

# Crinado Threads para conexoes de clientes

def cliente(soquete, online):
    while online == True:
        print("Esperando Conexão...")
        conn, address = soquete.accept()  # accept new connection
        print("Connection from: " + str(address))
        responderCliente(conn)

        
def responderCliente(conexao):

    data = conexao.recv(1024).decode()
    if not data:
        return
    print("from connected user: " + str(data))
    data = msgEsp8266
    conexao.send(data.encode())  # send data to the client
    conexao.close()  # close the connection
    print("Conexão Finalizada.")

#Iniciando threads
ouvirClientes = Thread(target=cliente,args=[serversocket,online])
ouvirClientes.start()


# Criando um loop continuo para ficar ouvindo o microfone
while True:
    # Lendo audio do microfone
    data = stream.read(4096)
    
    # Convertendo audio em texto
    if rec.AcceptWaveform(data):
      # Fazendo a leitura do JSON para extrair apenas o texto capturado
        #print(rec.Result())
        finalResult = json.loads(rec.Result())
        texto = finalResult.get("text")
        print("Ela Entendeu: " + texto)
        print("MSG ESP8266: " + msgEsp8266)
        # Verifica se ha texto a ser dito antes de enviar para o TTS
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
                print("A chamou!")        
                stream.stop_stream()
                #procurarComando(palavrasDitas,indexCarol)
                #procurarLocais(palavrasDitas,indexCarol)
                #engine.say("Execuntado Comandos...")
                
                engine.say(executarComando(palavrasDitas,indexCarol))

                engine.runAndWait()
                stream.start_stream()
            else:
                 print("Não a  chamou.")
                
        else:
            print(rec.PartialResult())
