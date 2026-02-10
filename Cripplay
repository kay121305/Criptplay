import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# TOKEN DO BOT
# =========================
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

# =========================
# IDS DOS ADMINS
# =========================
ADMINS = {8431121309}  # troque pelo SEU ID do Telegram

# =========================
# GRUPOS DE NÚMEROS
# =========================
grupo1 = {3, 6, 9, 13, 16, 19, 23, 26, 29, 33, 36}
grupo2 = {19, 15, 32, 0, 26, 3, 35, 12, 28, 8, 23, 10, 5}
grupo3 = {27, 17, 25, 5}

# =========================
# CONTADORES
# =========================
falha_g1 = 0
falha_g2 = 0
ultimas_5 = []
monitorando_rep = False
contador_4 = 0

# =========================
# TECLADO 0–36
# =========================
def teclado_roleta():
    kb = InlineKeyboardMarkup(row_width=6)
    botoes = [
        InlineKeyboardButton(str(i), callback_data=str(i))
        for i in range(37)
    ]
    kb.add(*botoes)
    return kb

# =========================
# START (USAR NO CANAL)
# =========================
@bot.message_handler(commands=["start"])
def start(msg):
    if msg.from_user.id not in ADMINS:
        return

    bot.send_message(
        msg.chat.id,
        "🎰 *$Criptoplay$ — Painel de Operação*\n\n"
        "Clique no número que saiu na roleta:",
        reply_markup=teclado_roleta(),
        parse_mode="Markdown"
    )

# =========================
# RECEBER CLIQUE DOS BOTÕES
# =========================
@bot.callback_query_handler(func=lambda call: True)
def receber(call):
    global falha_g1, falha_g2, ultimas_5, monitorando_rep, contador_4

    # BLOQUEIA NÃO-ADM
    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(
            call.id,
            "⛔ Apenas admins podem clicar."
        )
        return

    numero = int(call.data)

    # -------- REGRA 1 --------
    if numero in grupo1:
        falha_g1 = 0
    else:
        falha_g1 += 1
        if falha_g1 == 10:
            bot.send_message(
                call.message.chat.id,
                "🚨 *ALERTA 1*\n"
                "10 rodadas sem números do GRUPO 1",
                parse_mode="Markdown"
            )

    # -------- REGRA 2 --------
    if numero in grupo2:
        falha_g2 = 0
    else:
        falha_g2 += 1
        if falha_g2 == 10:
            bot.send_message(
                call.message.chat.id,
                "🚨 *ALERTA 2*\n"
                "10 rodadas sem números do GRUPO 2",
                parse_mode="Markdown"
            )

    # -------- REGRA 3 --------
    ultimas_5.append(numero)
    if len(ultimas_5) > 5:
        ultimas_5.pop(0)

    qtd_rep = len([n for n in ultimas_5 if n in grupo3])

    if not monitorando_rep and qtd_rep >= 2:
        monitorando_rep = True
        contador_4 = 0

    if monitorando_rep:
        contador_4 += 1

        if numero in grupo3:
            bot.send_message(
                call.message.chat.id,
                "🚨 *ALERTA 3*\n"
                "Padrão de repetição confirmado (GRUPO 3)",
                parse_mode="Markdown"
            )
            monitorando_rep = False
            contador_4 = 0

        elif contador_4 >= 4:
            monitorando_rep = False
            contador_4 = 0

    # MANTÉM O TECLADO ATIVO
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=teclado_roleta()
    )

    bot.answer_callback_query(call.id)

# =========================
# INICIAR BOT
# =========================
print("🤖 $Criptoplay$ rodando 24h...")
bot.infinity_polling()
