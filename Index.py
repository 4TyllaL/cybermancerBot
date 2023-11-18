import telebot
import openai
import requests
import random
import string
import pyautogui
import time

CHAVE_OPEN_WEATHER = ""
CHAVE_API_BOT = ""
openai.api_key = ""

bot = telebot.TeleBot(CHAVE_API_BOT)

@bot.message_handler(commands=['VERSION'])
def version(mensagem):
    bot.send_message(mensagem.chat.id,'Atualmente estou na versão 1.5 :)')

@bot.message_handler(commands=['CHATGPT'])
def chatgpt_handler(message):
    bot.send_message(message.chat.id, "Digite a sua pergunta:")
    bot.register_next_step_handler(message, chatgpt_search)
def chatgpt_search(message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message.text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        bot.send_message(message.chat.id, response.choices[0].text)
    except Exception as e:
        bot.send_message(message.chat.id, "Erro ao realizar a pesquisa: " + str(e))

@bot.message_handler(commands=['TEMPERATURA'])
def temperatura_handler(message):
    bot.send_message(message.chat.id, "Qual é a sua cidade?")
    bot.register_next_step_handler(message, temperatura_request)
def temperatura_request(message):
    try:
        # Obter cidade do usuário
        cidade = message.text

        # Chamar a API do OpenWeatherMap
        link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={CHAVE_OPEN_WEATHER}&lang=pt_br"
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        # Obter temperatura e descrição do clima
        temperatura_kelvin = requisicao_dic['main']['temp']
        temperatura_celsius = temperatura_kelvin - 273.15
        descricao = requisicao_dic['weather'][0]['description']

        # Enviar resposta ao usuário
        resposta = f"A temperatura atual em {cidade} é de {temperatura_celsius:.0f}°C, {descricao}."
        bot.send_message(message.chat.id, resposta)

    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao obter a temperatura da cidade {cidade}. Erro: {str(e)}")

@bot.message_handler(commands=['SENHA'])
def generation_handler(message):
    bot.send_message(message.chat.id, "Quantos caracteres deve ter a nova senha?")
    bot.register_next_step_handler(message, generation_request)
def generation_request(message):
    try:
        num_caracteres = int(message.text)

        # lista de caracteres permitidos na senha
        char_list = string.ascii_letters + string.digits + string.punctuation

        # gerar senha aleatória
        nova_senha = ''.join(random.choices(char_list, k=num_caracteres))

        # enviar a nova senha para o usuário
        resposta = f"Aqui está sua nova senha: {nova_senha}"
        bot.send_message(message.chat.id, resposta)

    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número inteiro válido.")

def verificar(mensagem):
    return True

@bot.message_handler(commands=['AUTO'])
def fazer_integracao(message):
    # Enviar uma mensagem informando que a integração começará
    bot.reply_to(message, "Iniciando integração...")

    # Executar as ações com pyautogui
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyautogui.write('chrome')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.click(x=568, y=850)
    time.sleep(3)

    # Navegar para a página desejada
    pyautogui.click(x=393, y=51)
    pyautogui.write('')
    bot.reply_to(message, "Acessando site...")
    pyautogui.press('enter')
    time.sleep(20)
    pyautogui.click(x=1075, y=517)
    time.sleep(15)

    # Preencher o campo de e-mail
    bot.reply_to(message, "Efetuando Login...")
    pyautogui.click(x=1194, y=247)
    pyautogui.write("")
    time.sleep(1)

    # Preencher o campo de senha
    pyautogui.click(x=1118, y=339)
    pyautogui.write("")
    time.sleep(1)

    # Clicar no botão de login
    pyautogui.click(x=1149, y=397)
    bot.reply_to(message, "Login Efetuado")
    time.sleep(5)


@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """ Olá, me chamo CybermancerBot! Por favor, escolha uma de minhas funcionalidades:
    /CHATGPT
    /TEMPERATURA
    /SENHA
    /AUTO
    /VERSION"""
    bot.reply_to(mensagem,texto)


bot.polling()