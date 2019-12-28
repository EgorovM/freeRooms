from bs4 import BeautifulSoup
from time import sleep
import api

groups_file = open("groups_list.txt")
#groups = eval(groups_file.read())
groups = eval(groups_file.read())
groups_file.close()

rooms = {}

for group in groups:
    try:
        web_page = api.get_page(group)
    except:
         rooms_file = open("rooms_list.py", "w")
         rooms_file.write("rooms = " + str(rooms))
         rooms_file.close()

         exit()

    soup = BeautifulSoup(web_page, "html5lib")
    rooms_list = soup.find_all("td", attrs={"class": "room"})

    for room in rooms_list:
        try:
            location = room.find("dt").span.text

            if location in rooms:
                rooms[location].add(str(room.find("dd"))[4:-9])
            else:
                rooms[location] = set([str(room.find("dd"))[4:-9]])
        except:
            pass

    sleep(0.5)

rooms_file = open("rooms_list.py", "w")
rooms_file.write("rooms = " + str(rooms))
rooms_file.close()
