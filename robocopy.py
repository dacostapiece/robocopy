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
    for i in range(len(dirsFound)):
        os.makedirs(os.path.join(destFolder,os.path.basename(dirsFound[i])))

    # # # COPY FILES NOT OLDER THAN 7 DAYS
    for i in range(len(filesFound)):
        shutil.copy2(filesFound[i],destFolder)

    print("")
    print("INSIDE FUNCTION")
    print("Scanning: ", sourceFolder)
    print("dirsFound inside Function: ", dirsFound)
    print("filesFound inside Function: ", filesFound)
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

######################START LOOPS##################
#START VARIABLES
N = 0 #N indicates the sublevel from a folder and it increases as deep as it goes

howManyLevels = [0]

while len(howManyLevels)>0:
    if N == 0:
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
        
        N+=1
    elif N > 0:

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
        for i in range (len(globals()[newDestFolderLoopFixListN])):
            globals()[newDestFolderLoopFixListN][i] = globals()[dirsFoundLoopFixListN][i].replace(origem, destino)
        
        N+=1

    #IS THERE MORE SUBLEVEL DIRECTORIES TO GO THROUGH?
    if globals()[dirsFoundLoopN]==[]:
        howManyLevels = []
    elif N>100:
        print("Stopping program, there are more than 100 sub-level directories, is that real good?")
        howManyLevels = []

#COMPARE SOURCE DEST
# def list_files(source_dir):
#     blankParentFolder = os.path.basename(source_dir)
#     file_list = []
#     newfile_list = []
#     for root, dirs, files in os.walk(source_dir):
#         for name in files:
#             full_path = os.path.join(root, name)
#             file_age = time.time() - os.stat(full_path).st_mtime
#             if file_age < 7 * 24 * 60 * 60:  # 7 days in seconds
#                 file_list.append(full_path)
#         for name in dirs:
#             full_path = os.path.join(root, name)
#             file_age = time.time() - os.stat(full_path).st_mtime
#             if file_age < 7 * 24 * 60 * 60:  # 7 days in seconds
#                 file_list.append(full_path)
    
#     newfile_list = list(file_list)

#     for i in range(len(file_list)):
#             newfile_list[i] = os.path.normpath(file_list[i].replace(blankParentFolder, ""))
            
#     return newfile_list

# source = list_files(sourceFolder)
# dest = list_files(destFolder)

# if source != dest:
#     print("algo está diferente")
# else:
#     print("tudo igual")

print("")
print("FIM")
