import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import datetime
import webbrowser
import os
from pathlib import Path


class HopeAssistantGUI:
    def __init__(self):
        # Usando ttkbootstrap para interface moderna
        self.root = tb.Window(themename="superhero")  # Tema escuro moderno
        self.root.title("Hope Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Variáveis de controle
        self.is_listening = False
        self.notes_file = "lembretes.txt"

        # Configurar interface
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        """Configura toda a interface do usuário"""
        # Frame principal com padding
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Título da aplicação
        title_label = tb.Label(
            main_frame,
            text="🤖 Hope Assistant",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=(0, 20))

        # Status do assistente
        self.status_frame = tb.Frame(main_frame)
        self.status_frame.pack(fill=X, pady=(0, 15))

        self.status_label = tb.Label(
            self.status_frame,
            text="Status: Aguardando comando",
            font=("Helvetica", 12),
            bootstyle="info"
        )
        self.status_label.pack(side=LEFT)

        # Indicador visual de status
        self.status_indicator = tb.Label(
            self.status_frame,
            text="●",
            font=("Helvetica", 16),
            bootstyle="success"
        )
        self.status_indicator.pack(side=RIGHT)

        # Frame para comandos rápidos
        commands_frame = tb.LabelFrame(main_frame, text="Comandos Rápidos", padding=15)
        commands_frame.pack(fill=X, pady=(0, 15))

        # Botões de comando organizados em grid
        commands = [
            ("🕐 Que horas são?", self.get_time, "primary"),
            ("📅 Que dia é hoje?", self.get_date, "secondary"),
            ("📝 Abrir lembretes", self.show_notes, "info"),
            ("🔍 Pesquisar Google", self.search_google, "warning"),
            ("🎥 Pesquisar YouTube", self.search_youtube, "danger"),
            ("⚙️ Minhas funções", self.show_functions, "success")
        ]

        # Organizar botões em 2 colunas
        for i, (text, command, style) in enumerate(commands):
            row = i // 2
            col = i % 2
            btn = tb.Button(
                commands_frame,
                text=text,
                command=command,
                bootstyle=style,
                width=25
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Configurar peso das colunas
        commands_frame.columnconfigure(0, weight=1)
        commands_frame.columnconfigure(1, weight=1)

        # Frame para entrada de texto
        input_frame = tb.LabelFrame(main_frame, text="Digite seu comando", padding=15)
        input_frame.pack(fill=X, pady=(0, 15))

        # Campo de entrada com estilo
        self.entry_var = tk.StringVar()
        self.command_entry = tb.Entry(
            input_frame,
            textvariable=self.entry_var,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        self.command_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.command_entry.bind("<Return>", lambda e: self.process_text_command())

        # Botão de envio
        send_btn = tb.Button(
            input_frame,
            text="Enviar",
            command=self.process_text_command,
            bootstyle="primary-outline"
        )
        send_btn.pack(side=RIGHT)

        # Área de log/histórico
        log_frame = tb.LabelFrame(main_frame, text="Histórico de Comandos", padding=15)
        log_frame.pack(fill=BOTH, expand=True)

        # Text widget com scroll para histórico
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1"
        )
        self.log_text.pack(fill=BOTH, expand=True)

        # Frame inferior com botões de controle
        control_frame = tb.Frame(main_frame)
        control_frame.pack(fill=X, pady=(15, 0))

        # Botão de limpar histórico
        clear_btn = tb.Button(
            control_frame,
            text="Limpar Histórico",
            command=self.clear_log,
            bootstyle="warning-outline"
        )
        clear_btn.pack(side=LEFT)

        # Botão de sair
        exit_btn = tb.Button(
            control_frame,
            text="Sair",
            command=self.root.quit,
            bootstyle="danger-outline"
        )
        exit_btn.pack(side=RIGHT)

        # Mensagem inicial
        self.log_message("Hope Assistant iniciado! Digite um comando ou use os botões.")

    def setup_shortcuts(self):
        """Configura atalhos de teclado"""
        self.root.bind("<Control-Return>", lambda e: self.process_text_command())
        self.root.bind("<F1>", lambda e: self.show_functions())
        self.root.bind("<Control-l>", lambda e: self.clear_log())

    def log_message(self, message, message_type="info"):
        """Adiciona mensagem ao log com timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # Cores baseadas no tipo
        colors = {
            "info": "#3498db",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "user": "#9b59b6"
        }

        formatted_message = f"[{timestamp}] {message}\n"

        # Inserir no final e fazer scroll automático
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)

        # Limitar tamanho do log (manter apenas últimas 100 linhas)
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 100:
            self.log_text.delete('1.0', '10.0')

    def update_status(self, status, indicator_color="info"):
        """Atualiza o status do assistente"""
        self.status_label.config(text=f"Status: {status}")
        self.status_indicator.config(bootstyle=indicator_color)

    def process_text_command(self):
        """Processa comando digitado pelo usuário"""
        command = self.entry_var.get().strip().lower()
        if not command:
            return

        # Limpar campo de entrada
        self.entry_var.set("")

        # Log do comando do usuário
        self.log_message(f"Você: {command}", "user")

        # Processar comando
        self.execute_command(command)

    def execute_command(self, command):
        """Executa comando baseado no texto recebido"""
        # Comando de horas
        if any(word in command for word in ["hora", "horas"]):
            self.get_time()

        # Comando de data  
        elif any(word in command for word in ["dia", "data", "hoje"]):
            self.get_date()

        # Comando de lembretes
        elif any(word in command for word in ["lembrete", "anotar", "nota"]):
            self.handle_note_command(command)

        # Comando de pesquisa Google
        elif any(word in command for word in ["pesquisar", "google", "buscar"]):
            search_term = self.extract_search_term(command, ["pesquisar", "google", "buscar"])
            if search_term:
                self.search_google(search_term)
            else:
                self.search_google()

        # Comando YouTube
        elif any(word in command for word in ["youtube", "vídeo", "música"]):
            search_term = self.extract_search_term(command, ["youtube", "vídeo", "música"])
            if search_term:
                self.search_youtube(search_term)
            else:
                self.search_youtube()

        # Comando de funções
        elif any(word in command for word in ["função", "funcionalidade", "fazer"]):
            self.show_functions()

        # Comando não reconhecido
        else:
            self.log_message("Comando não reconhecido. Digite F1 para ver as funções disponíveis.", "warning")

    def extract_search_term(self, command, keywords):
        """Extrai termo de pesquisa do comando"""
        for keyword in keywords:
            if keyword in command:
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return None

    def handle_note_command(self, command):
        """Lida com comandos de lembretes"""
        if "ler" in command or "mostrar" in command:
            self.show_notes()
        else:
            # Extrair conteúdo da nota
            note_keywords = ["lembrete", "anotar", "nota", "anote"]
            note_content = command
            for keyword in note_keywords:
                note_content = note_content.replace(keyword, "").strip()

            if note_content:
                self.add_note(note_content)
            else:
                self.show_note_dialog()

    def get_time(self):
        """Obtém e exibe a hora atual"""
        self.update_status("Consultando hora...", "warning")

        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute

        if hour == 1:
            time_text = f"É {hour} hora"
        else:
            time_text = f"São {hour} horas"

        if minute == 0:
            full_time = time_text
        elif minute == 1:
            full_time = f"{time_text} e {minute} minuto"
        else:
            full_time = f"{time_text} e {minute} minutos"

        self.log_message(f"Hope: {full_time}", "success")
        self.update_status("Pronto", "success")

    def get_date(self):
        """Obtém e exibe a data atual"""
        self.update_status("Consultando data...", "warning")

        # Dicionários de tradução
        days_pt = {
            'Monday': 'segunda-feira', 'Tuesday': 'terça-feira',
            'Wednesday': 'quarta-feira', 'Thursday': 'quinta-feira',
            'Friday': 'sexta-feira', 'Saturday': 'sábado', 'Sunday': 'domingo'
        }

        months_pt = {
            'January': 'janeiro', 'February': 'fevereiro', 'March': 'março',
            'April': 'abril', 'May': 'maio', 'June': 'junho',
            'July': 'julho', 'August': 'agosto', 'September': 'setembro',
            'October': 'outubro', 'November': 'novembro', 'December': 'dezembro'
        }

        now = datetime.datetime.now()
        day_name = days_pt[now.strftime('%A')]
        month_name = months_pt[now.strftime('%B')]
        day = now.day
        year = now.year

        date_text = f"Hoje é {day_name}, {day} de {month_name} de {year}"

        self.log_message(f"Hope: {date_text}", "success")
        self.update_status("Pronto", "success")

    def show_note_dialog(self):
        """Exibe diálogo para adicionar nova nota"""
        dialog = tb.Toplevel(self.root)
        dialog.title("Novo Lembrete")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centralizar diálogo
        dialog.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))

        frame = tb.Frame(dialog, padding=20)
        frame.pack(fill=BOTH, expand=True)

        tb.Label(frame, text="Digite seu lembrete:", font=("Helvetica", 12)).pack(pady=(0, 10))

        text_area = tk.Text(frame, height=5, font=("Helvetica", 10))
        text_area.pack(fill=BOTH, expand=True, pady=(0, 15))
        text_area.focus()

        def save_note():
            content = text_area.get("1.0", tk.END).strip()
            if content:
                self.add_note(content)
                dialog.destroy()
            else:
                messagebox.showwarning("Aviso", "Digite algum conteúdo para o lembrete!")

        button_frame = tb.Frame(frame)
        button_frame.pack(fill=X)

        tb.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side=RIGHT,
                                                                                                     padx=(5, 0))
        tb.Button(button_frame, text="Salvar", command=save_note, bootstyle="primary").pack(side=RIGHT)

    def add_note(self, content):
        """Adiciona nova nota ao arquivo"""
        try:
            timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            note_entry = f"[{timestamp}] {content}\n"

            with open(self.notes_file, "a", encoding="utf-8") as f:
                f.write(note_entry)

            self.log_message(f"Hope: Lembrete salvo - {content}", "success")
            self.update_status("Lembrete salvo", "success")

        except Exception as e:
            self.log_message(f"Erro ao salvar lembrete: {e}", "error")

    def show_notes(self):
        """Exibe janela com todos os lembretes"""
        notes_window = tb.Toplevel(self.root)
        notes_window.title("Lembretes Salvos")
        notes_window.geometry("600x400")
        notes_window.transient(self.root)

        frame = tb.Frame(notes_window, padding=20)
        frame.pack(fill=BOTH, expand=True)

        tb.Label(frame, text="📝 Seus Lembretes", font=("Helvetica", 16, "bold")).pack(pady=(0, 15))

        # Área de texto para mostrar lembretes
        notes_text = scrolledtext.ScrolledText(
            frame,
            font=("Helvetica", 10),
            wrap=tk.WORD
        )
        notes_text.pack(fill=BOTH, expand=True, pady=(0, 15))

        # Carregar e exibir lembretes
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        notes_text.insert("1.0", content)
                    else:
                        notes_text.insert("1.0", "Nenhum lembrete encontrado.")
            else:
                notes_text.insert("1.0", "Nenhum lembrete encontrado.")
        except Exception as e:
            notes_text.insert("1.0", f"Erro ao carregar lembretes: {e}")

        notes_text.config(state="disabled")  # Somente leitura

        # Botões
        button_frame = tb.Frame(frame)
        button_frame.pack(fill=X)

        tb.Button(button_frame, text="Fechar", command=notes_window.destroy, bootstyle="secondary").pack(side=RIGHT)
        tb.Button(button_frame, text="Novo Lembrete", command=lambda: [notes_window.destroy(), self.show_note_dialog()],
                  bootstyle="primary").pack(side=RIGHT, padx=(0, 10))

    def search_google(self, query=None):
        """Abre pesquisa no Google"""
        if not query:
            query = tk.simpledialog.askstring("Pesquisa Google", "O que deseja pesquisar?")

        if query:
            self.update_status("Abrindo pesquisa...", "warning")
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            self.log_message(f"Hope: Pesquisando '{query}' no Google", "success")
            self.update_status("Pesquisa aberta no navegador", "success")

    def search_youtube(self, query=None):
        """Abre pesquisa no YouTube"""
        if not query:
            query = tk.simpledialog.askstring("Pesquisa YouTube", "O que deseja procurar no YouTube?")

        if query:
            self.update_status("Abrindo YouTube...", "warning")
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            self.log_message(f"Hope: Procurando '{query}' no YouTube", "success")
            self.update_status("YouTube aberto no navegador", "success")

    def show_functions(self):
        """Exibe janela com todas as funções disponíveis"""
        functions_window = tb.Toplevel(self.root)
        functions_window.title("Minhas Funções")
        functions_window.geometry("500x400")
        functions_window.transient(self.root)

        frame = tb.Frame(functions_window, padding=20)
        frame.pack(fill=BOTH, expand=True)

        tb.Label(frame, text="🤖 O que eu posso fazer:", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        functions_list = [
            "🕐 Informar horário atual",
            "📅 Informar data de hoje",
            "📝 Gerenciar lembretes (criar e visualizar)",
            "🔍 Fazer pesquisas no Google",
            "🎥 Buscar vídeos no YouTube",
            "⌨️ Responder a comandos digitados",
            "",
            "Atalhos de teclado:",
            "• Ctrl+Enter: Enviar comando",
            "• F1: Mostrar funções",
            "• Ctrl+L: Limpar histórico"
        ]

        for function in functions_list:
            if function == "":
                tb.Label(frame, text="").pack()
            else:
                tb.Label(
                    frame,
                    text=function,
                    font=("Helvetica", 11),
                    anchor="w"
                ).pack(fill=X, pady=2)

        tb.Button(frame, text="Fechar", command=functions_window.destroy, bootstyle="primary").pack(pady=(20, 0))

    def clear_log(self):
        """Limpa o histórico de comandos"""
        self.log_text.delete("1.0", tk.END)
        self.log_message("Histórico limpo!", "info")

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


# Ponto de entrada da aplicação
if __name__ == "__main__":
    # Importar módulos necessários com tratamento de erro
    try:
        import tkinter.simpledialog

        app = HopeAssistantGUI()
        app.run()
    except ImportError as e:
        print(f"Erro: Biblioteca necessária não encontrada - {e}")
        print("Instale com: pip install ttkbootstrap")
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")