import time
import json
import threading
import getpass
import os
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium import  webdriver
import requests
import bs4
import datetime 
from configparser import ConfigParser



class BirthdayBash:

    options = webdriver.ChromeOptions()
    friend_about_pages = [] 
    id_to_details = {} 


    def __init__(self):
        self.options.add_argument("log-level=1") ; 
        self.options.add_argument("--disable-notifications") ; 
        self.options.add_argument("--headless") ; 
        self.common_cookies = None ; 


        self.config = ConfigParser() ; 
        self.config.read('config.ini') ; 


    def store_details_to_json(self):
        with open('id_to_details.json' , 'w' , encoding='utf-8') as  fp:
            json.dump(self.id_to_details, fp , indent=2 , ensure_ascii=False ) ;
    

    def login(self):
        driver = webdriver.Chrome("chromedriver.exe"  , options=self.options ) ; 
        driver.get("http://facebook.com/events/birthdays")  ; 
        userbox = driver.find_element_by_id("email") ; 
        passbox = driver.find_element_by_id('pass') ; 
        userbox.send_keys(self.config.get('facebook' , 'email')) ; 

        passbox.send_keys(self.config.get('facebook' , 'pass')) ; 
        passbox.submit() ; 
        self.common_cookies = driver.get_cookies() ; 
        self.driver = driver ; 



    def get_about_pages(self):
        try:
            driver = webdriver.Chrome("chromedriver.exe"  , options=self.options ) ; 
            driver.get("http://facebook.com/events/birthdays")  ; 
            userbox = driver.find_element_by_id("email") ; 
            passbox = driver.find_element_by_id('pass') ; 
            userbox.send_keys(self.config.get('facebook' , 'email') ); 

            passbox.send_keys(self.config.get('facebook' , 'pass')) ; 
            passbox.submit() ; 

            self.common_cookies = driver.get_cookies() ; 
            print(self.common_cookies) ; 


        finally:
            scrollendCounter= 0 ; 
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

                time.sleep(1) ; 

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scrollendCounter+=1 ;
                    if(scrollendCounter>2):
                        break ;
                last_height = new_height
            
            users = driver.find_elements_by_css_selector("li._43q7 a") ; 

            for user in users:
                url = user.get_attribute("href") ; 
                print(url) ; 

                if(url.find("profile.php?id=")>0):
                    url = url+"&sk=about" ; 
                else:
                    url = url+"/about" ; 
                self.friend_about_pages.append(url) ; 

            self.driver = driver ; 

            for url in self.friend_about_pages:
                self.handleabout(url) ; 
    

    def parse_dates_into_iso(self):
        for key in self.id_to_details.keys():
            temp = key.split(',') ;
            date = temp[0].split(' ') ; 

        pass ; 




    def handleabout(self , url  ):
        try:
            print(url) ; 
            if(not self.common_cookies):
                self.login() ; 

            self.driver.get(url) ; 
            driver = self.driver ;        

            
            try:
                possibles = driver.find_elements_by_css_selector("span._c24._2ieq") ; 

            except NoSuchElementException:
                ele = driver.find_element_by_css_selector("a[data-tab-key=about]") ;
                driver.get(ele.get_attribute('href')) ; 
                possibles = driver.find_elements_by_css_selector("span._c24._2ieq") ; 


            birthday = str ; 
            for ele in possibles:
                if(ele.get_attribute("innerHTML").find('Birthday')>0):
                    birthday = ele.find_element_by_css_selector("span div:last-of-type").text ; 
            
            try:
                userid = driver.find_element_by_css_selector("div#fbTimelineHeadline a[data-profileid]").get_attribute('data-profileid') ; 

            except NoSuchElementException:
                userid = driver.find_element_by_css_selector("a[data-profileid]").get_attribute('data-profileid') ; 
            
            fullname = driver.find_element_by_css_selector("div.cover a._2nlw._2nlv").text ; 

            self.id_to_details[userid] = {'name' : fullname , 'bday' : birthday }  ;
            # print(self.id_to_details) ; 
        
        finally:
            obj.store_details_to_json() ; 


    

if(__name__=="__main__"):
    obj = BirthdayBash()
    obj.get_about_pages() ; 
    obj.store_details_to_json() ; 
    # obj.handleabout("https://www.facebook.com/profile.php?id=100004456147835&sk=about") ; 
    obj.driver.close() ; 
