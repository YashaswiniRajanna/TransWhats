import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from whatsapplocator import *
from datetime import datetime
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
from selenium.webdriver.common.keys import Keys
from queue import Queue
from tkinter import *
from tkinter import ttk
from googletrans import Translator
from threading import Thread
from PIL import ImageTk,Image
from gtts import gTTS
import os
from playsound import playsound
import speech_recognition as sr
r=sr.Recognizer()
import httpx
xtimeout=httpx.Timeout(4)

msg_queue=Queue()
time_queue=Queue()
translatedmsg_queue=Queue()
translatedtime_queue=Queue()
def openWhatsapp(contact_name,source,destination):
    
    #Chromedriver path
    driver = webdriver.Chrome(executable_path='C:/Dell/143GSOP/chromedriver.exe')
    
    #url to be opened in chrome:
    url="https://web.whatsapp.com/"
    driver.get(url)
    driver.add_experimental_option('useAutomationExtension', False)
    driver.maximize_window()
    time.sleep(50)
    #max wait time given  for each operation 
    wait = WebDriverWait(driver, 300)

    target='"+contact_name+"'
   
    searchBarElement = wait.until(EC.presence_of_element_located((By.XPATH,searchbar_locator)))

    searchBarElement.send_keys(contact_name)
    
    searchBarElement.send_keys(Keys.ENTER)
    time.sleep(50)
    count=5
    scount=0
    rcount=0
    while count>0:
       input_box=driver.find_elements(By.XPATH,"//div[contains(@data-pre-plain-text,'Yashaswini Raj')]/div/span[1]/span")
       timestamp1=driver.find_elements(By.XPATH,"//div[contains(@data-pre-plain-text,'Yashaswini Raj')]")
       for i in range(0,len(input_box)-scount):
           msg=input_box[i].text
           mtime=timestamp1[i].get_attribute("data-pre-plain-text")
           msg_queue.put(msg)
           time_queue.put(mtime)
           translatedmsg_queue.put(Translator(timeout=xtimeout).translate(msg,src=source,dest=destination))
           translatedtime_queue.put(Translator(timeout=xtimeout).translate(mtime,src=source,dest=destination))
           scount+=1
       rinput_box=driver.find_elements(By.XPATH,"//div[contains(@data-pre-plain-text,'"+contact_name+"')]/div/span[1]/span")
       timestamp2=driver.find_elements(By.XPATH,"//div[contains(@data-pre-plain-text,'"+contact_name+"')]")
       for i in range(0,len(rinput_box)-rcount):
           msg=rinput_box[i].text
           mtime=timestamp2[i].get_attribute("data-pre-plain-text")
           msg_queue.put(msg)
           time_queue.put(mtime)
           translatedmsg_queue.put(Translator(timeout=xtimeout).translate(msg,src=source,dest=destination))
           translatedtime_queue.put(Translator(timeout=xtimeout).translate(mtime,src=source,dest=destination))
           rcount+=1
       ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
       
       count-=2
       
    print("DONE!!")
    print(time_queue.qsize())
    print(msg_queue.qsize())
    print(translatedmsg_queue.qsize())
    print(translatedtime_queue.qsize())
    
        

def gui():
         
        root = Tk()
        root.geometry('600x600')

        frame1=Frame(root,width=300,height=400)
        frame2=Frame(root,width=300,height=400)
        frame3=Frame(root,width=600,height=200)
        frame4=Frame(frame3,width=500,height=150)
        frame5=Frame(frame3,width=100,height=150,highlightbackground="black",highlightthickness=1)
        frame6=Frame(frame3,width=600,height=50,highlightbackground="black",highlightthickness=1)

#--------frames---------

        frame1.grid(row=0,column=0,sticky="nsew")
        frame2.grid(row=0,column=1,sticky="nsew")

#--------------frame3--------------
        frame3.grid(row=1,column=0,rowspan=2,columnspan=2,sticky="new")
        frame4.grid(row=0,column=0,sticky="nsew")
        frame5.grid(row=0,column=1,sticky="nsew")
        frame6.grid(row=2,column=0,rowspan=2,columnspan=2,sticky="nsew")

#-----------frame configuration-------------
        root.columnconfigure(0,weight=1)
        root.columnconfigure(1,weight=1)
        root.rowconfigure(0,weight=1)
        root.rowconfigure(1,weight=8)
        frame3.rowconfigure(0,weight=1)
        frame3.rowconfigure(1,weight=1)
        frame3.columnconfigure(0,weight=2)
        frame3.columnconfigure(1,weight=1)
        frame4.columnconfigure(0,weight=1)
#frame4.rowconfigure(0,weight=1)
#frame6.rowconfigure(0,weight=1)
        text_box1=Text(frame1,bg="white",fg="black",relief="solid",font=('Sans Serif',10))
        text_box2=Text(frame2,bg="white",fg="black",relief="solid",font=('Sans Serif',10))
        text_box3=Text(frame4,bg="white",fg="black",relief="solid",font=('Sans Serif',10))
