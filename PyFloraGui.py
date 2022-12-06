import webbrowser
import calendar
import datetime
import json
import random as rd
import sqlite3
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as tkf
from tkinter import ttk
from PIL import Image,ImageTk
import io
import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd
import requests



root = tk.Tk()

#slike biljaka
african_violet = ImageTk.PhotoImage(Image.open("slike/African Violet.jpg"))
aglaonema = ImageTk.PhotoImage(Image.open("slike/Aglaonema.jpg"))
moneytree = ImageTk.PhotoImage(Image.open("slike/Money Tree.jpg"))
peacelily = ImageTk.PhotoImage(Image.open("slike/Peace Lily.jpg"))
peperomia = ImageTk.PhotoImage(Image.open("slike/Peperomia.jpg"))
philodendron = ImageTk.PhotoImage(Image.open("slike/Philodendron.jpg"))
rubbertree = ImageTk.PhotoImage(Image.open("slike/Rubber Tree.jpg"))
snakeplant = ImageTk.PhotoImage(Image.open("slike/Snake plant.jpg"))
swisscheese = ImageTk.PhotoImage(Image.open("slike/Swiss Cheese Plant.jpg"))
zz = ImageTk.PhotoImage(Image.open("slike/zz plant.jpg"))

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData




lista_imena = ['African Violet','Aglaonema','Money Tree','Peace Lily','Peperomia','Philodendron','Rubber Tree','Snake plant','Swiss Cheese Plant','zz plant']
lista_slika = [african_violet,aglaonema,moneytree,peacelily,peperomia,philodendron,rubbertree,snakeplant,swisscheese,zz]

posude = ['Dnevni boravak1','Dnevni boravak2','Balkon1','Balkon2','Balkon3','Kuhinja1','Kuhinja2','Kuhinja3','Soba1','Soba2']

#korisnicke funkcije za login i izradu novog profila i brisanje profila

def signup():
    sign_window = ctk.CTkToplevel(root,bg='black')
    sign_window.grab_set()
    sign_window.title('Sign up')
    sign_window.geometry('600x600')

    sign_lbl =tk.Label(sign_window,text='Sign Up',font=(font_slova,50),fg='white',bg='black')
    sign_lbl.pack()
    

    email_lbl = tk.Label(sign_window,text='Unesite vas email',font =(font_slova,15),fg='white',bg='black')
    email_lbl.pack()

    email_ent = ctk.CTkEntry(sign_window,textvariable=email_var,border_color='red',corner_radius=5)
    email_ent.pack()

    kor_ime_lbl = tk.Label(sign_window,text='Unesite zeljeno korisnicko ime',font=(font_slova,15),fg='white',bg='black')
    kor_ime_lbl.pack()

    kor_ime_ent = ctk.CTkEntry(sign_window,textvariable=kor_ime_var,border_color='red',corner_radius=5)
    kor_ime_ent.pack()

    sif_lbl = tk.Label(sign_window,text='Unesite zeljenu sifru',font=(font_slova,15),fg='white',bg='black')
    sif_lbl.pack()

    sif_ent = ctk.CTkEntry(sign_window,textvariable=sifra_var,border_color='red',corner_radius=5)
    sif_ent.pack()

    #submit_button = tk.Button(sign_window,text='Submit',font=(font_slova,10),bg='red',fg='yellow',command=save_korisnik)
    #submit_button.pack()

    submit_button = ctk.CTkButton(sign_window,text='Submit',text_font=('Ariel',15),bg_color='red',fg_color='yellow',command=save_korisnik)
    submit_button.pack()

    exit_btn = ctk.CTkButton(sign_window,text='Exit',text_font=('Ariel',15),bg_color='black',fg_color='yellow',command=sign_window.destroy)
    exit_btn.pack()

