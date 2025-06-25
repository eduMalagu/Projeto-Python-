from tkinter import *
from tkinter import messagebox
import webbrowser
from datetime import datetime
import os

co1 = "#211A1A"
co2 = "#4a90e2"
co3 = "#2ca88d"
co4 = "#ff0000"

usuarios = {}
tentativas = 0
max_tentativas = 3

def carregar_usuarios():
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as f:
            for linha in f:
                nome, senha = linha.strip().split(";")
                usuarios[nome] = senha
carregar_usuarios()

def salvar_usuario(nome, senha):
    with open("usuarios.txt", "a") as f:
        f.write(f"{nome};{senha}\n")

def registrar_tentativa(usuario, sucesso):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log_tentativas.txt", "a") as f:
        status = "SUCESSO" if sucesso else "FALHA"
        f.write(f"{agora} - {usuario} - {status}\n")

def criar_login():
    global janela, entrada_nome, entrada_senha, mensagem, botao_login

    janela = Tk()
    janela.title("Tela de Login")
    janela.geometry("400x420")
    janela.configure(bg=co1)
    janela.resizable(False, False)

    Frame_cima = Frame(janela, width=380, height=150, bg=co1)
    Frame_cima.place(x=10, y=10)
    Label(Frame_cima, text="LOGIN", font=("Ivy", 30, 'bold'), bg=co1, fg=co4).place(relx=0.5, rely=0.5, anchor=CENTER)

    Frame_baixo = Frame(janela, width=380, height=230, bg=co1)
    Frame_baixo.place(x=10, y=170)

    Label(Frame_baixo, text="Usuário:", font=("Ivy", 13), bg=co1, fg="white").place(x=20, y=10)
    entrada_nome = Entry(Frame_baixo, width=30, font=("Ivy", 14), relief=FLAT)
    entrada_nome.place(x=20, y=35)

    Label(Frame_baixo, text="Senha:", font=("Ivy", 13), bg=co1, fg="white").place(x=20, y=75)
    entrada_senha = Entry(Frame_baixo, show="*", width=30, font=("Ivy", 14), relief=FLAT)
    entrada_senha.place(x=20, y=100)

    botao_login = Button(Frame_baixo, text="Entrar", width=30, bg=co2, fg="white", font=("Ivy", 12, 'bold'),
                         relief=FLAT, command=verificar_login)
    botao_login.place(x=20, y=140)

    Button(Frame_baixo, text="Resetar Tentativas", width=18, bg="#666", fg="white", font=("Ivy", 10),
           command=resetar_tentativas).place(x=220, y=175)

    Button(Frame_baixo, text="Cadastrar", width=18, bg=co3, fg="white", font=("Ivy", 10),
           command=abrir_cadastro).place(x=20, y=175)

    mensagem = Label(Frame_baixo, text="", font=("Ivy", 11), bg=co1, fg=co4)
    mensagem.place(x=20, y=210)

    janela.mainloop()

def resetar_tentativas():
    global tentativas
    tentativas = 0
    mensagem.config(text="")
    botao_login.config(state=NORMAL)
    entrada_senha.config(bg="white")

def verificar_login():
    global tentativas
    usuario = entrada_nome.get()
    senha = entrada_senha.get()

    if usuario in usuarios and senha == usuarios[usuario]:
        registrar_tentativa(usuario, True)
        criar_dashboard(usuario)
        tentativas = 0
    else:
        tentativas += 1
        registrar_tentativa(usuario, False)
        mensagem.config(text=f"Tentativa {tentativas}/{max_tentativas}")
        entrada_senha.config(bg="#ffe6e6")
        if tentativas == 1:
            webbrowser.open("https://www.youtube.com/watch?v=o079Yest154")
        elif tentativas == 2:
            webbrowser.open("https://www.youtube.com/watch?v=uM6XdDfvqd4")
        elif tentativas >= max_tentativas:
            mensagem.config(text="Número máximo de tentativas.")
            botao_login.config(state=DISABLED)

