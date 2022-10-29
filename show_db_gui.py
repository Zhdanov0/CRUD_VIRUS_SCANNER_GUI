import tkinter as tk
from db_connection import *

def open_show_gui():

    show_gui = tk.Tk()
    show_gui.title('Show db')       
    show_gui.geometry('500x600+400+200') 
    show_gui.resizable(False, False)
    show_gui.config(bg='black')

    cur.execute("execute select_all_order")

    show_res_lbl1 = tk.Label(show_gui, text = 'Show database', bg='black', fg='silver', font=('Impact', 30))
    show_res_lbl1.pack()

    show_text_frame = tk.Frame(show_gui)
    show_text_frame.pack()

    show_text = tk.Text(show_text_frame, width=60, height=30, bg='silver')
    show_text.pack(side=tk.LEFT)  
    show_scroll = tk.Scrollbar(show_text_frame, command=show_text.yview, bg='black')
    show_scroll.pack(side=tk.LEFT, fill=tk.Y)
    show_text.config(yscrollcommand=show_scroll.set)

    show_btn0 = tk.Button(show_gui, text='Menu', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command=lambda: show_gui.destroy())
    show_btn0.place(x=200, y=553)
    
    i = 1
    for row in cur.fetchall():
        show_text.insert('%d.0' % (i), row[0]+'\t\t')
        show_text.insert('%d.%d' % (i, len(row[0]) + 10), row[1]+'\n')
        i += 1
