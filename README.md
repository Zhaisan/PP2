
import os 
import fnmatch
from os import path

path = os.getcwd()
print("""HELLO!


>-< WRITE YOUR NAME """ )

# name = str(input())

def MENU(name):
    print(name + """,  
    What do you want to do?
                    
    press 1 to work with file
    press 2 to work with directory
    press 0 to go back/exit""")









def File_Menu():
    print("""
    Press 1 delete file
    Press 2 to rename file
    Press 3 to add content of this file
    Press 4 to rewrite content of this file
    Press 5 for return to the parent directory
    Press 0 to go back to Menu""")


# button = int(input())
def workWithFile(button):
    if button == 0:
        exit()


    elif button == 1:
        FileName = input("File name : ") + ".txt"
        
        try:
            os.remove()
        except FileNotFoundError:
            print("File was not found")
        
        else:
            print("File was deleted")

    elif button == 2:
        FileName1 = input("Old file name : ") + ".txt"
        FileName2 = input("New file name : ") + ".txt"
        try:
            os.rename(FileName1, FileName2)
        except FileNotFoundError:
            print("File was NOT found")
                
        else:
            print("File name successfully changed")
        

    elif button == 3:

        FileName = input("Open file : ") + ".txt"
        try:
            cmd = open(FileName, "at")
        except FileNotFoundError:
            print("File was not found")
                    
        else:
            information = input()
            cmd.write(information)
            cmd.close()



    elif button == 4:  
        FileName = input("Open file : ") + ".txt"
        try:
            cmd = open(FileName, "wt")
        except FileNotFoundError:
            print("File not found")
        
        else:
            information = input()
            cmd.write(information)
            cmd.close()
                

#elif button == 5:
#   from pathlib import Path
#path = Path("C:\Users\admin\Desktop\coding\Python\projectile")
#print(path.parent)






def Directory_Menu():
    print("""
    Press 1 to rename directory
    Press 2 to print number of files
    Press 3 to print number of directories 
    Press 4 to list content of the directory
    Press 5 to add file to this directory
    Press 6 to add new directory to this directory
    Press 7 to create new directory""" )

# button = int(input())
def workWithNames(button):
    if button == 0:
        exit()
    elif button == 1:
        Directory1=input("Old name:") + ".txt"
        Directory2=input("New name:") + ".txt"
        os.rename(Directory1,Directory2)
        print("The Directory was renamed")


        
    elif button == 2:
        count = 0
        for f in os.listdir():
                File=os.path.join(f)
                if os.path.isdir(File):
                    count+=1
        print("cnt of directory is: ",count)

    elif button == 3:
        count = 0
        for f in os.listdir():
                Dir=os.path.join(f)
                if os.path.isdir(Dir):
                    count+=1
        print("cnt of directory is: ",count)

    elif button == 4:
        print(os.listdir())


    elif button == 5:
        file = open(r"C:\Users\admin\Desktop\coding\Python\projectile\1.txt", "w")
        file.close()

    elif button == 6:
        os.mkdir(r"C:\Users\admin\Desktop\coding\Python\projectile")


    elif button == 7:
        Directory_name = input("Name of new directory: ")
        os.mkdir(Directory_name)
        print("Directory is created ")




FILE_MANAGER = True
while FILE_MANAGER:
    name = str(input())
    MENU(name)
    button = int(input())
    if button == 0:
        print("programm stopped")
        FILE_MANAGER=False 
    elif button == 1:
        print("YOU WORK WITH FILE")
        File_Menu()
        button = int(input())
        workWithFile(button)
    elif button == 2:
        print("YOU WORK WITH DIRECTORY")
        Directory_Menu()
        button = int(input())
        workWithNames(button)
