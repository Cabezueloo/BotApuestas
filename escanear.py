from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from google import genai
import io
import datetime
import os
from dotenv import load_dotenv
import time
from ufc import get_fighter,get_fighter_by_url_sherdor
import json

from ClassSearch import ClassSearch

from utils import *


load_dotenv()

API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE')

def crearPrediccion(event_url:str):
  
    eventoEspecifico = ClassSearch(event_url)

       
    # Encontrar los contenedores de luchadores
    peleas_json = []  # Lista para almacenar cada JSON de pelea
    inicio = time.time()

    nombres = eventoEspecifico.driver.find_elements(By.XPATH, "//a[@itemprop='url']")
    urls_fights = []
    
    for i in range(1, len(nombres), 2):
        # Get the URL from the anchor element
        url1 = nombres[i].get_attribute("href")
        url2 = nombres[i+1].get_attribute("href")
        
        fight = {
            "fighter1": url1,
            "fighter2": url2,
            
        }        
        
        urls_fights.append(fight)


    for fight in urls_fights:
        
        # Llamadas a la API para obtener los JSON de cada peleador
        p1 = get_fighter_by_url_sherdor(fight.get("fighter1"))
        p2 = get_fighter_by_url_sherdor(fight.get("fighter2"))

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
    with open("prompEnglish.txt", "r", encoding="utf-8") as f:
        PROMPT = f.read().format(fecha=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

  
    # Combinar PROMPT con el contenido del archivo JSON en texto
    PROMPT += peleas_json_text


    client = genai.Client(api_key=API_KEY_GOOGLE)

  
    # Configuración del modelo de IA
    inicio = time.time()
    response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05",
        contents=[PROMPT],
)

    # Generación del contenido

   
    with io.open("Prediccion_Garry-Prates.md", mode="w", encoding="utf-8") as f:
        f.write(response.text)

    print(f'Tiempo en dar respusta es: {time.time()-inicio} segundos')
    

    # convert_markdown_to_pdf("info.md", "Prediccion_"+"test")

if __name__ == "__main__":
    crearPrediccion("https://www.sherdog.com/events/UFC-on-ESPN-66-Garry-vs-Prates-106862")