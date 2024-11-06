DB_USERNAME = "****"
DB_PASSWORD = "*****"
DB_HOST = "****"
DB_PORT = "***"
DB_NAME = "***"

from selenium import webdriver
from message import Messenger
from login import MainWpPage
import time
import warnings
warnings.filterwarnings("ignore")
import replyTree
import pandas as pd
from dbConn import DbConnection


nameList=[]  
stateKeeper = {}
df = pd.DataFrame(columns = ['ID',  'IN_MESSAGE' , 'IN_MESSAGE_TIME' ,'OUT_MESSAGE' , 'OUT_MESSAGE_TIME'])

def openWpWeb():
    """
    Opens 'chromedriver.exe' with options file.

    Returns
    -------
    driver : TYPE
        DESCRIPTION.

    """
    chrom_options = webdriver.ChromeOptions()
    # chrom_options.add_argument(
    # "user-data-dir=C:\\Users\\INTOME~1.ADI\AppData\\Local\\Temp\\scoped_dir16956_1688294984\\Default\\Default\\Default\\Default")

    driver = webdriver.Chrome(executable_path=r"C:\\Users\\omer.adiguzel\\Desktop\\Projects\\Whatsapp Chatbot\\wpBot\\chromedriver.exe")
    driver.maximize_window()
    
    return driver

        

def mainWpPage(driver):
    """
    Loads main page of WhatsappWeb.

    Parameters
    ----------
    driver : Selenium Object
        Selenium webdriver to open 'web.whatsapp.com' .

    Returns
    -------
    mainPage : Selenium Object
        Main page of WhatsappWeb.

    """
    
    mainPage = MainWpPage(driver)
    mainPage.load()
    return mainPage


def removizer(raw_opened_chats , raw_contact_list):
    """
    Removes chats that should not be answered. 

    Parameters
    ----------
    raw_opened_chats : List
        List contains all chats selenium objects.
    raw_contact_list : TYPE
        List contains all contacts informations.

    Returns
    -------
    opened_chats : List
        List contains chats that should be answered.
    contact_list : List
        List contains contact informations that should be answered.

    """
    opened_chats = []
    contact_list = []

    for index,data in enumerate(raw_contact_list):
        if data[2] or data[0] in nameList:
            opened_chats.append(raw_opened_chats[index])
            contact_list.append(raw_contact_list[index])
            
    return opened_chats , contact_list


def getChats(mainPage):
    """
    
    Gets chat section of WhatsappWeb page.

    Parameters
    ----------
    mainPage : Selenium Object
        Main Whatsapp Web page object.

    Returns
    -------
    opened_chats : List
        List that contains selenium objects of Whatsapp Web chats.
    contact_list : List
        List that contains Whatsapp Web chats information(Eg, name,last massage time, notificiations ...).

    """
    raw_contact_list = []
    raw_opened_chats = []
   
    while len(raw_opened_chats)<1:
        time.sleep(5)
        raw_opened_chats = mainPage.openedChats()
        for oc in raw_opened_chats:
        
            name = mainPage.name(oc)  
            last_msg_time = mainPage.last_message_time(oc)
            has_notif = mainPage.has_notifications(oc)  
            count_notif = mainPage.notifications(oc) 
            
            raw_contact_list.append([name,last_msg_time,has_notif,count_notif])
        
        
        opened_chats , contact_list = removizer(raw_opened_chats , raw_contact_list)
        return opened_chats , contact_list  

def setStates(contact_list):
    """
    Sets inital state for first contact.

    Parameters
    ----------
    contact_list : List
        List that contains Whatsapp Web chats information(Eg, name,last massage time, notificiations ...).

    Returns
    -------
    None.

    """
    for index,data in enumerate(contact_list):
        if data[0] not in nameList:
            nameList.append(data[0])
            state = replyTree.createMenus()
            stateKeeper[data[0]] = state
  


def switchStates(data,selector):
    """
    Switches contact status.

    Parameters
    ----------
    data : List
        Contact informations .
    selector : int
        Pointer for state to switch.

    Returns
    -------
    None.

    """
    if data[0] in nameList:
        state = stateKeeper[data[0]]
        if selector in [1,2,3,4,5,6,7,8,9]:
            state = state.selectChildren(selector)
            stateKeeper[data[0]] = state
        elif selector == 0:
            state = replyTree.createMenus()
            stateKeeper[data[0]] = state
        elif selector == -1:       
            nameList.remove(data[0])
            del stateKeeper[data[0]]
            

