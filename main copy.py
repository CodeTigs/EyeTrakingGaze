import cv2 as cv
import numpy as np
import time
import json
import matplotlib.pyplot as plt
from GazeTracking.gaze_tracking import GazeTracking
import os

def jsonFormat(information):
    if os.path.exists('cache/informationEye.json'):
        with open('cache/informationEye.json', 'r') as f:
            data = json.load(f)
    else:
        data = []
    data.append(information)
    with open("cache/informationEye.json", 'w') as f:
        json.dump(data, f, indent=2)

def jsonFormat2(information):
    if os.path.exists('cache/norm.json'):
        with open('cache/norm.json', 'r') as f:
            data = json.load(f)
    else:
        data = []
    data.append(information)
    with open("cache/norm.json", 'w') as f:
        json.dump(data, f, indent=2)

def dictFormat( X, Y, width, height, time):
    dictonary = {}
    quadrante1 = (X > 0 and X < width/3) and (Y > 0 and Y < height/3)
    quadrante2 = (X > width/3 and X < 2 * (width/3)) and (Y > 0 and Y < height/3)
    quadrante3 = (X > 2 * (width/3) and X < width) and (Y > 0 and Y < height/3)
    quadrante4 = (X > 0 and X < width/3) and (Y > height/3 and Y < 2*(height/3))
    quadrante5 = (X > width/3 and X < 2 * (width/3)) and (Y > height/3 and Y < 2*(height/3))
    quadrante6 = (X > 2 * (width/3) and X < width) and (Y > height/3 and Y < 2*(height/3))
    quadrante7 = (X > 0 and X < width/3) and (Y > 2*(height/3) and Y < height)
    quadrante8 = (X > width/3 and X < 2 * (width/3)) and (Y > 2*(height/3) and Y < height)
    quadrante9 = (X > 2 * (width/3) and X < width) and (Y > 2*(height/3) and Y < height)

    if quadrante1:
        dictonary = dict(
            horizontal = 'esquerda',
            vertical = 'cima'
        )

    elif quadrante2:
        dictonary = dict(
            horizontal = 'centro',
            vertical = 'cima'
        )

    elif quadrante3:
        dictonary = dict(
            horizontal = 'direita',
            vertical = 'cima'
        )
    elif quadrante4:
        dictonary = dict(
            horizontal = 'esquerda',
            vertical = 'centro'
        )
    elif quadrante5:
        dictonary = dict(
            horizontal = 'centro',
            vertical = 'centro'
        )
    elif quadrante6:
        dictonary = dict(
            horizontal = 'direita',
            vertical = 'centro'
        )
    elif quadrante7:
        dictonary = dict(
            horizontal = 'esquerda',
            vertical = 'baixo'
        )
    elif quadrante8:
        dictonary = dict(
            horizontal = 'centro',
            vertical = 'baixo'
        )
    elif quadrante9:
        dictonary = dict(
            horizontal = 'direita',
            vertical = 'baixo'
        )
    else:
        return -1
    dict2 = dictFormatCenter(X, Y, time)
    dictonary['instante'] = time
    dictonary.update(dict2)
    print(dictonary)
    return dictonary

def dictFormatCenter( X, Y, starttime):
    #dictonary = {}
    if (X != None and Y != None) or (X > 0 and Y > 0):
        dictonary = dict(
                X = float(X),
                Y = float(Y),
                instante = time.time()- starttime,
                )
        print(dictonary)
        return dictonary
    else:
        return -1
    
def dictFormatnorm(X, Y, time):
    dictonary = {}
    dict2 = dictFormatCenter(X, Y, time)
    dictonary['instante'] = time
    dictonary.update(dict2)
    print(dictonary)
    return dictonary

def maiormenorxy():
    with open('cache/informationEye.json') as f:
        dados = json.load(f)
    maior_x = max(dado["X"] for dado in dados if isinstance(dado, dict) and "X" in dado and dado['instante'] < 30)
    maior_y = max(dado["Y"] for dado in dados if isinstance(dado, dict) and "Y" in dado and dado['instante'] < 60)
    menor_x = min(dado["X"] for dado in dados if isinstance(dado, dict) and "X" in dado and dado['instante'] < 90)
    menor_y = min(dado["Y"] for dado in dados if isinstance(dado, dict) and "Y" in dado and dado['instante'] < 120)

    normalx = maior_x - menor_x
    normaly = maior_y - menor_y
    if (normalx <= 0 or normaly <= 0) or (normalx == None or normaly == None):
        print("erro ao processar os dados")
        os._exit(0)
    return normalx, normaly

gaze = GazeTracking()
normalizar = False
# Variables
COUNTER = 0
TOTAL_BLINKS = 0
CLOSED_EYES_FRAME = 3
cameraID = 0
videoPath = "Video/Your Eyes Independently_Trim5.mp4"
# variables for frame rate.
FRAME_COUNTER = 0
START_TIME = time.time()
FPS = 0
# creating camera object
camera = cv.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
f = camera.get(cv.CAP_PROP_FPS)
width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)
print(width, height, f)
fileName = videoPath.split('/')[1]
name = fileName.split('.')[0]
bestMinT = 0
#image = cv.imread('images/9quadrantes.jpeg')

