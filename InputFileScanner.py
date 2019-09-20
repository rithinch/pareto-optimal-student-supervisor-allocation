"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    File: InputFileScanner.py
    
    Purpose:  Contains required code for Input File Scanner GUI.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


from pystsup.utilities import *
from pystsup.data import *
from pystsup.evolutionary import *

from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showinfo,showerror
import os

class Window(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):

        self.master.title("Input File Scanner - Student-Supervisor Allocation AI Tool")

        #creating menu

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)

        file.add_separator()
        
        file.add_command(label="Exit",command=self.app_exit)

        menu.add_cascade(label="File",menu=file)

        helper = Menu(menu)
        
        helper.add_command(label="About", command=self.showAbout)
        
        menu.add_cascade(label="Help",menu=helper)


        #Creating labels
        self.label_0 = Label(self.master,relief=RIDGE,width=63,text="Select Keywords File (.txt)")
        self.label_1 = Label(self.master,relief=RIDGE,width=63,text="Select Students File")
        self.label_2 = Label(self.master,relief=RIDGE,width=63,text="Select Supervisors File")
        
        self.label_0.grid(row=0, column=0, pady=10)
        self.label_1.grid(row=1,column=0,pady=10)
        self.label_2.grid(row=2,column=0,pady=10)
        
        button0 = Button(self.master,text="Browse",width=5,command=self.selectFile0)
        button1 = Button(self.master,text="Browse",width=5,command=self.selectFile1)
        button2 = Button(self.master,text="Browse",width=5,command = self.selectFile2)
        button4 = Button(self.master,text="Scan Input Files",command=self.runScan)

        button0.grid(row=0, column=1, pady=10)
        button1.grid(row=1,column=1,pady=10)
        button2.grid(row=2,column=1,pady=10)
        button4.grid(row=3,padx=20,pady=30)

        #Parameters

        self.keywordsFile = None
        self.stuFile = None
        self.supFile = None
        

    def runScan(self):

        #Getting the Data
        if self.stuFile != None or self.supFile!=None or self.keywordsFile!=None:
                  
            studentsError,supervisorsError = scanInputData(self.stuFile,self.supFile, self.keywordsFile)     

            if studentsError == 0 and supervisorsError == 0:
                showinfo("Success","No input errors have been found in both files. You're good to go!")
            else:
                showerror("Error", "Looks like there a few inconsistencies in files provided. Certain keywords provided in the excel files don't match the taxonomy tree. The incosistencies have been marked for you, please open and check again.")
                
        else:
            showerror("Error", "Input files not provided. Please select appropriate student and supervisor data files.")
            

    def selectFile0(self):

        filename = askopenfilename(title="Select Keywords taxonomy file",filetypes=[("Text Files","*.txt")])
        self.keywordsFile = filename
        toshow = "Keywords Taxonomy File = "+filename.split("/")[-1]
        
        self.label_0['text']=toshow

    def selectFile1(self):

        filename = askopenfilename(title="Select Student Data File",filetypes=[("Excel Files","*.xlsx")])
        self.stuFile = filename
        toshow = "Student File = "+filename.split("/")[-1]
        
        self.label_1['text']=toshow
        
    def selectFile2(self):

        filename = askopenfilename(title="Select Supervisor Data File",filetypes=[("Excel Files","*.xlsx")])
        self.supFile = filename
        toshow = "Supervisor File = " + filename.split("/")[-1]
        
        self.label_2['text']=toshow

    def app_exit(self):
        os._exit(0)

    def showAbout(self):
        showinfo("About","An AI Tool for Student-Supervisor Allocation in Coventry University\n\nVersion: 1.0\nCreated By: Rithin Chalumuri \nSupervisor: Victor Sanchez \n\nThis application was created as part of Coventry University Summer Research Project 2017.")
        
##########################################################################################################################

#Set the path to current director, if in case run from a desktop shortcut
        
try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

root = Tk()

root.geometry("500x300")
root.resizable(False, False)
app = Window(root)

root.mainloop()

    
