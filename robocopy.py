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
    # for i in range(len(dirsFound)):
    #     os.makedirs(os.path.join(destFolder,os.path.basename(dirsFound[i])))

    # # COPY FILES NOT OLDER THAN 7 DAYS
    # for i in range(len(filesFound)):
    #     shutil.copy2(filesFound[i],destFolder)

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

#START VARIABLES
N = 0 #N indicates the sublevel from a folder and it increases as deep as it goes

#first generic loop variables
dirsFoundLoopN = f"dirsFoundLoop{N}"
newDestFolderLoopN = f"newDestFolderLoop{N}"
dirsFoundLoopFixListN = f"dirsFoundLoopFixList{N}"
newDestFolderLoopFixListN = f"newDestFolderLoopFixList{N}"

#FIRST LOOP
globals()[dirsFoundLoopN] = []
globals()[newDestFolderLoopN] = []
globals()[dirsFoundLoopFixListN] = []
globals()[newDestFolderLoopFixListN] = []

for i in range(len(dirsFound)):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(dirsFound[i], newDestFolder[i])
    if completeItensFound[0]!=[]:
        globals()[dirsFoundLoopN].append(completeItensFound[0])
        globals()[newDestFolderLoopN].append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(globals()[dirsFoundLoopN])):
    globals()[dirsFoundLoopFixListN].extend(globals()[dirsFoundLoopN][i])

#create DEST FOLDER FROM FIXED FIRST LIST
globals()[newDestFolderLoopFixListN] = list(globals()[dirsFoundLoopFixListN])

#FIX NAME for DEST FOLDER
for i in range (len(globals()[newDestFolderLoopFixListN])):
    globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)

#######################SECOND LOOP##################

N+=1

#second generic loop variables
dirsFoundLoopN = f"dirsFoundLoop{N}"
newDestFolderLoopN = f"newDestFolderLoop{N}"
dirsFoundLoopFixListN = f"dirsFoundLoopFixList{N}"
newDestFolderLoopFixListN = f"newDestFolderLoopFixList{N}"

#SECOND LOOP
globals()[dirsFoundLoopN] = []
globals()[newDestFolderLoopN] = []
globals()[dirsFoundLoopFixListN] = []
globals()[newDestFolderLoopFixListN] = []

currentSourceLoop = f"dirsFoundLoopFixList{N-1}"
currentDestLoop = f"newDestFolderLoopFixList{N-1}"

for i in range(len(globals()[currentSourceLoop])):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(globals()[currentSourceLoop][i], globals()[currentDestLoop][i])
    if completeItensFound[0]!=[]:
        globals()[dirsFoundLoopN].append(completeItensFound[0])
        globals()[newDestFolderLoopN].append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(globals()[dirsFoundLoopN])):
    globals()[dirsFoundLoopFixListN].extend(globals()[dirsFoundLoopN][i])

#create DEST FOLDER FROM FIXED FIRST LIST
globals()[newDestFolderLoopFixListN] = list(globals()[dirsFoundLoopFixListN])

#FIX NAME for DEST FOLDER
for i in range (len(globals()[newDestFolderLoopN])):
    globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)

# ########################THIRD LOOP##################

N+=1

#third generic loop variables
dirsFoundLoopN = f"dirsFoundLoop{N}"
newDestFolderLoopN = f"newDestFolderLoop{N}"
dirsFoundLoopFixListN = f"dirsFoundLoopFixList{N}"
newDestFolderLoopFixListN = f"newDestFolderLoopFixList{N}"

#THIRD LOOP
globals()[dirsFoundLoopN] = []
globals()[newDestFolderLoopN] = []
globals()[dirsFoundLoopFixListN] = []
globals()[newDestFolderLoopFixListN] = []

currentSourceLoop = f"dirsFoundLoopFixList{N-1}"
currentDestLoop = f"newDestFolderLoopFixList{N-1}"

