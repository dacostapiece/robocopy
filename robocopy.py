import os
import datetime as dt
import shutil
import time

#DECLARE GLOBAL VARIABLES
currentDate = dt.date.today()
anoAtual = currentDate.strftime("%Y")
mesAtual = currentDate.strftime("%m")
anoPassado = int(currentDate.strftime("%Y"))-1
mesesLista =['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
mesPassado = int(currentDate.strftime("%m"))-1
maxAge = 7
#rootFolder = r"C:\Users\rafaellocal\Dropbox\PROGRAMAÇÃO\ROBOCOPY\CONFIGURACOES"
rootFolder = r"C:\Users\rafaellocal\Dropbox\PROGRAMAÇÃO\ROBOCOPY\CONFIGURACOES\Nova Pasta\Sample"

#VALIDATE mesPassado/anoOrigem
if mesPassado == 0:
    mesPassado = 12
    anoOrigem = anoPassado
else:
    anoOrigem = anoAtual

#LOOK FOR SOURCE AND DEST FOLDER
sourceFolder = rootFolder + ("\\")+str(anoOrigem) +("-")+ mesesLista[int(mesPassado-1)]
destFolder = rootFolder + ("\\")+str(anoAtual) + ("-")+mesesLista[int(mesAtual)-1]

#DEAL WITH FORWARD AND BACKSLASHES
rootFolder = rootFolder.replace("\\","/")
sourceFolder = sourceFolder.replace("\\","/")
destFolder = destFolder.replace("\\","/")

#ENTER ROOT FOLDER DIRECTORY
os.chdir(rootFolder)

#SOURCE/DEST BASEMAME
origem = os.path.basename(sourceFolder)
destino = os.path.basename(destFolder)

#START VARIABLES
folderLevel = 0
dirsFound = [1]

#INITIAL ROOT FUNCTION
def robocopyFolder(sourceFolder, destFolder):
    #LIST VARIABLES FOR TIME AND TYPE OBJECT VALIDATION (FOLDER OR FILE?)
    dirsFound = []
    filesFound = []
    fullPathItensFound = []
    newDestFolder = []

    #LIST SOURCE FOLDER CONTENT    
    itensFound = os.listdir(sourceFolder)

    #COMPARE AND SPLIT CONTENT
    for i in range(len(itensFound)):
        fullPathItensFound.append(os.path.join(sourceFolder,itensFound[i]))
        if os.path.isdir(fullPathItensFound[i]) == True:
            dirsFound.append(fullPathItensFound[i])
        elif os.path.isfile(fullPathItensFound[i]) == True:
            #VALIDATE FILE OLDER THAN 7 DAYS
            if (time.time() - os.path.getmtime(fullPathItensFound[i])) // (24 * 3600) <= maxAge:
                filesFound.append(fullPathItensFound[i])

    newDestFolder = list(dirsFound)

    #SET NEW DEST FOLDER PATH
    for i in range(len(dirsFound)):
            newDestFolder[i] = dirsFound[i].replace(origem, destino)

    # CREATE FOLDER STRUCTURE USING FULL MAIN DEST FOLDER AND ONLY NEW FOLDER
    for i in range(len(dirsFound)):
        os.makedirs(os.path.join(destFolder,os.path.basename(dirsFound[i])))

    # COPY FILES NOT OLDER THAN 7 DAYS
    for i in range(len(filesFound)):
        shutil.copy2(filesFound[i],destFolder)

    print("")
    print("INSIDE FUNCTION")
    print("Scanning: ", sourceFolder)
    print("dirsFound inside Function: ", dirsFound)
    print("dirsFound inside Function tamanho: ", len(dirsFound))
    print("")
    print("newDestFolder inside Function: ", newDestFolder)
    print("newDestFolder inside Function tamanho: ", len(newDestFolder))

    return dirsFound, newDestFolder

print("PRIMEIRA CHAMADA")
completeItensFound = robocopyFolder(sourceFolder, destFolder)
dirsFound = list(completeItensFound[0])
print("")
print("dirsFound Primeira Chamada: ",dirsFound)
newDestFolder = list(completeItensFound[1])

print("")
print('PRIMEIRO LOOP COMEÇA ABAIXO')

#FIRST LOOP
dirsFoundFirstLoop = []
newDestFolderFirstLoop = []
dirsFoundFirstLoopFixList = []
newDestFolderFirstLoopFixList = []

for i in range(len(dirsFound)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFound[i], newDestFolder[i])
    if completeItensFound[0]!=[]:
        dirsFoundFirstLoop.append(completeItensFound[0])
        newDestFolderFirstLoop.append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(dirsFoundFirstLoop)):
    dirsFoundFirstLoopFixList.extend(dirsFoundFirstLoop[i])

