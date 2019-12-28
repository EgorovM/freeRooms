from time import sleep

import groups_list
import api

groups = groups_list.groups

for group in groups:
    file = open(f"htmls/{group}.html", "w")

    html = api.get_page(group)

    file.write(html)

    sleep(0.5)
    
file.close()
