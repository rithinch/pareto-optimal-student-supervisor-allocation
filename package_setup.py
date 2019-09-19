import cx_Freeze
import sys
import os 

base = None

os.environ['TCL_LIBRARY'] = r'C:\\Anaconda3\\envs\\pystsup\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Anaconda3\\envs\\pystsup\\tcl\\tk8.6'
 

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("GUI_Application.py", base=base)]

cx_Freeze.setup(
    name = "Student Supervisor Allocation Tool",
    options = {"build_exe": {"packages":["tkinter","numpy", "pystsup", "pyomo", "pygmo", "hopcroftkarp", "openpyxl"], "include_files":["configGA.json"]}},
    version = "1.0.1",
    description = "AI Tool for Student Supervisor Allocation",
    executables = executables
    )