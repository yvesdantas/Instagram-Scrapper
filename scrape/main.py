from getpass import getpass
from connect import Scrapper
 
username = input("Enter your username: ")
password = getpass("Enter your password: ")

scrape = Scrapper(username, password)
scrape.open_account()
scrape.generating_files(scrape.following())