import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= CONFIG =================
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

ADMINS = {8431121309}

# ================= GRUPOS =================
grupo_369 = {3,6,9,13,16,19,23,26,29,33,36}
grupo_010 = {19,15,32,0,25,3,35,12,28}

# ================= CONTROLE =================
falha_369 = 0
falha_010 = 0

sinal_ativo = False
grupo_sinal = ""
gale = 0

green = 0
loss = 0

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
        "🎰 **Criptoplay — Painel**\nClique no número que saiu:",
        reply_markup=teclado(),
        parse_mode="Markdown"
    )

# ================= CLIQUE =================
@bot.callback_query_handler(func=lambda call: True)
def clique(call):
    global falha_369, falha_010, sinal_ativo, grupo_sinal, gale, green, loss

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Apenas ADM")
        return

    n = int(call.data)

    # ========== SEM SINAL ==========
    if not sinal_ativo:
        # grupo 3-6-9
        if n in grupo_369:
            falha_369 = 0
        else:
            falha_369 += 1

        # grupo 0-10
        if n in grupo_010:
            falha_010 = 0
        else:
            falha_010 += 1

        # DISPARO DE SINAL
        if falha_369 >= 10:
            sinal_ativo = True
            grupo_sinal = "3-6-9"
        elif falha_010 >= 10:
            sinal_ativo = True
            grupo_sinal = "0-10"

        if sinal_ativo:
            gale = 0
            falha_369 = 0
            falha_010 = 0

            bot.send_message(
                call.message.chat.id,
                f"🚨 **SINAL DE ENTRADA** 🚨\n"
                f"❌ 10 rodadas sem sair\n"
                f"🎯 Estratégia: **{grupo_sinal}**\n"
                f"⏭️ Entrar na PRÓXIMA\n"
                f"♻️ Até 3 gales",
                parse_mode="Markdown"
            )

    # ========== COM SINAL ==========
    else:
        gale += 1

        grupo_atual = grupo_369 if grupo_sinal == "3-6-9" else grupo_010

        if n in grupo_atual:
            green += 1
            bot.send_message(
                call.message.chat.id,
                f"🟢 **GREEN**\n"
                f"🎯 Estratégia {grupo_sinal}\n"
                f"📊 Placar: {green}x{loss}",
                parse_mode="Markdown"
            )
            sinal_ativo = False
            gale = 0

        elif gale >= 3:
            loss += 1
            bot.send_message(
                call.message.chat.id,
                f"🔴 **LOSS**\n"
                f"🎯 Estratégia {grupo_sinal}\n"
                f"📊 Placar: {green}x{loss}",
                parse_mode="Markdown"
            )
            sinal_ativo = False
            gale = 0

        else:
            bot.send_message(
                call.message.chat.id,
                f"⚠️ **GALE {gale}/3**\n"
                f"🎯 Estratégia {grupo_sinal}",
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
