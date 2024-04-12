from distutils.cmd import Command
from msilib.schema import ComboBox
import tkinter as tk
from tkinter import Entry, ttk
from tkinter import filedialog
import Time
from tkinter import messagebox
import os
from ttkthemes import ThemedStyle
import Graph
import ExceltoXML
import threading as th

k = None
def on_entry_click(event):
    current_text = trip_entry.get()

    if current_text == "Enter Trip ID":
        trip_entry.delete(0, tk.END)
        trip_entry.config(fg='black')
    elif current_text == '':
        trip_entry.insert(0, "Enter Trip ID")
        trip_entry.config(fg='grey')


def on_entry_ser(event):
    current_text = ser_entry.get()
    if current_text == "Service":
        ser_entry.delete(0, tk.END)
        ser_entry.config(fg='black')
    elif current_text == '':
        ser_entry.insert(0, "Service")
        ser_entry.config(fg='grey')

def on_entry_trip(event):
    current_text = tripno_entry.get()
    if current_text == "No of Trips":
        tripno_entry.delete(0, tk.END)
        tripno_entry.config(fg='black')
    elif current_text == '':
        tripno_entry.insert(0, "No of Trips")
        tripno_entry.config(fg='grey')

def headway_click(event):
    headway_entry.config(fg='black')

def on_combobox_select(event):
    selected_item = combobox.get()
    label_choice.config(text=f"Selected: {selected_item}")

def on_combobox_modes(event):
    selected_item = combobox_1.get()
    label_mode.config(text=f"Selected: {selected_item}")

def validate_time_input(P):
    if P == "" or P.count(":") > 2:
        return True
    parts = P.split(":")
    if len(parts) > 0:
        if not parts[0].isdigit() or int(parts[0]) > 23:
            messagebox.showinfo('ERROR','Enter valid Time')
            return False
    if len(parts) > 1:
        if not parts[1].isdigit() or int(parts[1]) > 59:
            return False
    if len(parts) > 2:
        if not parts[2].isdigit() or int(parts[2]) > 59:
            return False
    return True

def update_options(p):
    if sr.get() and dn.get():
        k = Time.d
        new_options = get_new_options(sr.get(), dn.get())
        try:
            combobox['values'] = list(set(k[new_options]))
            #v = k[new_options]
        except KeyError:
            messagebox.showerror('Key Error',"Please Enter Appropiate  Stations")
            sr.delete(0,tk.END)
            dn.delete(0,tk.END)
        

    else:
        combobox['values'] = []

def get_new_options(value1, value2):
    opt = value1+'-'+value2
    return opt

def validate_input(input):
    if input.isdigit():
        return True
    elif input == "Enter Trip ID":
        return True
    elif input == "":
        return True
    return False

def AskDir():
    di = filedialog.askdirectory()
    output_entry.delete(0,"end")
    output_entry.insert(0,di)
    if tripno_entry.get()!="" and sr.get()!='' and dn.get()!='' and combobox.get()!='' and combobox_1.get()!='' and ser_entry.get()!='' and time_entry.get()!='' and trip_entry.get()!='':
        run_button.config(state='normal')
out = []

def Validate_Alpha(input):
    if input.isupper():
        return True
    elif input == '':
        return True
    else:
        return False

def Show():
    #graph_thread = th.Thread(target = Graph.Show,args=(output_entry.get(),headway_entry.get()))
    #graph_thread.start()
    #graph_thread.join()
    Graph.Show(output_entry.get(),headway_entry.get())
    



