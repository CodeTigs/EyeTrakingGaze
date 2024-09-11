import subprocess
from flask import Flask, request, jsonify
import json
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from threading import Thread, Event
import selenium.webdriver as webdriver
import pyautogui
import signal
import sys
import requests

logging.basicConfig(level=logging.CRITICAL)

app = Flask(__name__)

# Configurações personalizáveis
DATA_DIR = 'data'
FILENAME = 'gaze_data.json'
OUTPUT_DIR = 'images'
OUTPUT_FILENAME = 'heatmap.png'

# Certifique-se de que o diretório existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def shutdown_server():
    requests.get('http://127.0.0.1:5000/shutdown')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Não foi possível encerrar o servidor.')
    func()
    return sys.exit()

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/save_data', methods=['POST', 'OPTIONS'])
def save_data():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful'}), 200
    
    logging.debug(f"Requisição recebida: {request.json}")
    
    try:
        data = request.get_json()
        timestamp = time.time()
        data['timestamp'] = timestamp

        # Caminho completo para o arquivo JSON
        filepath = os.path.join(DATA_DIR, FILENAME)
        
        # Se o arquivo já existir, carregar os dados existentes
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Adicionar novos dados
        existing_data.append(data)

        # Salvar de volta no arquivo JSON
        with open(filepath, 'w') as f:
            json.dump(existing_data, f, indent=4)

        return jsonify({'message': 'Dados salvos com sucesso!'})
    
    except Exception as e:
        logging.error(f"Erro ao salvar os dados: {e}", exc_info=True)
        return jsonify({'error': f'Ocorreu um erro ao salvar os dados: {str(e)}'}), 500

# Rota para servir o arquivo HTML
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Função para gerar o mapa de calor
def generate_heatmap():
    filepath = os.path.join(DATA_DIR, FILENAME)
    
    # Verifique se o arquivo existe
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")

    # Carregar os dados do JSON
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Converter para DataFrame
    df = pd.DataFrame(data)

    # Verificar se as colunas GazeX e GazeY existem
    if 'GazeX' not in df.columns or 'GazeY' not in df.columns:
        raise ValueError("As colunas 'GazeX' e 'GazeY' são necessárias para gerar o mapa de calor.")

    # Criar o mapa de calor
    plt.figure(figsize=(10, 8))
    sns.kdeplot(x=df['GazeX'], y=df['GazeY'], cmap="Blues", fill=True, thresh=0.05)
    plt.title('Mapa de Calor dos Dados de Gaze')
    plt.xlabel('GazeX')
    plt.ylabel('GazeY')

    # Caminho completo para o arquivo de saída
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    # Salvar o mapa de calor
    plt.savefig(output_path)
    plt.show()

def close_web_broser(broser):
    broser.quit()
# Função para encerrar o aplicativo executado via atalho
def kill_process_by_name(process_name):
    try:
        subprocess.run(['taskkill', '/f', '/im', process_name], check=True)
        print(f"Processo {process_name} encerrado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao encerrar o processo {process_name}: {e}")

def openBrowser(broser):
    broser.get('http://127.0.0.1:5000/')

acabar = Event().clear()

def handle_sigterm(signal_number, stack_frame):
    print("Recebido Ctrl+C. Encerrando o servidor...")
    acabar.set()

sinals = signal.signal(signal.SIGINT, handle_sigterm)

finish = False

def runserver(a):
    try:
        app.run(debug=False)
    except KeyboardInterrupt as e:
        print(f"Erro ao executar o servidor: {e}")

if __name__ == '__main__': 
    shortcut_path = 'C:\\Users\\Public\\Desktop\\GazePointer.lnk' 
    process_name = "GazePointer.exe"  
    broser = webdriver.Chrome()

    try:
        print(f"Executando {shortcut_path}...")
        subprocess.run(['cmd', '/c', 'start', '', shortcut_path], check=True)
        print(f"{shortcut_path} executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {shortcut_path}: {e}")
        sys.exit()
    try:
        server_thread = Thread(target=runserver, args=(sinals,))
        server_thread.start()
        time.sleep(5)
        openBrowser(broser)
        while not finish:
            if server_thread.is_alive() and acabar:
                print("Encerrando o servidor manualmente...")
                Thread(target=shutdown_server()).start()
        server_thread.join()

            
    except:
        print("Interrupção manual")
    finally: 
        close_web_broser(broser)
        kill_process_by_name(process_name)
        generate_heatmap()

