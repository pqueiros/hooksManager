from Tkinter import *

#refs:
#http://effbot.org/zone/tkinter-scrollbar-patterns.htm
#http://effbot.org/tkinterbook/text.htm
#http://effbot.org/tkinterbook/grid.htm#Tkinter.Grid.grid_remove-method

class GUIManager():
	def __init__(self):
		self.myParent = Tk() 
		self.wire_up()

	def wire_up(self):
		#self.myParent.geometry("640x400")
		self.build_layout()

		#TODO REMOVE ME
		self.counter = 0
		self.myParent.after(1000, self.gen_info)

  		print "enteting main loop"
  		self.myParent.mainloop()
  		print "leaving main loop"

  	def gen_info(self):
  		try:
  			self.counter= self.counter +1
  			self.append_Info(100*"TEST_INFO ")
  			self.append_Info(self.counter)
  		finally:
  			self.myParent.after(1000, self.gen_info)



  	def append_Info(self, info):
		self.infoText.config(state=NORMAL)
		self.infoText.insert(END, info)
		self.infoText.see(END)
		self.infoText.config(state=DISABLED)


	def build_layout(self):
		
		self.scrollbar = Scrollbar(self.myParent)
		
		self.infoText = Text(
			self.myParent
			,wrap=WORD
			,yscrollcommand=self.scrollbar.set
			,selectborderwidth=1
			,background="gray"
			,state = DISABLED)

		self.scrollbar.config(
			command=self.infoText.yview
			,borderwidth=1
			,width=10
			)

		#buttons
		button_width = 6      ### (1)
		button_padx = "2m"    ### (2)
		button_pady = "1m"    ### (2)

		self.button1 = Button(self.myParent, command=self.button1Click)
		self.button1.configure(text="OK", fg="green",bg= "blue")
		self.button1.focus_force()       
		self.button1.configure( 
			width=button_width,  ### (1)
			padx=button_padx,    ### (2) 
			pady=button_pady     ### (2)
			)

		self.button1.bind("<Return>", self.button1Click_a)  
		
		self.button2 = Button(self.myParent, command=self.button2Click)
		self.button2.configure(
		    text="Cancel",
		    background="red",
			width=button_width,  ### (1)
			padx=button_padx,    ### (2) 
			pady=button_pady     ### (2)
			)

		self.button2.bind("Return", self.button2Click_a) 
		
		self.infoText.grid(row=0, column=0, columnspan=2, stick=W+N)
		self.scrollbar.grid(row=0, column=2, stick=E+N+S)

		self.button2.grid(row=1, column=1, stick=E+S)
		self.button1.grid(row=1, column=0, stick=W+S)

		self.show_buttons()	

	def show_buttons(self):
		self.bVisible = 1
		self.button2.grid()
		self.button1.grid()

	def hide_buttons(self):
		self.bVisible = 0
		self.button2.grid_remove()
		self.button1.grid_remove()

	def toggle_buttonVisibility(self):
		if self.bVisible == 1:
			self.hide_buttons()
		else:
			self.show_buttons()

	def button1Click(self):      
		if self.button1["foreground"] != "yellow":  
			self.button1["foreground"] = "yellow"
		else:
			self.button1["foreground"] = "green"
	
	def button2Click(self): 
		self.myParent.destroy()     
		
	def button1Click_a(self, event): 
		print "button1Click_a just called" 
		self.append_Info ("TEST_ASYNC_INFO")
		self.toggle_buttonVisibility()
				
	def button2Click_a(self, event):
		print "button2Click_a just called"  
		self.button2Click() 
			
gui = GUIManager()

print "Done"