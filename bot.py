import config
import telebot
import os
import shutil
import pymysql.cursors

#Constants
SUPER = 'super user'
SIMPLE = 'simple user'

#Connection to MySQL database
#Server have db "active_users" with 2 tables
#Now uses for initialize users
connect = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = config.passwordSQL,
                             db = 'active_users',
                             charset = 'utf8',
                          cursorclass = pymysql.cursors.DictCursor)

#Find user in db
#If user not found add in table with simple users
def find_user(chat_id, username):
    with connect.cursor() as cursor:
        cursor.execute("select chat_id from super_users")
        for row in cursor:
            if chat_id == row['chat_id']:
                return SUPER
        cursor.execute("select chat_id from simple_users")
        for row in cursor:
            if chat_id == row['chat_id']:
                return SIMPLE
        cursor.execute("insert simple_users(chat_id, name) values ("+str(chat_id)+", '"+str(username)+"');")
        return SIMPLE

#Connecting to bot
bot = telebot.TeleBot(config.TOKEN)
path = "photos"

#Download all files from path to user
def WalkOnFiles(path, user):
    directory = os.listdir(path)
    for file in directory:
        if ('.png' in file) or ('.jpg' in file) or ('.jpeg' in file):
            bot.send_photo(user, open(path+'\\'+file, 'rb'))
        #if '.mp4' in file:
        #    bot.send_video(user, open(path+'\\'+file, 'rb'))
        if not ('.' in file):
            WalkOnFiles(path+'\\'+file, user)

#commands for bot
#@bot.message_handler(commands = ["pullout"])
#def pull_out_All_Files(message):
#    user_type = find_user(message.chat.id, message.chat.username)
#    #file = open('photos\\1.jpg', 'rb')
#    #bot.send_photo(message.chat.id, file)
#    WalkOnFiles(path, message.chat.id)
#    os.mkdir(path)
#    bot.send_message(message.chat.id, "Pulled out successfully")

@bot.message_handler(commands = ["show_id"])
def show_ID(message):
    user_type = find_user(message.chat.id, message.chat.username)
    bot.send_message(message.chat.id, message.chat)

#echo
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    user_type = find_user(message.chat.id, message.chat.username)
    bot.send_message(message.chat.id, message.text)

#Bot don't stop
if __name__ == '__main__':
     bot.polling(none_stop=True)
