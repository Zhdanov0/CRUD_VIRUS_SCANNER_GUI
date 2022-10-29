from db_connection import *
import tkinter as tk
import scan_gui
import show_db_gui
import add_gui
import edit_gui
  
cur.execute('''CREATE TABLE IF NOT EXISTS viruses (
                extension VARCHAR(50) NOT NULL,
                line VARCHAR(50) NOT NULL);''')

cur.execute('''PREPARE select_all_order AS
               SELECT * FROM viruses ORDER BY extension;''')

cur.execute('''PREPARE select_all AS
               SELECT * FROM viruses;''')

cur.execute('''PREPARE select_all_where AS 
               SELECT extension, line FROM viruses WHERE extension = $1 AND line = $2;''')

cur.execute('''PREPARE insert AS 
               INSERT INTO viruses (extension, line) VALUES ($1, $2);''')

cur.execute('''PREPARE update AS 
               UPDATE viruses SET extension = $1, line = $2 WHERE extension = $3 AND line = $4;''')

cur.execute('''PREPARE delete AS
               DELETE FROM viruses WHERE extension = $1 and line = $2;''')

def exit():
    con.close()
    win.destroy()

win = tk.Tk()
win.title('Virus scanner')       
win.geometry('500x600+400+200') 
win.resizable(False, False)
win.config(bg='black')

photo = tk.PhotoImage(file='fun.png')
win.iconphoto(False, photo)

menu_label0 = tk.Label(win, text='Menu', bg='black', fg='silver',
                  font=('Impact', 30))

menu_btn0 = tk.Button(win, text='Scanning', bg='black', fg='silver', font=('Arial', 14), width=15, command=scan_gui.open_scan_gui)
menu_btn1 = tk.Button(win, text='Add line', bg='black', fg='silver', font=('Arial', 14), width=15, command=add_gui.open_add_gui)
menu_btn2 = tk.Button(win, text='Show database', bg='black', fg='silver', font=('Arial', 14), width=15, command=show_db_gui.open_show_gui)
menu_btn3 = tk.Button(win, text='Exit', bg='black', fg='silver', font=('Arial', 14), width=15, command=exit)
menu_btn4 = tk.Button(win, text='Edit database', bg='black', fg='silver', font=('Arial', 14), width=15, command=edit_gui.open_edit_gui)

menu_label0.grid(row=0, column=0)
menu_btn0.grid(row=1, column=0)
menu_btn1.grid(row=2, column=0)
menu_btn2.grid(row=4, column=0)
menu_btn4.grid(row=3, column=0)
menu_btn3.grid(row=5, column=0)

win.grid_columnconfigure(0, minsize=500)
win.grid_rowconfigure(0, minsize=100)
win.grid_rowconfigure(1, minsize=50)
win.grid_rowconfigure(2, minsize=50)
win.grid_rowconfigure(3, minsize=50)
win.grid_rowconfigure(4, minsize=50)
win.grid_rowconfigure(5, minsize=50)

win.mainloop()
                