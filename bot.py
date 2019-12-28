from bs4 import BeautifulSoup
import groups_list
import rooms_list
import requests
import config
import telebot
import datetime
import api

telebot.apihelper.proxy = {'https':f'http://{config.BOT_CONFIG["proxy"]}'}
bot = telebot.TeleBot(config.BOT_CONFIG["access_token"])


@bot.message_handler(commands=['findFree',])
def get_freeRooms(message):
    filter = ""

    if len(message.text.split()) == 2:
        filter = message.text.split()[1]

    bot.send_message(message.chat.id, "Ваш запрос выполняется...")
    print(f"/findFree {filter} {message.chat.id}")

    rooms = rooms_list.rooms
    groups = groups_list.groups

    day = datetime.datetime.today().weekday()
    now_minutes = int(datetime.datetime.now().hour) * 60 + int(datetime.datetime.now().minute)

    for group in groups:
        page = open(f"{config.TEMPLATES_DIR}/{group}.html")
        web_page = page.read()

        try:
            times_lst, location_lst = api.parse_schedule_for_a_week(web_page, day)

            for ind, time in enumerate(times_lst):
                lesson_time_hour = time.split("-")
                lesson_time = list(map(int,lesson_time_hour[0].split(":") + lesson_time_hour[1].split(":")))
                lesson_start_minutes = lesson_time[0] * 60 + lesson_time[1]
                lesson_end_minutes = lesson_time[2] * 60 + lesson_time[3]

                if lesson_start_minutes < now_minutes < lesson_end_minutes:
                    building, room = location_lst[ind]
                    rooms[building].remove(room[:-4])
                    break
        except:
            pass

        page.close()

    answer = ""

    for location in rooms:
        if filter.lower() in location.lower():
            answer += f"По адресу {location} возможно свободны:\n"

            rooms_location = list(rooms[location])
            rooms_location.sort()

            for room in rooms_location:
                answer += f"{room}ауд. \n"

            answer += "\n"

    try:
        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id, "Проверьте корректность введенных данных")

@bot.message_handler(commands=['help',])
def get_freeRooms(message):
    bot.send_message(message.chat.id,
"""
/findFree вывести свободные кабинеты
/findFree {filter} фильтровать по зданию
"""
)

if __name__ == '__main__':
    bot.polling(none_stop=True)
