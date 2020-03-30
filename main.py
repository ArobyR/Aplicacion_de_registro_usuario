""" AUTHOR == Gr0b1t:
                    @Aroby
"""

from tkinter import messagebox
from tkinter import *
import sqlite3
from sqlite3 import Error

root = Tk()
root.title("Aplicacion de registro simple")
img = Image("photo", file="image.png")
root.tk.call('wm', 'iconphoto', root._w, img)
my_frame = Frame(root, width=600, height=600)
my_frame.pack(anchor="n")

asocia_id = StringVar() # Variables asociativa
asocia_nombre = StringVar()
asocia_password = StringVar()
asocia_apellido = StringVar()
asocia_direccion = StringVar()

# ------------------------------- Borrar campos ---------------------------
def clear():
    asocia_id.set("")
    asocia_nombre.set("")
    asocia_password.set("")
    asocia_apellido.set("")
    asocia_direccion.set("")
    
# -------------------------------- Funcion conectar -----------------------
def conectarDB():
    try:
        my_connect = sqlite3.connect("usuarios.db")
        Cursor = my_connect.cursor()

        Cursor.execute('''
            CREATE TABLE USUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDO VARCHAR(10),
            DIRECCION VARCHAR(50))   
        ''')
        my_connect.close()
        messagebox.showinfo("Aviso", "Base de datos creada con exito")
    except sqlite3.OperationalError: # Error
        # Mensaje de error si la base de datos ya existe
        messagebox.showwarning("Aviso", "La base de datos ya exite")

# ------------------------------- Crear usuario ---------------------------
def create_user():
    nombre_user = asocia_nombre.get() 
    contraseña = asocia_password.get()
    apellido = asocia_apellido.get()
    direccion = asocia_direccion.get()
                                            
    try:
        my_connect = sqlite3.connect("usuarios.db")
        Cursor = my_connect.cursor()
        #datos = [(nombre_user), (contraseña), (apellido), (direccion)]
        datos1 = [(nombre_user, contraseña, apellido, direccion)]
        Cursor.executemany("INSERT INTO usuarios VALUES(NULL, ?, ?, ?, ?)", datos1)
        my_connect.commit()
        Cursor.close()
        my_connect.close()
        clear()
        messagebox.showinfo("Aviso", "Registro creado con exito")
    except sqlite3.OperationalError:
        # Mensaje de base datos no encontrada 
        messagebox.showwarning("Error", "Base de datos no encontrada")

# ------------------------------- Leer datos ------------------------------
# Leer datos y devolverlos 
def read_datesDB():
    try:
        my_connect = sqlite3.connect("usuarios.db")
        Cursor = my_connect.cursor()
        Cursor.execute("SELECT * FROM usuarios WHERE ID=" + asocia_id.get())
        retornar = Cursor.fetchall()
        for usuario in retornar:
            asocia_id.set(usuario[0])
            asocia_nombre.set(usuario[1])
            asocia_password.set(usuario[2])
            asocia_apellido.set(usuario[3])
            asocia_direccion.set(usuario[4]) 
        my_connect.commit()
    except sqlite3.OperationalError:
    # Mensaje de base datos no encontrada 
        messagebox.showwarning("Error", "Campos vacios o base de datos no encontrada")

def back_application():
    value = messagebox.askokcancel("Salir", "¿Quieres salir de la aplicacion?")
    if value == True:
        root.destroy()

# ------------------------------- Actualizar ------------------------------
def actualizar():
    try:        
        my_connect = sqlite3.connect("usuarios.db")
        Cursor = my_connect.cursor()
        datos = asocia_nombre.get(), asocia_password.get(), asocia_apellido.get(), asocia_direccion.get()
        Cursor.execute ("UPDATE USUARIOS SET NOMBRE_USUARIO=?, PASSWORD=?, APELLIDO=?, DIRECCION=?" +
        "WHERE ID=" + asocia_id.get(), datos)
        my_connect.commit()
        messagebox.showinfo("Aviso", "Registro actualizado con exito")
    except sqlite3.OperationalError:
    # Mensaje de base datos no encontrada 
        messagebox.showwarning("Error", "Campos vacios o base de datos no encontrada")

