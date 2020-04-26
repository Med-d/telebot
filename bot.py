import config
import telebot
import os
import shutil

bot = telebot.TeleBot(config.TOKEN)
path = "photos"

def WalkOnFiles(path, user):
    directory = os.listdir(path)
    for file in directory:
        if ('.png' in file) or ('.jpg' in file) or ('.jpeg' in file):
            bot.send_photo(user, open(path+'\\'+file, 'rb'))
        if '.mp4' in file:
            bot.send_video(user, open(path+'\\'+file, 'rb'))
        if not ('.' in file):
            WalkOnFiles(path+'\\'+file, user)

@bot.message_handler(commands = ["pullout"])
def pull_out_All_Files(message):
    #file = open('photos\\1.jpg', 'rb')
    #bot.send_photo(message.chat.id, file)
    WalkOnFiles(path, message.chat.id)
    shutil.rmtree(path)
    os.mkdir(path)
    bot.send_message(message.chat.id, "Pulled out successfully")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.polling(none_stop=True)