def XmlManipulation():
    def Entry_time_Update():
        root_Entry = tk.Toplevel(root_xml)
        style = ttk.Style()
        style = ThemedStyle(root_Entry)
        style.theme_use("arc")
        root_Entry.title('XML Manipulation')
        root_Entry.geometry('900x500')
        root_Entry.config(bg='#ADDEF6')
        root_Entry.wm_attributes("-topmost", True)

    def convert_excel():
        thread_xml = th.Thread(target=ExceltoXML.XmlToExcel,args=(entry_import_xml.get(),))
        thread_xml.start()
        thread_xml.join()
        root_xml.after(0,lambda: messagebox.showinfo('Info','Excel Generated',parent = root_xml))
        
    def convert_xml():
        thread_excel = th.Thread(target=ExceltoXML.ExcelToXml,args=(entry_import_excel.get(),))
        thread_excel.start()
        thread_excel.join()
        root_xml.after(0,lambda: messagebox.showinfo('Info','XML Generated',parent = root_xml))
        
    def AskFile_xml():
        di = filedialog.askopenfile(parent=root_xml)
        entry_import_xml.delete(0,"end")
        entry_import_xml.insert(0,di.name)
        
    def AskFile_excel():
        di = filedialog.askopenfile(parent=root_xml)
        entry_import_excel.delete(0,"end")
        entry_import_excel.insert(0,di.name)
        

    root_xml = tk.Toplevel(root)
    style = ttk.Style()
    style = ThemedStyle(root_xml)
    style.theme_use("arc")
    root_xml.title('XML Manipulation')
    root_xml.geometry('900x500')
    root_xml.config(bg='#ADDEF6')
    root_xml.wm_attributes("-topmost", True)
    
    label_xml = tk.Label(root_xml,text= 'Time Table XML to Excel',font=('Alstom',16),bg='#ffffff')
    label_xml.place(x=350,y=10)
    
    label_import_xml = tk.Label(root_xml,text= 'Import Time Table',font=('Alstom',16),bg='#ffffff')
    label_import_xml.place(x=10,y=70)
    
    entry_import_xml = tk.Entry(root_xml,bd=1,width=30,font=('Alstom',16),bg='#ffffff')
    entry_import_xml.place(x = 200, y=70)
    
    button_import_xml = tk.Button(root_xml,text = 'Browse',font=('Alstom',16),command = AskFile_xml)
    button_import_xml.place(x=600,y=65)
    
    button_convert_excel = tk.Button(root_xml,text = 'Convert to Excel',font=('Alstom',16),command=convert_excel)
    button_convert_excel.place(x = 300,y=120)
    
    label_excel = tk.Label(root_xml,font=('Alstom',16),text='Excel To XML',bg='#ffffff')
    label_excel.place(x=400,y=200)
    
    label_import_excel = tk.Label(root_xml,text='Import Excel',font=('Alstom',16),bg='#ffffff')
    label_import_excel.place(x=10,y = 250)
    
    entry_import_excel = tk.Entry(root_xml,bd=1,width=30,font=('Alstom',16),bg='#ffffff')
    entry_import_excel.place(x=200,y = 250)

    button_import_excel = tk.Button(root_xml,text = 'Browse',font=('Alstom',16),command=AskFile_excel)
    button_import_excel.place(x=600, y = 250)
    
    button_convert_xml = tk.Button(root_xml,text = 'Convert to XML',font=('Alstom',16),command=convert_xml)
    button_convert_xml.place(x=300, y= 305)
    
    Entry_time_Update_button = tk.Button(root_xml,text = 'Entry time Update',font=('Alstom',16),command=Entry_time_Update)
    Entry_time_Update_button.place(x =10,y=350)

    #root_xml.grab_set()
    root_xml.mainloop()

    

def open_dwell():
    os.startfile(os.path.join(os.getcwd(), 'Dwell.ini'))

def Finish_back_end():
    Time.Run(Time.Update_Dwell(),int(tripno_entry.get()),out,sr.get()+'-'+dn.get(),dn.get()+'-'+sr.get(),combobox.get(),combobox_1.get(),ser_entry.get(),time_entry.get(),int(trip_entry.get()),output_entry.get(),'FINISH')

def Run_Back_end():
    Time.Run(Time.Update_Dwell(),int(tripno_entry.get()),out,sr.get()+'-'+dn.get(),dn.get()+'-'+sr.get(),combobox.get(),combobox_1.get(),ser_entry.get(),time_entry.get(),int(trip_entry.get()),output_entry.get(),'RUN')

root = tk.Tk()
style = ttk.Style()
style = ThemedStyle(root)
style.theme_use("arc")
root.title('Time Table Maker')
root.geometry('900x500')
root.config(bg='#ADDEF6')
reg = root.register(validate_input)
reg_Cap = root.register(Validate_Alpha)

title = tk.Label(root,text='TIME TABLE',font=('Alstom',16),bg='#ffffff')
title.place(x=400,y=10)

output_file = tk.Label(root,text='Output Folder',font=('Alstom',16),bg='#ADDEF6')
output_file.place(x=195,y=195)

output_entry = tk.Entry(root,bd=1,width=30,font=('Alstom',16),bg='#ffffff')
output_entry.place(x=355,y=195)

output_browse = tk.Button(root,font=('Alstom',16),bg='#99ff99',width=10,text = 'Browse',command = AskDir)
output_browse.place(x=750,y=185)

