# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:06:11 2022

@author: int.omer.adiguzel
"""

from selenium.webdriver.common.by import By

import time

class MainWpPage:
    def __init__(self,driver):
        self.driver = driver


    def load(self,url=None):
        """
        

        Parameters
        ----------
        url : str, optional
            Url to load. The default is None.

        Returns
        -------
        None.

        """
        if not url:
            self.driver.get("https://web.whatsapp.com/")
        else:
            self.driver.get(url)
        time.sleep(3)
        
    def openedChats(self):
        """
        Gets chat objects from left panel.

        Returns
        -------
        elements : Selenium Object
            Selenium objects representing chats.

        """



        #elements = driver.find_elements(By.CSS_SELECTOR, "#pane-side ._10e6M")
        elements = []
        driver = self.driver
        try:
            for i in range(0,20):
                elements.append(driver.find_element(By.XPATH, '//*[@data-testid ="list-item-{}"]'.format(i)))
        except:
            pass
        return elements
        

    def name(self,element):
        """
        Gets name of contact.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        str
            Contacts name.

        """
        return element.find_element(By.CSS_SELECTOR, ".ggj6brxn").text

   
    def last_message_time(self,element):
        """
        Gets time of last recieved message of contact.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        str
            Contacts last message time.

        """
        return element.find_element(By.CSS_SELECTOR, ".Dvjym").text

    
    def last_message(self,element):
        """
        Gets last recieved message of contact.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        str
            Contacts last recieved message.

        """
        return element.find_element(By.CSS_SELECTOR, "._11JPr").text
   
    
    def notifications(self,element):
        """
        Gets number of notifications(message) of contact.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        int
            Contacts notifications.

        """
        
        try:
            return int(element.find_element(By.CSS_SELECTOR, "._1pJ9J").text)
        except:
            return 0
    
    def has_notifications(self,element):
        """
        Checks if contact has notification.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        bool
            Is there a notification ? .

        """
        try:
            notifications = int(element.find_element(By.CSS_SELECTOR, "._1pJ9J").text)
            if notifications > 0:
                return True
        except:
            return False
    
    def click(self,element):
        """
        Clicks on element.

        Parameters
        ----------
        element : Selenium Object
            Selenium element of selected item.

        Returns
        -------
        None.

        """
        element.click()
        time.sleep(3)
    
        