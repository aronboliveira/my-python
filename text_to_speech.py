import os
import re
from datetime import datetime
from gtts import gTTS
from colorama import Fore, init
init(autoreset=True)
print(Fore.GREEN + f"Hello, {os.getlogin()}. This is a text to speech script!")
available_extensions = {r".txt", r".doc", r".docx", r".py"}
available_langs = {"pt", "en"}
available_tlds = {
	"pt": ("com.br", "pt"),
	"en": ("co.uk", "com", "com.au")
}
slowdown = False
filename = ''
lang = 'en'
tld = 'com'
count = 0
def read_text(text: str = 'No text was given', lang: str = 'en', tld: str = 'com', slow=False) -> None:
  try:
    gTTS(text=text, lang=lang, slow=slow, tld=tld).save(f"{filename}_{str(datetime.now().strftime("%Y%m%d_%H%M%S"))}.mp3")
    print(Fore.GREEN + "Filed created!")
    return
  except PermissionError as e:
    print(Fore.RED + "Permission error has halted the execution. Please recheck your user permissions.")
  except TypeError as e:
    print(Fore.RED + "A failure of typing has halted the execution. Check the logic of the script or your given arguments.")
  except Exception as e:
    print(Fore.RED + "As unkown error has halted the execution.")
while (lang not in available_langs) or (not any(re.search(re.escape(ext) + r'$', filename) for ext in available_extensions)):
  count += 1
  if count > 10:
    print(Fore.YELLOW + "You reached the limit of tries. Please try later. Aborting...")
    exit(1)
  try:
    filename = input(Fore.CYAN + f"Enter a valid filename with extension {available_extensions}:\n").strip()
    file_ext = os.path.splitext(filename)[1]
    if os.path.splitext(filename)[1] not in available_extensions:
        print(Fore.YELLOW + f"Invalid extension: {file_ext}. Valid options: {available_extensions}")
        continue
    if not os.path.isfile(filename):
      print(Fore.YELLOW + f"Hmmm... this path ({filename}) is not valid. Let's try again.")
      continue
    with open(file=filename, mode='r',encoding='utf-8') as f: content = f.read()
    lang_opt = input(Fore.CYAN + f"Please enter a valid language {str(available_langs)}:\n") or 'en'
    if not (lang_opt in available_langs): 
      print(Fore.YELLOW + f"Hmmm... this language ({lang_opt}) is not valid. Let's try again.")
      continue
    tld_opt = input(Fore.CYAN + f"Please enter a valid TLD variation for the chosen language:\n").strip().lower() or 'com'
    if lang_opt not in available_tlds or tld_opt not in available_tlds.get(lang_opt, ()):
      print(Fore.YELLOW + f"Hmmm... this variation {tld_opt} is not available. Let's try again.")
      continue
    slow_opt = input(Fore.CYAN + "Do you want the text to be read slowly? (Enter Y for yes, else it won't):\n").strip().upper()
    if slow_opt == 'Y': slowdown = True
    read_text(text=content, lang=lang_opt, tld=tld_opt, slow=slowdown)
    break
  except Exception as e:
    print(Fore.RED + "As unkown error has prevented the execution.")
  
  