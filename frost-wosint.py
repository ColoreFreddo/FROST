import os
import pyshorteners

def site_ping_test(URL):
  response = os.system("curl --head --silent --fail " + site_name + " > /dev/null")
  if response == 0:
    return True
  else:
    return False

def compressed_dilemma(URL):
  default_lenght = 20
  if len(URL) < default_lenght:
    return False
  else:
    return True

def expand_URL(URL):
  expanded = expand_URL(URL)
  return expanded 

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

site_name = input("Inesert the URL/IP to analize: ")
response = site_ping_test(site_name)
if response:
  print(f"Site {site_name} is reachable!")
  if compressed_dilemma(site_name):
    print("The URL is compressed.")
    print("Expanding...")
    expanded_site = expand_URL(site_name)
    if site_ping_test(expanded_site):
      print("Expanded correctly!")
    else:
      print("Could't expand! (Or maybe is not compressed...)")
  else:
    print("The URL is not compressed.")
else:
  print(f"Site {site_name} is unreachable! (maybe you misstyped the URL)")
