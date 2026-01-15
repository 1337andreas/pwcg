# pwcg

**PWCG 2000 **- The Password Checker/Generator is a Python program that checks your password against a database of known leaks and generates a new safe password which isn't in any known leaks.
The user is able to determine the new password's length, 8-16 characters.

**

Features:**
-A console-based menu


-Random password generation



-Generated password gets checked against leaks on HIBP before being given to the user


-Password length choice


-Key detection to prevent crashing


-Checking your existing password for data breaches using HIBP's API


-Changing the interface language (currently supports English, Swedish, German, French and Finnish.)


**
How to use:**

-Download the repo


-Run PWCG2000.py preferably from your console


-Use --lang sv or --lang fr or any of the other supported languages if you want everything translated, otherwise you can change the language from the menu later.


-PWCG2000 will perform a quick ICMP test to verify your Internet connection as well as check what OS you are running.


-You can now access the menu and check or generate a password


-In both scenarios, PWCG2000 will automatically send your chosen password's SHA-1 prefix to HIBP and return any with a matching prefix or suffix.


-If you've generated a new password that was a match, the script automatically generates another one and sends that to HIBP; it keeps trying until it finds one that does not match.


-If you're checking your existing password, the script tells you how many times it has been leaked (or ideally, if it hasn't been leaked.)


-PWCG2000 also writes to a log file. Your existing password is never saved anywhere though. File can be found in the same folder as the script and attached JSON files.

**
System requirements:**

-Linux or Windows with a working Internet connection. If you are on a different OS or don't have Internet, the program will still close in a controlled manner.



Demonstration:

https://www.youtube.com/watch?v=VbBWjfI-NkI


