from bs4 import BeautifulSoup

import requests
import config
import telebot
import datetime

response = requests.get("https://www.ifmo.ru/ru/exam/raspisanie_sessii.htm", verify=False)
web_page = response.text

soup = BeautifulSoup(web_page, "html5lib")

groups_list = []

groups_block = soup.find_all("div", attrs={"class": "groups"})
for groups in groups_block:
    for group in groups.find_all("a"):
        groups_list.append(group.text)

groups_file = open("groups_list.txt", "w")
groups_file.write(str(groups_list))
groups_file.close()
