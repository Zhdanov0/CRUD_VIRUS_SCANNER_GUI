from trie import Trie
from tkinter import ttk
import datetime
import psycopg2
import pyperclip
import os
import tkinter as tk
  
con = psycopg2.connect(
      database="project", 
      user="postgres", 
      password="", 
      host="127.0.0.1"
    )

cur = con.cursor()

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


def open_show_gui():

    show_gui = tk.Tk()
    show_gui.title('Show db')       
    show_gui.geometry('500x600+400+200') 
    show_gui.resizable(False, False)
    show_gui.config(bg='black')

    cur.execute("execute select_all_order")

    res_lbl1 = tk.Label(show_gui, text = 'Show database', bg='black', fg='silver', font=('Impact', 30))
    res_lbl1.pack()

    text_frame = tk.Frame(show_gui)
    text_frame.pack()

    text = tk.Text(text_frame, width=60, height=30, bg='silver')
    text.pack(side=tk.LEFT)  
    scroll = tk.Scrollbar(text_frame, command=text.yview, bg='black')
    scroll.pack(side=tk.LEFT, fill=tk.Y)
    text.config(yscrollcommand=scroll.set)

    btn0 = tk.Button(show_gui, text='Menu', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command=lambda: show_gui.destroy())
    btn0.place(x=200, y=553)
    
    i = 1
    for row in cur.fetchall():
        text.insert('%d.0' % (i), row[0]+'\t\t')
        text.insert('%d.%d' % (i, len(row[0]) + 10), row[1]+'\n')
        i += 1
   
def open_scan_gui():

    def scanning():

        #making cache here
        
        cur.execute('execute select_all')
        rows = cur.fetchall()
          
        cache = {}
        
        for row in rows:
        
            trie = cache.setdefault(row[0], Trie(row[0]))
            trie.insert(row[1])
                     
        #end; cache = { extension : Trie }
        
        path = ent1_sc.get()
        
        def scan(path):

            def defuse():

                for line in infected_files:

                    tmp_path = line[1] + '\\' + line[0]
                    os.remove(tmp_path)

                    res_lbl2 = tk.Label(scan_result, text = 'Infected files:\t0', bg='black', fg='silver', font=('Arial', 12))
                    res_lbl2.place(x=75, y=28)

                    text.delete(1.0, 'end')
                    
                
            if not os.path.exists(path):      
                err_lbl = tk.Label(scan_gui, text = 'DIRECTORY DOES NOT EXIST!!!', bg='black', fg='red', font=('Arial', 12))
                err_lbl.grid(row=4, column=0)
                return

            start_time = datetime.datetime.now()

            count_all = 0
            infected_files = list()
            error_files = list()
            os.chdir(path)       
            home = os.getcwd()
                   
            for (root, subd, files) in os.walk('.'):
                
                os.chdir(root)
                if files:
                    
                    for file_name in files:
                        count_all += 1
        
                        for c in range(len(file_name) - 1, 0, -1):      #get extension
                                if file_name[c] == '.':
                                    break
                        extension = file_name[c+1:]
        
                        try:
        
                            if cache.get(extension):                    
                                f = open(file_name, 'r')
        
                                for line in f.readlines():             
                                    if cache[extension].search(line):   
                                        infected_files.append((file_name, path+root[1:]))     
                        except:       
                            error_files.append(file_name)
        
                os.chdir(home)
            
            scan_time = datetime.datetime.now() - start_time

            scan_result = tk.Toplevel(win)
            scan_result.title('Results')
            scan_result.geometry('997x300+400+200') 
            scan_result.resizable(False, False)
            scan_result.config(bg='black')

            res_lbl1 = tk.Label(scan_result, text = 'Checked objects:\t%s' % (count_all), bg='black', fg='silver', font=('Arial', 12))
            res_lbl2 = tk.Label(scan_result, text = 'Infected files:\t%s' % (len(infected_files)), bg='black', fg='red', font=('Arial', 12))
            res_lbl3 = tk.Label(scan_result, text = 'Analysis errors:\t%s' % (len(error_files)), bg='black', fg='red', font=('Arial', 12))
            res_lbl4 = tk.Label(scan_result, text = 'Time:\t\t%s' % (scan_time), bg='black', fg='silver', font=('Arial', 12))
            
            heal_btn = tk.Button(scan_result, text='Defuse', bg='silver', fg='black',
                      font=('Arial', 12), width=10, command = defuse)

            heal_btn.place(x=700, y=35)

            res_lbl1.place(x=75, y=3)
            res_lbl2.place(x=75, y=28)
            res_lbl3.place(x=75, y=53)
            res_lbl4.place(x=75, y=78)

            files = tk.Frame(scan_result, bg='white')
            files.pack(side=tk.BOTTOM)

            text = tk.Text(files, width=122, height=12, bg='silver')
            text.pack(side=tk.LEFT)
             
            scroll = tk.Scrollbar(files, command=text.yview, bg='black')
            scroll.pack(side=tk.LEFT, fill=tk.Y)
             
            text.config(yscrollcommand=scroll.set)

            for i in range(len(infected_files)):             
                text.insert('%d.0' % (i+1), infected_files[i][0] + ' '*(50-len(infected_files[i][0])))
                text.insert('%d.40' % (i+1), infected_files[i][1] + '\n')
            
        scan(path)


    scan_gui = tk.Toplevel(win)
    scan_gui.title('Scanning')
    scan_gui.geometry('500x600+400+200') 
    scan_gui.resizable(False, False)
    scan_gui.config(bg='black')

    label1 = tk.Label(scan_gui, text = 'Directory', bg='black', fg='silver', font=('Arial', 14))
    ent1_sc = tk.Entry(scan_gui, width=30)

    label0 = tk.Label(scan_gui, text='Scanning', bg='black', fg='silver',
                      font=('Impact', 30))
    btn0 = tk.Button(scan_gui, text='Menu', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command=lambda: scan_gui.destroy())
    btn1 = tk.Button(scan_gui, text='Start', bg='black', fg='silver',
                      font=('Arial', 12), width=10, command = scanning)
    btn2 = tk.Button(scan_gui, text='Paste', bg='black', fg='silver',
                      font=('Arial', 12), width=5, command = lambda: ent1_sc.insert(0, pyperclip.paste()))

    label0.grid(row=0, column=0)
    label1.grid(row=1, column=0, stick='w', padx=45)
    ent1_sc.grid(row=1, column=0)
    btn1.grid(row=2, column=0)
    btn0.grid(row=3, column=0)
    btn2.grid(row=1, column=0, stick='e', padx = 55)

    scan_gui.grid_columnconfigure(0, minsize=500)
    scan_gui.grid_rowconfigure(0, minsize=100)
    scan_gui.grid_rowconfigure(1, minsize=50)
    scan_gui.grid_rowconfigure(2, minsize=50)
    scan_gui.grid_rowconfigure(3, minsize=50)
    scan_gui.grid_rowconfigure(4, minsize=50)

