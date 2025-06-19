import telebot

TOKEN = 'Токен бота из '

bot = telebot.TeleBot(TOKEN)


# Ответ на стикеры
@bot.message_handler(content_types=['sticker'])
def echo_sticker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

# Ответ на GIF-анимацию (animation)
@bot.message_handler(content_types=['animation'])
def echo_gif(message):
    bot.send_animation(message.chat.id, message.animation.file_id)

# Если хочешь отвечать и на видео-гифки
@bot.message_handler(content_types=['video'])
def echo_video(message):
    bot.send_video(message.chat.id, message.video.file_id)

bot.polling(none_stop=True)