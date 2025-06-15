import random
import threading
from playsound import playsound

from HopeCore.modules import ComandosAudioAssistente
from HopeCore.modules import ComandosRespostas
from HopeCore.modules import ComandosPesquisa
from HopeCore.modules import ComandosDataHora
from HopeCore.modules import ComandosMidia
from HopeCore.modules import ComandosLembretes


class HopeAssistant:

    def __init__(self, log_callback=None):
        self.meu_nome = "Hope"
        self.log_callback = log_callback
        self.listening = False

        self.setup_hope_components()

        self.play_sound('HopeCore/audios/n1.mp3')

    def setup_hope_components(self):
        print("Iniciando a Hope")

        self.comandos_audio_hope = ComandosAudioAssistente.AudioAssistente()
        self.comandos_pesquisa = ComandosPesquisa.ComandosPesquisa()
        self.comandos_data_hora = ComandosDataHora.ComandosDataHora()
        self.comandos_midia = ComandosMidia.ComandosMidia()
        self.comandos_lembretes = ComandosLembretes.ComandosLembretes()

        self.comandos = ComandosRespostas.comandos
        self.respostas = ComandosRespostas.respostas
        self.despedidas = ComandosRespostas.despedidas

        print('[INFO] Pronto para começar!')

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def play_sound(self, sound_file):
        try:
            threading.Thread(target=lambda: playsound(sound_file), daemon=True).start()
        except:
            pass

    def voice_loop(self):
        while self.listening:
            try:
                result = self.comandos_audio_hope.listen_microphone()

                if not self.listening:
                    break

                if self.meu_nome in result:
                    result = str(result.split(self.meu_nome + ' ')[1])
                    result = result.lower()
                    self.log('Acionou a assistente!')

                    self.process_command(result)

                elif result:
                    self.play_sound('HopeCore/audios/n3.mp3')

            except Exception as e:
                if self.listening:
                    self.log(f"❌ Erro: {str(e)}")
                break

    def process_command(self, result):
        # 0 - funcoes
        if result in self.comandos[0]:
            self.play_sound('HopeCore/audios/n2.mp3')
            response = 'Até agora minhas funções são: ' + self.respostas[0]
            self.comandos_audio_hope.speak(response)
            self.log(f"🤖 Hope: {response}")

        # 1 - lembretes
        elif result in self.comandos[1]:
            self.play_sound('HopeCore/audios/n2.mp3')

            while True:
                self.comandos_audio_hope.speak('Qual lembrete você quer adicionar?')
                self.log("🤖 Hope: Qual lembrete você quer adicionar?")
                lembrete_solicitado = self.comandos_audio_hope.listen_microphone_extended()

                if lembrete_solicitado:
                    if any(palavra in lembrete_solicitado.lower() for palavra in
                           ['cancelar', 'cancela', 'desistir', 'deixa pra lá', 'esquecer', 'não quero mais']):
                        self.comandos_audio_hope.speak('Ok, operação cancelada.')
                        self.log("🤖 Hope: Ok, operação cancelada.")
                        break

                    self.comandos_audio_hope.speak(f'Você quer que eu adicione o lembrete: "{lembrete_solicitado}"?')
                    self.log(f"🤖 Hope: Você quer que eu adicione o lembrete: '{lembrete_solicitado}'?")
                    confirmacao = self.comandos_audio_hope.listen_microphone()

                    if confirmacao.lower() in ['sim', 'yes', 'confirma', 'confirmo', 'isso mesmo', 'isso',
                                               'correto', 'certo']:
                        self.comandos_lembretes.adicionar_lembrete(lembrete_solicitado)
                        self.comandos_audio_hope.speak('Lembrete adicionado com sucesso.')
                        self.log("📝 Hope: Lembrete adicionado com sucesso.")
                        break
                    elif confirmacao.lower() in ['não', 'nao', 'no', 'errado', 'não é esse', 'não era esse']:
                        self.comandos_audio_hope.speak('Ok, vamos tentar novamente.')
                        self.log("🤖 Hope: Ok, vamos tentar novamente.")
                    else:
                        self.comandos_audio_hope.speak(
                            'Não entendi. Você quer que eu adicione esse lembrete? Diga sim ou não.')
                        self.log("🤖 Hope: Não entendi. Você quer que eu adicione esse lembrete? Diga sim ou não.")
                        nova_confirmacao = self.comandos_audio_hope.listen_microphone()
                        if nova_confirmacao.lower() in ['sim', 'yes', 'confirma', 'confirmo']:
                            self.comandos_lembretes.adicionar_lembrete(lembrete_solicitado)
                            self.comandos_audio_hope.speak('Lembrete adicionado com sucesso.')
                            self.log("📝 Hope: Lembrete adicionado com sucesso.")
                            break
                        else:
                            self.comandos_audio_hope.speak('Vamos tentar novamente então.')
                            self.log("🤖 Hope: Vamos tentar novamente então.")
                else:
                    self.comandos_audio_hope.speak(
                        'Não consegui entender. Tente falar novamente ou diga "cancelar" para sair.')
                    self.log("🤖 Hope: Não consegui entender. Tente falar novamente ou diga 'cancelar' para sair.")

        # 2 - ajuda/pesquisa google
        elif result in self.comandos[2]:
            self.play_sound('HopeCore/audios/n2.mp3')
            response = ''.join(random.sample(self.respostas[2], k=1))
            self.comandos_audio_hope.speak(response)
            self.log(f"🤖 Hope: {response}")
            result = self.comandos_audio_hope.listen_microphone()
            search_response = ''.join(random.sample(self.respostas[5], k=1)) + 'sobre ' + result
            self.comandos_audio_hope.speak(search_response)
            self.log(f"🤖 Hope: {search_response}")
            self.comandos_pesquisa.search(result)
            self.log(f"🔍 Pesquisando: {result}")

        # 3 - horas
        elif result in self.comandos[3]:
            self.play_sound('HopeCore/audios/n2.mp3')
            hora_atual = self.comandos_data_hora.obter_hora_atual()
            self.comandos_audio_hope.speak(hora_atual)
            self.log(f"🕐 Hope: {hora_atual}")

        # 4 - data
        elif result in self.comandos[4]:
            self.play_sound('HopeCore/audios/n2.mp3')
            data_atual = self.comandos_data_hora.obter_data_atual()
            self.comandos_audio_hope.speak(data_atual)
            self.log(f"📅 Hope: {data_atual}")

        # 5 - pesquisa no youtube
        elif result in self.comandos[5]:
            self.play_sound('HopeCore/audios/n2.mp3')
            response = ''.join(random.sample(self.respostas[2], k=1))
            self.comandos_audio_hope.speak(response)
            self.log(f"🤖 Hope: {response}")
            result = self.comandos_audio_hope.listen_microphone()
            search_response = ''.join(random.sample(self.respostas[6], k=1)) + result
            self.comandos_audio_hope.speak(search_response)
            self.log(f"🤖 Hope: {search_response}")
            self.comandos_pesquisa.search_youtube(result)
            self.log(f"🎥 Buscando no YouTube: {result}")

        # 6 - Tocar música
        elif result in self.comandos[6]:
            self.play_sound('HopeCore/audios/n2.mp3')

            while True:
                self.comandos_audio_hope.speak('Qual música você quer ouvir?')
                self.log("🤖 Hope: Qual música você quer ouvir?")
                musica_solicitada = self.comandos_audio_hope.listen_microphone_extended()

                if musica_solicitada:
                    if any(palavra in musica_solicitada.lower() for palavra in
                           ['cancelar', 'cancela', 'desistir', 'deixa pra lá', 'esquecer', 'não quero mais']):
                        self.comandos_audio_hope.speak('Ok, operação cancelada.')
                        self.log("🤖 Hope: Ok, operação cancelada.")
                        break

                    self.comandos_audio_hope.speak(f'Você quer que eu toque {musica_solicitada}?')
                    self.log(f"🤖 Hope: Você quer que eu toque {musica_solicitada}?")
                    confirmacao = self.comandos_audio_hope.listen_microphone()

                    if confirmacao.lower() in ['sim', 'yes', 'pode tocar', 'toca', 'confirmo', 'isso mesmo', 'isso',
                                               'está certo', 'correto', 'certo']:
                        self.comandos_audio_hope.speak(''.join(random.sample(self.respostas[7], k=1)))
                        self.log("🎵 Hope: Procurando música...")
                        resposta = self.comandos_midia.procura_e_busca_youtube(musica_solicitada)
                        self.comandos_audio_hope.speak(resposta)
                        self.log(f"🎵 Hope: {resposta}")
                        break
                    elif confirmacao.lower() in ['não', 'no', 'nao', 'errado', 'não é essa', 'não era essa']:
                        self.comandos_audio_hope.speak('Ok, vamos tentar novamente.')
                        self.log("🤖 Hope: Ok, vamos tentar novamente.")
                    else:
                        self.comandos_audio_hope.speak(
                            'Não entendi. Você quer que eu toque essa música? Diga sim ou não.')
                        self.log("🤖 Hope: Não entendi. Você quer que eu toque essa música? Diga sim ou não.")
                        nova_confirmacao = self.comandos_audio_hope.listen_microphone()
                        if nova_confirmacao.lower() in ['sim', 'yes', 'pode tocar', 'toca']:
                            self.comandos_audio_hope.speak(''.join(random.sample(self.respostas[7], k=1)))
                            self.log("🎵 Hope: Procurando música...")
                            resposta = self.comandos_midia.procura_e_busca_youtube(musica_solicitada)
                            self.comandos_audio_hope.speak(resposta)
                            self.log(f"🎵 Hope: {resposta}")
                            break
                        else:
                            self.comandos_audio_hope.speak('Vamos tentar novamente então.')
                            self.log("🤖 Hope: Vamos tentar novamente então.")
                else:
                    self.comandos_audio_hope.speak(
                        'Não consegui entender. Tente falar novamente ou diga "cancelar" para sair.')
                    self.log("🤖 Hope: Não consegui entender. Tente falar novamente ou diga 'cancelar' para sair.")

        # 7 - pausar musica
        elif result in self.comandos[7]:
            self.play_sound('HopeCore/audios/n2.mp3')
            resposta = self.comandos_midia.pausa_musica()
            self.comandos_audio_hope.speak(resposta)
            self.log(f"⏸️ Hope: {resposta}")

        # 8 - retomar musica
        elif result in self.comandos[8]:
            self.play_sound('HopeCore/audios/n2.mp3')
            resposta = self.comandos_midia.retomar_musica()
            self.comandos_audio_hope.speak(resposta)
            self.log(f"▶️ Hope: {resposta}")

        # 9 - Musica atual
        elif result in self.comandos[9]:
            self.play_sound('HopeCore/audios/n2.mp3')
            resposta = self.comandos_midia.obter_nome_musica_atual()
            self.comandos_audio_hope.speak(resposta)
            self.log(f"🎵 Hope: {resposta}")

        # 10 - Ler Lembrete
        elif result in self.comandos[10]:
            self.play_sound('HopeCore/audios/n2.mp3')
            lembretes = self.comandos_lembretes.ler_lembretes()
            if lembretes:
                for lembrete in lembretes:
                    self.comandos_audio_hope.speak(lembrete)
                    self.log(f"📝 Hope: {lembrete}")
            else:
                response = "Você não tem lembretes salvos"
                self.comandos_audio_hope.speak(response)
                self.log(f"📝 Hope: {response}")

            # Despedida
        elif any(palavra in result for palavra in self.despedidas):
            self.play_sound('HopeCore/audios/n2.mp3')
            response = ''.join(random.sample(self.respostas[3], k=1))
            self.comandos_audio_hope.speak(response)
            self.log(f"🤖 Hope: {response}")
            return "SAIR"

        else:
            response = "Desculpe, não entendi esse comando"
            self.log(f"🤖 Hope: {response}")

        return "CONTINUAR"

    def start_listening(self):
        self.listening = True

    def stop_listening(self):
        self.listening = False

    def cleanup(self):
        try:
            self.comandos_midia.stop_music()
        except:
            pass