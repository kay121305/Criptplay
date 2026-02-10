import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import Counter

# ================= CONFIG =================
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

ADMINS = {8431121309}

# ================= GRUPOS =================
grupo1 = {3,6,9,13,16,19,23,26,29,33,36}
grupo2 = {19,15,32,0,26,3,35,12,28,8,23,10,5}
grupo3 = {27,17,25,5}

# SINAIS ESPECIAIS
sinal_369 = {3,6,9}
sinal_010 = {0,10}

# ================= ROLETAS =================
vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
pretos   = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

# ================= CONTROLE =================
historico = []          # ORDEM REAL (NÃO ALTERA)
falha_g1 = falha_g2 = 0
ultimas_5 = []
monitorando = False
contador_4 = 0

# ================= TECLADO =================
def teclado():
    kb = InlineKeyboardMarkup(row_width=6)
    kb.add(*[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(37)])
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    if msg.from_user.id not in ADMINS:
        return
    bot.send_message(
        msg.chat.id,
        "🎰 Criptoplay\nClique no número que saiu:",
        reply_markup=teclado()
    )

# ================= CLIQUE =================
@bot.callback_query_handler(func=lambda call: True)
def clique(call):
    global falha_g1, falha_g2, monitorando, contador_4

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Apenas ADM")
        return

    n = int(call.data)

    # 🔹 REGISTRO NA ORDEM EXATA
    historico.append(n)

    # ================= SINAIS REATIVOS =================
    if n in sinal_369:
        bot.send_message(
            call.message.chat.id,
            f"🎯 SINAL 3–6–9 CONFIRMADO\nNúmero: {n}\n👉 ENTRAR NA PRÓXIMA RODADA"
        )

    if n in sinal_010:
        bot.send_message(
            call.message.chat.id,
            f"🎯 SINAL 0–10 CONFIRMADO\nNúmero: {n}\n👉 ENTRAR NA PRÓXIMA RODADA"
        )

    # ================= ALERTAS GRUPO 1 =================
    falha_g1 = 0 if n in grupo1 else falha_g1 + 1
    if falha_g1 == 10:
        bot.send_message(call.message.chat.id, "🚨 10 falhas — Grupo 1")

    # ================= ALERTAS GRUPO 2 =================
    falha_g2 = 0 if n in grupo2 else falha_g2 + 1
    if falha_g2 == 10:
        bot.send_message(call.message.chat.id, "🚨 10 falhas — Grupo 2")

    # ================= REPETIÇÃO GRUPO 3 =================
    ultimas_5.append(n)
    if len(ultimas_5) > 5:
        ultimas_5.pop(0)

    if not monitorando and len([x for x in ultimas_5 if x in grupo3]) >= 2:
        monitorando = True
        contador_4 = 0

    if monitorando:
        contador_4 += 1
        if n in grupo3:
            bot.send_message(call.message.chat.id, "🚨 Repetição confirmada — Grupo 3")
            monitorando = False
        elif contador_4 >= 4:
            monitorando = False

    # ================= RELATÓRIO 10 =================
    if len(historico) == 10:
        analisar(call.message.chat.id)
        historico.clear()

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=teclado())
    bot.answer_callback_query(call.id)

# ================= ANALISE (ORDEM REAL) =================
def analisar(chat):
    c = Counter(historico)

    quentes = [str(n) for n, _ in c.most_common(3)]
    frios = [str(i) for i in range(37) if i not in c][:6]

    msg = (
        "📊 Criptoplay — 10 Rodadas\n"
        f"Sequência real:\n{' '.join(map(str, historico))}\n\n"
        f"🔥 Quentes: {', '.join(quentes)}\n"
        f"❄️ Frios: {', '.join(frios)}\n\n"
        "⚠️ Entrada sempre NA PRÓXIMA rodada\n"
        "🛑 Gestão obrigatória"
    )

    bot.send_message(chat, msg)

print("🤖 Criptoplay rodando 24h")
bot.infinity_polling()
