import tkinter as tk
from db_connection import *

def open_edit_gui():

    def check_number():

        try:
            index = int(edit_ent.get())
        except:
            error_lbl = tk.Label(edit_gui, text = 'Invalid format!!!', anchor='nw', bg='black', fg='red', font=('Arial', 14), width=30,
                                 height=5)
            error_lbl.place(x=20, y=97)
            return False
        else:
            if index > (i_bd_index - 1) or index < 1:
                error_lbl = tk.Label(edit_gui, text = 'Invalid number!!!', anchor='nw', bg='black', fg='red', font=('Arial', 14), width=30,
                                     height=5)
                error_lbl.place(x=20, y=97)
                return False
        return True

    
    def edit():

        def update_line():

            extension_new = edit_func_ent1.get()
            line_new =  edit_func_ent2.get()

            if not line_new or not extension_new:
                error_lbl = tk.Label(edit_gui, text = 'Empty input fields!!!', bg='black', fg='red', font=('Arial', 14))
                error_lbl.place(x=140, y=220)
                return

            cur.execute("execute update ('%s', '%s', '%s', '%s')" 
                        % (extension_new, line_new, extension_old, line_old))
            con.commit()

            edit_gui.destroy()
            open_edit_gui()

        if check_number():

            index = int(edit_ent.get())
            extension_old = rows[index-1][0]
            line_old = rows[index-1][1]

            edit_func_label1 = tk.Label(edit_gui, text = 'Extension',anchor='w', bg='black', fg='silver', font=('Arial', 14), width=20)
            edit_func_label2 = tk.Label(edit_gui, text = 'Line', bg='black', fg='silver', font=('Arial', 14))
            edit_func_ent1 = tk.Entry(edit_gui, width=19)
            edit_func_ent2 = tk.Entry(edit_gui, width=19)
            edit_func_btn1 = tk.Button(edit_gui, text='Accept', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command = update_line)

            edit_func_ent1.insert(0, extension_old)
            edit_func_ent2.insert(0, line_old)

            edit_func_label1.place(x=20, y=98)
            edit_func_label2.place(x=20, y=128)
            edit_func_ent1.place(x=165, y=103)
            edit_func_ent2.place(x=165, y=133)
            edit_func_btn1.place(x=175, y=163)


    def delete():

        if check_number():

            index = int(edit_ent.get())
            extension = rows[index-1][0]
            line = rows[index-1][1]

            cur.execute("execute delete ('%s', '%s')" % (extension, line))
            con.commit()
            edit_gui.destroy()
            open_edit_gui()

    cur.execute('execute select_all_order')
    rows = cur.fetchall()

    edit_gui = tk.Tk()
    edit_gui.title('edit db')       
    edit_gui.geometry('500x600+400+200') 
    edit_gui.resizable(False, False)
    edit_gui.config(bg='black')

    edit_lbl1 = tk.Label(edit_gui, text = 'Edit database', bg='black', fg='silver', font=('Impact', 30))
    edit_lbl2 = tk.Label(edit_gui, text = 'Enter number', bg='black', fg='silver', font=('Arial', 14))
    edit_ent = tk.Entry(edit_gui, width=5)
    edit_btn0 = tk.Button(edit_gui, text='Edit', bg='black', fg='silver',
                      font=('Arial', 12), width=5, command=edit)
    edit_btn1 = tk.Button(edit_gui, text='Delete', bg='black', fg='silver',
                      font=('Arial', 12), width=5, command=delete)

    edit_lbl1.pack()
    edit_lbl2.place(x=20, y=65)
    edit_ent.place(x=165, y=70)
    edit_btn0.place(x=227, y=65)
    edit_btn1.place(x=305, y=65)

    text_frame = tk.Frame(edit_gui)
    text_frame.pack(side=tk.BOTTOM)

    text = tk.Text(text_frame, width=60, height=20, bg='silver')
    text.pack(side=tk.LEFT)
    scroll = tk.Scrollbar(text_frame, command=text.yview, bg='black')
    scroll.pack(side=tk.LEFT, fill=tk.Y)
    text.config(yscrollcommand=scroll.set)

    i_bd_index = 1
    for row in rows:
        text.insert('%d.0' % (i_bd_index), str(i_bd_index)+'\t\t')
        text.insert('%d.10' % (i_bd_index), row[0]+'\t\t')
        text.insert('%d.%d' % (i_bd_index, len(row[0]) + 10), row[1]+'\n')
        i_bd_index += 1
