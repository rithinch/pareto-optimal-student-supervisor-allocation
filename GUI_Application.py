"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    File: GUI_Application.py
    
    Purpose:  Contains required code for GUI.
             
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

        self.master.title("AI Tool For Student - Supervisor Allocation")

        #creating menu

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)

        file.add_separator()
        
        file.add_command(label="Exit",command=self.app_exit)

        menu.add_cascade(label="File",menu=file)

        options = Menu(menu)

        options.add_command(label="Change GA Parameters",command = self.editGAConfig)
        menu.add_cascade(label="Options",menu=options)

        helper = Menu(menu)
        
        helper.add_command(label="About", command=self.showAbout)
        
        helper.add_separator()
        
        helper.add_command(label="Show Tutorial", command=self.showTutorial)

        menu.add_cascade(label="Help",menu=helper)


        #Creating labels
        self.label_0 = Label(self.master,relief=RIDGE,width=63,text="Select Keywords File (.txt)")
        self.label_1 = Label(self.master,relief=RIDGE,width=63,text="Select Students File")
        self.label_2 = Label(self.master,relief=RIDGE,width=63,text="Select Supervisors File")
        self.label_3 = Label(self.master,relief=RIDGE,width=63,text="Select Where to Save the Results")
        
        self.label_0.grid(row=0, column=0, pady=10)
        self.label_1.grid(row=1,column=0,pady=10)
        self.label_2.grid(row=2,column=0,pady=10)
        self.label_3.grid(row=3,column=0,pady=10)
        
        button0 = Button(self.master,text="Browse",width=5,command=self.selectFile0)
        button1 = Button(self.master,text="Browse",width=5,command=self.selectFile1)
        button2 = Button(self.master,text="Browse",width=5,command = self.selectFile2)
        button3 = Button(self.master,text="Save As",width=5,command=self.saveAs)
        button4 = Button(self.master,text="Start Genetic Algorithm",command=self.runGA)

        button0.grid(row=0, column=1, pady=10)
        button1.grid(row=1,column=1,pady=10)
        button2.grid(row=2,column=1,pady=10)
        button3.grid(row=3,column=1,pady=10)
        button4.grid(row=4,padx=20,pady=30)

        #Parameters

        self.keywordsFile = None
        self.stuFile = None
        self.supFile = None
        self.outputName = None
        

    
        
    def startRUN(self,students,supervisors):

        #Creating Fitness Cache and RankWeights
        print("Creating the fitness cache..")
        
        rankWeights = Solution.calcRankWeights()
        fitnessCache = calcFitnessCache(students,supervisors,rankWeights)
        

        #Setting up the parameters

        print("Parsing the GA Config file..")

        gen,size,crOp,muOp,selOp,muProb,swProb,trProb = parseConfigFile("configGA.json")
            
        geneticAlgorithm = GeneticAlgorithm(students,supervisors,fitnessCache,rankWeights,muOp,crOp,selOp)

        #Running the GA

        print("Starting GA Run..")
        
        metricData,front = geneticAlgorithm.start(size,gen,muProb,swProb,trProb)
        

        return front,metricData

        
    def saveAs(self):

        filename = asksaveasfilename(title="Select where to save the results",filetypes=[("Excel Files","*.xlsx")])
        self.outputName = filename
        self.label_3['text']= filename + ".xlsx"
        
        
    def runGA(self):

        #Getting the Data
        if self.stuFile != None or self.supFile!=None or self.outputName!=None or self.keywordsFile!=None:
                  
            print("Getting the input data from excel files..")
            students,supervisors = getData(self.stuFile,self.supFile, keywordsFile=self.keywordsFile)     

            
            non_dominated_solutions,metricData = self.startRUN(students,supervisors)

            print("Saving the results..")
            writeFrontier(self.outputName,non_dominated_solutions,metricData,supervisors,students)

            filename = self.outputName.split("/")[-1] + ".xlsx"

            showinfo("Success","Genetic Algoritm Evolution completed. The results have been saved in "+filename+".")
                
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

    def editGAConfig(self):

        gen,size,crOp,muOp,selOp,muProb,swProb,trProb = parseConfigFile("configGA.json")
        
        self.top1 = Toplevel(self.master)
        self.top1.transient(self.master)
        self.top1.title("Update GA Parameters")
        label1 = Label(self.top1,text="Generation Convergence Limit")
        label2 = Label(self.top1, text="Population Size")
        label3 = Label(self.top1, text = "Mutation Probability")
        label4 = Label(self.top1,text = "Swap Probability")
        label5 = Label(self.top1,text="Transfer Probability")

        button1 = Button(self.top1,text="Update Parameters",command=self.updateConfig)
        button2 = Button(self.top1,text="Cancel",command=self.cancelUpdate)
        
        label1.grid(row=0)
        label2.grid(row=1)
        label3.grid(row=2)
        label4.grid(row=3)
        label5.grid(row=4)

        self.entry1 = Entry(self.top1)
        self.entry1.insert(0,str(gen))
        self.entry2 = Entry(self.top1)
        self.entry2.insert(0,str(size))
        self.entry3 = Entry(self.top1)
        self.entry3.insert(0,str(muProb))
        self.entry4 = Entry(self.top1)
        self.entry4.insert(0,str(swProb))
        self.entry5 = Entry(self.top1)
        self.entry5.insert(0,str(trProb))

        self.entry1.grid(row=0,column=1)
        self.entry2.grid(row=1,column=1)
        self.entry3.grid(row=2,column=1)
        self.entry4.grid(row=3,column=1)
        self.entry5.grid(row=4,column=1)

        button1.grid(row=5,column=0,padx=10,pady=20)
        button2.grid(row=5,column=1,padx=10,pady=20)
        


    def updateConfig(self):
        updateConfigFile("configGA.json",int(self.entry1.get()),int(self.entry2.get()),float(self.entry3.get()),float(self.entry4.get()),float(self.entry5.get()))
        showinfo("Success","Genetic Algorithm Parameters have been sucessfully updated.")
        self.top1.destroy()

    def cancelUpdate(self):
        self.top1.destroy()

    def showAbout(self):
        showinfo("About","An AI Tool for Student-Supervisor Allocation in Coventry University\n\nVersion: 1.0\nCreated By: Rithin Chalumuri \nSupervisor: Victor Sanchez \n\nThis application was created as part of Coventry University Summer Research Project 2017.")
        
        
    def showTutorial(self):
        showinfo("Tutorial","The find out how to use this application please go through 'tutorial.pdf' in the installation folder.")

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

    
