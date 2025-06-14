import random

from HopeCore.modules import ComandosAudioAssistente
from HopeCore.modules import ComandosRespostas
from HopeCore.modules import ComandosPesquisa
from HopeCore.modules import ComandosDataHora
from HopeCore.modules import ComandosMidia
from HopeCore.modules import ComandosLembretes


from playsound import playsound

if __name__ == "__main__":
    print("Iniciando a Hope")

    meu_nome = "Hope"

    comandos = ComandosRespostas.comandos
    respostas = ComandosRespostas.respostas
    despedidas = ComandosRespostas.despedidas

    playing = False
    mode_control = False
    print('[INFO] Pronto para começar!')
    playsound('HopeCore/audios/n1.mp3')

    comandos_audio_hope = ComandosAudioAssistente.AudioAssistente()
    comandos_pesquisa = ComandosPesquisa.ComandosPesquisa()
    comandos_data_hora = ComandosDataHora.ComandosDataHora()
    comandos_midia = ComandosMidia.ComandosMidia()
    comandos_lembretes = ComandosLembretes.ComandosLembretes()


    while True:
        result = comandos_audio_hope.listen_microphone()

        if meu_nome in result:
            result = str(result.split(meu_nome + ' ')[1])
            result = result.lower()
            print('Acionou a assistente!')

            # 0 - funcoes
            if result in comandos[0]:
                playsound('HopeCore/audios/n2.mp3')
                comandos_audio_hope.speak('Até agora minhas funções são: ' + respostas[0])

            # 1 - lembretes
            if result in comandos[1]:
                playsound('HopeCore/audios/n2.mp3')

                while True:
                    comandos_audio_hope.speak('Qual lembrete você quer adicionar?')
                    lembrete_solicitado = comandos_audio_hope.listen_microphone_extended()

                    if lembrete_solicitado:

                        if any(palavra in lembrete_solicitado.lower() for palavra in
                               ['cancelar', 'cancela', 'desistir', 'deixa pra lá', 'esquecer', 'não quero mais']):
                            comandos_audio_hope.speak('Ok, operação cancelada.')
                            break

                        comandos_audio_hope.speak(f'Você quer que eu adicione o lembrete: "{lembrete_solicitado}"?')
                        confirmacao = comandos_audio_hope.listen_microphone()

                        if confirmacao.lower() in ['sim', 'yes', 'confirma', 'confirmo', 'isso mesmo', 'isso',
                                                   'correto', 'certo']:

                            comandos_lembretes.adicionar_lembrete(lembrete_solicitado)
                            comandos_audio_hope.speak('Lembrete adicionado com sucesso.')
                            break
                        elif confirmacao.lower() in ['não', 'nao', 'no', 'errado', 'não é esse', 'não era esse']:
                            comandos_audio_hope.speak('Ok, vamos tentar novamente.')
                        else:
                            comandos_audio_hope.speak(
                                'Não entendi. Você quer que eu adicione esse lembrete? Diga sim ou não.')
                            nova_confirmacao = comandos_audio_hope.listen_microphone()
                            if nova_confirmacao.lower() in ['sim', 'yes', 'confirma', 'confirmo']:
                                comandos_lembretes.adicionar_lembrete(lembrete_solicitado)
                                comandos_audio_hope.speak('Lembrete adicionado com sucesso.')
                                break
                            else:
                                comandos_audio_hope.speak('Vamos tentar novamente então.')
                    else:
                        comandos_audio_hope.speak(
                            'Não consegui entender. Tente falar novamente ou diga "cancelar" para sair.')

            # 2 - ajuda/pesquisa google
            if result in comandos[2]:
                playsound('HopeCore/audios/n2.mp3')
                comandos_audio_hope.speak(''.join(random.sample(respostas[2], k=1)))
                result = comandos_audio_hope.listen_microphone()
                comandos_audio_hope.speak(''.join(random.sample(respostas[5], k=1)) + 'sobre' + result)
                comandos_pesquisa.search(result)

            # 3 - horas
            if result in comandos[3]:
                playsound('HopeCore/audios/n2.mp3')
                hora_atual = comandos_data_hora.obter_hora_atual()
                comandos_audio_hope.speak(hora_atual)

            # 4 - data
            if result in comandos[4]:
                playsound('HopeCore/audios/n2.mp3')
                data_atual = comandos_data_hora.obter_data_atual()
                comandos_audio_hope.speak(data_atual)

            # 5 - pesquisa no youtube
            if result in comandos[5]:
                playsound('HopeCore/audios/n2.mp3')
                comandos_audio_hope.speak(''.join(random.sample(respostas[2], k=1)))
                result = comandos_audio_hope.listen_microphone()
                comandos_audio_hope.speak(''.join(random.sample(respostas[6], k=1)) + result)
                comandos_pesquisa.search_youtube(result)

            # 6 - TOCAR MÚSICA
            if result in comandos[6]:
                playsound('HopeCore/audios/n2.mp3')

                while True:
                    comandos_audio_hope.speak('Qual música você quer ouvir?')
                    musica_solicitada = comandos_audio_hope.listen_microphone_extended()

                    if musica_solicitada:
                        if any(palavra in musica_solicitada.lower() for palavra in
                               ['cancelar', 'cancela', 'desistir', 'deixa pra lá', 'esquecer', 'não quero mais']):
                            comandos_audio_hope.speak('Ok, operação cancelada.')
                            break

                        comandos_audio_hope.speak(f'Você quer que eu toque {musica_solicitada}?')
                        confirmacao = comandos_audio_hope.listen_microphone()

                        if confirmacao.lower() in ['sim', 'yes', 'pode tocar', 'toca', 'confirmo', 'isso mesmo', 'isso',
                                                   'está certo', 'correto', 'certo']:
                            comandos_audio_hope.speak(''.join(random.sample(respostas[7], k=1)))
                            resposta = comandos_midia.procura_e_busca_youtube(musica_solicitada)
                            comandos_audio_hope.speak(resposta)
                            break
                        elif confirmacao.lower() in ['não', 'no', 'nao', 'errado', 'não é essa', 'não era essa']:
                            comandos_audio_hope.speak('Ok, vamos tentar novamente.')
                        else:
                            comandos_audio_hope.speak(
                                'Não entendi. Você quer que eu toque essa música? Diga sim ou não.')
                            nova_confirmacao = comandos_audio_hope.listen_microphone()
                            if nova_confirmacao.lower() in ['sim', 'yes', 'pode tocar', 'toca']:
                                comandos_audio_hope.speak(''.join(random.sample(respostas[7], k=1)))
                                resposta = comandos_midia.procura_e_busca_youtube(musica_solicitada)
                                comandos_audio_hope.speak(resposta)
                                break
                            else:
                                comandos_audio_hope.speak('Vamos tentar novamente então.')
                    else:
                        comandos_audio_hope.speak(
                            'Não consegui entender. Tente falar novamente ou diga "cancelar" para sair.')

            # 7 - pausar musica
            if result in comandos[7]:
                playsound('HopeCore/audios/n2.mp3')
                resposta = comandos_midia.pausa_musica()
                comandos_audio_hope.speak(resposta)

            # 8 - retomar musica
            if result in comandos[8]:
                playsound('HopeCore/audios/n2.mp3')
                resposta = comandos_midia.retomar_musica()
                comandos_audio_hope.speak(resposta)

            # 10 - Musica atual
            if result in comandos[9]:
                playsound('HopeCore/audios/n2.mp3')
                resposta = comandos_midia.obter_nome_musica_atual()
                comandos_audio_hope.speak(resposta)

            # 11 - Ler Lembrete
            if result in comandos[10]:
                playsound('HopeCore/audios/n2.mp3')
                resposta = comandos_lembretes.ler_lembretes()
                comandos_audio_hope.speak(resposta)

            # Despedida
            if any(palavra in result for palavra in despedidas):
                playsound('HopeCore/audios/n2.mp3')
                comandos_audio_hope.speak(''.join(random.sample(respostas[3], k=1)))
                break

        else:
            playsound('HopeCore/audios/n3.mp3')
