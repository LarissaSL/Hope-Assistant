import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import datetime

from HopeAssistant import HopeAssistant

class HopeInterface:

    def __init__(self):
        self.root = tb.Window(themename="superhero")
        self.root.title("Hope Assistant")
        self.root.geometry("800x800")

        self.listening = False
        self.voice_thread = None

        self.hope = HopeAssistant(log_callback=self.log)

        self.create_interface()

    def create_interface(self):
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        title = tb.Label(
            main_frame,
            text="Hope Assistant",
            font=("Arial", 24, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        self.status_frame = tb.Frame(main_frame)
        self.status_frame.pack(fill=X, pady=(0, 20))

        self.status_label = tb.Label(
            self.status_frame,
            text="Status: Aguardando",
            font=("Arial", 14),
            bootstyle="info"
        )
        self.status_label.pack(side=LEFT)

        self.status_dot = tb.Label(
            self.status_frame,
            text="●",
            font=("Arial", 16),
            bootstyle="success"
        )
        self.status_dot.pack(side=RIGHT)

        self.control_button = tb.Button(
            main_frame,
            text="Começar a Escutar",
            command=self.toggle_listening,
            bootstyle="success",
            style="Outline.TButton"
        )
        self.control_button.pack(pady=10)

        info_frame = tb.LabelFrame(main_frame, text="Como usar", padding=15)
        info_frame.pack(fill=X, pady=(0, 20))

        info_text = """
            Diga "Hope" seguido do comando:
            • "Hope, que horas são?"
            • "Hope, que dia é hoje?"  
            • "Hope, anotar"
            • "Hope, ler lembretes"
            • "Hope, pesquisar"
            • "Hope, youtube"
            • "Hope, tocar música"
            • "Hope, música atual"
            • "Hope, pausar" / "Hope, continuar"
            • "Hope, tchau" (para sair)
        """

        tb.Label(info_frame, text=info_text, justify=LEFT).pack()

        functions_frame = tb.LabelFrame(main_frame, text="Minhas Funções", padding=15)
        functions_frame.pack(fill=X, pady=(0, 20))

        tb.Label(
            functions_frame,
            text=self.hope.respostas[0],
            font=("Arial", 11),
            justify=LEFT
        ).pack()

        log_frame = tb.LabelFrame(main_frame, text="Atividades", padding=15)
        log_frame.pack(fill=BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.log_text.pack(fill=BOTH, expand=True)

        self.log("Hope Assistant iniciada!")
        self.log("Clique no botão para começar a escutar")

    def toggle_listening(self):
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.listening = True
        self.hope.start_listening()

        self.control_button.config(text="🛑 Parar de Escutar", bootstyle="danger")
        self.update_status("Escutando...", "warning")

        self.voice_thread = threading.Thread(target=self.voice_loop_wrapper, daemon=True)
        self.voice_thread.start()

        self.log("🎤 Escuta ativada - Diga 'Hope' + comando")

    def stop_listening(self):
        self.listening = False
        self.hope.stop_listening()

        self.control_button.config(text="Começar a Escutar", bootstyle="success")
        self.update_status("Aguardando", "success")
        self.log("🛑 Escuta desativada")

    def voice_loop_wrapper(self):
        try:
            self.hope.voice_loop()
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Erro na escuta: {str(e)}"))
            self.root.after(0, self.stop_listening)

    def update_status(self, status, color):
        self.status_label.config(text=f"Status: {status}")
        self.status_dot.config(bootstyle=color)

    def log(self, message):

        def _log():
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"

            self.log_text.insert(tk.END, formatted_message)
            self.log_text.see(tk.END)

            lines = int(self.log_text.index('end-1c').split('.')[0])
            if lines > 100:
                self.log_text.delete('1.0', '10.0')

        self.root.after(0, _log)

    def close_app(self):
        if self.listening:
            self.stop_listening()

        self.hope.cleanup()

        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.root.mainloop()


# Classe principal
class HopeApp:
    def __init__(self):
        self.interface = HopeInterface()

    def run(self):
        self.interface.run()


if __name__ == "__main__":
    app = HopeApp()
    app.run()