idx = tk.Label(root,text='Source and Destination',font=('Alstom',16),bg='#ADDEF6')
idx.place(x=10,y=60)
sr = tk.Entry(root,bd=1,width=6,font=('Alstom',16),bg='#ffffff')
sr.place(x=245,y=60)


to = tk.Label(root,text='TO',font=('Alstom',16),bg='#ADDEF6')
to.place(x=320,y=60)

dn = tk.Entry(root,bd=1,width=6,font=('Alstom',16),bg='#ffffff')
dn.place(x=355,y=60)


trip_entry = tk.Entry(root,font=('Alstom',16),fg='grey',width=10, validate="key")
trip_entry.insert(0, "Enter Trip ID")
trip_entry.bind("<FocusIn>", on_entry_click)
trip_entry.bind("<FocusOut>", on_entry_click)
trip_entry.place(x=10,y=130)
trip_entry.config(validatecommand=(reg, "%P"))

label_choice = tk.Label(root, text="Select Pattern",bg='#ADDEF6')
label_choice.place(x=550,y=45)
combobox = ttk.Combobox(root,width=45)
combobox.place(x=500,y=66)
combobox.bind("<<ComboboxSelected>>", on_combobox_select) 
sr.bind("<FocusOut>", update_options)
dn.bind("<FocusOut>", update_options)
sr.bind("<FocusIn>", update_options)
dn.bind("<FocusIn>", update_options)
sr.config(validate="key",validatecommand=(reg_Cap,"%P"))
dn.config(validate="key",validatecommand=(reg_Cap,"%P"))

ser_entry = tk.Entry(root,bd=1,width=10,font=('Alstom',16),bg='white',fg='grey', validate="key")
ser_entry.insert(0, "Service")
ser_entry.bind("<FocusIn>", on_entry_ser)
ser_entry.bind("<FocusOut>", on_entry_ser)
ser_entry.place(x=10,y=195)
ser_entry.config(validatecommand=(reg, "%P"))

tripno_entry = tk.Entry(root,bd=1,width=10,font=('Alstom',16),bg='white',fg='grey', validate="key")
tripno_entry.insert(0, "No of Trips")
tripno_entry.bind("<FocusIn>", on_entry_trip)
tripno_entry.bind("<FocusOut>", on_entry_trip)
tripno_entry.place(x=10,y=260)
tripno_entry.config(validatecommand=(reg, "%P"))

label_mode = tk.Label(root, text="Select Mode",bg='#ADDEF6')
label_mode.place(x=270,y=110)

Modes = ["Tight running profile", "Normal Tight", "Normal Untight", "Normal Running","Energy Saving","Coasting"]
combobox_1 = ttk.Combobox(root, values=Modes,width = 30)
combobox_1.place(x=245,y=130)
combobox_1.bind("<<ComboboxSelected>>", on_combobox_modes)

label_time = tk.Label(root, text="Time(hh:mm:ss):",font=('Alstom',16),bg='#ADDEF6')
label_time.place(x=500,y=125)

validate_time = root.register(validate_time_input)
time_entry = ttk.Entry(root, validatecommand=(validate_time, "%P"),width=30)
time_entry.place(x=650,y=130)


run_button = tk.Button(root,font=('Alstom',16),text="RUN",command=Run_Back_end)
run_button.place(x=320,y=300)
run_button.config(state='disable')

finish_button = tk.Button(root,font=('Alstom',16),text="FINISH",command=Finish_back_end)
finish_button.place(x=400,y=300)

dwell_button = tk.Button(root,font=('Alstom',16),text="DWELL",command=open_dwell)
dwell_button.place(x=500,y=300)

dwell_button = tk.Button(root,font=('Alstom',16),text="Show Graph",command=Show)
dwell_button.place(x=350,y=400)

XML_button = tk.Button(root,font=('Alstom',16),text="XML Manipulation",command=XmlManipulation)
XML_button.place(x=550,y=400)


headway_label = tk.Label(root,text = 'Headway',font= ('Alstom',16),bg='#ADDEF6')
headway_label.place(x =10,y=400)

headway_entry = tk.Entry(root,font=('Alstom',16),bg='white',width=5,bd=2,fg='grey')
headway_entry.place(x=110,y=400)
headway_entry.insert(0,'30')
headway_entry.bind('<FocusIn>',headway_click)
headway_entry.bind('<FocusOut>',headway_click)

root.mainloop()

