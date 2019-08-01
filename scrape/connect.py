import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class Scrapper:

    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(15)

    def open_account(self):    

        #openning the instagram perfil
        self.driver.get("https://www.instagram.com/?hl=en")
        self.driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a").click()
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").click()
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(self.username)
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").click()
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(self.password)
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button").click()
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click() 

    def following(self):

        #openning the following section
        self.driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]/a").click() # open the profile page
        self.driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[3]/a").click() # open the following list
        
        #scrolling down
        target = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li[12]/div/div[2]/div[1]/div/div/a")
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        #scrolling up
        target = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li[2]/div/div[1]/div[2]/div[1]/a")
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        #generating the following list   
        aux = int(self.driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[3]/a/span").text.replace(',', ''))
        
        list_1 = list(range(1, aux, 12))
        list_2 = list(range(13, aux, 12))
        list_2.append(aux+1)
        
        following_zip = list(zip(list_1, list_2))

        following_list = []

        for a, b in following_zip:
            for x in range(a, b):
                try:
                    follower = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li[{0}]/div/div[1]/div[2]/div[1]/a".format(x)).text
                    following_list.append(follower)
                    print(follower, 'listed') 
                    target = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li[{0}]/div/div[1]/div[2]/div[1]/a".format(x))
                    self.driver.execute_script('arguments[0].scrollIntoView(true);', target)
                except:
                    pass
        
        print(len(following_list), 'accounts were added to the list.')

        return following_list

    def generating_files(self, following_list):

        #creating a folder to insert the files 
        filepath = os.getcwd() + '/json_files/'

        os.makedirs(filepath)

        #scrapping the view-source links
        for count, data in enumerate(following_list,1):

            if count%100 == 0:
                print("Waiting a couple of seconds...")
                sleep(30)

            self.driver.get("view-source:https://www.instagram.com/{0}/".format(data))
            
            try:
                json_text = self.driver.find_element_by_xpath("/html/body/pre/span[275]").text

                json_text = json_text.strip("window._sharedData = ")
                json_text = json_text.strip(";")

                json_file = json.loads(json_text)

            except:
                json_text = self.driver.find_element_by_xpath("/html/body/pre/span[279]").text

                json_text = json_text.strip("window._sharedData = ")
                json_text = json_text.strip(";")

                json_file = json.loads(json_text)

            with open(filepath + '{0}.json'.format(data), 'w', encoding='utf8') as fp:
                json.dump(json_file, fp, ensure_ascii=False)

            print("File number {0} was created".format(count))

        self.driver.close()
        print("All the files were created.")