def open_add_gui():

    def addLine():

        extension = ent1_line.get()
        line = ent2_line.get()

        if not extension or not line:
            error_lbl = tk.Label(add_gui, text = 'Empty input fields!!!', bg='black', fg='red', font=('Arial', 14))
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

        


    add_gui = tk.Toplevel(win)
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

def open_edit_gui():

    def check_number():

        try:
            index = int(edit_ent.get())
        except:
            error_lbl = tk.Label(edit_gui, text = 'Invalid format!!!',anchor='w', bg='black', fg='red', font=('Arial', 14), width=20)
            error_lbl.place(x=20, y=97)
            return False
        else:
            if index > (i_bd_index - 1) or index < 1:
                error_lbl = tk.Label(edit_gui, text = 'Invalid number!!!', bg='black', fg='red', font=('Arial', 14))
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

label0 = tk.Label(win, text='Menu', bg='black', fg='silver',
                  font=('Impact', 30))

btn0 = tk.Button(win, text='Scanning', bg='black', fg='silver', font=('Arial', 14), width=15, command=open_scan_gui)
btn1 = tk.Button(win, text='Add line', bg='black', fg='silver', font=('Arial', 14), width=15, command=open_add_gui)
btn2 = tk.Button(win, text='Show database', bg='black', fg='silver', font=('Arial', 14), width=15, command=open_show_gui)
btn3 = tk.Button(win, text='Exit', bg='black', fg='silver', font=('Arial', 14), width=15, command=exit)
btn4 = tk.Button(win, text='Edit database', bg='black', fg='silver', font=('Arial', 14), width=15, command=open_edit_gui)

label0.grid(row=0, column=0)
btn0.grid(row=1, column=0)
btn1.grid(row=2, column=0)
btn2.grid(row=4, column=0)
btn4.grid(row=3, column=0)
btn3.grid(row=5, column=0)

win.grid_columnconfigure(0, minsize=500)
win.grid_rowconfigure(0, minsize=100)
win.grid_rowconfigure(1, minsize=50)
win.grid_rowconfigure(2, minsize=50)
win.grid_rowconfigure(3, minsize=50)
win.grid_rowconfigure(4, minsize=50)
win.grid_rowconfigure(5, minsize=50)

win.mainloop()
                