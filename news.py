#! /usr/bin/python3
# encoding=utf8

from time import sleep
import telebot
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests


bot = telebot.TeleBot("TOKEN")


@bot.message_handler(func=lambda message:True)

def mensaje(message):

    variable = message.text

    if " " in variable:
            variable = variable.replace(" ","")

    if "ñ" in variable:
            variable = variable.replace("ñ","n")

    if "ç" in variable:
            variable = variable.replace("ç","c")
    

    try:    
            link = "https://www.google.com/search?q="+variable+"&client=firefox-b-d&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiZpbWpsZH2AhVlxYUKHRoYCpYQ_AUoAXoECAIQAw&biw=1157&bih=681&dpr=2"
            req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

            webpage = urlopen(req).read()

            links_list = list()

            with requests.Session() as c:
                    soup = BeautifulSoup(webpage,'html5lib')

                    for item in soup.find_all('div', attrs={'class':'egMi0'}):
                            link = (item.find('a', href=True)['href'])
                            link = link.split("/url?q=")[1].split('&sa=U&')[0]
                            links_list.append(link)
                            
        
            cont = 0

            for i in links_list:
                sleep(1.5)
                bot.reply_to(message, i)
                cont += 1
                if cont >= 5:
                 break



            if cont == 0:
                bot.reply_to(message, "No se ha encontrado ninguna noticia con el texto, prueba a no poner carácteres especiales:"+message.text)
            
            

    except UnicodeEncodeError:
         bot.reply_to(message, "No se ha encontrado ninguna noticia con el texto, prueba a no poner carácteres especiales:"+message.text)


bot.polling(none_stop=True)