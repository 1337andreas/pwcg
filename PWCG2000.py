#!/usr/bin/python

#Welcome to PWCG2000!
#This script can both generate a secure password and check an existing one against a list of millions of known leaked passwords.
#Furthermore, the user may upon generating a new password choose the amount of symbols needed. 
#The script will automatically throw in upper- and lowercase letters from A to Z, as well as numbers and special symbols. The generated password also gets cross-checked for leaks to verify its safety.
#Version 1.7 | Last updated 14-01-2026
#Code Reviewed by IsacL on 14-01-2026, Good job

import logging                                                                                                  #For writing to a log file.
import argparse
import platform                                                                                                 #As this script depends on having an Internet connection, a check using "platform" is performed in order to ping Google's DNS. The commands on Windows and Linux are different for this.
import os
import subprocess                                                                                               #Subprocess is used to check your Internet connection, which is of course necessary to reach the API.
import time
import json                                                                                                     #Json is a required module for the localisation feature. More languages could easily be added.
import getpass
import secrets
import string                                                                                                   #Secrets is used for random and string for all necessary characters.
import urllib.request                                                                                           #This library is used for requesting data from HaveIBeenPwnd (HIBP). 
import hashlib                                                                                                  #Importing this is necessary for checking passwords online, as the database API only takes hashes rather than cleartext. From a security standpoint, this is a good thing.

os.chdir(os.path.dirname(os.path.abspath(__file__)))                                                            #Ensures the json files can be read in the same folder as the script, regardless of OS.

#--- LOGGING ---
log = "PWCG2000_output.txt"

file_handler = logging.FileHandler(log, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))                         #Separates writing to the log file from writing to the terminal.

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
logging.info("Initialised PWCG2000.")

#--- FLAGS ---                                                                                                #Allows you to choose a language from the terminal when running PWCG2000. This can later be changed in the program's menu. Also shows the current version of PWCG2000.

parser = argparse.ArgumentParser()

parser.add_argument("--lang", choices=["en", "sv", "fi", "de", "fr"], default="en", help="Choose a language. If none is chosen, PWCG2000 defaults to English.")
parser.add_argument("--version", action="version", version="PWCG2000 v1.5", help="Shows PWCG2000 version.")
args = parser.parse_args()

#--- LOCALISATION ---

class Localisation:
    def __init__(self, language="en"):
        with open(f"{language}.json", "r", encoding="utf-8") as f:
            self.texts = json.load(f)

    def t(self, key, **kwargs):
        text = self.texts.get(key, f"[{key}]")
        return text.format(**kwargs)

translator = Localisation(args.lang)                                                                                 #Chooses English automatically. Note that this script has dependencies, namely "lang_en.json", "lang_sv.json" and so on.
t = translator.t

    #--- OS CHECK AND INTERNET CONNECTIVITY TEST ---

def connectiontest(ip_address):
    logging.info(t("system_detect"))
    system = platform.system()
    try:
        if system == "Linux":
            logging.info(t("system_linux"))
            output = subprocess.check_output(["ping", "-c", "1", ip_address])                                    #An OS check is performed here, because the ping commands for Windows and Linux are different.
        elif system == "Windows":
            logging.info(t("system_windows"))
            output = subprocess.check_output(["ping", "-n", "1", ip_address])
        else:
            logging.error(t("system_unknown"))
            exit()
        logging.info(output.decode())
        input(t("icmp_success"))
    except subprocess.CalledProcessError:
        logging.warning(t("icmp_fail"))
        exit()

connectiontest("8.8.8.8")                                                                                         #Pinging Google DNS to ensure the user has an Internet connection.


#--- MENU ---

