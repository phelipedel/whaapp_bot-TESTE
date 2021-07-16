import json
import requests
import datetime

# A biblioteca JSON lida com o formato JSON. Solicitações - Precisamos dele para acessar a API do site.

class WABot():
def __init__(self, json):
    self.json = json
    self.dict_messages = json['messages']
    self.APIUrl = 'api'
    self.token = 'abcdefg'


    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()


    def send_message(self, chatId, text):
        """

        :param self:
        :param chatId:ID do chat para onde a mensagem deve ser enviada
        :param text:  Texto da mensagem
        :return:
        """
        data = {"chatId" : chatId,
                "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def welcome(self, chatId, noWelcome=False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "WhatsApp Chat\n"
        else:
            welcome_string = """
        Commandos:
        1. chatId - mostrar ID do chat atual
        2. tempo - mostrar a hora do servidor
        3. eu - mostre seu apelido
        4. arquivo [format] - pegue um arquivo. Formato disponível: doc/gif/jpg/png/pdf/mp3/mp
        5. geo - obter uma localização
        6. group - crie um grupo com o bot"""
        return self.send_message(chatId, welcome_string)


    # Saída chatId
    def show_chat_id(self,chatId):
        return self.send_message(chatId, f"Chat ID : {chatId}")

    # Saída de tempo
    def time(self, chatId):
        t = datetime.datetime.now()
        time = t.strftime('%d:%m:%Y')
        return self.send_message(chatId, time)

    # Função “arquivo”
    def file(self, chatId, format):
        availableFiles = {'doc' : 'document.doc',
                        'gif' : 'gifka.gif',
                        'jpg' : 'jpgfile.jpg',
                        'png' : 'pngfile.png',
                        'pdf' : 'presentation.pdf',
                        'mp4' : 'video.mp4',
                        'mp3' : 'mp3file.mp3'}
        if format in availableFiles.keys():
            data = {
                        'chatId' : chatId,
                        'body': f'https://domain.com/Python/{availableFiles[format]}',
                        'filename' : availableFiles[format],
                        'caption' : f'Get your file {availableFiles[format]}'
            }
        return self.send_requests('sendFile', data)

    # enviod e localizacao no whats
    def geo(self, chatId):
        data = {
            "lat" : '',
            "lng" : '',
            "address" :'Your address',
            "chatId" : chatId
        }
        answer = self.send_requests('sendLocation', data)
        return answer

    # EU
    def me(self, chatId, name):
        return self.send_message(chatId, name)

    # Função “grupo”
    def group(self, author):
        phone = author.replace('@c.br', '')
        data = {
            "groupName" : 'Chat Group',
            "phones" : phone,
            'messageText' : 'Ola'
        }
        answer = self.send_requests('group', data)
        return answer

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    id  = message['chatId']
                    if text[0].lower() == 'hi':
                        return self.welcome(id)
                    elif text[0].lower() == 'tempo':
                        return self.time(id)
                    elif text[0].lower() == 'chatId':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'eu':
                        return self.me(id, message['nome do remetente'])
                    elif text[0].lower() == 'arquivo':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else: return 'NoCommand'

