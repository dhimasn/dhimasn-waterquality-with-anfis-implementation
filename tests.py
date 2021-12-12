import anfis
import membership.mfDerivs
import membership.membershipfunction
import numpy
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

#ts = numpy.loadtxt("trainingSet.txt", usecols=[1,2,3])#numpy.loadtxt('c:\\Python_fiddling\\myProject\\MF\\trainingSet.txt',usecols=[1,2,3])
#X = ts[:,0:2]
#Y = ts[:,2]

conn = mysql.connector.connect(host='localhost',
                                 database='waterquality',
                                 user='root',
                                 password='',
                                 charset='utf8',
                                 use_unicode=True)
         
if conn.is_connected():
    # get records training
    sql_select_Query = '''SELECT `Suhu (C)` as suhu,`Zat padat terlarut (TDS) mg/L` as zt_tds, `Zat padat tersuspensi (TSS) mg/L` as zt_tss,`pH` as ph,`COD (dichromat) mg/L` as cod,`Nitrat mg/L` as nitrat,`Minyak dan Lemak Âµg/L` as minyak,`Bakteri Koli Jml/100 mL`as bk,`Bakteri Koli Tinja Jml/100 mL` as bkt, `Indeks Pencemar` as ipc FROM `waterquality_jakarta_training`
                             WHERE `periode` = '2018-1' 
                             AND `Suhu (C)` != ""
                             AND `Zat padat terlarut (TDS) mg/L` != "" 
                             AND `Zat padat tersuspensi (TSS) mg/L`!= ""
                             AND `Nitrat mg/L` != ""
                             AND `Minyak dan Lemak Âµg/L` != ""
                             AND `Bakteri Koli Jml/100 mL` != ""
                             AND `Bakteri Koli Tinja Jml/100 mL` != "" ;'''
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute(sql_select_Query)        
    data_training = cursor.fetchall()
    #menampilkan data hasil select database
    #print(data_training)
    df = pd.DataFrame(data_training)

x = {0:[],1:[]}
for i in range(len(df['zt_tds'])):
    x[0].append(int(i))
for i in range(len(df['zt_tss'])):
    x[1].append(int(i))
y = {0:[]}  
for i in range(len(df['ipc'])):
    y[0].append(int(i))        
    
dataX = [x[1]]
dataY = [y[0]]

mf = [
        [
            ['gaussmf',{'mean':0.,'sigma':1.}],
            ['gaussmf',{'mean':-1.,'sigma':2.}],
            ['gaussmf',{'mean':-4.,'sigma':10.}],
            ['gaussmf',{'mean':-7.,'sigma':7.}]
        ],
        [
            ['gaussmf',{'mean':1.,'sigma':2.}],
            ['gaussmf',{'mean':2.,'sigma':3.}],
            ['gaussmf',{'mean':-2.,'sigma':10.}],
            ['gaussmf',{'mean':-10.5,'sigma':5.}]
        ]
    ]


mfc = membership.membershipfunction.MemFuncs(mf)
anf = anfis.ANFIS(dataX, dataY, mfc)
anf.trainHybridJangOffLine(epochs=20)
"""print(round(anf.consequents[-1][0],6))
print(round(anf.consequents[-2][0],6))
print(round(anf.fittedValues[9][0],6))
if round(anf.consequents[-1][0],6) == -5.275538 and round(anf.consequents[-2][0],6) == -1.990703 and round(anf.fittedValues[9][0],6) == 0.002249:
	print('test is good')

print("Plotting errors")
anf.plotErrors()
print("Plotting results")
anf.plotResults() """
