import yt_dlp
import vlc

class ComandosMidia:

    def __init__(self):
        self.player = None
        self.current_song = None
        self.is_playing = False
        self.volume = 80

    def procura_e_busca_youtube(self, query):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch1:{query}"
                info = ydl.extract_info(search_query, download=False)

                if info['entries']:
                    video_info = info['entries'][0]
                    stream_url = video_info['url']
                    title = video_info['title']

                    self.play_stream(stream_url, title)
                    return f"Tocando: {title}"
                else:
                    return "Música não encontrada"

        except Exception as e:
            print(f"[DEBUG] Erro no yt-dlp: {str(e)}")
            return f"Erro ao buscar música"

    def play_stream(self, stream_url, title):
        try:
            self.stop_music()
            self.player = vlc.MediaPlayer(stream_url)
            self.player.audio_set_volume(self.volume)
            self.player.play()
            self.current_song = title
            self.is_playing = True
        except Exception as e:
            return  "Erro ao iniciar reprodução"

    def pausa_musica(self):
        if self.player and self.is_playing:
            self.player.pause()
            self.is_playing = False
            return "Música pausada"
        return "Nenhuma música tocando"

    def retomar_musica(self):
        if self.player:
            state = self.player.get_state()
            if state == vlc.State.Paused:
                self.player.play()
                self.is_playing = True
                return "Música retomada"
            elif state == vlc.State.Playing:
                return "Música já está tocando"
            else:
                return "Não há música pausada"
        return "Nenhuma música foi carregada"

    def stop_music(self):
        if self.player:
            self.player.stop()
            self.player.release()
            self.player = None
            self.current_song = None
            self.is_playing = False
            return "Música parada"
        return "Nenhuma música para parar"

    def obter_nome_musica_atual(self):
        if self.current_song:
            status = "tocando" if self.is_playing else "pausada"
            return f"Música atual: {self.current_song} - {status}"
        return "Nenhuma música carregada"
