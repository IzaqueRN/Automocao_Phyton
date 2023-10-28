from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json

# Validacao da pasta de modelo
# Eh necessario criar a pasta model-br a partir de onde estiver este fonte
if not os.path.exists("model-br"):
    print ("Modelo em portugues nao encontrado.")
    exit (1)

#Preparando Locutor
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
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
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Apontando o algoritmo para ler o m odelo treinado na pasta "model-br"
model = Model("model-br")
rec = KaldiRecognizer(model, 16000)

# Criando um loop continuo para ficar ouvindo o microfone
while True:
    # Lendo audio do microfone
    data = stream.read(4000)
    
    # Convertendo audio em texto
    if rec.AcceptWaveform(data):
      # Fazendo a leitura do JSON para extrair apenas o texto capturado
        #print(rec.Result())
        finalResult = json.loads(rec.Result())
        texto = finalResult.get("text")
        print(texto)
        # Verifica se ha texto a ser dito antes de enviar para o TTS
        if len(texto) > 0 :
            #Verifica se chamou o nome da assistente
            chamou = False
            palavrasDitas = texto.split()
            for x in palavrasDitas: 
              if x == "carol":
                chamou = True
                break
            if chamou == True:
                print("A chamou!")
                stream.stop_stream()
                engine.say("Estou aqui,meu Senhor.")
                engine.runAndWait()
                stream.start_stream()
            else:
                 print("Não a  chamou.")
                

        else:
            print(rec.PartialResult())
