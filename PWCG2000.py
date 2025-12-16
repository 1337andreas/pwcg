#Welcome to PWCG2000!
#This script can both generate a secure password and check an existing one against a list of millions of known leaked passwords.
#Furthermore, the user may upon generating a new password choose the amount of symbols needed. 
#The script will automatically throw in upper- and lowercase letters from A to Z, as well as numbers and special symbols. The generated password also gets cross-checked for leaks to verify its safety.

print("""WELCOME TO
    ____ _       _________________   ____  ____  ____ 
   / __ \ |     / / ____/ ____/__ \ / __ \/ __ \/ __ \ 
  / /_/ / | /| / / /   / / __ __/ // / / / / / / / / /
 / ____/| |/ |/ / /___/ /_/ // __// /_/ / /_/ / /_/ / 
/_/     |__/|__/\____/\____//____/\____/\____/\____/ !
      
      MAKE A CHOICE:
      -(C)heck existing password
      -(G)enerate a new password
      -
      -E(x)it""")
        
        #User's choice in the menu. Variable gets defined by their input.
        #The "or" statements prevent returning "Invalid choice!" should the user write in lowercase.

userchoice=input()

if userchoice=="C" or userchoice=="c":
    print ("Please enter the password you would like to check.")
elif userchoice=="G" or userchoice=="g":
    print ("Please enter the amount of symbols (8-16) you want for the new password.")
elif userchoice=="X" or userchoice=="x":
    print("Exiting...")
else: print ("Invalid choice! Please press one of the keys asked.") #Prevents the program from crashing.

        #Add the different features here