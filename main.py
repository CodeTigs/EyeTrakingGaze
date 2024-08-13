from GazeTracking.gaze_tracking import GazeTracking
import cv2 
import json
import plt

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
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 'q':
        break


frame.release()
# Recoder.release()
# closing  all the windows
cv2.destroyAllWindows()

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
