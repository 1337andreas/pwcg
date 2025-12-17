#Welcome to PWCG2000!
#This script can both generate a secure password and check an existing one against a list of millions of known leaked passwords.
#Furthermore, the user may upon generating a new password choose the amount of symbols needed. 
#The script will automatically throw in upper- and lowercase letters from A to Z, as well as numbers and special symbols. The generated password also gets cross-checked for leaks to verify its safety.


import secrets
import string                                                                                                   #Imports the necessary modules containing random generation and all necessary characters.
                                                                                                                #User's choice in the menu. Variable gets defined by their input.

print("""WELCOME TO
    ____ _       _________________   ____  ____  ____ 
   / __ \ |     / / ____/ ____/__ \ / __ \/ __ \/ __ \ 
  / /_/ / | /| / / /   / / __ __/ // / / / / / / / / /
 / ____/| |/ |/ / /___/ /_/ // __// /_/ / /_/ / /_/ / 
/_/     |__/|__/\____/\____//____/\____/\____/\____/ !
      
      MAKE A CHOICE:
      -(C)heck existing password
      -(G)enerate a new password
      -(L)anguage selection
      -E(x)it""")                                                                                                   #Language selection will be in a later feature branch.
        
        
        

userchoice=input()

if userchoice=="C" or userchoice=="c":
    print ("Please enter the password you would like to check.")                                                    #The user input here will define the output password's length. The input gets converted to an integer.
    existing_password=input()                                                                                       #Note to self: Make the password show in asterisks?

                                                                                                                    #The "or" statements prevent returning "Invalid choice!" should the user write in lowercase.
elif userchoice=="G" or userchoice=="g":
    try:                                                                                                            #Try/Except ensure this whole section gets skipped should newpassword_length not be an integer.         
        print ("Please enter the amount of symbols (8-16) you want for the new password.") 

        newpassword_length=int(input("Password length: "))
        if newpassword_length < 8:
            print ("Password is too short! Terminating program.")
        elif newpassword_length > 16:
            print ("Password is too long! Terminating program.") 

        elif (newpassword_length > 7) and (newpassword_length < 17):                                               #The password generation logic. Program continues here if a valid length (8-16 characters) was chosen.
            print ("Generating password...")
            newpassword_characters =""
            newpassword_characters += string.punctuation                                                           #Punctuation such as commas and exclamation marks.
            newpassword_characters += string.ascii_letters                                                         #Letters A-Z and a-z
            newpassword_characters += string.digits                                                                #Numbers 0-9
            newpassword = []
            for i in range(newpassword_length):                                                                    #This checks the amount of letters chosen by the user.
                randomchar = secrets.choice(newpassword_characters)                                                #This selects a random set of characters out of the set defined above.
                newpassword.append(randomchar)
            print ("Secure password suggestion: " + "".join(newpassword))

        else: 
            print ("Input invalid! Terminating program.")                                                          #Change this to return to the menu instead, if possible. Or prompt the user to try again. Better option would be to put the menu in a loop and go back there when the user makes a mistake.
    except:
        print ("Invalid input! Terminating program.")

        
elif userchoice=="X" or userchoice=="x":
    print("Exiting...")                                                                                            #This exits the program.

        
else: print ("Invalid choice! Please press one of the keys asked.")                                                #Prevents the program from crashing.


        #Add the different features here
        #Make a log file!
        
        #Changelog 17-12-2025: 
        #Importing function "secrets" instead of "random", for a better generation algorithm based on what OS you have.
        #Try/Except added to the generation logic to prevent crashes when the password length variable isn't defined as an integer.
        #Moved the comments to improve code readability.
        #Added this very list and one explaining the variables to help developers keep track of what's what.

        #Variables:
        #userchoice - String that acts as the user's choice in the menu.
        #existing_password - String for the user's current password to get checked against known leaks.
        #newpassword - The new password that the program generates, with certain characteristics.
        #newpassword_length - Integer defining the amount of characters in the generated new password. User chooses this.
        #newpassword_characters - String containing the character set that gets used in the password. Defined by the imported ASCII character set; A-Z, a-z, 0-9, punctuation.
        