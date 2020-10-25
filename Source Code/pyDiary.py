import pymysql
import datetime
from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import getpass


def getter():
    getter.x = 1

def addlog(mycursor,usrid,conn):
    mycursor.execute("USE " + usrid)

    query = "UPDATE profile SET lastlog = %s ;"
    value = (str(datetime.datetime.now()))
    mycursor.execute(query, value)
    conn.commit()
    print(">Updated log")


def lastlogin(cursor,usrid):
    cursor.execute("use "+usrid)
    cursor.execute("select lastlog from profile ")
    ll = cursor.fetchone()
    return str(ll[0])

def fetchpass(cursor,usrid):
    cursor.execute("use " + usrid)
    cursor.execute("select password from profile ")
    ll = cursor.fetchone()
    return str(ll[0])



def connectDb():
    try:
        conn = pymysql.connect(
        host='localhost',
        user='user',
        passwd='12345',
        )

        print(">DB Connected")
        return conn
    except Exception :
        print(">Database not connected")


def checkUser(mycursor,usrid):

    i = 0
    l = []
    for x in mycursor:
        l.append(str(x).translate({ord(','): None, ord('('): None, ord(')'): None,
                                   ord("'"): None}))  # this removes the circular bracktes and comma from the sql output

    if (l.__contains__(usrid)):
        return True
    else:
        return False

def createTable(mycursor,notetitle):
    sql_command = """
                CREATE TABLE %s ( 
                password VARCHAR(20)
                );
                """ % notetitle

    mycursor.execute(sql_command)


def createUser(usrid, passwd , mycursor,conn):
    if (usrid != "n"):
        print("\n>Setting up your pyDiary profile.")
        print(">Creating a db..")
        query = "CREATE DATABASE "+usrid
        mycursor.execute(query)

        mycursor.execute("USE "+usrid )

        sql_command = """CREATE TABLE profile (username VARCHAR(30),password VARCHAR(30), lastlog VARCHAR(500) );"""

        mycursor.execute(sql_command)


        mycursor.execute("USE "+usrid)

        query = """INSERT INTO profile (username,password,lastlog) VALUES (%s,%s,%s);"""
        value = (usrid,passwd,str(datetime.datetime.now()))
        mycursor.execute(query,value)
        conn.commit()


        print("> pyDiary ready!")
        print("=============================( pyDiary Session : "+str(datetime.date.today())+" || UserID : "+usrid+" )=================>")

        print(">Welcome to pyDiary : Your secrets, encrypted.")
        HomePage(conn,mycursor,usrid)
        #try:


        # except Exception as e:
        #     print("Error initializing .... History feature will not work untill next restart.")
        #     print(e)




def NewNote(conn,title,mycursor,usrid):

    ################################################### MAKE TABLE NOTE
    mycursor.execute("USE " + usrid)

    sql_command = """CREATE TABLE %s ( log VARCHAR(500),Note VARCHAR(999999999));""" % title

    mycursor.execute(sql_command)

    ################################################### MAKE TABLE NOTE

    ################################### Window for writing
    window = tk.Tk()

    window.resizable(False,True)

    window.title(title+" @"+usrid)
    width =750
    height = 500
    window.geometry(str(width)+'x'+str(height))

    txt = scrolledtext.ScrolledText(window, width=70, height=40)
    txt.insert(INSERT,"Here you go...")

    tk.Label(window,
              text="pyDiary.",
              font=("Times New Roman", 15),
              background='green',
              foreground="white").pack(padx=0, pady=5,side =tk.TOP)
    tk.Label(window,
             text=title,
             font=("Times New Roman", 12),
             background='white',
             foreground="green").pack(padx=0, pady=5, side=tk.TOP)

    def commit(text,comm,cursor,usrid):

        try:
            mycursor.execute("USE " + usrid)

            query = "INSERT INTO " + str(title) + " (log,Note) VALUES (%s,%s);"
            value = (str(datetime.datetime.now()), text)
            mycursor.execute(query, value)
            conn.commit()
            if messagebox.showinfo("Notes Saved", "Your notes were successfully saved!"):
                print(">Notes Saved and Closed.")
                window.destroy()
        except Exception:
            messagebox.showwarning("Notes Not Saved", "Your notes were not saved due to some error !")







    btnSave = Button(window, text="Save & Exit",fg="white",bg="green",width = 20, height = 2,command = lambda :commit(str(txt.get('1.0',END)),conn,mycursor,usrid))

    def word_count(str):
        counts = dict()
        words = str.split()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts



    def clicked(text):
        words = len(text.split())
        wc = word_count(text)
        messagebox.showinfo("Metrics","Word Count :\n\n"+str(wc)+"\n\nTotal Words :"+str(words))

    btnClose = Button(window, text="Metrics",fg= "green",bg="WHITE", width=20, height=2,command = lambda :clicked(str(txt.get('1.0',END))))

    # btnSave.grid(column=2, row=0)
    # btnClose.grid(column=2, row=1)
    txt.pack(padx=5, pady=10, side=tk.LEFT)
    btnSave.pack(padx=5, pady=20, side=tk.BOTTOM)
    btnClose.pack(padx=5, pady=5, side=tk.BOTTOM)

    btnClose.pack()


    window.mainloop()
    print("\n========================<Session closed>=================>")

    choose(conn,mycursor,usrid)




