from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import google.generativeai as genai
import io
import datetime
import os
from dotenv import load_dotenv
import time
from ufc import get_fighter
import json

from ClassSearch import ClassSearch

from utils import *


load_dotenv()

API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE')

def crearPrediccion():
    # URL de la página de eventos de la UFC en Tapology
    url = 'https://www.tapology.com/fightcenter?group=ufc'

    paginaEventos = ClassSearch(url)


    # Seleccionar el primer enlace de evento que contenga "UFC"
    result = selectFirstEventUFC(paginaEventos)

    if result:

        # Construir URL del evento específico
        event_url = "https://www.tapology.com/"+result.get("href")

        eventoEspecifico = ClassSearch(event_url)

        soupUFC = eventoEspecifico.soup
    
        nombreEvento = getNameEvent(soupUFC)

        # Encontrar los contenedores de luchadores
        

        data = soupUFC.find('div', {"id": "sectionFightCard"}) 

        divs = data.find_all("li",{"class": "border-b border-dotted border-tap_6"})


        peleas : str = ""
        peleas_json = []  # Lista para almacenar cada JSON de pelea
        inicio = time.time()
        
        for item in divs:
            
            peleador = item.find_all("a",{"class": "link-primary-red"})    
            p1t = peleador[0].text.strip()
            p2t = peleador[2].text.strip()
            
            print("PELEADOR 1 -> ",p1t)
            print("PELEADOR 2 -> ",p2t)
            peleas += f'{p1t} VS {p2t}\n'
            
            # Llamadas a la API para obtener los JSON de cada peleador
            p1 = get_fighter(p1t)
            p2 = get_fighter(p2t)

            # Agregar los JSON a la lista de peleas
            peleas_json.append({"peleador1": p1, "peleador2": p2})

        

            # Guardar peleas_json en un archivo llamado "peleas.json"
            with open("peleas.json", "w") as archivo:
                json.dump(peleas_json, archivo, indent=4, ensure_ascii=False)
            
            
            

    print(f'Tiempo en generar el archivo json de las peleas: {time.time()-inicio} segundos')


        
    with open("peleas.json", 'r') as f:
        # Carga la lista de objetos JSON
        data_list = json.load(f)

    peleas_json_text = ""

    for item in data_list:
        # Convierte cada objeto JSON a una cadena de texto
        peleas_json_text += json.dumps(item) + '\n'  # Elimina el f.write()


    # Lee las instrucciones desde el archivo de texto
    inicio = time.time()
    with open("prompt.txt", "r", encoding="utf-8") as f:
        PROMPT = f.read().format(fecha=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(f'Tiempo en crear el prompt es: {time.time()-inicio} segundos')

    # Combinar PROMPT con el contenido del archivo JSON en texto
    PROMPT += peleas_json_text



    genai.configure(api_key=API_KEY_GOOGLE)

    fileJSON = genai.upload_file("peleas.json")
    # Configuración del modelo de IA
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(PROMPT))

    # Generación del contenido
    inicio = time.time()
    response = model.generate_content(peleas)
    print(f'Tiempo en dar respusta es: {time.time()-inicio} segundos')


    # Guardar la respuesta en un archivo
    inicio = time.time()
    with io.open("info.md", mode="w", encoding="utf-8") as f:
        f.write(response.text)

    print(f'Tiempo en copiar la respuesta a el archivo: {time.time()-inicio} segundos')

    convert_markdown_to_pdf("info.md", "Prediccion_"+nombreEvento)

if __name__ == "__main__":
    crearPrediccion()