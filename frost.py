import os
import pyshorteners
import whois
import tkinter
from tkinter import ttk
import mysql.connector
import configparser

#library to import configurations from  the file db.conf
config = configparser.ConfigParser()
config.read('config.ini')
HOST = config.get('default', 'HOST')
USER = config.get('default', 'USER')
PASSWORD = config.get('default', 'PASSWORD')

# I use curl to test if the site is up and i direct the output to null just for more cleansiness
def site_ping_test(URL):
  response = os.system("curl --head --silent --fail " + site_name + " > /dev/null")
  if response == 0:
    return True
  else:
    return False

# I determine if the URL is compressed or not
def compressed_dilemma(URL):
  default_lenght = 20
  if len(URL) < default_lenght:
    return False
  else:
    return True
  
# I need this to expanded a shortened URL using pyshortener
def expand_URL(URL):
  expanded = pyshorteners.expand_URL(URL)
  return expanded 

# The real analisys of the web page
def web_osint(URL):
  analisys = whois.whois(URL)
  print("Domain name: ", analisys.domain_name[0])
  print("Creation date: ", analisys.creation_date[0])
  print("Registrar: ", analisys.registrar)
  print("Expiration date: ", analisys.expiration_date[0])
  print("Name server: ", analisys.name_servers[0])
  print("Email registered: ", analisys.emails[0])
  print("Country : ", analisys.country)
  print("Registrant: ", analisys.registrant) #!!!!gives a nontype maybe it could be the problem
  return analisys

# initialized variable for the loop
site_name = ""

# Database
db_name = "frost-db"
db = mysql.connector.connect(host = HOST, user = USER, password = PASSWORD)
cursor = db.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
cursor.execute("USE `frost-db`")
cursor.execute(f"CREATE TABLE IF NOT EXISTS frost (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Domain VARCHAR(255), Creation_date VARCHAR(255), Registrar VARCHAR(255), Expiration_date VARCHAR(255), Name_server VARCHAR(255), Mail_registered VARCHAR(255), Country VARCHAR(255))") #removed registrant from query due to nontype object
insert_statement = "INSERT INTO TABLE frost (Domain, Creation_date, Registrar, Expiration_date, Name_server, Mail_registered, Country, Registrant) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# Just an ascii art :)
ascii_art = """
  █████▒██▀███   ▒█████    ██████ ▄▄▄█████▓
▓██   ▒▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
▒████ ░▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
░▓█▒  ░▒██▀▀█▄  ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
░▒█░   ░██▓ ▒██▒░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
 ▒ ░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
 ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
 ░ ░     ░░   ░ ░ ░ ░ ▒  ░  ░  ░    ░      
          ░         ░ ░        ░           
                                           
  """
print(ascii_art)
# loop to reiterate the menu
while site_name != "exit":
  # Asking for the URL
  site_name = input("Inesert the URL/IP to analize or type exit to quit (URL/exit): ")
  # Using site_ping_test to verify if the site is still up
  response = site_ping_test(site_name)
  if site_name == "exit":
    print("Bye! :)")
    cursor.close()
    db.close()
    exit()
  else:
    if response:
      print(f"Site {site_name} is reachable!")
      if compressed_dilemma(site_name):
        print("The URL is compressed.")
        print("Expanding...")
        expanded_site = expand_URL(site_name)
        if site_ping_test(expanded_site):
          print("Expanded correctly!")
          analisys = web_osint(expanded_site)
          values = (analisys.domain_name[0], analisys.creation_date[0], analisys.registrar, analisys.expiration_date[0], analisys.name_servers[0], analisys.emails[0], analisys.country, analisys.registrant)
          db.cursor.executemany(insert_statement, values) 
          db.commit()
          print()
        else:
          print("Could't expand!")
          exit()
      else:
        print("The URL is not compressed.")
        analisys = web_osint(site_name) 
        values = (analisys.domain_name[0], analisys.creation_date[0], analisys.registrar, analisys.expiration_date[0], analisys.name_servers[0], analisys.emails[0], analisys.country, analisys.registrant)
        db.cursor.executemany(insert_statement, values) 
        db.commit()
        print()
    else:
      print(f"Site {site_name} is unreachable! (maybe you misstyped the URL)")