def OpenNote(conn , mycursor, usrid, note_data, title):
    window = tk.Tk()

    window.resizable(False, True)

    window.title(title + " @" + usrid)
    width = 750
    height = 500
    window.geometry(str(width) + 'x' + str(height))

    txt = scrolledtext.ScrolledText(window, width=70, height=40)
    note_data = str(note_data).translate({ord(','): None, ord('('): None, ord(')'): None, ord("'"): None})
    txt.insert(INSERT, str(note_data).replace("\\n"," \n "))

    tk.Label(window,
             text="pyDiary.",
             font=("Times New Roman", 15),
             background='green',
             foreground="white").pack(padx=0, pady=5, side=tk.TOP)
    tk.Label(window,
             text=title,
             font=("Times New Roman", 12),
             background='white',
             foreground="green").pack(padx=0, pady=5, side=tk.TOP)


    def commit(text, conn, mycursor, usrid):

        try:
            mycursor.execute("USE " + usrid)

            query = "UPDATE " + title + " SET log = %s, Note = %s ;"
            value = (str(datetime.datetime.now()), text)
            mycursor.execute(query, value)
            conn.commit()


            print(">Note's Progress Saved.")



        except Exception as e:
            messagebox.showwarning("Notes Not Saved", "Your notes were not saved due to some error !\n "+str(e))

    btnSave = Button(window, text="Save progress", fg="white", bg="green", width=20, height=2,
                     command=lambda: commit(str(txt.get('1.0', END)), conn, mycursor, usrid))


    def clicked(text):
        try:
            mycursor.execute("USE "+usrid )

            query = "UPDATE "+title+" SET log = %s, Note = %s ;"
            value = (str(datetime.datetime.now()), text)
            mycursor.execute(query, value)
            conn.commit()
            if messagebox.showinfo("Notes Saved", "Your note's progress have been saved!"):
                print(">Note's Progress Saved .")
            window.destroy()





        except Exception as e:
            messagebox.showwarning("Notes Not Saved", "Your notes were not saved due to some error !\n "+str(e))



    btnClose = Button(window, text="Save & Exit", fg="green", bg="WHITE", width=20, height=2,
                      command=lambda :clicked(str(txt.get('1.0',END))))

    # btnSave.grid(column=2, row=0)
    # btnClose.grid(column=2, row=1)
    txt.pack(padx=5, pady=10, side=tk.LEFT)
    btnSave.pack(padx=5, pady=20, side=tk.BOTTOM)
    btnClose.pack(padx=5, pady=5, side=tk.BOTTOM)

    btnClose.pack()

    window.mainloop()
    print("\n========================<Session closed>=================>")

    choose(conn,mycursor,usrid)

