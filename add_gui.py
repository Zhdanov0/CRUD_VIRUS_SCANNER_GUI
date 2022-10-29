import tkinter as tk
from db_connection import *

def open_add_gui():

    def addLine():

        extension = ent1_line.get()
        line = ent2_line.get()

        if not extension or not line:
            error_lbl = tk.Label(add_gui, text = 'Empty input fields!!!', bg='black', fg='red', font=('Arial', 14), width = 20)
            error_lbl.grid(row=5, column=0)
            return

        cur.execute("execute select_all_where ('%s', '%s')" % (extension, line))
        rows = cur.fetchall()
        
        if rows:
            error_lbl = tk.Label(add_gui, text = 'This line is already in db!!!', bg='black', fg='red', font=('Arial', 14))
            error_lbl.grid(row=5, column=0)
        else:
            cur.execute("execute insert ('%s', '%s')" % (extension, line))
            con.commit()

            tmp_lbl = tk.Label(add_gui, text = 'Successfully added', bg='black', fg='gold', font=('Arial', 14), width=30)
            tmp_lbl.grid(row=5, column=0)

            ent1_line.delete(0, 'end')
            ent2_line.delete(0, 'end')

        


    add_gui = tk.Tk()
    add_gui.title('Add line')
    add_gui.geometry('500x600+400+200') 
    add_gui.resizable(False, False)
    add_gui.config(bg='black')

    label0 = tk.Label(add_gui, text='Add line', bg='black', fg='silver',
                      font=('Impact', 30))
    btn0 = tk.Button(add_gui, text='Menu', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command=lambda: add_gui.destroy())
    btn1 = tk.Button(add_gui, text='Add', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command=addLine)

    label1 = tk.Label(add_gui, text = 'Extension', bg='black', fg='silver', font=('Arial', 14))
    ent1_line = tk.Entry(add_gui)
    ent1_line.insert(0, 'txt')
    label2 = tk.Label(add_gui, text = 'Line', bg='black', fg='silver', font=('Arial', 14))
    ent2_line = tk.Entry(add_gui)

    label0.grid(row=0, column=0)
    label1.grid(row=1, column=0, stick='w', padx=60)
    ent1_line.grid(row=1, column=0)
    label2.grid(row=2, column=0, stick='w', padx=60)
    ent2_line.grid(row=2, column=0)
    btn1.grid(row=3, column=0)
    btn0.grid(row=4, column=0)

    add_gui.grid_columnconfigure(0, minsize=500)
    add_gui.grid_rowconfigure(0, minsize=100)
    add_gui.grid_rowconfigure(1, minsize=50)
    add_gui.grid_rowconfigure(2, minsize=50)
    add_gui.grid_rowconfigure(3, minsize=50)
    add_gui.grid_rowconfigure(4, minsize=50)
    add_gui.grid_rowconfigure(5, minsize=50)