#create DEST FOLDER FROM FIXED FIRST LIST
newDestFolderFirstLoopFixList = list(dirsFoundFirstLoopFixList)

#FIX NAME for DEST FOLDER
for i in range (len(newDestFolderFirstLoopFixList)):
    newDestFolderFirstLoopFixList[i] = dirsFoundFirstLoopFixList[i].replace(origem, destino)

########################SECOND LOOP##################

#SECOND LOOP
dirsFoundSecondLoop = []
newDestFolderSecondLoop = []
dirsFoundSecondLoopFixList = []
newDestFolderSecondLoopFixList = []

for i in range(len(dirsFoundFirstLoopFixList)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFoundFirstLoopFixList[i], newDestFolderFirstLoopFixList[i])
    if completeItensFound[0]!=[]:
        dirsFoundSecondLoop.append(completeItensFound[0])
        newDestFolderSecondLoop.append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(dirsFoundSecondLoop)):
    dirsFoundSecondLoopFixList.extend(dirsFoundSecondLoop[i])

#create DEST FOLDER FROM FIXED FIRST LIST
newDestFolderSecondLoopFixList = list(dirsFoundSecondLoopFixList)

#FIX NAME for DEST FOLDER
for i in range (len(newDestFolderSecondLoop)):
    newDestFolderSecondLoopFixList[i] = dirsFoundSecondLoopFixList[i].replace(origem, destino)

########################THIRD LOOP##################

#THIRD LOOP
dirsFoundThirdLoop = []
newDestFolderThirdLoop = []
dirsFoundThirdLoopFixList = []
newDestFolderThirdLoopFixList = []

for i in range(len(dirsFoundSecondLoopFixList)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFoundSecondLoopFixList[i], newDestFolderSecondLoopFixList[i])
    if completeItensFound[0]!=[]:
        dirsFoundThirdLoop.append(completeItensFound[0])
        newDestFolderThirdLoop.append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(dirsFoundThirdLoop)):
    dirsFoundThirdLoopFixList.extend(dirsFoundThirdLoop[i])

#create DEST FOLDER FROM FIXED FIRST LIST
newDestFolderThirdLoopFixList = list(dirsFoundThirdLoopFixList)

#FIX NAME for DEST FOLDER
for i in range (len(newDestFolderThirdLoop)):
    newDestFolderThirdLoopFixList[i] = dirsFoundThirdLoopFixList[i].replace(origem, destino)

########################FOURTH LOOP##################

#THIRD LOOP
dirsFoundFourthLoop = []
newDestFolderFourthLoop = []
dirsFoundFourthLoopFixList = []
newDestFolderFourthLoopFixList = []

for i in range(len(dirsFoundThirdLoopFixList)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFoundThirdLoopFixList[i], newDestFolderThirdLoopFixList[i])
    if completeItensFound[0]!=[]:
        dirsFoundFourthLoop.append(completeItensFound[0])
        newDestFolderFourthLoop.append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(dirsFoundFourthLoop)):
    dirsFoundFourthLoopFixList.extend(dirsFoundFourthLoop[i])

#create DEST FOLDER FROM FIXED FIRST LIST
newDestFolderFourthLoopFixList = list(dirsFoundFourthLoopFixList)

#FIX NAME for DEST FOLDER
for i in range (len(newDestFolderFourthLoop)):
    newDestFolderFourthLoopFixList[i] = dirsFoundFourthLoopFixList[i].replace(origem, destino)

########################FIFTH LOOP##################

#THIRD LOOP
dirsFoundFifthLoop = []
newDestFolderFifthLoop = []
dirsFoundFifthLoopFixList = []
newDestFolderFifthLoopFixList = []

for i in range(len(dirsFoundFourthLoopFixList)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFoundFourthLoopFixList[i], newDestFolderFourthLoopFixList[i])
    if completeItensFound[0]!=[]:
        dirsFoundFifthLoop.append(completeItensFound[0])
        newDestFolderFifthLoop.append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(dirsFoundFifthLoop)):
    dirsFoundFifthLoopFixList.extend(dirsFoundFifthLoop[i])

#create DEST FOLDER FROM FIXED FIRST LIST
newDestFolderFifthLoopFixList = list(dirsFoundFifthLoopFixList)

#FIX NAME for DEST FOLDER
for i in range (len(newDestFolderFifthLoop)):
    newDestFolderFifthLoopFixList[i] = dirsFoundFifthLoopFixList[i].replace(origem, destino)

print("")
print("FIM")
