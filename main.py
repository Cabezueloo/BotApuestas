import telegram
from telegram.ext import Application, CommandHandler
import os
import logging
from ClassSearch import ClassSearch 
from utils import *
import escanear
from datetime import datetime

def checkearPrediccionCreada():
    url = 'https://www.tapology.com/fightcenter?group=ufc'

    paginaEventos = ClassSearch(url)
    
    result = selectFirstEventUFC(paginaEventos)

    if result:

        # Construir URL del evento específico
        event_url = "https://www.tapology.com/"+result.get("href")

        eventoEspecifico = ClassSearch(event_url)

        soupUFC = eventoEspecifico.soup
    
        nombreEvento = getNameEvent(soupUFC)
        

        return (parsearNombreParaElPDF("Prediccion_"+nombreEvento))
    

API_KEY_BOT = os.getenv('API_KEY_BOT')

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

# Define la función que envía el PDF
async def sendPrediccion(update, context):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    
    pathChatID = "chats/"+user_name+"_"+str(chat_id)+".txt"
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    f = open(pathChatID,'a',encoding="UTF8")
    f.write(f'El usuario {user_name} ha solicitado la predicción a las {date_time}\n')

    logger.info(f'El usuario {user_name} ha solicitado la predicción.')
    
    #Si la prediccion no esta el en sistema la tendremos que generar
    nombreArchivoPrediccion = checkearPrediccionCreada()
    print("El nombre del archivo para ver si ya ha sido creado es-> ",nombreArchivoPrediccion)

    if not os.path.isfile(nombreArchivoPrediccion):

        escanear.crearPrediccion()
        await context.bot.send_message(chat_id=chat_id, text="Generando predicción, por favor espere")

    
    await context.bot.send_document(chat_id=chat_id, document=open(nombreArchivoPrediccion, "rb"))
    print("Archivo enviado")
    

if __name__ == "__main__":
    '''Run the bot'''

    # Crea la aplicación y añade el token
    application = Application.builder().token(API_KEY_BOT).build()
    
    # Añade el comando para enviar la predicción
    application.add_handler(CommandHandler("Prediccion", sendPrediccion))

    # Inicia el bot
    application.run_polling()


