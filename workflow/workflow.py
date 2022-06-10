# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 01:36:05 2022

@author: alper
"""
import pandas as pd
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
import sqlite3 as db
from tkinter import *
import os


 
conn = db.connect('workflow.db') #Veritabanı oluşturur ya da var olana bağlanır / Create a database or connect one
c = conn.cursor() 


#Tablo oluşturur. / Creates a table.
c.execute(""" CREATE TABLE IF NOT EXISTS veriler (
    takip_no text,
    kimden text,
    tur text,
    tanim text,
    is_tarihi text,
    baslama_saat text,
    bitis_saat text,
    aciklama text
    )""")


#FONKSİYONLAR / FUNCTIONS


#SQL ile tabloya veri eklememizi sağlayan fonksiyon / Function that allows us to add data to the table with SQL
def insert_data (takip_no, kimden, tur, tanim, is_tarihi, baslama_saat, bitis_saat, aciklama):
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    c.execute("INSERT INTO veriler(takip_no, kimden, tur, tanim, is_tarihi, baslama_saat, bitis_saat, aciklama) VALUES(?,?,?,?,?,?,?,?)",(takip_no, kimden, tur, tanim, is_tarihi, baslama_saat, bitis_saat, aciklama))
    messagebox.showinfo("workflow","İş akışı girildi.")
    conn.commit()
    c.close()

#Verileri excel ile görüntülemeyi sağlayan fonksiyon. / Function that allows displaying data with excel.
def excele_aktar():
    
    df=pd.read_sql(sql="Select * from veriler",con=conn)
    df.to_excel("workflow.xlsx", index=False)
    
    os.system("workflow.xlsx")

#Girilen verileri kaydeden fonksiyon. / Function that saves the entered data.        
def kaydet():
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    takip_no = takipno_girdi.get(1.0,END)
    kimden = kimden_girdi.get(1.0,END)
    tur = tur_opsiyon.get()
    tanim = tanim_girdi.get(1.0,END)
    is_tarihi = is_tarihi_girdi.get()
    baslama_saat = baslama_saat_girdi.get(1.0,END)
    bitis_saat = bitis_saat_girdi.get(1.0,END)
    aciklama = metin.get(1.0,END)
    
    if is_tarihi =='':
        is_tarihi = is_tarihi_girdi.set_date(dt)
        
    if kontrol() == 1:
        c.execute("UPDATE veriler  SET kimden = ?, tur = ?, tanim = ?, is_tarihi = ?, baslama_saat = ?, bitis_saat = ?, aciklama = ? where takip_no = ?",(kimden, tur,tanim,is_tarihi,baslama_saat,bitis_saat,aciklama,takip_no))
        conn.commit()
        
        messagebox.showinfo("workflow","Güncelleme işlemi gerçekleşti.")
        clear()
        read_only()
        
        
    else:
        
        insert_data(takip_no, kimden, tur, tanim, is_tarihi, baslama_saat, bitis_saat, aciklama)
        
        
    clear()
    akis_ozet()
    read_only()
    c.close()

#Veri girişine izin verir / allows data entry
def kaydet_oku():
    
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
   
    takip_no = takipno_girdi.get(1.0,END)
    kimden = kimden_girdi.get(1.0,END)
    tur = tur_opsiyon.get()
    tanim = tanim_girdi.get(1.0,END)
    is_tarihi = is_tarihi_girdi.get()
    baslama_saat = baslama_saat_girdi.get(1.0,END)
    bitis_saat = bitis_saat_girdi.get(1.0,END)
    aciklama = metin.get(1.0,END)
        
    if kontrol() == 1:
        oku()
           
    else:
        able()
        clear()
    
    akis_ozet()
    
    c.close()

#Akış geçmişini görüntelemeyi sağlar / Allows viewing streaming history
def display():
    
    def detay():
        detay_metin.configure(state='normal')
        detay_metin.delete(1.0,END)
        
        conn = db.connect('workflow.db')   
        c = conn.cursor()  
        takp_no = detay_girdi.get(1.0,END)
        sorgula = "select * from veriler where takip_no = '"+takp_no+"'"           
        c.execute(sorgula)
        listem = c.fetchall()
        
        aciklama_detay = listem[0][7]
        detay_metin.insert(1.0, aciklama_detay)
        detay_metin.configure(state='disabled')
        c.close()
        
    
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    display_window = Tk()
    display_window.resizable(width=False, height=False)
    display_window.title("İş Akış Geçmişi")
    display_window.geometry("700x450")
    
    frame_ust_d = Frame(display_window, bg='#add8e6')
    frame_ust_d.place(relx=0.01, rely=0.01, relwidth=0.98, relheight= 0.49)
    
    frame_orta = Frame(display_window, bg='#add8e6')
    frame_orta.place(relx=0.01, rely=0.51, relwidth=0.49, relheight= 0.10)
    
    frame_orta_s = Frame(display_window, bg='#add8e6')
    frame_orta_s.place(relx=0.51, rely=0.51, relwidth=0.48, relheight= 0.10)
    
    frame_alt_d = Frame(display_window, bg='#add8e6')
    frame_alt_d.place(relx=0.01, rely=0.62, relwidth=0.98, relheight= 0.35)
    
        
    tk_no_tag = Label(frame_orta,bg='#add8e6', text="Takip No:", font="Verdana 10 bold")
    tk_no_tag.grid(row=0, column=0, padx= 10, pady=10)

    detay_girdi = Text(frame_orta, height=1, width=14)
    detay_girdi.grid(row=0, column=1, padx= 1, pady=10)
   
    detay_buton = Button(frame_orta, text='Oku',width=9, height=1, command=lambda: detay())
    detay_buton.grid(row=0, column=2, padx=15, pady=1)
    
    excele_aktar_buton = Button(frame_orta_s, text='Excel İle Görüntüle',width=25, height=1, command=lambda: excele_aktar())
    excele_aktar_buton.grid(row=0, column=0, padx=75, pady=9, sticky='E')
    
    detay_tag = Label(frame_alt_d, bg='#add8e6', text="Açıklama Detay", font="Verdana 10 bold")
    detay_tag.grid(row=1, column=0, padx= 15, pady=15,sticky='W')

    detay_metin = Text(frame_alt_d, height=5, width=81, bg='#FFFFE1')
    detay_metin.grid(row=2, column=0, padx= 15, pady=1,sticky='W')
    
    detay_metin.configure(state='disabled')
    
        
    table = ttk.Treeview(display_window,height=9)
    table["columns"] = ["bir","iki","uc","dort","bes","alti","yedi","sekiz"]
    table.heading("bir", text= "T.No")
    table.heading("iki", text= "Kimden")
    table.heading("uc", text= "Tür")
    table.heading("dort", text= "Tanım")
    table.heading("bes", text= "Tarih")
    table.heading("alti", text= "Başlama")
    table.heading("yedi", text= "Bitiş")
    table.heading("sekiz", text= "Açıklama")
    
    table.column("#0", width =0, minwidth=0)
    table.column("bir", anchor=CENTER, width=45) 
    table.column("iki", anchor=W, width=70) 
    table.column("uc", anchor=W, width=85)
    table.column("dort", anchor=W, width=135)
    table.column("bes", anchor=CENTER, width=75)
    table.column("alti", anchor=CENTER, width=65)
    table.column("yedi", anchor=CENTER, width=65)
    table.column("sekiz", anchor=W, width=130)
    
    data = c.execute("SELECT rowid,* FROM veriler ORDER BY takip_no DESC")
    i=0   
    for veriler in data:
        table.insert('',i, text="" + str(veriler[0]), values=(veriler[1],veriler[2],veriler[3],veriler[4],veriler[5],veriler[6],veriler[7],veriler[8]))
        i +=1
    table.grid(row=1, column=0, padx= 10, pady=10)
    c.close()

#Veri silme / data deletion
def clear():
    kimden_girdi.delete(1.0,END)
    tanim_girdi.delete(1.0,END)
    tur_opsiyon.set('\t')
    is_tarihi_girdi.delete(0,END)
    baslama_saat_girdi.delete(1.0,END)
    bitis_saat_girdi.delete(1.0,END)
    metin.delete(1.0,END)
 

def kontrol ():
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    takip_no = takipno_girdi.get(1.0,END)
    kontrol = "select takip_no from veriler"
    c.execute(kontrol)
    kontrol = c.fetchall()
    control=0
    for i in kontrol:
        for j in i:
            if j == takip_no:
                control=1
    c.close()
    return control

#Akış özetini gerçekleştirir. / the flow summary
def akis_ozet():
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    
    table = ttk.Treeview(frame_alt_sag,height=6)
    table["columns"] = ["bir","iki","uc"]
    table.heading("bir", text= "Takip No")
    table.heading("iki", text= "Tür")
    table.heading("uc", text= "Tanım")
     
    
    table.column("#0", width =0, minwidth=0)
    table.column("bir", anchor=W, width=65) 
    table.column("iki", anchor=W, width=85) 
    table.column("uc", anchor=W, width=150) 
    

    
    data = c.execute("SELECT rowid,takip_no, tur, tanim  FROM veriler ORDER BY takip_no DESC")
    i=0
   
    for veriler in data:
        table.insert('',i, text=" " + str(veriler[0]), values=(veriler[1],veriler[2],veriler[3]))
        i +=1
    table.grid(row=1, column=0, padx= 10, pady=1,sticky='S')
    
    c.close()
               
def oku():
    able()
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    
    takip_no = takipno_girdi.get(1.0,END)
    sorgu = "select * from veriler where takip_no = '"+takip_no+"'"
     
        
    c.execute(sorgu)
    liste = c.fetchall()
    
    kimden = liste[0][1]
    tur = liste[0][2]
    tanim = liste[0][3]
    is_tarihi = liste[0][4]
    baslama_saat = liste[0][5]
    bitis_saat = liste[0][6]
    aciklama = liste[0][7]
    
    kimden_girdi.delete(1.0,END)
    kimden_girdi.insert(1.0,kimden)
        
    tur_opsiyon.set(tur)
    
    tanim_girdi.delete(1.0, END)
    tanim_girdi.insert(1.0, tanim)
    
    is_tarihi_girdi.set_date(is_tarihi)
    
    baslama_saat_girdi.delete(1.0,END)
    baslama_saat_girdi.insert(1.0,baslama_saat)
    
    bitis_saat_girdi.delete(1.0,END)
    bitis_saat_girdi.insert(1.0,bitis_saat)
    
    metin.delete(1.0,END)
    metin.insert(1.0,aciklama)
    
    c.close()
    
def sil():
    
    conn = db.connect('workflow.db')   
    c = conn.cursor()  
    takip_no = takipno_girdi.get(1.0,END)
    if kontrol() == 1:
        delete = "delete from veriler where takip_no = '"+takip_no+"'"
        c.execute(delete)
        messagebox.showinfo("workflow","Silme işlemi başarılı.")
        conn.commit()
        c.close()
    else:
        messagebox.showinfo("workflow","Takip No mevcut değil.")
    
    clear()
    akis_ozet()
    read_only()
    c.close()
    
def read_only():
    kimden_girdi.config(state = DISABLED)
    tanim_girdi.config(state = DISABLED)
    tur_acilir_menu.config(state=DISABLED)
    is_tarihi_girdi.config(state=DISABLED)
    baslama_saat_girdi.config(state = DISABLED)
    bitis_saat_girdi.config(state = DISABLED)
    metin.config(state=DISABLED)
 
def able():
    kimden_girdi.config(state = NORMAL)
    tanim_girdi.config(state = NORMAL)
    tur_acilir_menu.config(state=NORMAL)
    is_tarihi_girdi.config(state=NORMAL)
    baslama_saat_girdi.config(state = NORMAL)
    bitis_saat_girdi.config(state = NORMAL)
    metin.config(state=NORMAL)



master = Tk()
master.title("workflow")
master.geometry('740x450')
master.resizable(width=False, height=False)

frame_ust = Frame(master, bg='#add8e6')
frame_ust.place(relx=0.05, rely=0.05, relwidth=0.9, relheight= 0.1)

frame_sol_orta = Frame(master, bg='#add8e6')
frame_sol_orta.place(relx=0.05, rely=0.16, relwidth=0.45, relheight= 0.30)

frame_sag_orta = Frame(master, bg='#add8e6')
frame_sag_orta.place(relx=0.51, rely=0.16, relwidth=0.44, relheight= 0.30)

frame_alt = Frame(master, bg='#add8e6')
frame_alt.place(relx=0.05, rely=0.47, relwidth=0.45, relheight= 0.48)

frame_alt_sag = Frame(master, bg='#add8e6')
frame_alt_sag.place(relx=0.51, rely=0.47, relwidth=0.44, relheight= 0.48)




takipno_tag = Label(frame_ust, bg='#add8e6', text="Takip No", font="Verdana 10 bold")
takipno_tag.grid(row=0, column=0, padx= 7, pady=10,sticky='W')

takipno_girdi = Text(frame_ust, height=1, width=15)
takipno_girdi.grid(row=0, column=1, padx=10, pady=10,sticky='W')


kimden_tag = Label(frame_sol_orta, bg='#add8e6', text="Kimden", font="Verdana 10 bold")
kimden_tag.grid(row=0, column=0, padx= 10, pady=10,sticky='W')

kimden_girdi = Text(frame_sol_orta, height=1, width=15)
kimden_girdi.grid(row=0, column=1, padx= 10, pady=10,sticky='W')



tur_tag = Label(frame_sol_orta, bg='#add8e6', text="Tür", font="Verdana 10 bold")
tur_tag.grid(row=1, column=0, padx=9 , pady=12,sticky='W')

tur_opsiyon = StringVar(frame_sol_orta)
tur_opsiyon.set("\t")


tur_acilir_menu = OptionMenu(
    frame_sol_orta, 
    tur_opsiyon, 
    "Etkinlikler",
    "Yazılım",
    "ARGE",
    "Pazarlama",
    "Finans",
    "İş Birlikleri",
    "Diğer")

tur_acilir_menu.grid(row=1, column=1, padx= 10, pady=10,sticky='W')


tanim_tag = Label(frame_sol_orta, bg='#add8e6', text="Tanım", font="Verdana 10 bold")
tanim_tag.grid(row=2, column=0, padx= 10, pady=10,sticky='W')

tanim_girdi = Text(frame_sol_orta, height=1, width=26,bg='#FFFFE1')
tanim_girdi.grid(row=2, column=1, padx= 10, pady=10,sticky='W')




is_tarihi_tag = Label(frame_sag_orta, bg='#add8e6', text="İş Tarihi", font="Verdana 10 bold")
is_tarihi_tag.grid(row=0, column=0, padx=10, pady=10,sticky='W')

is_tarihi_girdi = DateEntry(frame_sag_orta, width=15, background='brown', forefround='black', borderwidth=1, locale="de_DE")
is_tarihi_girdi._top_cal.overrideredirect(False)
is_tarihi_girdi.grid(row=0, column=1, padx= 10, pady=10,sticky='W')


baslama_saat_tag = Label(frame_sag_orta, bg='#add8e6', text="Başlama Saati", font="Verdana 10 bold")
baslama_saat_tag.grid(row=1, column=0, padx= 10, pady=10, sticky='W')

baslama_saat_girdi = Text(frame_sag_orta, height=1, width=14)
baslama_saat_girdi.grid(row=1, column=1, padx= 10, pady=10,sticky='W')


bitis_saat_tag = Label(frame_sag_orta, bg='#add8e6', text="Bitiş Saati", font="Verdana 10 bold")
bitis_saat_tag.grid(row=2, column=0, padx= 10, pady=10,sticky='W')

bitis_saat_girdi = Text(frame_sag_orta, height=1, width=14)
bitis_saat_girdi.grid(row=2, column=1, padx= 10, pady=10,sticky='W')


aciklama_tag = Label(frame_alt, bg='#add8e6', text="Açıklama", font="Verdana 10 bold")
aciklama_tag.grid(row=0, column=0, padx= 10, pady=10,sticky='W')

metin = Text(frame_alt, height=9.45, width=36,bg='#FFFFE1')
metin.grid(row=1, column=0, padx= 10, pady=1,sticky='NW')

akis_ozet_tag = Label(frame_alt_sag, bg='#add8e6', text="Son Akışlar", font="Verdana 10 bold")
akis_ozet_tag.grid(row=0, column=0, padx= 10, pady=10,sticky='W')

read_only()




#BUTONLAR / BUTTONS

kaydet_butonu = Button(frame_ust, text='Kaydet / Güncelle',width=15, command=lambda: kaydet())
kaydet_butonu.grid(row=0, column=2, padx=10, pady=10)

oku_butonu = Button(frame_ust, text='Oku',width=10, command=lambda: kaydet_oku())
oku_butonu.grid(row=0, column=3, padx=10, pady=10)

sil_butonu = Button(frame_ust, text='Sil',width=10, command=lambda: sil())
sil_butonu.grid(row=0, column=4, padx=10, pady=10)

akis_gecmis_butonu = Button(frame_ust, text='Akış Detay',width=10, command=lambda: display())
akis_gecmis_butonu.grid(row=0, column=5, padx=10, pady=10)

akis_ozet()  



master.mainloop()
