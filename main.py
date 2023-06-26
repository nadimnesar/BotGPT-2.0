import telegram.ext
import openai
import numpy

openai.api_key = "Your OpenAi Key"
token = "Your Telegram Bot Token"

messages = []


def start(update, context):
    messages.clear()
    messages.append({"role": "system", "content": "Assistant"})
    messages.append({"role": "user", "content": "From now, your name is BotGPT 2.0!"})
    update.message.reply_text("Hey! This is your assistant BotGPT 2.0!")


def ask(update, context):
    messages.append({"role": "user", "content": update.message.text[5:]})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    update.message.reply_text(reply)


def img(update, context):
    response = openai.Image.create(
        prompt=update.message.text[5:],
        n=1,
        size="1024x1024")
    reply = response['data'][0]['url']
    update.message.reply_text(reply)


def handle_message(update, context):
    update.message.reply_text(
        "If you want to ask anything use, /ask Your Text.\nIf you want to "
        "create a image use, /img Your Text.\nIf you want to reset the bot use, /start.")


updater = telegram.ext.Updater(token, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler('start', start))
disp.add_handler(telegram.ext.CommandHandler('ask', ask))
disp.add_handler(telegram.ext.CommandHandler('img', img))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
