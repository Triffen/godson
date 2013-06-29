import json
import urllib.request
import time
import subprocess
import sys
import os

def shtime():
    tm = time.strftime("%c",time.localtime())
    return tm

def open_config():
    config = False
    try:
        confname = "godconfig.txt"
        confpath = sys.path[0]
        conflines = {}        
        config = open(os.path.join(confpath,confname))
        print(config)
        for line in config:
            #print(line)
            (prop,value) = line.split("=")            
            conflines[prop.strip()] = value.strip()
        print("Username is currently",conflines["username"])
        return conflines
    
    except IOError:
        conf = open(os.path.join(confpath,confname),'a')
        conftext = "username="+"input God's name in place of this text"+'\n'
        conftext += "letter="+"input first letter on trophy for craft in place of this text"+'\n'
        conftext += "trophy="+"input trophy name in place of this text"+'\n'
        conftext += "reportfolder="+os.path.join(confpath,"trophy.txt")+'\n'
        conf.write(conftext)
        conf.close()
        print("Input your username in the file",
              confpath+'/'+confname+',',
              "save and run this script again.")
        sys.exit()
    except ValueError:
        print("Invalid config file")
        sys.exit()
        
    finally:
        if config:
            config.close()
        
def pvp(data):
    try:
        if data['arena_fight'] != False:
            print("ПВП!")
            alertend = time.time() + 20
            while time.time() < alertend: 
                print(int(time.time()),"of ",int(alertend),"seconds left")
                subprocess.call(["mplayer","/home/triffen/Documents/alert.wav"])
        else:
            print("Тихо-мирно")
    except KeyError:
        print("Включите оперативные данные в API в профиле, чтобы получать уведомления о ПВП")

def gsearch(config):
    name = config["username"]
    letter = config["letter"]
    trophy = config["trophy"]
    repfolder = config["reportfolder"]
    
    while 1 == 1:
        page = ""
        while page == "":
            try:
                url = "http://godville.net/gods/api/"+urllib.parse.quote(name)+".json"
                print("Trying URL " + url)
                page = urllib.request.urlopen(url)
            except urllib.error.URLError:
                print("Упала сетка, упала...")
                time.sleep(10)
        text = page.read().decode('unicode-escape')
        data = json.loads(text,"utf-8")
        g = 0
        for trof in data['inventory'].keys():
            if trof[0] == letter:
                print(trof,shtime())
                g = g + 1
            if trof == trophy:
                print(trophy+" найден!  "+shtime())
                umbr = open(repfolder, 'a')
                umbrtxt = str(trophy+" найден!  "+shtime()+'\n')
                umbr.write(umbrtxt)
                umbr.close()
        if g == 0:
            print("Трофеев на букву "+letter+" не обнаружено",shtime())
        else:
            print("Обнаружено трофеев для крафта: ",g)
        if g >= 2:
            print("Трофеев для крафта достаточно!")
        pvp(data)
        time.sleep(65)

def main(): 
    ##subprocess.call(["mplayer", "alert.wav"])
    #print(data['arena_fight'])
    #pvp(data)
    #print(sys.path[0])
    
    config = open_config()
    gsearch(config)

    #or ask for input: username, letter, trophy
    #write input to config file
    #maybe arguments overriding config file?


try:
    main()
except SystemExit:
    print("До встречи!")
