import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class RegistrationSystem:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('students.db')
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao banco de dados: {e}")
            return

        self.root = tk.Tk()
        self.root.title("Sistema de Registro de Alunos - Gitel")
        self.root.geometry("600x400")

        # Interface
        tk.Label(self.root, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nome_entry = tk.Entry(self.root, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="E-mail:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Nível de Inglês:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nivel_entry = tk.Entry(self.root, width=30)
        self.nivel_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="ID (para atualizar/excluir):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self.root, width=30)
        self.id_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Adicionar", command=self.add_student).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Visualizar", command=self.view_students).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Atualizar", command=self.update_student).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Excluir", command=self.delete_student).grid(row=5, column=1, padx=5, pady=5)

        # Tabela
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "E-mail", "Nível"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("E-mail", text="E-mail")
        self.tree.heading("Nível", text="Nível")
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=150)
        self.tree.column("E-mail", width=200)
        self.tree.column("Nível", width=100)
        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configurar redimensionamento
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS students
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 nome TEXT NOT NULL,
                                 email TEXT NOT NULL,
                                 nivel TEXT NOT NULL)''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao criar tabela: {e}")

    def add_student(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        nivel = self.nivel_entry.get().strip()

        if not nome or not email or not nivel:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Aviso", "Digite um e-mail válido!")
            return

        try:
            self.cursor.execute("INSERT INTO students (nome, email, nivel) VALUES (?, ?, ?)",
                              (nome, email, nivel))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
            self.clear_entries()
            self.view_students()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao adicionar aluno: {e}")

    def view_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.cursor.execute("SELECT * FROM students")
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao visualizar alunos: {e}")

    def update_student(self):
        id_str = self.id_entry.get().strip()
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        nivel = self.nivel_entry.get().strip()

        if not id_str or not nome or not email or not nivel:
            messagebox.showwarning("Aviso", "Preencha todos os campos, incluindo o ID!")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Aviso", "Digite um e-mail válido!")
            return

        try:
            id_aluno = int(id_str)
            self.cursor.execute("UPDATE students SET nome = ?, email = ?, nivel = ? WHERE id = ?",
                              (nome, email, nivel, id_aluno))
            if self.cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "ID não encontrado!")
            else:
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                self.clear_entries()
                self.view_students()
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao atualizar aluno: {e}")

    def delete_student(self):
        id_str = self.id_entry.get().strip()

        if not id_str:
            messagebox.showwarning("Aviso", "Digite o ID do aluno!")
            return

        try:
            id_aluno = int(id_str)
            self.cursor.execute("DELETE FROM students WHERE id = ?", (id_aluno,))
            if self.cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "ID não encontrado!")
            else:
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                self.clear_entries()
                self.view_students()
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao excluir aluno: {e}")

    def clear_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.nivel_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

if __name__ == "__main__":
    try:
        app = RegistrationSystem()
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Falha ao iniciar o programa: {e}")