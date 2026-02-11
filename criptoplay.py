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

# Histórico de números para o resumo
ultimos_numeros = []

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

# ================= FUNÇÃO DE RESUMO =================
def resumo_15_rodadas(chat_id):
    if len(ultimos_numeros) < 15:
        return

    # Pegando os últimos 15 números
    ultimos_15 = ultimos_numeros[-15:]

    preto = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
    vermelho = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

    resumo = {
        "Preto": sum(1 for n in ultimos_15 if n in preto),
        "Vermelho": sum(1 for n in ultimos_15 if n in vermelho),
        "Alto": sum(1 for n in ultimos_15 if 19 <= n <= 36),
        "Baixo": sum(1 for n in ultimos_15 if 1 <= n <= 18),
        "Par": sum(1 for n in ultimos_15 if n != 0 and n % 2 == 0),
        "Ímpar": sum(1 for n in ultimos_15 if n % 2 != 0),
    }

    bot.send_message(
        chat_id,
        f"📊 **Resumo das últimas 15 rodadas**\n"
        f"⬛ Preto: {resumo['Preto']}  🔴 Vermelho: {resumo['Vermelho']}\n"
        f"⬆️ Alto: {resumo['Alto']}  ⬇️ Baixo: {resumo['Baixo']}\n"
        f"➗ Par: {resumo['Par']}  ❌ Ímpar: {resumo['Ímpar']}",
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

    # Adiciona ao histórico
    ultimos_numeros.append(n)

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

        # ========== DISPARO DE SINAL ==========
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
                f"⏭️ Entrar na PRÓXIMA rodada após o número: **{n}**\n"
                f"♻️ Até 3 gales\n"
                f"🎰 Roleta de aposta: **AutoRolet**",
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

    # ========== RESUMO A CADA 15 RODADAS ==========
    if len(ultimos_numeros) % 15 == 0:
        resumo_15_rodadas(call.message.chat.id)

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=teclado()
    )
    bot.answer_callback_query(call.id)

print("🤖 Criptoplay rodando 24h")
bot.infinity_polling()
