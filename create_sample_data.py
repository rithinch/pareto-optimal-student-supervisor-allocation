from pystsup.utilities import *
from pystsup.data import *
from pystsup.evolutionary import *


f1 = 'students_sample_international_development.xlsx'
f2 = 'supervisors_sample_international_development.xlsx'

students,supervisors = createRandomDataExcel(20,100,200, keywordsFile="international_development_keywords.txt")

createExcelFile(f1,students,True)
createExcelFile(f2,supervisors,False)