def abrir_cadastro():
    def cadastrar_usuario():
        nome = novo_nome.get()
        senha = nova_senha.get()

        if nome in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
        elif nome == "" or senha == "":
            messagebox.showerror("Erro", "Preencha todos os campos.")
        else:
            usuarios[nome] = senha
            salvar_usuario(nome, senha)
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            cadastro.destroy()

    cadastro = Toplevel(janela)
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("300x220")
    cadastro.configure(bg=co1)

    Label(cadastro, text="Novo usuário:", font=("Ivy", 12), bg=co1, fg="white").pack(pady=5)
    novo_nome = Entry(cadastro, width=30, font=("Ivy", 12))
    novo_nome.pack(pady=5)

    Label(cadastro, text="Nova senha:", font=("Ivy", 12), bg=co1, fg="white").pack(pady=5)
    nova_senha = Entry(cadastro, show="*", width=30, font=("Ivy", 12))
    nova_senha.pack(pady=5)

    Button(cadastro, text="Cadastrar", bg=co2, fg="white", font=("Ivy", 12, 'bold'),
           command=cadastrar_usuario).pack(pady=10)

def criar_dashboard(usuario):
    janela.withdraw()
    dash = Toplevel()
    dash.title("Painel")
    dash.geometry("700x600")
    dash.configure(bg=co1)

    Label(dash, text=f"Bem-vindo, {usuario}!", font=("Ivy", 16, 'bold'), bg=co1, fg="white").pack(pady=10)

    frame_cards = Frame(dash, bg=co1)
    frame_cards.pack(pady=20)

    videos = [
        ("Vídeo 1", "https://www.youtube.com/watch?v=eVftah6DU6k"),
        ("Vídeo 2", "https://www.youtube.com/watch?v=OrvxyaUN90Y"),
        ("Vídeo 3", "https://www.youtube.com/watch?v=wy-djZ0EZhI"),
        ("Vídeo 4", "https://www.youtube.com/watch?v=CTVGrg_gGgE"),
        ("Vídeo 5", "https://www.youtube.com/watch?v=ah_3uKxdOjM"),
        ("Vídeo 6", "https://www.youtube.com/watch?v=wmFJ9D3c55o"),
    ]

    for titulo, link in videos:
        criar_card(frame_cards, titulo, link)

    botao_imc = Button(dash, text="Calculadora IMC", command=abrir_tela_imc, bg=co3, fg="white", font=("Ivy", 12, 'bold'))
    botao_imc.pack(pady=5)

    botao_conversor = Button(dash, text="Conversor de Moedas", command=abrir_tela_conversor, bg=co2, fg="white", font=("Ivy", 12, 'bold'))
    botao_conversor.pack(pady=5)

    botao_quiz_dificil = Button(dash, text="Quiz Difícil", command=abrir_quiz_dificil, bg="#8833cc", fg="white", font=("Ivy", 12, 'bold'))
    botao_quiz_dificil.pack(pady=5)

def criar_card(parent, titulo, link):
    card = Frame(parent, width=150, height=80, bg="white", highlightbackground=co4, highlightthickness=1)
    card.pack(side=LEFT, padx=10)

    label = Label(card, text=titulo, font=("Ivy", 12), bg="white", fg=co4)
    label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def abrir(e):
        webbrowser.open(link)

    card.bind("<Button-1>", abrir)
    label.bind("<Button-1>", abrir)

def abrir_tela_imc():
    imc = Toplevel()
    imc.title("Calculadora de IMC")
    imc.geometry("300x250")
    imc.configure(bg=co1)

    Label(imc, text="Peso (kg):", bg=co1, fg="white", font=("Ivy", 12)).pack(pady=5)
    peso = Entry(imc, font=("Ivy", 12))
    peso.pack()

    Label(imc, text="Altura (m):", bg=co1, fg="white", font=("Ivy", 12)).pack(pady=5)
    altura = Entry(imc, font=("Ivy", 12))
    altura.pack()

    resultado = Label(imc, text="", font=("Ivy", 12), bg=co1, fg=co4)
    resultado.pack(pady=10)

    def calcular():
        try:
            p = float(peso.get())
            a = float(altura.get())
            imc_valor = p / (a * a)
            resultado.config(text=f"Seu IMC é: {imc_valor:.2f}")
        except:
            resultado.config(text="Erro nos dados!")

    Button(imc, text="Calcular", command=calcular, bg=co2, fg="white", font=("Ivy", 12, 'bold')).pack(pady=5)

