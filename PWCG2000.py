#Welcome to PWCG2000!
#This script can both generate a secure password and check an existing one against a list of millions of known leaked passwords.
#Furthermore, the user may upon generating a new password choose the amount of symbols needed. 
#The script will automatically throw in upper- and lowercase letters from A to Z, as well as numbers and special symbols. The generated password also gets cross-checked for leaks to verify its safety.
#Version 1.2 | Last updated 07-01-2026 | Changelog at the end!

import os
import time
import json                                                                                                     #Json is a required module for the localisation feature. More languages could easily be added.
import getpass
import secrets
import string                                                                                                   #Imports the necessary modules containing random generation and all necessary characters.
import urllib.request                                                                                           #This library is used for requesting data from HaveIBeenPwnd (HIBP). Importing the "requests" library would also work, but that one is external and would have to be installed then.
import hashlib                                                                                                  #Importing this is necessary for checking passwords online, as the database API only takes hashes rather than cleartext. From a security standpoint, this is a good thing.

os.chdir(os.path.dirname(os.path.abspath(__file__)))                                                            #Ensures the json files can be read in the same folder as the script, regardless of OS.
                                                                                                                #Variable "userchoice" gets defined by the user's input and makes the script do different things. The while loop ensures the menu shows again after completing a chosen task.
#---LOCALISATION---

class Localisation:
    def __init__(self, language="en"):
        with open(f"{language}.json", "r", encoding="utf-8") as f:
            self.texts = json.load(f)

    def t(self, key, **kwargs):
        text = self.texts.get(key, f"[{key}]")
        return text.format(**kwargs)

translator = Localisation("en")                                                                                 #Chooses English automatically. Note that this script has dependencies, namely "lang_en.json", "lang_sv.json" and so on.
t = translator.t

#---MENU---

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

    #---PASSWORD CHECKER---
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

    userchoice=input()
    if userchoice.lower() in ("c", "k", "t"):                                                                           #A simpler alternative to having loads of or conditions. Uppercase input gets converted to lowercase.
        print(t("enter_password_check"))
        time.sleep(0.2)
        existing_password = getpass.getpass()                                                                           #Using "getpass" instead of "input" hides the password from shoulder-peeking. The password should only be in the RAM whilst the code runs. However, some terminals might save your input so putting sensitive information in here happens at your own risk.
                                                                                                                        #This function checks your existing password against the HIBP database.

        count = check_password(existing_password)                                                                       #This calls the function and prints the check result.

        if count > 0:
            print(t("password_found", count=count))
        else:
            print(t("password_safe"))

        input(t("press_return"))                                                                                        #Takes the user back to the menu.

#---PASSWORD GENERATOR---
                                                                                                                        #The "or" statements prevent returning "Invalid choice!" should the user write in lowercase.
    elif userchoice=="G" or userchoice=="g":
        try:                                                                                                            #Try/Except ensure this whole section gets skipped should newpassword_length not be an integer.         
            print (t("enter_password_length")) 

            newpassword_length=int(input(t("password_length_prompt")))
            if newpassword_length < 8:
                input(t("password_too_short"))
            elif newpassword_length > 16:
                input(t("password_too_long")) 
            elif (newpassword_length > 7) and (newpassword_length < 17):                                               #The password generation logic. Program continues here if a valid length (8-16 characters) was chosen.
                print (t("generating_password"))
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
                    print(t("password_found_db"))
                    newpassword = passwordgen()
                print(t("password_suggestion"))                                                                        #A check of the new password will be performed here once that feature is implemented.
                print("".join(newpassword)) 
                input(t("press_return_menu"))
        except:
            input(t("invalid_input"))

            #---LANGUAGE MENU---
            
    elif userchoice.lower() in ("l", "s"):
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
        exit()                                                                                                         #This stops the program. User might have to close the console themselves.
            
    else: print (t("invalid_choice"))                                                                                  #Prevents the program from crashing due to invalid input.

            #Changelog 07-01-2026 (v1.2)
            #Improved portability with import os; correct file path for the JSON files is ensured.
            #Passwords generated by this program are now checked before being given to the user. 
            #The function is the same as when a user checks their existing password; in the code it has been moved outside the menu loop.
            #Added a small time delay to mitigate a getpass text display glitch in the password check logic. Displays correctly on all languages now.
            #Code clean-up with removing multiple or conditions in a row for different languages. (line 51)
            #Language menu now goes directly back to the main menu after making a choice, which prevents an invalid choice prompting user to press RETURN twice.

            #Changelog 03-01-2026 (v1.1)
            #Minor formatting changes for improved readability.
            #Added French localisation.

            #Changelog 02-01-2026 (v1.0)
            #Issues with password length have been resolved. Now passwords generate as they should.
            #Finnish localisation added. Thank you Vilho / saabismi for writing the translation!  
            #Welcome sign in the menu now translates correctly, it was still hard-coded before.     
    

            #Changelog 02-01-2026 (v0.9e - Localisation branch)
            #Added Localisation class.
            #Added three language JSON files that the script reads from.
            #Added a language selection which is accessed from the menu.
            #These changes have lead to issues with the password length and a few text formatting errors.

            #Changelog 02-01-2026 (v0.8b - HIPB branch)
            #Importing "getpass" to hide the existing password input.

            #Changelog 01-01-2026 (v0.7b - HIPB branch)
            #Added the "check_password" function to check an existing password against HaveIBeenPwnd's API using a SHA-1 hash.
            #Importing standard libraries which should work on different operating systems. Tested on Windows.
            #Upon checking a password, the script returns the number of known leaks the password was found in, including when there are none.
            #Password input currently shows in plaintext, potential security issue that will get fixed.

            #Changelog 01-01-2026 (v0.6)
            #Importing function "secrets" instead of "random", for a better generation algorithm based on what OS you have.
            #Try/Except added to the generation logic to prevent crashes when the password length variable isn't defined as an integer.
            #Moved the comments to improve code readability.
            #Added this very list and one explaining the variables to help developers keep track of what's what.
            #The user can now return to the menu without having to run the script again, with a while loop. Waits for user input to continue.
            #Language selection menu has been added in order to template the script's structure, but the feature itself has yet to be implemented.

            #Variables:
            #userchoice - String that acts as the user's choice in the menu.
            #existing_password - String for the user's current password to get checked against known leaks.
            #newpassword - The new password that the program generates, with certain characteristics.
            #newpassword_length - Integer defining the amount of characters in the generated new password. User chooses this.
            #newpassword_characters - String containing the character set that gets used in the password. Defined by the imported ASCII character set; A-Z, a-z, 0-9, punctuation.
            #lang_choice - Defines which JSON file to read in order to print different languages. The value is given to the Localisation class.
            
