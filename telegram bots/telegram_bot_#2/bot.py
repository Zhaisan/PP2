import requests
import misc
import json

token = misc.token

# https://api.telegram.org/bot1250789803:AAHuit5b-U-k1S_g_RLrwF3NR8oKz2PC80I/sendmessage?chat_id=478376002&text=hi
URL = 'https://api.telegram.org/bot' + token + '/'



#пакет обновления сообщения которые пишем нашему боту
def get_updates():
    url = URL + 'getupdates'
    #print(url)
    r = requests.get(url)
    return r.json()

def get_message():
    data = get_updates()

    chat_id = data['result'][-1]['message']['chat']['id']
    
    message_text = data['result'][-1]['message']['text']
    print(message_text)
    
    message = {'chat_id': chat_id,
               'text': message_text}

    return message



def main():
    # d = get_updates()

    #Контекстный менеджер 'with',открываем файл для записи

    # with open('updates.json', 'w') as file:
        #записываем файл,дампим
        # json.dump(d, file, indent=2, ensure_ascii=False) #Делаем так чтобы слова кириллицы не были в виде кода
    print(get_message())
    


if __name__ == '__main__':
    main() 