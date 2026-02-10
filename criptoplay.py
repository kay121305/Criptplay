import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============== CONFIG ==============
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

ADMINS = {8431121309}

# ============== GRUPOS ==============
grupo_A = {3,6,9,13,16,19,23,26,29,33,36}
grupo_B = {19,15,32,0,25,3,35,12,28}
grupo_total = grupo_A.union(grupo_B)

# ============== CONTROLE ==============
falha = 0
sinal_ativo = False
gale = 0

green = 0
loss = 0

historico = []

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
    global falha, sinal_ativo, gale, green, loss

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Apenas ADM")
        return

    n = int(call.data)
    historico.append(n)

    # ================= SEM SINAL =================
    if not sinal_ativo:
        if n in grupo_total:
            falha = 0
        else:
            falha += 1

        if falha == 10:
            sinal_ativo = True
            gale = 0
            falha = 0
            bot.send_message(
                call.message.chat.id,
                "🚨 **SINAL DE ENTRADA**\n"
                "10 rodadas sem números do grupo\n"
                "🎯 Entrada na PRÓXIMA\n"
                "♻️ Até 3 gales",
                parse_mode="Markdown"
            )

    # ================= COM SINAL =================
    else:
        gale += 1

        if n in grupo_total:
            green += 1
            bot.send_message(
                call.message.chat.id,
                f"🟢 **GREEN**\n"
                f"Número: {n}\n"
                f"Resultado: {green}x{loss}",
                parse_mode="Markdown"
            )
            sinal_ativo = False
            gale = 0

        elif gale >= 3:
            loss += 1
            bot.send_message(
                call.message.chat.id,
                f"🔴 **LOSS**\n"
                f"Não bateu em 3 gales\n"
                f"Resultado: {green}x{loss}",
                parse_mode="Markdown"
            )
            sinal_ativo = False
            gale = 0

        else:
            bot.send_message(
                call.message.chat.id,
                f"⚠️ GALE {gale}/3\n"
                "Manter entrada",
                parse_mode="Markdown"
            )

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=teclado()
    )
    bot.answer_callback_query(call.id)

print("🤖 Criptoplay rodando 24h")
bot.infinity_polling()