# ------------------------------- eliminar --------------------------------
def eliminar():
    try:
        my_connect = sqlite3.connect("usuarios.db")
        Cursor = my_connect.cursor()

        Cursor.execute("DELETE FROM usuarios WHERE ID=" + asocia_id.get())    
        my_connect.commit()
        messagebox.showinfo("Aviso", "Registro borrado con exito")
        clear()
    except sqlite3.OperationalError:
        # Mensaje de base datos no encontrada 
        messagebox.showwarning("Error", "Campos vacios o base de datos no encontrada")

def ayuda():
    messagebox.showinfo("Información", "Esta es una aplicacion simple de registro de usuarios")

# ------------------------------- Menu superior ---------------------------
menubar = Menu(root)
root.config(menu=menubar) # lo asignamos a la base / raiz

# sub menus, son menus perteneciente a menubar
conection_menu = Menu(menubar, tearoff=0)
delete_menu = Menu(menubar, tearoff=0)
crud_menu = Menu(menubar, tearoff=0)
help_menu = Menu(menubar, tearoff=0)

# add to bar menu
menubar.add_cascade(label="BBDD", menu=conection_menu)
menubar.add_cascade(label="BORRAR", menu=delete_menu, command=eliminar)
menubar.add_cascade(label="CRUD", menu=crud_menu)
menubar.add_cascade(label="Ayuda", menu=help_menu)

# elements conection menu
conection_menu.add_command(label="Conectar", command=conectarDB)
conection_menu.add_separator()
conection_menu.add_command(label="Salir", command=back_application) 

delete_menu.add_command(label="Borrar campos", command=clear) 

crud_menu.add_command(label="Crear", command=create_user)            
crud_menu.add_command(label="Actualizar", command=actualizar)     
crud_menu.add_separator()
crud_menu.add_command(label="Borrar")

help_menu.add_command(label="Acerca de...", command=ayuda)  # element help menu

# ------------------------------- Textos interfaz -------------------------
id_texto = Label(my_frame, text="ID:")
id_texto.grid(row=0, column=1, pady=5, padx=2, sticky="e")
id_texto.config(font=15)

nombre_usuario_texto = Label(my_frame, text="Nombre:")
nombre_usuario_texto.grid(row=1, column=1, pady=5, sticky="e")
nombre_usuario_texto.config(font=15)

password_texto = Label(my_frame, text="Password:")
password_texto.grid(row=2, column=1, pady=5, sticky="e")
password_texto.config(font=15)

apellido_texto = Label(my_frame, text="Apellido:")
apellido_texto.grid(row=3, column=1, pady=5, sticky="e")
apellido_texto.config(font=15)

direccion_texto = Label(my_frame, text="Direccion:")
direccion_texto.grid(row=4, column=1, pady=5, sticky="e")
direccion_texto.config(font=15)

# ------------------------------ Entrys ----------------------------------
id_entry = Entry(my_frame, textvariable=asocia_id)
id_entry.grid(row=0, column=2, pady=10)
id_entry.config(font=15) # state = DISABLED

nombre_entry = Entry(my_frame, textvariable=asocia_nombre)
nombre_entry.grid(row=1, column=2, padx=5)
nombre_entry.config(font=15)

password_entry = Entry(my_frame, textvariable=asocia_password)
password_entry.grid(row=2, column=2)
password_entry.config(show="*")
password_entry.config(font=15)

apellido_entry = Entry(my_frame, textvariable=asocia_apellido)
apellido_entry.grid(row=3, column=2)
apellido_entry.config(font=15)

direccion_entry = Entry(my_frame, textvariable=asocia_direccion)
direccion_entry.grid(row=4, column=2)
direccion_entry.config(font=15)

# ---------------------------- Botones inferiores ------------------------
my_frame2 = Frame(root, width=600, height=600)
my_frame2.pack()

create_button = Button(my_frame2, text="CREATE", fg="green", command=create_user)
create_button.grid(row=5, column=1, padx=9, pady=25)

read_button = Button(my_frame2, text="READ", fg="blue", command=read_datesDB)
read_button.grid(row=5, column=2, padx=9)

update_button = Button(my_frame2, text="UPDATE", command=actualizar)
update_button.grid(row=5, column=3, padx=9)

delete_button = Button(my_frame2, text="DELETE", fg="red", command=eliminar)
delete_button.grid(row=5, column=4, padx=9)

root.mainloop()