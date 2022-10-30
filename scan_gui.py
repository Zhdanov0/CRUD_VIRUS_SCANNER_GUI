from trie import Trie
from db_connection import *
import pyperclip
import datetime
import os
import tkinter as tk

def open_scan_gui() -> None:

    def scanning() -> None:

        #making cache here
        
        cur.execute('execute select_all')
        rows = cur.fetchall()
          
        cache = {}
        
        for row in rows:
        
            trie = cache.setdefault(row[0], Trie(row[0]))
            trie.insert(row[1])
                     
        #end; cache = { extension : Trie }
        
        path = scan_ent1_sc.get()
        
        def scan(path: str) -> None:

            def defuse() -> None:

                for line in infected_files:

                    tmp_path = line[1] + '\\' + line[0]
                    os.remove(tmp_path)

                    res_lbl2 = tk.Label(scan_result, text = 'Infected files:\t0', bg='black', fg='silver', font=('Arial', 12))
                    res_lbl2.place(x=75, y=28)

                    res_text.delete(1.0, 'end')
                    
                
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

            scan_result = tk.Tk()
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

            res_files = tk.Frame(scan_result, bg='white')
            res_files.pack(side=tk.BOTTOM)

            res_text = tk.Text(res_files, width=122, height=12, bg='silver')
            res_text.pack(side=tk.LEFT)
             
            res_scroll = tk.Scrollbar(res_files, command=res_text.yview, bg='black')
            res_scroll.pack(side=tk.LEFT, fill=tk.Y)
             
            res_text.config(yscrollcommand=res_scroll.set)

            for i in range(len(infected_files)):             
                res_text.insert('%d.0' % (i+1), infected_files[i][0] + ' '*(50-len(infected_files[i][0])))
                res_text.insert('%d.40' % (i+1), infected_files[i][1] + '\n')
            
        scan(path)


    scan_gui = tk.Tk()
    scan_gui.title('Scanning')
    scan_gui.geometry('500x600+400+200') 
    scan_gui.resizable(False, False)
    scan_gui.config(bg='black')

    scan_label1 = tk.Label(scan_gui, text = 'Directory', bg='black', fg='silver', font=('Arial', 14))
    scan_ent1_sc = tk.Entry(scan_gui, width=30)

    scan_label0 = tk.Label(scan_gui, text='Scanning', bg='black', fg='silver',
                           font=('Impact', 30))
    scan_btn0 = tk.Button(scan_gui, text='Menu', bg='black', fg='silver',
                          font=('Arial', 12), width=10, command=lambda: scan_gui.destroy())
    scan_btn1 = tk.Button(scan_gui, text='Start', bg='black', fg='silver',
                          font=('Arial', 12), width=10, command = scanning)
    scan_btn2 = tk.Button(scan_gui, text='Paste', bg='black', fg='silver',
                          font=('Arial', 12), width=5, command = lambda: scan_ent1_sc.insert(0, pyperclip.paste()))

    scan_label0.grid(row=0, column=0)
    scan_label1.grid(row=1, column=0, stick='w', padx=45)
    scan_ent1_sc.grid(row=1, column=0)
    scan_btn1.grid(row=2, column=0)
    scan_btn0.grid(row=3, column=0)
    scan_btn2.grid(row=1, column=0, stick='e', padx = 55)

    scan_gui.grid_columnconfigure(0, minsize=500)
    scan_gui.grid_rowconfigure(0, minsize=100)
    scan_gui.grid_rowconfigure(1, minsize=50)
    scan_gui.grid_rowconfigure(2, minsize=50)
    scan_gui.grid_rowconfigure(3, minsize=50)
    scan_gui.grid_rowconfigure(4, minsize=50)

