from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import os
import time
import pyttsx3

subscription_key = "ab9ae7803979414b8bf913c55a1e578e"
endpoint = "https://cp3-rm94075.cognitiveservices.azure.com/"

# Autenticar o cliente
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#
# Inicia o programa de fala
#
engine = pyttsx3.init()


def falar(texto):
    engine.say(texto)
    engine.runAndWait()


#
# Leitura de Imagem Local
#

# Pasta criada anteriormente
images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

# Pergunta qual imagem deseja ler
imagem = input("Digite o nome do arquivo da imagem:\n") + ".png"

'''
Este exemplo extrai texto de uma imagem local e depois imprime os resultados
'''
print("Lendo Arquivo...")
# Obter caminho da imagem
read_image_path = os.path.join(images_folder, imagem)
# Abre a imagem
read_image = open(read_image_path, "rb")

read_response = computervision_client.read_in_stream(read_image, raw=True)
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status.lower () not in ['notstarted', 'running']:
        break
    print('Esperando resultado...')
    time.sleep(10)

# Salva o texto detectado em um arquivo .txt
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            with open("frases.txt", 'a') as arquivo:
                arquivo.write(line.text)


# Lê a frase da imagem
with open("frases.txt", "r") as arquivo:
    frase = arquivo.readlines()
    falar(frase)

# Limpa o arquivo para poder ler outra imagem
with open("frases.txt", "w") as arquivo:
    arquivo.write("")

arquivo.close()


