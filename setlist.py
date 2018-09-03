from lxml import html
from bs4 import BeautifulSoup
from collections import Counter
import requests

# number of concerts that the data will be gathered
number_of_concerts = 20

f = open('song_count.txt', 'w')
set_list = []
concert_count = 0


for i in range(1,2):
    page = requests.get('https://www.setlist.fm/setlists/radiohead-bd6bd12.html?page=' + str(i))

    tree = html.fromstring(page.content)

    concerts = tree.xpath('/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[@*]/div[2]/h2/a/@href')

    for i in concerts:
        url = 'https://www.setlist.fm/' + str(i)[2:]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        concert_count += 1
        for elem in soup.findAll("a", {"class": "songLabel"}):
            song_name = str(elem["href"]).split('=')[1].replace('+', ' ').encode("utf-8")
            set_list.append(song_name)
        if concert_count == number_of_concerts:
            break

song_count = Counter(set_list)

f.write("Number of concerts: " + str(concert_count) + '\n')

for song in song_count.most_common(len(song_count)):
    line = "   %32.32s - %s\n" % (song[0], song[1])
    f.write(line)

f.close()