def choose(conn,mycursor,usrid):
    mycursor.execute("use " + usrid)
    print("\n>What to do today ?")
    print(""
          "\n1.NEW NOTE\n"
          "2.OPEN NOTE\n"
          "3.DELETE NOTE\n"
          "4.LOG OUT\n"
          )
    inp = input(">Select : ")

    if (int(inp) == 1):
        title = input(">Note Title : ")
        title = "`" + title + "`"
        NewNote(conn, title, mycursor, usrid)

    if (int(inp) == 2):
        print("\n>Open Notes Selected.")
        mycursor.execute("use " + usrid)
        mycursor.execute("show tables;")
        print("\n>Notes Library:\n")
        n = 1
        l = []
        for i in mycursor:
            tbname = str(i).translate({ord(','): None, ord('('): None, ord(')'): None, ord("'"): None})
            if tbname != "profile":
                print(n, "-> ", tbname)
                if tbname.__contains__(" "):
                    tbname = '`' + tbname + '`'
                    l.append(tbname)
                else:
                    l.append(tbname)
                n = n + 1
        if (len(l)==0):
            print("Note Library Empty, add some notes.")
            print("\n========================<Session closed>=================>")
            choose(conn,mycursor,usrid)
        else:
            inp = input("\n\nSelect Note (By S.No): ")
            note = l[int(inp) - 1]

            mycursor.execute("select Note from " + note + ";")
            note_data = mycursor.fetchone()
            OpenNote(conn, mycursor, usrid, note_data, note)


    if (int(inp)==3):
         print("\n>Delete Notes Selected.")
         mycursor.execute("use " + usrid)
         mycursor.execute("show tables;")
         print("\n>Notes Library:\n")
         n = 1
         l = []
         for i in mycursor:
             tbname = str(i).translate({ord(','): None, ord('('): None, ord(')'): None, ord("'"): None})
             if tbname != "profile":
                 print(n, "-> ", tbname)
                 if tbname.__contains__(" "):
                     tbname = '`' + tbname + '`'
                     l.append(tbname)
                 else:
                     l.append(tbname)
                 n = n + 1

         inp = input("\n\nSelect Note (By S.No): ")
         note = l[int(inp) - 1]
         while(True):
             confirm = input("Write '" + note + "' to confirm : ")

             if (confirm == note):
                 query = "DROP TABLE %s;" % note
                 mycursor.execute(query)
                 print("Deleted Note :"+note)
                 print("\n========================<Session closed>=================>")
                 choose(conn,mycursor,usrid)
    if int(inp) == 4:
        print(">Logging out.")
        auth(mycursor,conn)



def HomePage(conn,mycursor,usrid):
    print("\n========================<Profile>==============")
    print("HELLO,"+str(usrid).upper()+"!")
    ll = lastlogin(mycursor,usrid)
    print("Last Login : ",ll)
    print("=========================<Profile>===============\n")
    choose(conn,mycursor,usrid)




def auth(mycusor,conn):
    print("\n========================<pyDiary Auth>======================")
    while(True):
        usrId = input("\nEnter UserID or type 'n' for new user :")

        if usrId != 'n':
            mycusor.execute("show databases;")
            if (checkUser(mycusor,usrId)):
                pass_in = getpass.getpass(prompt="Enter your Password : ")
                mycusor.execute("use "+usrId)
                pass_db =fetchpass(mycusor,usrId)

                if (pass_in == pass_db):
                    print(">Login Successful , Welcome.")
                    print(">pyDiary ready!")
                    print("\n=============================( pyDiary v1.0a Session : " + str(
                        datetime.date.today()) + " || UserID : " + usrId + " )=================>")

                    print(">Welcome to pyDiary : Your secrets, encrypted.")
                    addlog(mycusor,usrId,conn)

                    HomePage(conn, mycusor, usrId)
                else:
                    print("Profile Locked! , you can't proceed !")
                    break



            else:
                n = input(">UserID not found , Make new account(y/n) : ")
                if (n=="y"):
                    continue
                else :
                    print("OK, closing pyDiary.")
                    quit()
                    break



        else:
            userId = input("Enter your new UserID (Example: user123) :")
            passwd = getpass.getpass(prompt="Enter your new Password : ")
            userId = '`'+userId+'`'
            print(usrId)
            createUser(userId,passwd,mycusor,conn)








def Dinit():

    try:
        print(">Enter SQL server password (default is '' , just press enter ) :")
        db = getpass.getpass()
        conn = pymysql.connect("localhost", "root", str(db))
        print(">DB Connected")
        cursor = conn.cursor()
        cursor.execute("show databases;")
        auth(cursor, conn)

    except Exception as e:
        print("ERROR, DB NOT CONNECTED : RUN THE SERVER  : "+str(e))








Dinit()
#HomePage("efs","aprit")
#OpenNote()