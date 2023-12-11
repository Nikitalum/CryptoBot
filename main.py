import telebot
from Config import keys, TOKEN
from Extensions import ConvertionException, CryptoConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
    \n<имя валюты, в которую надо перевести первую валюту> \
    \n<количество переводимой валюты>\nСписок всех доступных валют доступен по команде: \n/values'
    bot.reply_to(message,text)
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Количество параметров должно быть равно трем.\nКоманда не распознана')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        #text = f'Цена {amount} {quote}(а/ов/ей) в {base}(ах/ях) - {(total_base * (float(amount)))}'
        text = f'Цена {amount} {quote}(а/ов/ей) в {base}(ах/ях) - {round((total_base * (float(amount))), 8)}'
        bot.send_message(message.chat.id, text)

bot.infinity_polling()