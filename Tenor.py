import requests
import json
import urllib
from os import chdir, getcwd, mkdir

API_KEY = "M9YAESOTVOLX"

r = requests.get(f"https://api.tenor.com/v1/anonid?&key={API_KEY}")

if r.status_code == 200:
    with open("anon_id.txt", "a+") as f:
        if f.read() == "":
            r = requests.get(f"https://api.tenor.com/v1/anonid?&key={API_KEY}")
            anon_id = json.loads(r.content)["anon_id"]
            f.write(anon_id)
        else:
            anon_id = f.read()
            mkdir("media")
else:
    print("Failed Connection, Please try again")
    exit()

chdir(getcwd() + "\\media")
while True:
    limit = int(input("Limit: "))
    search_term = input("Search Term: ")
    filetype = input("Filetype [h for options]: ")

    if filetype ==  "h":
        print("Currently supported filetypes:")
        print("-gif")
        print("-mp4")
        print("-webm")
        
        filetype = input("Filetype: ")

    r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={API_KEY}&limit={limit}&anon_id={anon_id}")

    if r.status_code == 200:
        tenorjson = json.loads(r.content)
        
        for i in range(len(tenorjson["results"])):
            filename = search_term + str(i + 1) + "." + filetype
            print(f"Downloading {filename} ... ")
            url = tenorjson["results"][i]["media"][0][filetype]["url"]
            urllib.request.urlretrieve(url=url, filename=filename)
    else:
        tenorjson = None
        print("Failed connection Please Try Again")
        continue
    
    if input("Would you like to download any more files[Y or N]: ").upper() == "Y":
        continue
    else:
         print("Thank you for using TenorDownloader.py")
         break
        
