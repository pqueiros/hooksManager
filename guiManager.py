from Tkinter import *
import tkMessageBox

#refs:
#http://effbot.org/zone/tkinter-scrollbar-patterns.htm
#http://effbot.org/tkinterbook/text.htm
#http://effbot.org/tkinterbook/grid.htm#Tkinter.Grid.grid_remove-method

class GUIManager():
	def __init__(self):
		self.__myParent = Tk() 
		self.__wire_up()

	def __wire_up(self):
		#self.myParent.geometry("640x400")
		self.__build_layout()

		#TODO REMOVE ME
		self.__counter = 0
		self.__myParent.after(1000, self.__gen_info)

  		print "enteting main loop"
  		try:
  			self.__myParent.mainloop()
  		except:
  			print "exit exception" 

  		print "leaving main loop"

  	def __gen_info(self):
  		try:
  			self.__counter= self.__counter +1
  			self.__append_Info(100*"TEST_INFO ")
  			self.__append_Info(self.__counter)
  		finally:
  			self.__myParent.after(1000, self.__gen_info)



  	def __append_Info(self, info):
		self.__infoText.config(state=NORMAL)
		self.__infoText.insert(END, info)
		self.__infoText.see(END)
		self.__infoText.config(state=DISABLED)


	def __build_layout(self):
		
		#widgets creation
		self.__scrollbar = Scrollbar(self.__myParent)
		
		self.__infoText = Text(
			self.__myParent
			,wrap=WORD
			,yscrollcommand=self.__scrollbar.set
			,selectborderwidth=1
			,background="gray"
			,state = DISABLED)

		self.__scrollbar.config(
			command=self.__infoText.yview
			,borderwidth=1
			,width=10
			)

		#buttons
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
		self.__button1.bind("<Return>", self.__button1Click_a) #TODO REMOVE
		self.__button1.bind("<Escape>", self.__terminateCallback)
		self.__myParent.protocol("WM_DELETE_WINDOW", self.__terminateCallback)
		

	def __toggle_buttonVisibility(self):
		self.__button1.configure(state=NORMAL)
		

	def __confirmationCallBack(self):
		print "button1Click just called"
		if tkMessageBox.askokcancel(":)", "Do you really wish to Continue?"):
			print "you really continued"
		else:
			print "you are a chicken"
	
	def __terminateCallback(self, aux=None): 
		print "cancelExecution just called"
		self.__myParent.destroy()     

	#TODO REMOVE	
	def __button1Click_a(self, event): 
		print "button1Click_a just called" 
		self.__append_Info ("TEST_ASYNC_INFO")
		self.__toggle_buttonVisibility()

			
gui = GUIManager()

print "Done"