while True:
    print(t("menu_title"))                                                                                        #Instead of having the user instructions directly in the script, it reads from the chosen language JSON file.
    print(f"""
       ____ _       _________________   ____  ____  ____ 
      / __ \ |     / / ____/ ____/__ \ / __ \/ __ \/ __ \ 
     / /_/ / | /| / / /   / / __ __/ // / / / / / / / / /
    / ____/| |/ |/ / /___/ /_/ // __// /_/ / /_/ / /_/ / 
   /_/     |__/|__/\____/\____//____/\____/\____/\____/ !
        
            {t("menu_choice")}
            {t("menu_checker")}
            {t("menu_generator")}
            {t("menu_language")}
            {t("menu_exit")}""")


    #--- PASSWORD CHECKER ---
    def check_password(password: str) -> int:                                                                                                  
            sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()                                           #This hashes the password in SHA-1 in order to make the API accept it. The HIBP API does not accept passwords in plaintext, only hashes.
            prefix = sha1[:5]                                                                                           #Splits the hash value into two variables: Prefix (for the HIPB API) and suffix (for cross-reference). Only the first 5 characters in the hash key are sent to the API. The exact password in itself does therefore not get checked, but rather each password with the same prefix. 
            suffix = sha1[5:]
            url = f"https://api.pwnedpasswords.com/range/{prefix}"                                                      #URL to the API. The "prefix" variable in brackets will be different each time the code is run and is defined by the generated hash.
                                                                                                                
            req = urllib.request.Request(                                                                               #This makes a HTTP request with User-Agent, which is not necessary but recommended by the API to avoid error 400/403.
                url,
                headers={"User-Agent": "PWCG2000"}
            )

            with urllib.request.urlopen(req, timeout=10) as response:                                                   #Then this reads the data returned by the API, using the "urllib.request" library imported by the script.
                data = response.read().decode("utf-8")                                                                  #API responds with a line of text that gets converted back.
                
            for line in data.splitlines():                                                                      
                hash_suffix, count = line.split(":")                                                                    #This splits the text into different suffixes which are checked.
                if hash_suffix == suffix:                                                                               #If there is a suffix match, it means the password is in a leak known by HIBP.
                    return int(count)                                                                                   #No suffix match means the password is not in any known leaks. "return 0" is in case no match is found during the loop.

            return 0
            logging.info("Made API request to HIBP")

    userchoice=input()
    if userchoice.lower() in ("c", "k", "t"):                                                                           #A simpler alternative to having loads of or conditions. Uppercase input gets converted to lowercase.
        logging.info(t("enter_password_check"))
        time.sleep(0.2)
        existing_password = getpass.getpass()                                                                           #Using "getpass" instead of "input" hides the password from shoulder-peeking. The password should only be in the RAM whilst the code runs. However, some terminals might save your input so putting sensitive information in here happens at your own risk.
                                                                                                                        #This function checks your existing password against the HIBP database.

        count = check_password(existing_password)                                                                       #This calls the function and prints the check result.

        if count > 0:
            logging.warning(t("password_found", count=count))
        else:
            logging.info(t("password_safe"))

        input(t("press_return"))                                                                                        #Takes the user back to the menu.

#--- PASSWORD GENERATOR ---
                                                                                                                        #The "or" statements prevent returning "Invalid choice!" should the user write in lowercase.
    elif userchoice=="G" or userchoice=="g":
        try:                                                                                                            #Try/Except ensure this whole section gets skipped should newpassword_length not be an integer.         
            logging.info (t("enter_password_length")) 

            newpassword_length=int(input(t("password_length_prompt")))
            if newpassword_length < 8:
                input(t("password_too_short"))
            elif newpassword_length > 16:
                input(t("password_too_long")) 
            elif (newpassword_length > 7) and (newpassword_length < 17):                                               #The password generation logic. Program continues here if a valid length (8-16 characters) was chosen.
                logging.info (t("generating_password"))
                newpassword_characters =""
                newpassword_characters += string.punctuation                                                           #Punctuation such as commas and exclamation marks.
                newpassword_characters += string.ascii_letters                                                         #Letters A-Z and a-z
                newpassword_characters += string.digits                                                                #Numbers 0-9
                newpassword = []
                def passwordgen():                                                                                     #The new password generated by the program gets checked against HIBP automatically before being given to the user.
                    newpassword = "".join(secrets.choice(newpassword_characters) for i in range(newpassword_length))   #If a match is found, a different random password gets generated and checked until no match is found.
                    return newpassword                                                                                 #It is highly unlikely an 8-16 letter password generated by this script will be in a leak; for demonstrative purposes, the minimum number could be set to 2 or 3 above or certain character sets disabled.
                newpassword = passwordgen()

                while int((check_password(newpassword))) > 0:
                    logging.warning(t("password_found_db"))
                    newpassword = passwordgen()
                logging.info(t("password_suggestion"))                                                                        #A check of the new password will be performed here once that feature is implemented.
                logging.info("".join(newpassword)) 
                input(t("press_return_menu"))
        except:
            input(t("invalid_input"))

            #--- LANGUAGE MENU ---
            
    elif userchoice.lower() in ("l", "s"):
        logging.info("Showed language menu")
        print(t("language_menu"))
        lang_choice = input()
        if lang_choice == "en":
            translator = Localisation("en")
            t = translator.t
        elif lang_choice == "sv":
            translator = Localisation("sv")
            t = translator.t
        elif lang_choice == "fi":
            translator = Localisation("fi")
            t = translator.t
        elif lang_choice == "de":
            translator = Localisation("de")
            t = translator.t
        elif lang_choice == "fr":
            translator = Localisation("fr")
            t = translator.t
        else:
            input(t("invalid_input"))

    elif userchoice=="X" or userchoice=="x":
        logging.info("Terminated PWCG2000.")
        exit()                                                                                                         #This stops the program. User might have to close the console themselves.
            
    else: logging.error(t("invalid_choice"))                                                                                  #Prevents the program from crashing due to invalid input.

            