def writeToDatabase(conn):
    """
    Function to writes recieved and sent messages to database. 

    Parameters
    ----------
    conn : sqlalchemy.engine.base.Engine
        SqlAlchemy engine to connect database.

    Returns
    -------
    None.

    """
    global df
    try:
        conn.connect()
        print("connection successfull")
    except Exception as err:
        print("error- ", err)  
        conn = DbConnection(username= DB_USERNAME, password= DB_PASSWORD, host = DB_HOST, port= DB_PORT, name = DB_NAME)
    finally:
        conn.dataToDB(df,'wpbotdeneme', if_there='append' , index = False)
        df = df.truncate(before=-1, after=-1)


def chatter(opened_chats,contact_list,mainPage,msg):
    """
    Function that magic happens, checks if there's an unreplied message exist and replies based on contacts state.

    Parameters
    ----------
    opened_chats : List
        List that contains selenium objects of Whatsapp Web chats.
    contact_list : List
        List that contains Whatsapp Web chats information(Eg, name,last massage time, notificiations ...).
    mainPage : Selenium Object
        Main Whatsapp Web page object.
    msg : Str
        Message to send.

    Returns
    -------
    None.

    """
    
    global df
    for index,data in enumerate(contact_list):
        if data[2]:    
            mainPage.click(opened_chats[index])
            recievedMsg = msg.read_last_message(who = 'in')
            if recievedMsg == "-1":
                msg.send_message("Tüm taleplerinize çözüm bulmak için İnsan Kaynakları olarak tüm enerjimizle yanınızdayız. Yardımcı olabileceğim başka bir konu olursa beni yine burada bulabilirsiniz. İlginiz için teşekkür eder,  iyi çalışmalar dileriz.")
                switchStates(data, -1)
            elif recievedMsg.isdigit() and int(recievedMsg) in  [0,1,2,3,4,5,6,7,8,9]:
                if stateKeeper[data[0]].order != 0 and int(recievedMsg) != 0 :
                    msg.send_message("Üzgünüm ne dediğinizi anlayamadım. Size yardımcı olabilmemiz için listeden seçim yapmanız gereklidir.Listeyi yeninden görmek için 0 yazabilirsiniz.")
                else:
                    switchStates(data, int(recievedMsg))
                    try:
                        msgToSend = stateKeeper[data[0]].getInfo()
                        msg.send_message(msgToSend)
                        outTime = time.strftime("%H:%M" , time.localtime())
                        df = df.append({'ID':data[0] ,
                                    'IN_MESSAGE': recievedMsg , 
                                    'IN_MESSAGE_TIME': data[1] , 
                                    'OUT_MESSAGE': msgToSend ,
                                    'OUT_MESSAGE_TIME' : outTime
                                    } ,ignore_index = True)
                        writeToDatabase(conn)
                    except Exception as err :
                        print("error - " ,err)
            else:
                try:
                    if stateKeeper[data[0]].order != 0:
                        msg.send_message("Üzgünüm ne dediğinizi anlayamadım. Size yardımcı olabilmemiz için listeden seçim yapmanız gereklidir.Listeyi yeninden görmek için 0 yazabilirsiniz.")
                    msgToSend = stateKeeper[data[0]].getInfo()
                    msg.send_message(msgToSend)
                    outTime = time.strftime("%H:%M" , time.localtime())
                    df = df.append({'ID':data[0] ,
                                'IN_MESSAGE': recievedMsg , 
                                'IN_MESSAGE_TIME': data[1] , 
                                'OUT_MESSAGE': msgToSend ,
                                'OUT_MESSAGE_TIME' : outTime
                                } ,ignore_index = True)
                    writeToDatabase(conn)
                except Exception as err:
                  print("error - " , err)




driver = openWpWeb()
mainPage = mainWpPage(driver)
msg = Messenger(driver)    
conn = DbConnection(username= DB_USERNAME, password= DB_PASSWORD, host = DB_HOST, port= DB_PORT, name = DB_NAME)

while True:
    
    opened_chats , contact_list = getChats(mainPage)
    setStates(contact_list)   
    chatter(opened_chats, contact_list, mainPage, msg)
    time.sleep(1)
    driver.refresh()
    time.sleep(5)

