from tkinter import Tk
import customtkinter
import tkinter.messagebox
import string
import random
import threading
import pyperclip  # Adicionando a importação do módulo pyperclip
import tkinter as tk  # Alterando a importação para incluir o alias "tk"
import platform

# Classe principal do aplicativo de gerador de senhas ------------------------------------------------------
class PasswordGeneratorApp:
    def __init__(self, janela):
        # Configurações iniciais da janela
        self.master = janela
        janela.geometry('450x300+100+100')
        janela.resizable(False, False)
        janela.title('Gerador de senhas © Dev Joel')
        janela.iconbitmap(r'C:\Users\HP\Desktop\Programas em python\gerador de senhas\Password.ico')

         # Verificar a arquitetura do sistema
        if platform.architecture()[0] != '64bit':
            tkinter.messagebox.showerror('Erro', 'Este aplicativo é compatível apenas com plataformas x64.')
            janela.destroy()
            return  
 
        # Variáveis de controle para opções de senha
        self.letras_maiusculas_var = customtkinter.StringVar()
        self.letras_minusculas_var = customtkinter.StringVar()
        self.caracteres_especiais_var = customtkinter.StringVar()
        self.numeros_var = customtkinter.StringVar()

        # Criar a caixa de texto para inserir caracteres da senha
        self.caracteres = customtkinter.CTkEntry(janela, width=400, placeholder_text='Caracteres da Senha')
        self.caracteres.place(x=10, y=30)

        # Criar as checkboxes para selecionar tipos de caracteres
        customtkinter.CTkCheckBox(janela, text='Letras Maiúsculas', variable=self.letras_maiusculas_var, command=self.atualizar_senha).place(x=10, y=70)
        customtkinter.CTkCheckBox(janela, text='Letras Minúsculas', variable=self.letras_minusculas_var, command=self.atualizar_senha).place(x=10, y=110)
        customtkinter.CTkCheckBox(janela, text='Caracteres Especiais', variable=self.caracteres_especiais_var, command=self.atualizar_senha).place(x=10, y=150)
        customtkinter.CTkCheckBox(janela, text='Números', variable=self.numeros_var, command=self.atualizar_senha).place(x=10, y=190)

        # Criar o rótulo para exibir o número de caracteres
        self.Lcaracteres = customtkinter.CTkLabel(janela, text='Numero de caracteres: 0')
        self.Lcaracteres.place(x=10, y=230)

        # Criar o controle deslizante para selecionar o comprimento da senha
        self.Scaracteres = customtkinter.CTkSlider(janela, from_=0, to=255, width=400, command=self.atualizar_senha)
        self.Scaracteres.place(x=10, y=260)

        # Criar o botão para gerar senha
        customtkinter.CTkButton(janela, text='Gerar senha', command=self.gerar_senha_threaded).place(x=265, y=70)
        customtkinter.CTkButton(janela, text='Copiar Senha', command=self.copiar_senha).place(x=265, y=100)

        # Inicializar senha ao abrir o aplicativo
        self.atualizar_senha()
#--------------------------------------------------------------------------------------------------------------------
 # Método para gerar a senha com base nas opções selecionadas -------------------------------------------------------
    def gerar_senha(self):
        comprimento_senha = int(self.Scaracteres.get())

        letras_maiusculas = string.ascii_uppercase if self.letras_maiusculas_var.get() == "1" else ''
        letras_minusculas = string.ascii_lowercase if self.letras_minusculas_var.get() == "1" else ''
        caracteres_especiais = '!@#$%^&*()' if self.caracteres_especiais_var.get() == "1" else ''
        numeros = string.digits if self.numeros_var.get() == "1" else ''

        caracteres_permitidos = letras_maiusculas + letras_minusculas + caracteres_especiais + numeros

        # Verificar se pelo menos um tipo de caractere foi selecionado
        if not caracteres_permitidos:
            tkinter.messagebox.showinfo('Aviso', 'Selecione pelo menos um tipo de caractere.')
            return

        # Gerar a senha e atualizar a caixa de texto e o rótulo
        senha = ''.join(random.choice(caracteres_permitidos) for _ in range(comprimento_senha))

        self.caracteres.delete(0, "end")
        self.caracteres.insert(0, senha)
        self.Lcaracteres.configure(text=f'Numero de caracteres: {comprimento_senha}')

    # Método para gerar a senha em uma thread separada
    def gerar_senha_threaded(self):
        threading.Thread(target=self.gerar_senha).start()

    # Método para atualizar a senha quando as opções são modificadas
    def atualizar_senha(self, event=None):
        self.gerar_senha()
#-----------------------------------------------------------------------------------------------------------------        
# Método para copiar a senha para a área de transferência --------------------------------------------------------
    def copiar_senha(self):
        # Obter a senha atual da entrada
        senha = self.caracteres.get()

        # Verificar se há uma senha para copiar
        if senha:
            # Usar o módulo pyperclip para copiar a senha para a área de transferência
            pyperclip.copy(senha)
            tkinter.messagebox.showinfo('Copiado', 'Senha copiada para a área de transferência.')
        else:
            tkinter.messagebox.showinfo('Aviso', 'Não há senha para copiar.')
#-----------------------------------------------------------------------------------------------------------------            
# Execução do aplicativo quando o script é executado -------------------------------------------------------------
if __name__ == "__main__":
    janela = customtkinter.CTk()
    app = PasswordGeneratorApp(janela)
    janela.mainloop()
#-----------------------------------------------------------------------------------------------------------------