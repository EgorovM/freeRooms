from bs4 import BeautifulSoup

import requests
import config
import telebot
import datetime


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.BOT_CONFIG["domain"],
        week=week,
        group=group)

    print(url)
    response = requests.get(url, verify=False)
    web_page = response.text

    return web_pages


def parse_schedule_for_a_week(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": f"{day}day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [(room.span.text, room.dd.text) for room in locations_list]

    return times_list, locations_list
