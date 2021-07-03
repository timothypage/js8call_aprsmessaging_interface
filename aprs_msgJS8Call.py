#! /usr/bin/python3
'''
Created on 23 September 2019
APRS Messageing Using JS8Call Copyright 2019 M0IAX

With thanks to Jordan, KN4CRD for JS8Call - http://js8call.com

@author: Mark Bumstead M0IAX
http://m0iax.com

this is the lite version and uses a unix command to send the message to JS8Call,
this was adapted from a script by Jason, KM4ACK.

I may consider writing a more complicated version to use more of the JS8Call API
'''

from tkinter import * 
from tkinter import messagebox

from tkinter.ttk import *

from tkinter.scrolledtext import ScrolledText
from subprocess import call
import os
import psutil

TYPE_TX_SEND='TX.SEND_MESSAGE'
TYPE_TX_SETMESSAGE='TX.SET_TEXT'
MSG_ERROR='ERROR'
MSG_INFO='INFO'
MSG_WARN='WARN'

     
class UserInterface:
    mycall="N0TZW"
    first=True
    addr = ('127.0.0.1',65500)
    getResponse=False
    laststatusString=""
    seq=1
    def showMessage(self, messagetype, messageString):
        if messagetype==MSG_ERROR:
            messagebox.showerror("Error", messageString)
        elif messagetype==MSG_WARN:
            messagebox.showwarning("Warning",messageString)
        elif messagetype==MSG_INFO:
            messagebox.showinfo("Information",messageString)
            
    def sendMessageToJS8Call(self, messageType, messageString):
        print(messageString)
        return True

        if self.checkJS8CallRunning()==False:
            self.showMessage(MSG_ERROR, "JS8Call is not runnung. Please run it before clicking the button,")
            return False
        
        if messageString==None:
            return False
        
       # print(messageType+" "+messageString)
        
        cmdstring = "echo '{\"params\": {}, \"type\": \""+messageType+"\", \"value\":\""+messageString+"\"'} | nc -l -u -w 10 2237"
        #print(cmdstring)
        os.system(cmdstring)
        
        return True
        
    def createMessageString(self):
        messageString=""
        mode=""
        if self.combo.get()=="Email":
            mode="EMAIL-2"
        elif self.combo.get()=="SMS":
            mode = "SMSGTE"
        elif self.combo.get()=="APRS":
            mode=self.combo.get()
        elif self.combo.get()=="APRS2SOTA":
            mode=self.combo.get()
           
        mode = mode.ljust(9)
       # print(mode)
        # if self.tocall.get()=="":
        #     return "Error, no email address is set"
        
        text=self.st.get('1.0', 'end-1c')  # Get all text in widget.
    
        if text=="":
            return "Error, message is empty, please enter a message to send"
        
        number = self.seq
        number = format(number, '02d')
