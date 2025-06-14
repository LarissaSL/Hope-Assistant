from datetime import datetime

class ComandosDataHora:
    DIAS_SEMANA = {
        'Monday': 'segunda-feira',
        'Tuesday': 'terça-feira',
        'Wednesday': 'quarta-feira',
        'Thursday': 'quinta-feira',
        'Friday': 'sexta-feira',
        'Saturday': 'sábado',
        'Sunday': 'domingo'
    }

    MESES = {
        'January': 'janeiro',
        'February': 'fevereiro',
        'March': 'março',
        'April': 'abril',
        'May': 'maio',
        'June': 'junho',
        'July': 'julho',
        'August': 'agosto',
        'September': 'setembro',
        'October': 'outubro',
        'November': 'novembro',
        'December': 'dezembro'
    }

    def obter_data_atual(self):
        agora = datetime.now()

        # Pegando cada parte da data completa
        dia_semana_en = agora.strftime('%A')
        mes_en = agora.strftime('%B')
        dia = int(agora.strftime('%d'))
        ano = agora.strftime('%Y')

        # Pegar o valor em PT correspondente a chave no dic. em Inglês
        dia_semana_pt = self.DIAS_SEMANA[dia_semana_en]
        mes_pt = self.MESES[mes_en]

        return f"Hoje é {dia_semana_pt}, {dia} de {mes_pt} de {ano}"

    def obter_hora_atual(self):
        agora = datetime.now()
        hora = int(agora.strftime('%H'))
        minuto = int(agora.strftime('%M'))

        if hora == 1:
            texto_hora = f"É {hora} hora"
        else:
            texto_hora = f"São {hora} horas"

        if minuto == 0:
            return texto_hora
        elif minuto == 1:
            return f"{texto_hora} e {minuto} minuto"
        else:
            return f"{texto_hora} e {minuto} minutos"