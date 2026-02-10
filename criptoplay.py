import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import Counter

# ============== CONFIG ==============
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

ADMINS = {8431121309}

# ============== ESTRATÉGIAS ==============
grupo_A = {3,6,9,13,16,19,23,26,29,33,36}
grupo_B = {19,15,32,0,25,3,35,12,28}

# ============== CORES ==============
vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
pretos   = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

# ============== CONTROLE ==============
historico = []
falha_A = 0
falha_B = 0

# ============== TECLADO ==============
def teclado():
    kb = InlineKeyboardMarkup(row_width=6)
    kb.add(*[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(37)])
    return kb

# ============== START ==============
@bot.message_handler(commands=['start'])
def start(msg):
    if msg.from_user.id not in ADMINS:
        return
    bot.send_message(
        msg.chat.id,
        "🎰 Criptoplay\nClique no número que saiu:",
        reply_markup=teclado()
    )

# ============== CLIQUE ==============
@bot.callback_query_handler(func=lambda call: True)
def clique(call):
    global falha_A, falha_B

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Apenas ADM")
        return

    n = int(call.data)
    historico.append(n)

    # --------- ESTRATÉGIA A ---------
    if n in grupo_A:
        falha_A = 0
    else:
        falha_A += 1
        if falha_A == 10:
            bot.send_message(
                call.message.chat.id,
                "🚨 ALERTA ESTRATÉGIA A\n"
                "10 rodadas sem números do grupo\n"
                "👉 POSSÍVEL ENTRADA NA PRÓXIMA"
            )

    # --------- ESTRATÉGIA B ---------
    if n in grupo_B:
        falha_B = 0
    else:
        falha_B += 1
        if falha_B == 10:
            bot.send_message(
                call.message.chat.id,
                "🚨 ALERTA ESTRATÉGIA B\n"
                "10 rodadas sem números do grupo\n"
                "👉 POSSÍVEL ENTRADA NA PRÓXIMA"
            )

    # --------- RELATÓRIO ---------
    if len(historico) == 10:
        analisar(call.message.chat.id)
        historico.clear()

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=teclado()
    )
    bot.answer_callback_query(call.id)

# ============== ANÁLISE COMPLEMENTAR ==============
def analisar(chat):
    c = Counter(historico)

    pares = len([n for n in historico if n != 0 and n % 2 == 0])
    impares = len(historico) - pares

    verm = len([n for n in historico if n in vermelhos])
    pret = len([n for n in historico if n in pretos])

    baixa = len([n for n in historico if 1 <= n <= 18])
    alta  = len([n for n in historico if 19 <= n <= 36])

    msg = (
        "📊 Análise — 10 Rodadas\n"
        f"Sequência: {' '.join(map(str, historico))}\n\n"
        f"Par/Ímpar: {pares}/{impares}\n"
        f"Vermelho/Preto: {verm}/{pret}\n"
        f"Baixa/Alta: {baixa}/{alta}\n\n"
        "🧠 Leitura:\n"
        "Mercado em correção — aguarde confirmação\n\n"
        "🛑 Gestão obrigatória"
    )

    bot.send_message(chat, msg)

print("🤖 Criptoplay rodando 24h")
bot.infinity_polling()
