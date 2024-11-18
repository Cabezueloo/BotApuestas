from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler, filters)

import os
import logging
from ClassSearch import ClassSearch 
from utils import *
import escanear
from datetime import datetime





# Define la función que envía el PDF
async def sendPrediccion(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print("NTR")
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    
    pathChatID = "chats/"+user_name+"_"+str(chat_id)+".txt"
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    f = open(pathChatID,'a',encoding="UTF8")
    f.write(f'El usuario {user_name} ha solicitado la predicción a las {date_time}\n')

    logger.info(f'El usuario {user_name} ha solicitado la predicción.')
    
    #Si la prediccion no esta el en sistema la tendremos que generar
    nombreArchivoPrediccion,urlEvento = checkearPrediccionCreada()
    print("El nombre del archivo para ver si ya ha sido creado es-> ",nombreArchivoPrediccion)

    if not os.path.isfile(nombreArchivoPrediccion):

        escanear.crearPrediccion(urlEvento)
        await context.bot.send_message(chat_id=chat_id, text="Generando predicción, por favor espere")

    
    await context.bot.send_document(chat_id=chat_id, document=open(nombreArchivoPrediccion, "rb"))
    print("Archivo enviado")

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="Te genera un archivo PDF en base a el próximo evento que venga de la UFC.\n"
                                    "Genera la prediccion en base a una IA personalizado y un archivo JSON que se genera para cada pelea de la cartelera con detalles de los peleadores.\n"
                                    "La inteligencia artificial se encarga de generar la predicción.\n"
                                    "Utilza /Prediccion para generar la prediccion del proximo evento")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



async def status(update: Update, context: ContextTypes.DEFAULT_TYPE,):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text=f"Estado del servidor -> OK\n{speedServer()}")

API_KEY_BOT = os.getenv('API_KEY_BOT')

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()


if __name__ == "__main__":
    '''Run the bot'''

    # Crea la aplicación y añade el token
    application = Application.builder().token(API_KEY_BOT).build()
    
    # Comandos validos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('Prediccion', sendPrediccion))
    application.add_handler(CommandHandler('cancel', cancel))
    application.add_handler(CommandHandler('status', status))
    

    # Inicia el bot
    application.run_polling()