for i in range(len(globals()[currentSourceLoop])):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(globals()[currentSourceLoop][i], globals()[currentDestLoop][i])
    if completeItensFound[0]!=[]:
        globals()[dirsFoundLoopN].append(completeItensFound[0])
        globals()[newDestFolderLoopN].append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(globals()[dirsFoundLoopN])):
    globals()[dirsFoundLoopFixListN].extend(globals()[dirsFoundLoopN][i])

#create DEST FOLDER FROM FIXED FIRST LIST
globals()[newDestFolderLoopFixListN] = list(globals()[dirsFoundLoopFixListN])

#FIX NAME for DEST FOLDER
for i in range (len(globals()[newDestFolderLoopN])):
    globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)

########################FOURTH LOOP##################

N+=1

#FOURTH LOOP

#fourth generic loop variables
dirsFoundLoopN = f"dirsFoundLoop{N}"
newDestFolderLoopN = f"newDestFolderLoop{N}"
dirsFoundLoopFixListN = f"dirsFoundLoopFixList{N}"
newDestFolderLoopFixListN = f"newDestFolderLoopFixList{N}"

globals()[dirsFoundLoopN] = []
globals()[newDestFolderLoopN] = []
globals()[dirsFoundLoopFixListN] = []
globals()[newDestFolderLoopFixListN] = []

currentSourceLoop = f"dirsFoundLoopFixList{N-1}"
currentDestLoop = f"newDestFolderLoopFixList{N-1}"

for i in range(len(globals()[currentSourceLoop])):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(globals()[currentSourceLoop][i], globals()[currentDestLoop][i])
    if completeItensFound[0]!=[]:
        globals()[dirsFoundLoopN].append(completeItensFound[0])
        globals()[newDestFolderLoopN].append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(globals()[dirsFoundLoopN])):
    globals()[dirsFoundLoopFixListN].extend(globals()[dirsFoundLoopN][i])

#create DEST FOLDER FROM FIXED FIRST LIST
globals()[newDestFolderLoopFixListN] = list(globals()[dirsFoundLoopFixListN])

#FIX NAME for DEST FOLDER
for i in range (len(globals()[newDestFolderLoopN])):
    globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)

########################FIFTH LOOP##################

N+=1

#fifth generic loop variables
dirsFoundLoopN = f"dirsFoundLoop{N}"
newDestFolderLoopN = f"newDestFolderLoop{N}"
dirsFoundLoopFixListN = f"dirsFoundLoopFixList{N}"
newDestFolderLoopFixListN = f"newDestFolderLoopFixList{N}"

#FIFTH LOOP
globals()[dirsFoundLoopN] = []
globals()[newDestFolderLoopN] = []
globals()[dirsFoundLoopFixListN] = []
globals()[newDestFolderLoopFixListN] = []

currentSourceLoop = f"dirsFoundLoopFixList{N-1}"
currentDestLoop = f"newDestFolderLoopFixList{N-1}"

for i in range(len(globals()[currentSourceLoop])):
    print("")
    print("PRIMEIRO LOOP: Index: ", i)
    completeItensFound = robocopyFolder(globals()[currentSourceLoop][i], globals()[currentDestLoop][i])
    if completeItensFound[0]!=[]:
        globals()[dirsFoundLoopN].append(completeItensFound[0])
        globals()[newDestFolderLoopN].append(completeItensFound[1])

#FIX LIST ARRAY
for i in range (len(globals()[dirsFoundLoopN])):
    globals()[dirsFoundLoopFixListN].extend(globals()[dirsFoundLoopN][i])

#create DEST FOLDER FROM FIXED FIRST LIST
globals()[newDestFolderLoopFixListN] = list(globals()[dirsFoundLoopFixListN])

#FIX NAME for DEST FOLDER
for i in range (len(globals()[newDestFolderLoopN])):
    globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)

print("")
print("FIM")
