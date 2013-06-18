from Tkinter import *
import tkMessageBox
import Queue

#refs:
#http://effbot.org/zone/tkinter-scrollbar-patterns.htm
#http://effbot.org/tkinterbook/text.htm
#http://effbot.org/tkinterbook/grid.htm#Tkinter.Grid.grid_remove-method


class InfoFormat:
    CONFIRMATION = "inf_conf"
    ERROR        = "inf_err"
    NONE         = "inf_n"

class CMD:
    RESUME= "R"
    STOP= "S"

class GUITerminating(Exception):
    pass

class GUI():
    def __init__(self, periodic_callback, notifications_callback):
        self.__myParent = Tk()
        self.__monitor_period = 10
        self.__periodic_cb = periodic_callback
        self.__gui_not_cb = notifications_callback
       
        #self.myParent.geometry("640x400")
        self.__build_layout()

        #schedule monitor for the first time
        self.__myParent.after(self.__monitor_period, self.__monitor)

    def main_loop(self):
        self.__myParent.mainloop()

    def stop(self):
        print "gui stopping"
        self.__myParent.destroy()

    def display_data(self, text, format):
        if format == InfoFormat.CONFIRMATION:
            self.__activateConfirmationButton()
        
        #write info to text box
        self.__infoText.config(state=NORMAL)
        self.__infoText.insert(END, str(text),format)
        self.__infoText.see(END)
        self.__infoText.config(state=DISABLED)

    def __monitor(self):
        self.__myParent.update_idletasks()
        try:
            self.__periodic_cb()
        finally:
            #reschedule monitor
            self.__myParent.after(self.__monitor_period, self.__monitor)

    def __build_layout(self):
        
        #Text and scrollbar creation
        self.__scrollbar = Scrollbar(self.__myParent)
        
        self.__infoText = Text(
            self.__myParent
            ,wrap=WORD
            ,yscrollcommand=self.__scrollbar.set
            ,selectborderwidth=1
            ,background="gray"
            ,state = DISABLED)

        #text tags creation
        self.__infoText.tag_config(InfoFormat.CONFIRMATION, foreground="blue")
        self.__infoText.tag_config(InfoFormat.ERROR, foreground="red")

        self.__scrollbar.config(
            command=self.__infoText.yview
            ,borderwidth=1
            ,width=10
            )

        #create buttons
        button_width = 8      ### (1)
        button_padx = "2m"    ### (2)
        button_pady = "1m"    ### (2)

        self.__button1 = Button(self.__myParent)
        self.__button1.focus_force()
        self.__button1.configure( 
            text="Continue"
            ,fg="green"
            ,bg= "blue"
            ,width=button_width  ### (1)
            ,padx=button_padx    ### (2) 
            ,pady=button_pady    ### (2)
            ,state = DISABLED
            )

        self.__button2 = Button(self.__myParent)
        self.__button2.configure(
            text="Cancel",
            background="red",
            width=button_width,  ### (1)
            padx=button_padx,    ### (2) 
            pady=button_pady     ### (2)
            )

        #set layout
        self.__infoText.grid(row=0, column=0, columnspan=2, stick=W+N)
        self.__scrollbar.grid(row=0, column=2, stick=E+N+S)

        self.__button2.grid(row=1, column=1, stick=E+S)
        self.__button1.grid(row=1, column=0, stick=W+S)

        #bind events
        self.__button1.configure(command=self.__confirmationCallBack)
        self.__button2.configure(command=self.__terminateCallback)
        self.__button1.bind("<Escape>", self.__terminateCallback)
        self.__myParent.protocol("WM_DELETE_WINDOW", self.__terminateCallback)
        
    def __activateConfirmationButton(self):
        self.__button1.configure(state=NORMAL)

    def __disableConfirmationButton(self):
        self.__button1.configure(state=DISABLED)
    
    def __confirmationCallBack(self):
        if tkMessageBox.askokcancel(":)", "Do you really wish to Continue?"):
            print "pop-up confirmed, here we go..."
            self.__disableConfirmationButton()
            self.__gui_not_cb(CMD.RESUME)
        else:
            print "pop-up canceled, do nothing"

    def __terminateCallback(self, aux=None): 
        print "cancelExecution triggered"
        self.__gui_not_cb(CMD.STOP)
        self.stop()


class GuiManager():
    def __init__(self):
        self.__gui = GUI(self.gui_periodic_callback, self.gui_notifications_callback)
        self.__acceptData = True
        self.__in_queue = Queue.Queue(5)
        self.__out_queue = Queue.Queue(1)

    def main_loop(self):
        print "entering main loop"
        self.__gui.main_loop()
        print "leaving main loop"

    def waitUserConfirmation(self):
        cmd = self.__out_queue.get()
        return cmd == CMD.RESUME

    def waitUserCancel(self,):
        cmd = self.__out_queue.get()
        return cmd == CMD.STOP

    def updateUserInfo(self, info, format=InfoFormat.NONE):
        if self.__acceptData:
            self.__send_in_queue_message([info, format])
        else:
            print "gui shutting down, skipping send data"
            raise GUITerminating

    """
    Gui stop function to be called by external
    worker thread
    """
    def stop(self):
        self.__send_in_queue_message([CMD.STOP])


    #GUI callbacks
    def gui_periodic_callback(self):
        try:
            data = self.__in_queue.get_nowait()
            if len(data) == 2: #gui display request
                [info, format] = data
                self.__gui.display_data(info, format)
            elif len(data) == 1: #gui command
                print "cmd received:", data
                if data[0] == CMD.STOP:
                    self.__gui.stop()
            else:
                raise Exception("Invalid data received data:{0}".format(data))
        except Queue.Empty:
            pass

    def gui_notifications_callback(self, cmd):
        self.__send_out_queue_message(cmd)
        if cmd == CMD.STOP:
            self.__acceptData = False
            print "unblock feeders"
            try:
                self.__in_queue.get_nowait()
            except Queue.Empty:
                pass

    def __send_in_queue_message(self, data):
        #if self.__in_queue.full():
        #    print "WARNING IN queue full"
        self.__in_queue.put(data, timeout=1)
    
    def __send_out_queue_message(self, data):
        #if self.__out_queue.full():
        #    print "WARNING OUT queue full"
        self.__out_queue.put(data, timeout=1)


################### TEST CODE ####
def __test_gui_mananger():
    gui = GuiManager()
    gui.main_loop()
    print "Done"

if __name__ == '__main__':
    __test_gui_mananger()


