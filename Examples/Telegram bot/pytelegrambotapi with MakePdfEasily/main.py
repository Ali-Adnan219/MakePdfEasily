import MakePdfEasily
from  MakePdfEasily import *
import telebot
import os
import time
import shutil


TELEGRAM_TOKEN="5689364691:AAHILlRscQ_F2WzBZ90BnOXHcW30FryMaiU"

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None )



txtword=["Picture saved successfully...send word\n/pdf\nCreate a pdf file","He didn't find any pictures for you yet...you can send pictures now"]

#make folder img and pdf

try:
    for names in ["img","pdf"]:
        os.mkdir(names) 
except OSError as error: 
    pass

@bot.message_handler(commands=['pdf'] )
def convert_to_pdf(message):
    path_img="./img/"+str(message.from_user.id)
    path_pdf="./pdf/"+str(message.from_user.id)
    if  os.path.exists(path_img) == True:
        MakePdf(path_img,"./pdf/"+str(message.from_user.id)+".pdf")
        i = open(path_pdf, 'rb')
        bot.send_document(message.chat.id, i ,caption= "here pdf" ,reply_to_message_id=message.message_id)
        shutil.rmtree(path_img)
        shutil.rmtree(path_pdf)
    else:
        bot.send_message(message.chat.id,txtword[1] ,reply_to_message_id=message.message_id)



@bot.message_handler(  content_types=['photo','document']   )
def name(message):
    try:
        if    message.content_type =='photo'  or 'image' in str(message.document.mime_type):
            raw=''
            if message.content_type =='document':
                raw=message.document.file_id
            else:
                raw=message.photo[-1].file_id
            try: 
                os.mkdir("./img/"+str(message.from_user.id)) 
            except OSError as error: 
                bot.send_message(message.chat.id,error ,reply_to_message_id=message.message_id)
            path = "./img/"+str(message.from_user.id)+"/"+raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id,txtword[0] ,reply_to_message_id=message.message_id)
    except  OSError as error :
        print( error)
        pass



# Run bot
def ii ():
    while True:
        try:      
            bot.polling(none_stop=True, interval=0, timeout=0)
        except Exception as e:
            print(e)
            time.sleep(10)
#ii ()
bot.polling(none_stop=True)
