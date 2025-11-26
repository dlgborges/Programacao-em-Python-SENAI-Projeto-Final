import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter


def conectar():
    return sqlite3.connect('C:/Users/Aluno/Downloads/Programacao-em-Python-SENAI-Projeto-Final/banco.db')


def criar_tabela():
    conn =  conectar()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes(
              nome TEXT,
              email TEXT,
              telefone TEXT,
              endereco TEXT
              )''')
    conn.commit()
    conn.close()


# create
def inserir_usuario():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    endereco = endereco_entry.get()

    if nome and email and telefone and endereco:
        conn =  conectar()
        c = conn.cursor()
        c.execute("INSERT INTO clientes VALUES(?,?,?,?)", (nome, email, telefone, endereco))
        conn.commit()
        conn.close()   
        messagebox.showinfo('', 'DADOS INSERIDOS COM SUCESSO!')
        
        #clear all entry_boxes - final version
        clear_entry_boxes([nome_entry, email_entry, telefone_entry, endereco_entry])
        
        # #teste para limpar os campos após a inserção bem sucedida do novo usuário
        # nome_entry.delete(0, tk.END)
        
        # # executa a mesma acao acima, encapsulado em uma funcao
        # clear_entry_box(email_entry)
        # clear_entry_box(telefone_entry)
        # clear_entry_box(endereco_entry)
        mostrar_usuario()
    else:
        messagebox.showwarning('','INSIRA TODOS OS DADOS SOLICITADOS')


def clear_entry_box(box_name):
    box_name.delete(0, tk.END)


def clear_entry_boxes(entry_boxes):
    for entry_box in entry_boxes:
        clear_entry_box(entry_box)


# read 
def mostrar_usuario(): 
    for row in tree.get_children():
        tree.delete(row)
        
    conn =  conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert("", "end",values = (cliente[0], cliente[1], cliente[2], cliente[3]))
    conn.close()    


# atualizar
def atualizar():
    selecao = tree.selection()
    if selecao:
        dado_edit = tree.item(selecao)['values'][2]
        novo_nome = nome_entry.get()
        novo_email = email_entry.get()
        novo_telefone = telefone_entry.get()
        novo_endereco = endereco_entry.get()

        if novo_nome and  novo_email and novo_telefone and novo_endereco:
            conn =  conectar()
            c = conn.cursor()
            c.execute("UPDATE clientes SET  nome = ?, email = ? , telefone =?, endereco=? WHERE telefone = ? ", (novo_nome, novo_email, novo_telefone, novo_endereco, dado_edit))
            conn.commit()
            conn.close()   
            messagebox.showinfo('', 'DADOS ATUALIZADOS COM SUCESSO!')
            #clear all entry_boxes - final version
            clear_entry_boxes([nome_entry, email_entry, telefone_entry, endereco_entry])
            mostrar_usuario()
        else:
            messagebox.showwarning('','TODOS OS DADOS PRECISAM SER PREENCHIDOS ')


# delete 
def delete_usuario():
    selecao = tree.selection()
    if selecao:
        user_del = tree.item(selecao)['values'][2]
        conn =  conectar()
        c = conn.cursor()     
        c.execute("DELETE FROM clientes WHERE telefone = ?", (user_del,))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'CLIENTE DELETADO COM SUCESSO')
        #clear all entry_boxes - final version
        clear_entry_boxes([nome_entry, email_entry, telefone_entry, endereco_entry])
        mostrar_usuario()
    else:
        messagebox.showerror('', 'ERRO AO DELETAR O CLIENTE')    


# interface grafica
# grid  

janela =  customtkinter.CTk()
janela.configure(fg_color='gray')
janela.title('XYZ Comércio - CRM')
janela.geometry('700x630')
caminho = 'icons/systemfilemanager.ico'
janela.iconbitmap(caminho)


tk.Label(janela, text = 'XYZ Comércio - Gerenciamento de Clientes', font=('arial', 15)).grid(row=0, column=0, pady=10, padx=10)


fr0 =  customtkinter.CTkFrame(janela)
fr0.grid(columnspan=3)

#nome do cliente
nome_label =  tk.Label(fr0, text='Nome', font=('arial', 15))
nome_label.grid(row=0, column=0, pady=10, padx=10)

nome_entry = tk.Entry(fr0, font=('arial', 15))
nome_entry.grid(row=0, column=1, pady=10, padx=10)

#email
email_label =  tk.Label(fr0, text='Email', font=('arial', 15))
email_label.grid(row=1, column=0, pady=10, padx=10)

email_entry = tk.Entry(fr0, font=('arial', 15))
email_entry.grid(row=1, column=1, pady=10, padx=10)

#telefone
telefone_label =  tk.Label(fr0, text='Telefone', font=('arial', 15))
telefone_label.grid(row=2, column=0, pady=10, padx=10)

telefone_entry = tk.Entry(fr0, font=('arial', 15))
telefone_entry.grid(row=2, column=1, pady=10, padx=10)

#Endereco
endereco_label =  tk.Label(fr0, text='Endereço', font=('arial', 15))
endereco_label.grid(row=3, column=0, pady=10, padx=10)

endereco_entry = tk.Entry(fr0, font=('arial', 15))
endereco_entry.grid(row=3, column=1, pady=10, padx=10)


fr =  customtkinter.CTkFrame(janela)
fr.grid( columnspan=2)


btn_salvar =  customtkinter.CTkButton(fr, text= 'SALVAR', font=('arial', 15), command=inserir_usuario, fg_color='purple')
btn_salvar.grid(row=5, column=0, padx=10, pady=10)

btn_atualizar =  customtkinter.CTkButton(fr, text= 'ATUALIZAR', font=('arial', 15), command=atualizar,fg_color='purple')
btn_atualizar.grid(row=5, column=2, padx=10, pady=10)

btn_delete =  customtkinter.CTkButton(fr, text= 'DELETAR', font=('arial', 15), command=delete_usuario, fg_color='purple')
btn_delete.grid(row=5, column=3, padx=10, pady=10)

fr2 = customtkinter.CTkFrame(janela)
fr2.grid( columnspan=2)

colunas = ('Nome', 'email', 'Telefone', 'Endereço')
tree =  ttk.Treeview(fr2, columns=colunas, show='headings', height=40)
tree.grid(row=6, column=0,padx=5, sticky='nsew')


for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor= tk.CENTER)

criar_tabela()
mostrar_usuario()

janela.mainloop()