def create_db_users():
    conn= sqlite3.connect('PyFloraUsers.db')
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Users(email TEXT PRIMARY KEY NOT NULL UNIQUE, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    conn.commit()
    conn.close()
create_db_users()

def save_korisnik():
    email = email_var.get()
    kor_ime = kor_ime_var.get()
    sifra=sifra_var.get()
    
    conn= sqlite3.connect('PyFloraUsers.db')
    c=conn.cursor()
    
    c.execute("INSERT INTO Users(email,username,password) VALUES (?,?,?)",(email,kor_ime,sifra)) 
    conn.commit()
    print('Korisnik spremljen')
    tkinter.messagebox.showinfo('Bravo','Uspjesno ste napravili racun')

    email_var.get('')
    kor_ime_var.get('')
    sifra_var.get('')


    
#NOVI PROZOR nakon logina
def novi_prozor():
    unos_window = tk.Toplevel(bg='khaki1')
    #unos_window.grab_set()
    unos_window.title('Biljke')
    unos_window.geometry('800x600')


    lbl_biljke = tk.Label(unos_window,text='Biljke',font=(font_slova,25),fg='black',bg='khaki1')
    lbl_biljke.grid(row=0,column=1,padx=100,pady=20)
    profil_btn = ctk.CTkButton(unos_window,text='Moj Profil',corner_radius=3,border_color='black',border_width=1,command=my_profile)
    profil_btn.grid(row=0,column=2,padx=20,pady=10,sticky='e')

    
    sync_btn = ctk.CTkButton(unos_window,text='Sync',corner_radius=3,border_color='black',border_width=1,command=sync)
    sync_btn.grid(row=0,column=0,padx=10,pady=10)

    items_listbox = tk.Listbox(unos_window,listvariable=lista_biljaka_var,bg='khaki1',fg='black',font=(font_slova,15),selectmode=tk.SINGLE)
    items_listbox.grid(row=1,column=0,rowspan=2)



    
    #prikazivanje izabranog itema iz listboxa na novom labelu
    def selected_item():
        
        global prikaz,prikaz_id,prikaz_ime,prava_slika,saznaj
        for i in items_listbox.curselection():
            izbor=items_listbox.get(i)
            konekcija = sqlite3.connect('Posude_i_biljke.db')
            biljke_frm = tk.LabelFrame(unos_window,text='Biljke detaljni prikaz',padx=10,pady=10,bg='khaki1')
            biljke_frm.grid(row=1,column=1,columnspan=2,rowspan=2,sticky='ne')

            cur = konekcija.cursor()

            
            cur.execute('SELECT * From Biljke WHERE ime_biljke = ?',(izbor,))

            sve = cur.fetchall()

            for red in sve:
                slika = red[2]
                ime = red[1]
                id = red[0]

                
                imageStream = io.BytesIO(slika)
                imageFile = Image.open(imageStream)
                
                smaller_image=imageFile.resize((200,200))

                prava_slika = ImageTk.PhotoImage(smaller_image)

                prikaz_ime = tk.Label(biljke_frm,text=f'Ime biljke: {ime}',font=(font_slova,12),bg='khaki1')
                prikaz_ime.pack(side=tk.TOP)
                
                prikaz_id = tk.Label(biljke_frm,text=f'ID: {id}',font=(font_slova,12),bg='khaki1')
                prikaz_id.pack(side=tk.TOP)


                prikaz = tk.Label(biljke_frm,image=prava_slika,bg='khaki1')
                prikaz.pack(padx=10,pady=10,ipadx=10,ipady=10,fill='both')

                saznaj = ctk.CTkButton(biljke_frm,text=f'Saznaj sve o {ime}',command=lambda:webbrowser.open_new_tab(f'https://en.wikipedia.org/wiki/{ime}'))
                saznaj.pack(padx=10,pady=10,ipadx=10,ipady=10,fill='x')
                clr_crn_btn = ctk.CTkButton(unos_window,text='Ocisti unos',command=clear_screen,corner_radius=3,border_color='black',border_width=1)
                clr_crn_btn.grid(row=3,column=1,padx=10,pady=10)
                

    show_btn = ctk.CTkButton(unos_window,text='Prikazi biljku',command=selected_item,corner_radius=3,border_color='black',border_width=1)
    show_btn.grid(row=3,column=0,padx=10,pady=10)

    #spajanje biljke i posude te punjenje tablice Biljke_posude
    def dodaj_biljku_posudi():
        
        add_biljka = tk.Toplevel(bg='cyan')
        add_biljka.title('Dodavanje nove biljke')
        add_biljka.geometry('500x500')
        dodaj_bilj_lbl = tk.Label(add_biljka,text='Izaberi biljku: ',font=(font_slova,12),bg='cyan')
        dodaj_bilj_lbl.grid(row=0,column=0,padx=10,pady=10)
        baza = sqlite3.connect('Posude_i_biljke.db')
        cur=baza.cursor()
        cur.execute('SELECT * FROM Biljke')
        sve = cur.fetchall()
        biljke=[]
        for i in sve:
            biljke.append(i[1])
        baza.close()   
        biljke_box = ttk.Combobox(add_biljka,values=biljke,width=30,textvariable=izbor_biljke,font=(font_slova,12))
        biljke_box.current(0)
        biljke_box.grid(row=0,column=1,padx=10,pady=10)
        #biljke_box.bind('<<ComboboxSelected>>',pick_biljka)

        baza2 = sqlite3.connect('Posude_i_biljke.db')
        cur2=baza2.cursor()
        cur2.execute('SELECT * FROM Biljke_Posude')
        posude1=[]

        zauzete_posude = cur2.fetchall()
        lista_zauzetih = []
        for z in zauzete_posude:
            lista_zauzetih.append(z[1])
            

        for ime in posude:
            #for z in zauzete_posude:

                if ime not in lista_zauzetih:
                    posude1.append(ime)
                    

        
        dodaj_pos_lbl = tk.Label(add_biljka,text='Izaberi posudu',font=(font_slova,12),bg='cyan')
        dodaj_pos_lbl.grid(row=1,column=0,padx=10,pady=10)

        posude_box = ttk.Combobox(add_biljka,values=posude1,width=30,textvariable=izbor_posude,font=(font_slova,12))
        posude_box.current(0)
        posude_box.grid(row=1,column=1,padx=10,pady=10)

      

        def add_to_baza():
            pos=izbor_posude.get()
            bilj=izbor_biljke.get()
            con=sqlite3.connect('Posude_i_biljke.db')
            cur=con.cursor()
            cur.execute('INSERT INTO Biljke_Posude(ime_posude,ime_biljke) Values(?,?)',(pos,bilj))
            con.commit()
            tkinter.messagebox.showinfo('Uspjeh','Uspjesno dodana biljka u posudu')
            cur.close()

        sbm_btn = ctk.CTkButton(add_biljka,text='Potvrdi',command=add_to_baza,corner_radius=3,border_color='black',border_width=1)
        sbm_btn.grid(row=2,column=1,padx=150,pady=10)
    
    dodaj_btn = ctk.CTkButton(unos_window,text='Dodaj biljku u posudu',command=dodaj_biljku_posudi,corner_radius=3,border_color='black',border_width=1)
    dodaj_btn.grid(row=4,column=0,padx=10,pady=10)

    #statistika i plotanje podataka gdje korisnik moze izabrati sto zeli vidjeti
    #vlaznost i temperatura su line plotovi
    #svjetlost je pie chart
    def statistika():
        stat_window = tk.Toplevel(bg='pink')
        stat_window.title('Statistika')
        stat_window.geometry('500x500')
        global posuda_za_stat

        posuda_za_stat = tk.StringVar()

        con = sqlite3.connect('Posude_i_biljke.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM Biljke_Posude')
        sve = cur.fetchall()
        posude=[]
        for item in sve:
            posude.append(item[1])
        
        izbor_za_stat = ctk.CTkComboBox(stat_window,values=posude,variable=posuda_za_stat,border_color='green',border_width=1,corner_radius=3,width=300)
        izbor_za_stat.set('Izaberi posudu za prikaz statistike')
        izbor_za_stat.grid(row=0,column=0,padx=20,pady=20)

        def potvrdi():
            con = sqlite3.connect('Posude_i_biljke.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM Posude WHERE ime_posude=?',(posuda_za_stat.get(),))
            podaci = cur.fetchall()

            df=pd.DataFrame(podaci,columns=['ime_posude','temp','humidity','dt','day','svjetlost'])

            def temp_stat():
                ax = df.plot(ylabel='Temperatura',xlabel='Vrijeme',x='day',y='temp',title='Temperatura zraka')
                plt.xticks(rotation=20)
                plt.show()

            show_temp_btn = ctk.CTkButton(stat_window,text='Temperatura',command=temp_stat,corner_radius=3,border_color='black',border_width=1)
            show_temp_btn.grid(row=1,column=0,padx=10,pady=10)

            def hum_stat():
                ax = df.plot(ylabel='Vlaznost',xlabel='Vrijeme',x='day',y='humidity',title='Vlaznost zemlje')
                plt.xticks(rotation=20)
                
                plt.show()

            show_hum_btn = ctk.CTkButton(stat_window,text='Vlaznost',command=hum_stat,corner_radius=3,border_color='black',border_width=1)
            show_hum_btn.grid(row=2,column=0,padx=10,pady=10)

            def del_biljka():
                cur.execute('DELETE FROM Biljke_Posude WHERE ime_posude=?',(posuda_za_stat.get(),))
                tkinter.messagebox.showinfo('Uspjeh',f'Biljka vise nije u posudi {posuda_za_stat.get()}')
                con.commit()
                stat_window.destroy()

                                    

            del_biljku = ctk.CTkButton(stat_window,text='Isprazni posudu',command=del_biljka,corner_radius=3,border_color='black',border_width=1,bg_color='red')
            del_biljku.grid(row=2,column=1,padx=10,pady=10)

            def svjetlost_stat():
                zbroj = df['svjetlost'].value_counts()

                plt.pie(zbroj)
                plt.title('Svjetlost')
                plt.legend(df['svjetlost'])
                plt.show()

            show_light_btn = ctk.CTkButton(stat_window,text='Svjetlost',command=svjetlost_stat,corner_radius=3,border_color='black',border_width=1)
            show_light_btn.grid(row=3,column=0,padx=10,pady=10)
            

            
            
            
        potvrdi_btn = ctk.CTkButton(stat_window,text='Potvrdi',command=potvrdi,border_color='green',border_width=1,corner_radius=3)
        potvrdi_btn.grid(row=0,column=1,padx=10,pady=10)

    stat_btn = ctk.CTkButton(unos_window,text='Statistika',command=statistika,corner_radius=3,border_color='black',border_width=1)
    stat_btn.grid(row=4,column=1,padx=10,pady=10)


    def clear_screen():
        prikaz_ime.pack_forget()
        prikaz_id.pack_forget()
        prikaz.pack_forget()
        saznaj.pack_forget()


    





conn = sqlite3.connect('Posude_i_biljke.db')
conn.execute('PRAGMA foreign_keys=1')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Biljke_Posude(
            id INTEGER PRIMARY KEY,
            ime_posude TEXT NOT NULL,
            ime_biljke TEXT NOT NULL,
            FOREIGN KEY(ime_posude) REFERENCES Posude(ime_posude),
            FOREIGN KEY(ime_biljke) REFERENCES Biljke(ime_biljke))''')
conn.close()
   


    

def my_profile():
    profil_prozor = tk.Toplevel(bg='khaki1') 
    profil_prozor.title('Moj profil')
    profil_prozor.geometry('500x500') 

    global provjera_email_var
    provjera_kor_ime_var =tk.StringVar()
    provjera_sifra_var =tk.StringVar()
    provjera_email_var =tk.StringVar()
    
    
    



    username_entry_label=tk.Label(profil_prozor,text='Unesite svoje korisnicko ime',font=(font_slova,12),bg='khaki1',fg='black')
    username_entry_label.grid(row=0,column=0)

    username_entry=tk.Entry(profil_prozor,textvariable=provjera_kor_ime_var)
    username_entry.grid(row=0,column=1)

    sifra_entry_label=tk.Label(profil_prozor,text='Unesite svoju sifru',font=(font_slova,12),bg='khaki1',fg='black')
    sifra_entry_label.grid(row=1,column=0)


    sifra_entry=tk.Entry(profil_prozor,textvariable=provjera_sifra_var)
    sifra_entry.grid(row=1,column=1)
    
    email_entry_label=tk.Label(profil_prozor,text='Unesite svoj email',font=(font_slova,12),bg='khaki1',fg='black')
    email_entry_label.grid(row=2,column=0)
    
    email_entry=tk.Entry(profil_prozor,textvariable=provjera_email_var)
    email_entry.grid(row=2,column=1)

    
    
    
                    

    def update_kor_podatke():
        update_lvl =  tk.Toplevel(profil_prozor,bg='black')
        update_lvl.geometry('400x400')
        update_lvl.title('Azuriranje korisnika')

        global novo_kor_ime_var
        global nova_sifra_var
    

        novo_kor_ime_var = tk.StringVar()
        nova_sifra_var = tk.StringVar()

        
        

        update_lbl = tk.Label(update_lvl,text='Azuriranje podataka',font=(font_slova,20),fg='white',bg='black')
        update_lbl.pack()
        
        lbl_novo_kor_ime = tk.Label(update_lvl,text='Unesite novo korisnicko ime',font=(font_slova,12),fg='white',bg='black')
        lbl_novo_kor_ime.pack(padx=10,pady=10,ipadx=10,ipady=10)
        ent_novo_kor_ime = tk.Entry(update_lvl,textvariable=novo_kor_ime_var)
        ent_novo_kor_ime.pack(padx=10,pady=10,ipadx=10,ipady=10)

        lbl_nova_sifra = tk.Label(update_lvl,text='Unesite novu sifru',font=(font_slova,12),fg='white',bg='black')
        lbl_nova_sifra.pack(padx=10,pady=10,ipadx=10,ipady=10)
        ent_nova_sifra = tk.Entry(update_lvl,textvariable=nova_sifra_var)
        ent_nova_sifra.pack(padx=10,pady=10,ipadx=10,ipady=10)

    

        

        

        azuriraj_btn=tk.Button(update_lvl,text='Azuriraj',bg='red',fg='white',command=azuriraj_podatke)
        azuriraj_btn.pack(padx=10,pady=10,ipadx=10,ipady=10)
        
        exit_btn = tk.Button(update_lvl,text='Exit',bg='red',fg='white',command=update_lvl.destroy)
        exit_btn.pack(padx=10,pady=10,ipadx=10,ipady=10)

    

    


        

    
    def submit():
        kor_ime = provjera_kor_ime_var.get()
        sifra= provjera_sifra_var.get()
        
        conn= sqlite3.connect('PyFloraUsers.db')
        c=conn.cursor()
        c.execute("SELECT * FROM Users WHERE username=? AND password=?",(kor_ime,sifra))
        provjera = c.fetchone()

        if provjera:
            lbl_user= tk.Label(profil_prozor,text=f'Email: {provjera[0]}',font=(font_slova,15),bg='khaki1',fg='black')
            lbl_user.grid(row=4,column=0)

            lbl_username= tk.Label(profil_prozor,text=f'Korisnicko ime: {provjera[1]}',font=(font_slova,15),bg='khaki1',fg='black')
            lbl_username.grid(row=5,column=0)

            lbl_pass= tk.Label(profil_prozor,text=f'Lozinka: {provjera[2]}',font=(font_slova,15),bg='khaki1',fg='black')
            lbl_pass.grid(row=6,column=0)
        
                
        else:
            tkinter.messagebox.showerror('Ups','Niste korisnik')

        #korisnik_label = tk.Label(profil_prozor,text=f'Korisniki podatci: {provjera_var}')
        #korisnik_label.grid(row=2,column=0)

    update_button = tk.Button(profil_prozor,text='Azuriraj podatke',font=(font_slova,12),bg='cyan',command=update_kor_podatke)
    update_button.grid(row=3,column=2)

    del_button = tk.Button(profil_prozor,text='Delete User',font=(font_slova,12),bg='red',fg='white',command=delete_user)
    del_button.grid(row=2,column=2)
    
    submit_btn = tk.Button(profil_prozor,text='Submit',font=(font_slova,12),bg='green2',command=submit)
    submit_btn.grid(row=1,column=2)

    exit_btn = tk.Button(profil_prozor,text='Exit',font=(font_slova,12),bg='black',fg='white',command=profil_prozor.destroy)
    exit_btn.grid(row=4,column=2)

    

#promjena korisnickih podataka   
def azuriraj_podatke():


            database_name = 'PyFloraUsers.db'

            update_table_query = '''UPDATE Users
                                    SET username=?,
                                        password=?
                                    WHERE email=?
            '''

            novi_username = novo_kor_ime_var.get()
            nova_sifra = nova_sifra_var.get()
            email = provjera_email_var.get()

            try: 
                sqliteConnection = sqlite3.connect(database_name)
                cursor = sqliteConnection.cursor()
                print("Baza je uspješno kreirana!")
                cursor.execute(update_table_query,(novi_username,nova_sifra,email))
                sqliteConnection.commit()
                print("Kreirana je nova tablica Users")
                cursor.close()
                print("Resursi objekta cursor uspješno su otpušteni")

            except sqlite3.Error as error:
                print("Dogodila se pogreška prilikom spajanja na SQLite: ", error)

            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("SQL konekcija je uspješno zatvorena!")    

def delete_user():


            database_name = 'PyFloraUsers.db'

            delete_table_query = '''DELETE FROM Users
                                    WHERE email=?
            '''

            email = provjera_email_var.get()

            try: 
                sqliteConnection = sqlite3.connect(database_name)
                cursor = sqliteConnection.cursor()
                print("Baza je uspješno kreirana!")
                cursor.execute(delete_table_query,(email,))
                sqliteConnection.commit()
                print("Kreirana je nova tablica Users")
                cursor.close()
                print("Resursi objekta cursor uspješno su otpušteni")
                tkinter.messagebox.showinfo('Uspjeh','Korisnicki profil izbrisan!')

            except sqlite3.Error as error:
                print("Dogodila se pogreška prilikom spajanja na SQLite: ", error)
                tkinter.messagebox.showerror(f'Greska',{error})

            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("SQL konekcija je uspješno zatvorena!") 

#provjera korisnika kod logina
def provjera_korisnik():
    ime = kor_ime_var.get()
    sifra=sifra_var.get()

    conn= sqlite3.connect('PyFloraUsers.db')
    c=conn.cursor()
    c.execute("SELECT * FROM Users WHERE username=? AND password=?",(ime,sifra))
    provjera = c.fetchone()
    if provjera:
        tkinter.messagebox.showinfo('Success',f'Welcome {ime}')


        kor_ime_var.set('')
        sifra_var.set('')
        dalje=ctk.CTkButton(root,text='Dalje',bg_color='white',fg_color='red',command=novi_prozor)
        dalje.grid(column=4,row=4)
        #dalje.bind('<Button-1>',novi_prozor)
    else:
        tkinter.messagebox.showwarning('Ups! ','Niste korisnik')
    kor_ime_var.set('')
    sifra_var.set('')

            
def set_prikaz_lozinke():
    if switch_sifra.get()== 'prikazi':
        entry_sifra.config(show="")
    else:
        entry_sifra.config(show='*')

#API WEATHER
profin_api='c94a2499bf7fc730cc0e2d7777112526'   
lat = 43.508133
lon = 16.440193
#current time
#current_time = datetime.datetime.now()
#unix_time = calendar.timegm(current_time.utctimetuple())



lat = [44.86833,45.23878,45.33673,45.09485,45.40788,45.40837,45.27602,45.12284,45.14391,44.95896,]
lon = [13.84806,13.93497,13.82821,14.12319,13.96559,13.65914,13.71887,13.83850,13.90868,13.85134]
#current time
current_time = datetime.datetime.utcnow()
unix_time = calendar.timegm(current_time.utctimetuple())
unix_dates=[unix_time - 7200,unix_time - 3600,unix_time]


#uzimanje podataka sa weather stranice kao simulaciju ocitavanja senzora
def nabavljanje_podataka(current_data,city_name):
    global data
    temp = current_data['temp'] - 273.15
    humidity=current_data['humidity']
    dt=current_data['dt']
    izlaz_sunca = current_data['sunrise']
    zalaz_sunca = current_data['sunset']
    description=current_data['weather'][0]['description']

    if unix_time<zalaz_sunca and unix_time>izlaz_sunca:
        if description == 'clear sky':
            svjetlost = 'velika'
        else:
            svjetlost='srednja'
    else:
        svjetlost='mala'
    

    data=[round(temp,2),humidity,dt,city_name,
    datetime.datetime.strftime(datetime.datetime.fromtimestamp(dt),'%Y-%m-%d %H:%M:%S'),svjetlost]

    return data
#punjenje dataframea svaki put kada korisnik pritisne sync button
def sync():
    conn= sqlite3.connect('Posude_i_biljke.db')
    c=conn.cursor()
    
    i = 0
    for pos in posude:
        
        data_frame_list=[]
        

        posuda_result = json.loads(requests.get(f'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat[i]}&lon={lon[i]}&dt={unix_time}&appid={profin_api}').text)
        #for i in range(len(posuda_result['current'])):
        temp_df = nabavljanje_podataka(posuda_result['current'], pos)
    
            
            
        data_frame_list.append(temp_df)
        i+=1
    
        headings = ['temp', 'humidity', 'dt', 'ime_posude', 'day','svjetlost']       
        data_frame = pd.DataFrame(data_frame_list, columns=headings)

        #data_frame.to_csv(f'df_{posuda}.csv', mode='w')
        
        data_frame.to_sql('Posude',conn,if_exists='append',index=False)
        
    
##konvertiranje slika u binary tako da ih mozemo spremiti u bazu te ih poslije putem funkcije prebacimo iz binary u img
def baza_posude():
    baza = sqlite3.connect('Posude_i_biljke.db')
    baza.execute('CREATE TABLE IF NOT EXISTS Posude(ime_posude TEXT NOT NULL,temp REAL, humidity REAL,dt INTEGER, day TEXT,svjetlost TEXT NOT NULL)')
    baza.execute('CREATE TABLE IF NOT EXISTS Biljke(biljka_id INTEGER PRIMARY KEY AUTOINCREMENT,ime_biljke TEXT NOT NULL,slika BLOB)')

    for ime in lista_imena:
        
        baza.execute('INSERT INTO Biljke(ime_biljke,slika) Values(?,?)',(ime,convertToBinaryData('slike/'+ime +'.jpg')))
    baza.commit()
#baza_posude() 




    
#VARIJABLE
lista_biljaka_var = tk.Variable(value=lista_imena)
sifra_var = tk.StringVar()
kor_ime_var = tk.StringVar()
sakrij_lozinku = tk.StringVar()
prikazi_lozinku_var = tk.StringVar()
email_var = tk.StringVar()
prikazi_lozinku_var.set('prikazi')
izbor_biljke = tk.StringVar()
izbor_posude = tk.StringVar()




#izgled prve stranic
root.title('PyFlora')
ikonica = tk.PhotoImage(file='ikona1.png')
root.iconphoto(True,ikonica)

root.geometry('800x600')
bg_label = tk.Label(root,image=ikonica)
bg_label.place(x=100,y=0,width='800')
font_slova = 'Ink Free'
main_label = tk.Label(root,text='Prijava',fg = 'black',font=(font_slova,25))
main_label.grid(row=1,column=1)

ime_label = tk.Label(root,text='Unesite korisnicko ime',fg='black',font=(font_slova,15))
ime_label.grid(row=2,column=0)
sifra_label = tk.Label(root,text='Unesite vasu sifru',fg='black',font=(font_slova,15))
sifra_label.grid(row=3,column=0)
entry_ime = tk.Entry(relief=tk.RAISED,textvariable=kor_ime_var)
entry_ime.grid(row=2,column=1)
entry_sifra = tk.Entry(relief=tk.RAISED,textvariable=sifra_var)
entry_sifra.grid(row=3,column=1)


switch_sifra = ctk.CTkSwitch(root,text='Sakrij lozinku',command=set_prikaz_lozinke,variable=prikazi_lozinku_var,onvalue='prikazi',offvalue='sakrij')
switch_sifra.grid(row=4,column=0)


login= tk.Button(root,text='Login',font=(font_slova,10),command=provjera_korisnik)
login.grid(row=4,column=1,padx=5,pady=5)

signup = tk.Button(root,text='Sign Up',font=(font_slova,10),command=signup)
signup.grid(row=5,column=1)




root.mainloop()