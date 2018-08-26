from pyquery import PyQuery as pq
import re
import os.path
import urllib.request
from time import sleep
from json import load

numberreg = re.compile(r".+ \((\d)\)")

with open("locals.json") as f:
    id_to_name = load(f)


# I just want to add that this won't function perfectly, I manually checked every ID after the download and adjusted them
# I additionally also have more item sprites, but I don't know how to extract the id information from the sprite atlas
# so if someone knows how to, he can feel free to add more items

def extract_icons_from_wiki():
    d = pq(url="https://graveyardkeeper.gamepedia.com/Items")
    items = d("img[width='34']")
    # print(items)
    for item in items:
        n = str(pq(item).attr("alt")).split(" item.png")[0]
        url = str(pq(item).attr("src"))
        special = False
        num = 0
        if numberreg.match(n):
            special = True
            num = int(n.split(" (")[-1].split(")")[0])
            n = n.split(" (")[:-1]
            if(type(n) == list):
                n = "".join(n)

        for key in id_to_name:
            if n == id_to_name[key]:
                if special:
                    n = "_".join(key.split("_")[:-1] + [str(num)])
                else:
                    n =key
        try:
            n = n.replace(":", "__")
        except:
            print(n)
        filename = os.path.join('./html/rsc/', n + ".png")
        sleep(0.05)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')]
        urllib.request.install_opener(opener)
        if not os.path.isfile(filename):
            print('Downloading: ' + filename)
            try:
                urllib.request.urlretrieve(url, filename)
            except Exception as inst:
                print(inst)
                print('  Encountered unknown error. Continuing.')



extract_icons_from_wiki()