# Obtém as dimensões da tela
screen_width = 1920 # Coloque a largura da sua tela
screen_height = 1080 # Coloque a altura da sua tela
# Redimensiona a imagem para o tamanho da telaimage = cv.resize(image, (screen_width, screen_height))
# Mostra a imagem em tela cheia
#cv.namedWindow('Imagem', cv.WND_PROP_FULLSCREEN)
#cv.setWindowProperty('Imagem', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
#cv.imshow('Imagem', image)
cv.waitKey(1)
while True:
    SECONDS = time.time() - START_TIME
    FRAME_COUNTER += 1
    # getting frame from camera
    ret, frame = camera.read()
    ret, frame2 = camera.read()
    if ret == False:
        break
    gaze.refresh(frame)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if int(SECONDS) >= 0 and int(SECONDS) < 30:
        direita = cv.imread('pointImages/direita.png')
        direita = cv.resize(direita, (screen_width, screen_height))
        cv.namedWindow('Direita', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty('Direita', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Direita', direita) 
        print('direita')
    if int(SECONDS) >= 30 and int(SECONDS) < 60:
        cv.destroyWindow('Direita')
        cima = cv.imread('pointImages/cima.png')
        cima = cv.resize(cima, (screen_width, screen_height))
        cv.namedWindow('Cima', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty('Cima', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Cima', cima)
        print('cima')
    if int(SECONDS) >= 60 and int(SECONDS) < 90:
        cv.destroyWindow('Cima')
        esquerda = cv.imread('pointImages/esquerda.png')
        esquerda = cv.resize(esquerda, (screen_width, screen_height))
        cv.namedWindow('Esquerda', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty('Esquerda', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Esquerda', esquerda)
        print('esquerda')
    if int(SECONDS) >= 90 and int(SECONDS) <= 120:
        cv.destroyWindow('Esquerda')
        baixo = cv.imread('pointImages/baixo.png')
        baixo = cv.resize(baixo, (screen_width, screen_height))
        cv.namedWindow('Esquerda', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty('Esquerda', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Baixo', baixo)
    if SECONDS >= 120 and not normalizar:
        cv.destroyWindow('Baixo')
        normx, normy = maiormenorxy()
        normalizar = True
        video_path = 'Video.mp4'
        cap = cv.VideoCapture(video_path)

    if normalizar:
        if left_pupil == None:
            cordenates = dictFormat(0.0, 0.0,normx, normy, SECONDS)
        else:
            cordenates = dictFormat(left_pupil[0], left_pupil[1],normx, normy, SECONDS)
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler o vídeo")
            break
        cv.imshow('Video', frame)
        jsonFormat(cordenates)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    if not normalizar:
        if left_pupil == None:
            cordenates = dictFormatnorm(0.0, 0.0, SECONDS)
        else: 
            cordenates = dictFormatnorm(left_pupil[0], left_pupil[1], SECONDS)
        jsonFormat2(cordenates)
    key = cv.waitKey(1)

    # if q is pressed on keyboard: quit
    if key == ord('q'):
        break
# closing the camera
camera.release()
# Recoder.release()
# closing  all the windows
cv.destroyAllWindows()

with open('cache/informationEye.json') as f:
    dados = json.load(f)

#maior_x = max(dado["X"] for dado in dados if isinstance(dado, dict) and "X" in dado)
#maior_y = max(dado["Y"] for dado in dados if isinstance(dado, dict) and "Y" in dado)
#menor_x = min(dado["X"] for dado in dados if isinstance(dado, dict) and "X" in dado)
#menor_y = min(dado["Y"] for dado in dados if isinstance(dado, dict) and "Y" in dado)

x = [dado["X"] for dado in dados  if isinstance(dado, dict)]
y = [dado["Y"] for dado in dados  if isinstance(dado, dict)]



# Crie um dicionário para armazenar a contagem de cada ponto
pontos = {}
for i in range(len(x)):
    ponto = (x[i], y[i])
    if ponto in pontos:
        pontos[ponto] += 1
    else:
        pontos[ponto] = 1

# Separe os pontos únicos e repetidos
pontos_unicos = [ponto for ponto, count in pontos.items() if count == 1]
pontos_repetidos = [ponto for ponto, count in pontos.items() if count > 1]
tamanho_repetidos = [pontos[ponto] * 50 for ponto in pontos_repetidos]  # Tamanho proporcional ao número de repetições

# Plote os pontos únicos
plt.scatter([ponto[0] for ponto in pontos_unicos], [ponto[1] for ponto in pontos_unicos], color='blue', label='Pontos únicos')

# Plote os pontos repetidos com tamanhos maiores
plt.scatter([ponto[0] for ponto in pontos_repetidos], [ponto[1] for ponto in pontos_repetidos], s=tamanho_repetidos, color='blue', label='Pontos repetidos')

# Adicione legendas e rótulos
plt.legend()
plt.xlabel('Valores de X')
plt.ylabel('Valores de Y')
plt.title('Gráfico de Dispersão com Pontos Repetidos Destacados')
plt.grid(True)

# Exiba o gráfico
plt.show()
