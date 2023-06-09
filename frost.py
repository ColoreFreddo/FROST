# used libraries  
import os # used for the ping section
import requests # used for expanding links
import whois # main library used for web-osint
import tkinter as tk # library used for the database interface
import mysql.connector # library used for connecting the database
import configparser # library used to import settings from a file

# library to import configurations from the file conf.ini
config = configparser.ConfigParser()
config.read('config.ini')
# allocating variables to use later in the database
HOST = config.get('default', 'HOST')
USER = config.get('default', 'USER')
PASSWORD = config.get('default', 'PASSWORD')

# Main menu function
def Main_menu():
  print("(1) Domain analisys")
  print("(2) Open the database")
  print("(3) Exit")
  select = input("Select (1/2/3): ")
  print()
  return select

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
  
# I need this to expanded a shortened URL using requests
def expand_URL(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        expanded_url = response.url
        return expanded_url
    except requests.exceptions.RequestException:
        print("Error: Unable to expand the URL.")
    print("The URL is compressed.")
    print("Expanding...")
    print()
    return None
    
# Check if is a list or a string
def get_value(analisys):
    if isinstance(analisys, list):
      if analisys:
        return analisys[0]
      else:
        return "None"
    elif isinstance(analisys, str):
      if analisys:
        return analisys
      else:
        return "None"
    else:
      return "None"

# The real analisys of the web page
def web_osint(URL):
  analisys = whois.whois(URL)
  print("Domain name: ", get_value(analisys.domain_name))
  print("Registrar: ", get_value(analisys.registrar))
  print("Name server: ", get_value(analisys.name_servers))
  print("Email registered: ", get_value(analisys.emails))
  print("Country : ", get_value(analisys.country))
  print("Registrant: ", get_value(analisys.registrant))
  return [get_value(analisys.domain_name), get_value(analisys.registrar), get_value(analisys.name_servers), get_value(analisys.emails), get_value(analisys.country), get_value(analisys.registrant)]

# This create the database window
def db_interface(window):
  window.title("MySQL Database Viewer")
  window.geometry("1000x500")
  search_frame = tk.Frame(window)
  search_frame.pack(pady=10)
  entry = tk.Entry(search_frame, font=("Helvetica", 14))
  entry.pack(side=tk.LEFT, padx=10)
  search_button = tk.Button(search_frame, text="Search", command=lambda: search(entry.get(),window,listbox))
  search_button.pack(side=tk.LEFT)
  listbox = tk.Listbox(window)
  listbox.pack(fill=tk.BOTH, expand=True)
  window.mainloop()

# Create Listbox to display data and request data from database
def search(search_term, window,listbox):
  cursor = db.cursor()
  query = f'''SELECT * FROM frost WHERE  
  Domain LIKE '%{search_term}%' 
  OR Registrar LIKE '%{search_term}%' 
  OR Name_server LIKE '%{search_term}%' 
  OR Mail_registered LIKE '%{search_term}%' 
  OR Country LIKE '%{search_term}%' 
  OR Registrant LIKE '%{search_term}%'
  '''
  cursor.execute(query)
  listbox.delete(0, tk.END)
  data = cursor.fetchall()
  for row in data:
      listbox.insert(tk.END, row) 
  listbox.pack(fill=tk.BOTH, expand=True)
# Close database connection
  cursor.close()
# Start Tkinter event loop
  window.mainloop()

# initialized variable for the loop
select = "0"

# Database creation
db_name = "frostdb"
db = mysql.connector.connect(host = HOST, user = USER, password = PASSWORD)
cursor = db.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
cursor.execute("USE `frostdb`")
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS frost 
  (
  Domain VARCHAR(255),
  Registrar VARCHAR(255),
  Name_server VARCHAR(255),
  Mail_registered VARCHAR(255),
  Country VARCHAR(255),
  registrant VARCHAR(255)
  )
  ''')
insert_statement = '''
  INSERT INTO frost 
  (
  Domain, 
  Registrar, 
  Name_server,
  Mail_registered,
  Country,
  Registrant
  )
  VALUES (%s, %s, %s, %s, %s, %s)
'''

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
while select != "3":
  select = Main_menu()
  if select == "3":
    print("Bye! :)")
    cursor.close()
    db.close()
    exit()
  if select == "2":
    window = tk.Tk()
    db_interface(window)
    cursor.close()
    db.close()
    exit("Bye! :)")
  if select == "1":
    print()
    site_name = input("Enter the URL or IP for the domain: ")
    response = site_ping_test(site_name)
    if response:
      print()
      print(f"Site {site_name} is reachable!")
      if compressed_dilemma(site_name):
        expanded_site = expand_URL(site_name)
        if site_ping_test(expanded_site):
          print("Expanded correctly!")
          print()
          analisys = web_osint(expanded_site)
          cursor.execute(insert_statement, analisys) 
          db.commit()
          print()
        else:
          print()
          print("Could't expand!")
          exit()
      else:
        print()
        print("The URL is not compressed.")
        analisys = web_osint(site_name) 
        cursor.execute(insert_statement, analisys)
        db.commit()
        print()
    else:
      print()
      print(f"Site {site_name} is unreachable! (maybe you misstyped the URL)")
  else:
    print()
    print("Error! (Invalid input)")