#text_box1.grid(row=0,column=0,sticky="nsew")
#text_box2.grid(row=0,column=1,sticky="nsew")
#text_box1.rowconfigure(0,weight=1)
#text_box1.columnconfigure(0,weight=1)
#text_box2.columnconfigure(1,weight=1)
        text_box1.pack(expand=True,fill=BOTH)
        text_box2.pack(expand=True,fill=BOTH)
        text_box3.pack(expand=True,fill=BOTH)
#text_box3.grid(row=0,column=0,sticky="nsew")
#text_box3.rowconfigure(0,weight=1)
#text_box3.columnconfigure(0,weight=1)
        def display_translated_messages():
                while translatedtime_queue.qsize()>0:
                  text_box2.insert(INSERT,translatedtime_queue.get().text+"\t")
                  text_box2.insert(INSERT,translatedmsg_queue.get().text+"\n\n")   
       
        btnimage=PhotoImage(file="translate.png")
        btn=Button(frame5,image=btnimage,command=display_translated_messages)
        btn.grid(row=1,column=0,pady=20,padx=30)

        photo=PhotoImage(file="speaker.png")
        speakerbtn=Button(frame5,image=photo)
        speakerbtn.grid(row=0,column=0,pady=10,padx=5)

        def mic_input():
            with sr.Microphone() as source:
                 print("Speak:")
                 audio=r.listen(source)
            try:
                 text_box3.insert(INSERT,"You said:"+r.recognize_google(audio,language="en")) 
            except sr.UnknownValueError:
                text_box3.insert(INSERT,"Could not understand audio") 
  
        micbtnimage=ImageTk.PhotoImage(Image.open("miclogo.jpg"))
        micbtn=Button(frame5,image=micbtnimage,command=mic_input)
        micbtn.grid(row=0,column=1,pady=10,padx=5)
        frame5.rowconfigure(0,weight=2)
        frame5.rowconfigure(1,weight=3)
        frame5.columnconfigure(0,weight=2)
        frame5.columnconfigure(1,weight=2)
        contact_combotext=StringVar()
        contact_combotext.set('Type or enter Contact')

        box=ttk.Combobox(frame6,textvariable=contact_combotext)
        box['values']=("Shruthi SIT",
                       "Suha SIT",
                       "Clg")
        box.grid(row=0,column=0,sticky="nsew")    

        source_language=StringVar()
        source_language.set('Source Language')

        sbox=ttk.Combobox(frame6,textvariable=source_language,state="read-only")
        sbox['values']=("English",
                "Kannada",
                "Hindi")
        sbox.grid(row=0,column=1,sticky="nsew")  
        destination_language=StringVar()
        destination_language.set('Destination Language')

        dbox=ttk.Combobox(frame6,textvariable=destination_language,state="read-only")
        dbox['values']=("English",
                "Kannada",
                "Hindi",
                "French",
                "German",)
        dbox.grid(row=0,column=2,sticky="nsew")  
        frame6.columnconfigure(0,weight=1)
        frame6.columnconfigure(1,weight=1)
        frame6.columnconfigure(2,weight=1)
        text_box1.tag_config("color_change",foreground="red")
   
        language={
                "English":"en",
                "Kannada":"kn",
                "Hindi":"hi",
                "French": "fr",
                "German":"de",
        }
        #source="English"
        def source_lanaguage_code():
                global source
                source=sbox.get()
               

        #destination="Kannada"       
        def destination_language_code():
                global destination
                destination=dbox.get()
                

        def call_whatsapp():
            name=box.get()
            whatsapp_thread=threading.Thread(target=openWhatsapp,args=[name,language[source],language[destination]])
            whatsapp_thread.start()
            whatsapp_thread.join()
            while time_queue.qsize()>0:
                text_box1.insert(INSERT,time_queue.get()+"\t")
                text_box1.insert(INSERT,msg_queue.get()+"\n\n")
             
                        
            

        sbox.bind("<<ComboboxSelected>>",lambda event:source_lanaguage_code()) 
        dbox.bind("<<ComboboxSelected>>",lambda event:destination_language_code())
       
                  
              
        box.bind("<<ComboboxSelected>>",lambda event:call_whatsapp()) 
            
        root.call('encoding','system','utf-8')
        root.mainloop() 
        
 


#whatsapp_thread=box.bind("<<ComboboxSelected>>",lambda event:threading.Thread(target=openWhatsapp(box.get(),120)))

#whatsapp_thread=threading.Thread(target=openWhatsapp,args=["Suha"])
 
gui_thread=threading.Thread(target=gui,args=[])
gui_thread.start()
gui_thread.join()

print("Completed!!!")