def abrir_tela_conversor():
    conv = Toplevel()
    conv.title("Conversor de Moedas")
    conv.geometry("300x220")
    conv.configure(bg=co1)

    Label(conv, text="Valor em Reais:", font=("Ivy", 12), bg=co1, fg="white").pack(pady=5)
    entrada = Entry(conv, font=("Ivy", 12))
    entrada.pack()

    resultado = Label(conv, text="", font=("Ivy", 12), bg=co1, fg=co4)
    resultado.pack(pady=10)

    def converter():
        try:
            real = float(entrada.get())
            dolar = real / 5.0
            euro = real / 5.5
            resultado.config(text=f"Dólar: ${dolar:.2f} | Euro: €{euro:.2f}")
        except:
            resultado.config(text="Erro na conversão!")

    Button(conv, text="Converter", command=converter, bg=co3, fg="white", font=("Ivy", 12, 'bold')).pack(pady=5)


def abrir_quiz_dificil():
    perguntas_dificeis = [
        {"pergunta": "Quem desenvolveu o cálculo infinitesimal simultaneamente a Newton?", "alternativas": ["Leibniz", "Euler", "Descartes", "Gauss"], "resposta": "Leibniz"},
        {"pergunta": "Qual é o valor de π com 5 casas decimais?", "alternativas": ["3.14159", "3.14149", "3.14169", "3.14179"], "resposta": "3.14159"},
        {"pergunta": "Qual elemento tem o símbolo químico 'Sb'?", "alternativas": ["Antimônio", "Prata", "Selênio", "Estrôncio"], "resposta": "Antimônio"},
        {"pergunta": "Qual é a menor unidade de tempo reconhecida?", "alternativas": ["Yoctosegundo", "Nanosegundo", "Planck", "Atosegundo"], "resposta": "Planck"},
        {"pergunta": "Em que país nasceu Nikola Tesla?", "alternativas": ["Croácia", "Sérvia", "Áustria", "Hungria"], "resposta": "Croácia"},
        {"pergunta": "Qual é a distância média da Terra ao Sol?", "alternativas": ["149,6 milhões km", "100 milhões km", "200 milhões km", "300 milhões km"], "resposta": "149,6 milhões km"},
        {"pergunta": "Qual cientista ganhou dois prêmios Nobel em áreas diferentes?", "alternativas": ["Marie Curie", "Einstein", "Bohr", "Hawking"], "resposta": "Marie Curie"},
        {"pergunta": "Quem escreveu 'A República'?", "alternativas": ["Platão", "Sócrates", "Aristóteles", "Demócrito"], "resposta": "Platão"},
        {"pergunta": "O que mede um barômetro?", "alternativas": ["Pressão atmosférica", "Temperatura", "Volume", "Corrente elétrica"], "resposta": "Pressão atmosférica"},
        {"pergunta": "Qual o país com maior número de vulcões ativos?", "alternativas": ["Indonésia", "Japão", "Itália", "Chile"], "resposta": "Indonésia"},
        {"pergunta": "Em que ano caiu o Império Romano do Ocidente?", "alternativas": ["476", "1453", "410", "1492"], "resposta": "476"},
        {"pergunta": "Qual é o nome da teoria que unifica as forças fundamentais da física?", "alternativas": ["Teoria das Cordas", "Relatividade", "Gravidade Quântica", "Campo Unificado"], "resposta": "Teoria das Cordas"},
        {"pergunta": "Qual é o idioma mais falado como língua materna?", "alternativas": ["Chinês Mandarim", "Inglês", "Espanhol", "Hindi"], "resposta": "Chinês Mandarim"},
        {"pergunta": "Quantos cromossomos humanos existem?", "alternativas": ["46", "44", "48", "23"], "resposta": "46"},
        {"pergunta": "Qual o nome do fóton no modelo padrão?", "alternativas": ["Bóson de gauge", "Gluon", "Higgs", "Gráviton"], "resposta": "Bóson de gauge"},
        {"pergunta": "Qual foi a missão que levou o homem à Lua?", "alternativas": ["Apollo 11", "Voyager", "Sputnik", "Challenger"], "resposta": "Apollo 11"},
        {"pergunta": "Quem formulou a Lei da Gravitação Universal?", "alternativas": ["Newton", "Einstein", "Kepler", "Galileu"], "resposta": "Newton"},
        {"pergunta": "Qual é o maior número primo conhecido (em 2023)?", "alternativas": ["2⁸²⁵⁸⁹⁹³³−1", "2⁶⁹⁷²⁵−1", "Mersenne", "Número de Fermat"], "resposta": "2⁸²⁵⁸⁹⁹³³−1"},
        {"pergunta": "Em qual camada da Terra ocorre o movimento das placas tectônicas?", "alternativas": ["Litosfera", "Astenosfera", "Manto", "Crosta"], "resposta": "Litosfera"},
        {"pergunta": "Qual filósofo disse: 'Penso, logo existo'?", "alternativas": ["Descartes", "Kant", "Hume", "Nietzsche"], "resposta": "Descartes"},
        {"pergunta": "Quantos segundos há em um dia?", "alternativas": ["86400", "3600", "604800", "7200"], "resposta": "86400"},
        {"pergunta": "O que significa a sigla 'DNA'?", "alternativas": ["Ácido desoxirribonucleico", "Ácido ribonucleico", "Desoxinucleico ácido", "Desoxiriboácido nucleico"], "resposta": "Ácido desoxirribonucleico"},
        {"pergunta": "Qual é o metal mais leve?", "alternativas": ["Lítio", "Hidrogênio", "Berílio", "Alumínio"], "resposta": "Lítio"},
        {"pergunta": "Maior número de vértices em um poliedro regular?", "alternativas": ["20", "12", "8", "60"], "resposta": "20"},
        {"pergunta": "Quantos bits tem um IPv6?", "alternativas": ["128", "64", "256", "32"], "resposta": "128"},
        {"pergunta": "Qual é o símbolo da constante de Planck?", "alternativas": ["h", "p", "λ", "γ"], "resposta": "h"},
        {"pergunta": "Maior planeta anão do sistema solar?", "alternativas": ["Eris", "Ceres", "Plutão", "Haumea"], "resposta": "Eris"},
        {"pergunta": "Qual país foi a URSS antes da dissolução?", "alternativas": ["União Soviética", "Rússia", "Iugoslávia", "Cazaquistão"], "resposta": "União Soviética"},
        {"pergunta": "Maior osso do corpo humano?", "alternativas": ["Fêmur", "Tíbia", "Úmero", "Costela"], "resposta": "Fêmur"},
        {"pergunta": "Elemento mais abundante no universo?", "alternativas": ["Hidrogênio", "Hélio", "Oxigênio", "Carbono"], "resposta": "Hidrogênio"}
    ]

    def iniciar_quiz():
        quiz = Toplevel()
        quiz.title("Quiz Difícil")
        quiz.geometry("700x400")
        quiz.configure(bg=co1)

        pontuacao = [0]
        pergunta_atual = [0]

        pergunta_label = Label(quiz, text="", font=("Ivy", 14), wraplength=600, bg=co1, fg="white")
        pergunta_label.pack(pady=20)

        botoes = []

        def responder(escolha):
            if escolha == perguntas_dificeis[pergunta_atual[0]]["resposta"]:
                pontuacao[0] += 1
            pergunta_atual[0] += 1
            if pergunta_atual[0] < len(perguntas_dificeis):
                carregar_pergunta()
            else:
                resultado = Toplevel()
                resultado.title("Resultado Final")
                resultado.geometry("300x150")
                Label(resultado, text=f"Pontuação: {pontuacao[0]} de {len(perguntas_dificeis)}", font=("Ivy", 14)).pack(pady=30)

        def carregar_pergunta():
            pergunta = perguntas_dificeis[pergunta_atual[0]]
            pergunta_label.config(text=pergunta["pergunta"])
            for i, btn in enumerate(botoes):
                btn.config(text=pergunta["alternativas"][i], command=lambda escolha=pergunta["alternativas"][i]: responder(escolha))

        for _ in range(4):
            btn = Button(quiz, text="", font=("Ivy", 12), width=40, bg=co2, fg="white")
            btn.pack(pady=5)
            botoes.append(btn)

        carregar_pergunta()

    iniciar_quiz()

if __name__ == "__main__":
    criar_login()