#        t.rjust(10, '0')
        if self.combo.get()=="Email":
            message = "@APRSIS CMD :"+mode+":"+self.tocall.get()+" "+text+"{"+number+"}"
        elif self.combo.get()=="APRS":
            tocallsign=self.tocall.get()
            tocallsign=tocallsign.ljust(9)
            message = "@APRSIS CMD :"+tocallsign+":"+text+"{"+number+"}"
        elif self.combo.get()=="APRS2SOTA":
            #  G0LGS-2>APRS,WIDE2-1*::SOTA     :ON/ON-010 144.320 SSB ON/G0LGS/P Calling now{003
            message = "@APRSIS CMD :"+mode+":"+self.summit.get()+" "+self.freq.get()+" "+self.radio_mode.get()+" "+self.mycall+" "+text+"{"+number+"}"

        else: 
            message = "@APRSIS CMD :"+mode+":@"+self.tocall.get()+" "+text+"{"+number+"}"
        
        self.seq=self.seq+1
        #APRS sequence number is 2 char, so reset if >99
        if self.seq>99:
            self.seq=1
        
        
        messageString = message #mode+" "+self.tocall.get()+" "+text
        return messageString

    def checkJS8CallRunning(self):
        
        retval = False
        #js8callText = "JS8Call Is not running."
        if "js8call" in (p.name() for p in psutil.process_iter()):
            retval = True
            #print("JS8Call is RUNNING")
        
        #print ("retval is "+str(retval))
        return retval
    
    def setMessage(self):
        messageType=TYPE_TX_SETMESSAGE
        
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
            self.showMessage(MSG_ERROR, messageString)
            return
    
        success = self.sendMessageToJS8Call(messageType, messageString)
        
        if success==True:
            self.showMessage(MSG_INFO, "Message text set in JS8Call, please use JS8Call to send the message.")
            
    def txMessage(self):
        
        messageType=TYPE_TX_SEND
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
          #  print(messageString)
            return

        success = self.sendMessageToJS8Call(messageType, messageString)
        if success==True:
            self.showMessage(MSG_INFO,"JS8Call will now transmit the message,")
    def comboChange(self, event):
      #  print(self.combo.get())
        mode = self.combo.get()
        if mode=="APRS":
            self.callLbl.config(text='Enter Callsign (including SSID)')
        elif mode=="Email":
            self.callLbl.config(text='Enter Email Address to send to')
        elif mode=="SMS":
            self.callLbl.config(text='Enter cell phone number')
        elif mode=="APRS2SOTA":
            self.callLbl.config(text='Enter summit')
            
    def __init__(self):
        
        self.window = Tk()
 
        self.window.title("APRS Messaging for JS8Call")
 
        # self.window.geometry('550x500')
 
        self.combo = Combobox(self.window, state='readonly')
        
        self.combo.bind('<<ComboboxSelected>>', self.comboChange)    
    
        self.combo['values']= ("Email", "SMS", "APRS", "APRS2SOTA")
 
        self.combo.current(3) #set the selected item
 
        self.combo.grid(column=0, row=0,columnspan=2)
 
        self.lbl1 = Label(self.window, text="JS8Call Mode", justify="left")
 
        self.lbl1.grid(column=0, row=1,columnspan=2)
 
        self.combo2 = Combobox(self.window, state='readonly')
 
        self.combo2['values']= ("Normal")
 
        self.combo2.current(0) #set the selected item
 
        self.combo2.grid(column=0, row=2,columnspan=2)
 
 
        self.callLbl = Label(self.window, text="Enter Email Address", justify="left")
 
        self.callLbl.grid(column=0, row=3,columnspan=2)
 
        self.tocall = Entry(self.window,width=30)
 
        self.tocall.grid(column=0, row=4, columnspan=2)

        self.summitLabel = Label(self.window, text="Enter Summit", justify="left")
        self.summitLabel.grid(column=0, row=5, columnspan=2);

        self.summit = Entry(self.window, width=30)
        self.summit.grid(column=0, row=6, columnspan=2)

        self.freqLabel = Label(self.window, text="Frequency (MHz)", justify="left")
        self.freqLabel.grid(column=0, row=7, columnspan=2)

        self.freq = Entry(self.window, width=30)
        self.freq.grid(column=0, row=8, columnspan=2)

        self.radio_modeLabel = Label(self.window, text="Mode", justify="left")
        self.radio_modeLabel.grid(column=0, row=9, columnspan=2)

        self.radio_mode = Combobox(self.window)
        self.radio_mode['values'] = ("FM", "SSB", "CW", "DATA")
        self.radio_mode.current(1)
        self.radio_mode.grid(column=0, row=10, columnspan=2)

        self.msgLabel = Label(self.window, text="Message Text", justify="left")
 
        self.msgLabel.grid(column=0, row=11,columnspan=2)
 
        self.st = ScrolledText(self.window, height=5, width=40)
        self.st.grid(row=12, column=0,columnspan=2)

        self.btn = Button(self.window, text="Set JS8Call Text", command=self.setMessage)
 
        self.btn.grid(column=0, row=13)

        self.btn2 = Button(self.window, text="TX With JS8Call", command=self.txMessage)

        self.btn2.grid(column=1, row=13)

        self.note1label = Label(self.window, text="Click Set JS8Call text to set the message text in JS8Call", justify="center", wraplength=300)
 
        self.note1label.grid(column=0, row=15,columnspan=2)
 
        self.note1label = Label(self.window, text="Click TX with JS8Call to set the message text in JS8Call and start transmitting", justify="center", wraplength=300)
 
        self.note1label.grid(column=0, row=16,columnspan=2)
 
        self.window.geometry("400x500")
        self.window.mainloop()
    
ui = UserInterface()

