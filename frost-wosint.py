import os
import pyshorteners
import whois

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
  print("Domain name: ", analisys.domain_name)
  print("Creation name: ", analisys.creation_date)
  print("Registrar: ", analisys.registrar)
  print("Expiration date: ", analisys.expiration_date)
  print("Name server: ", analisys.name_servers)
  print("Email registered: ", analisys.emails)
  print("Country : ", analisys.country)
  print("Registrant: ", analisys.registrant)
  return analisys

# initialized variable for the loop
site_name = ""

# Just an ascii art :)
ascii_art = """
    █████▒██▀███   ▒█████    ██████ ▄▄▄█████▓ █     █░ ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓
  ▓██   ▒▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒▓█░ █ ░█░▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
  ▒████ ░▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░▒█░ █ ░█ ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
  ░▓█▒  ░▒██▀▀█▄  ▒██   ██░  ▒   ██▒░ ▓██▓ ░ ░█░ █ ░█ ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
  ░▒█░   ░██▓ ▒██▒░ ████▓▒░▒██████▒▒  ▒██▒ ░ ░░██▒██▓ ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
   ▒ ░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▓░▒ ▒  ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
   ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░      ▒ ░ ░    ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
   ░ ░     ░░   ░ ░ ░ ░ ▒  ░  ░  ░    ░        ░   ░  ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
            ░         ░ ░        ░               ░        ░ ░        ░   ░           ░                                                                                                      
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
          print()
        else:
          print("Could't expand!")
          exit()
      else:
        print("The URL is not compressed.")
        analisys = web_osint(site_name)
        print()
    else:
      print(f"Site {site_name} is unreachable! (maybe you misstyped the URL)")