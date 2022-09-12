import sqlite3
import telebot
from telebot import types
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

bot = telebot.TeleBot("2133177983:AAF0URvPZCm0A-lwTtoBXpk5PZ-IZ8qNWsg")


options = Options()
options.headless = True

@bot.message_handler(commands=['start'])

def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Поиск по названию')
    itembtn2 = types.KeyboardButton('Поиск по описанию')
    itembtn3 = types.KeyboardButton('Случайный')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(chat_id, "Что найти?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Поиск по названию':
        f = open("text.txt", "w")
        f.write("название")
        f.close()
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите название:")


    elif message.text == 'Поиск по описанию':
        f = open("text.txt", "w")
        f.write("описание")
        f.close()
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите описание:")        

    elif message.text == 'Случайный':
        f = open("text.txt", "w")
        f.write("cлучайный")
        f.close()
        
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")

        db = sqlite3.connect('KINO3.db')
        cur = db.cursor()

        for rand in cur.execute('SELECT * FROM KINO3 WHERE ID IN (SELECT ID FROM KINO3 ORDER BY RANDOM() LIMIT 1)'):

            print(rand)       
            name = rand[2]
            god = rand[3]
            opisanie = rand[4]
            link1 = rand[5]

            driver = webdriver.Firefox(options=options)

            try:
                driver.get(link1)
                time.sleep(2)
            
                driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")
            
                            
                print(element2.get_attribute('src'))
            
                itog = str(element2.get_attribute('src'))
            
                a1 = itog.split('/240.mp4') 
                a2 = str(a1[0]) + "/720.mp4"
                print(a2)
            
                link2 = a2
            
            except:
                print("Ошибка")
            
                link2 = "Ошибка"

            driver.quit()

            q = open("text.txt", "w")
            q.write(str(name))
            q.write('\n')
            q.write(str(god))
            q.write('\n')
            q.write('\n')
            q.write(str(opisanie))
            q.write('\n')
            q.write('\n')
            q.write(str(link1))
            q.write('\n')
            q.write('\n')
            q.write(str(link2))
            q.close()
            
            msg = open("text.txt", "r")
            msgR = msg.read()
            chat_id = message.chat.id
            bot.send_message(chat_id, msgR)                            




    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")

        db = sqlite3.connect('KINO3.db')
        cur = db.cursor()

        word = message.text
        r = open("text.txt", "r")
        readR = r.read()

        if readR == "название":
            driver = webdriver.Firefox(options=options)
            
            name_list = []
            opisanie_list = []
            god_list = []
            Link1_list = []
            Link2_list = []

            
            for name in cur.execute('SELECT NAME FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                name_list.append(name[0])

            for opisanie in cur.execute('SELECT OPISANIE FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                opisanie_list.append(opisanie[0]) 

            for god in cur.execute('SELECT GOD FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                god_list.append(god[0])     

            for Link1 in cur.execute('SELECT LINK_STR FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                Link1_list.append(Link1[0])  

            for film in Link1_list:
                try:
                    driver.get(film)
                    time.sleep(2)
                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                    itog = str(element2.get_attribute('src'))
                    a1 = itog.split('/240.mp4')
                    a2 = str(a1[0]) + "/720.mp4"
                    print(a2)                

                    Link2_list.append(a2)

                except:
                    print("Ошибка")

                    Link2_list.append("Ошибка") 


            driver.quit()

            i = 0
            while i < len(name_list):

                q = open("text.txt", "w")
                q.write(str(name_list[i]))
                q.write('\n')
                q.write(str(god_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(opisanie_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link1_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link2_list[i]))
                q.close()

                msg = open("text.txt", "r")
                msgR = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msgR)
                time.sleep(1)
                i = i + 1

        elif readR == "описание":

            driver = webdriver.Firefox(options=options)
            z = open('text.txt', 'w')
            z.seek(0)
            z.close()
            name_list = []
            opisanie_list = []
            god_list = []
            Link1_list = []
            Link2_list = []
            for name in cur.execute('SELECT NAME FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                print(name)
                name_list.append(name[0])

            for opisanie in cur.execute('SELECT OPISANIE FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                print(opisanie)
                opisanie_list.append(opisanie[0])

            for god in cur.execute('SELECT GOD FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                print(god)
                god_list.append(god[0])                        

            for Link1 in cur.execute('SELECT LINK_STR FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                print(Link1)
                Link1_list.append(Link1[0])

            for film in Link1_list:
            
                try:
                    driver.get(film)
                    time.sleep(2)

                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                
                    print(element2.get_attribute('src'))

                    itog = str(element2.get_attribute('src'))

                    a1 = itog.split('/240.mp4') 
                    a2 = str(a1[0]) + "/720.mp4"
                    print(a2)

                    Link2_list.append(a2)

                except:

                    print("Ошибка")

                    Link2_list.append("Ошибка")
                 
            

            
            i = 0
            driver.quit()             
            while i < len(name_list):
                

                q = open("text.txt", "w")
                q.write(str(name_list[i]))
                q.write('\n')
                q.write(str(god_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(opisanie_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link1_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(Link2_list[i]))
                q.close()

                msg = open("text.txt", "r")
                msgR = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msgR)
                time.sleep(1)
                i = i + 1 
                

bot.polling()
