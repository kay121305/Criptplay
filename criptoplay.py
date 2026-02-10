import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import Counter

# =========================
# CONFIGURAÇÕES
# =========================
API_TOKEN = "8502821738:AAFMPDzVKl9B1KIPvp5dX9jhRBIScy_SQv0"
bot = telebot.TeleBot(API_TOKEN)

ADMINS = {8431121309}  # COLOQUE SEU ID AQUI

# =========================
# GRUPOS DE ALERTA
# =========================
grupo1 = {3,6,9,13,16,19,23,26,29,33,36}
grupo2 = {19,15,32,0,26,3,35,12,28,8,23,10,5}
grupo3 = {27,17,25,5}

# =========================
# ROLETAS
# =========================
vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
pretos   = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

col1 = {1,4,7,10,13,16,19,22,25,28,31,34}
col2 = {2,5,8,11,14,17,20,23,26,29,32,35}
col3 = {3,6,9,12,15,18,21,24,27,30,33,36}

# =========================
# CONTROLE
# =========================
historico = []
falha_g1 = 0
falha_g2 = 0
ultimas_5 = []
monitorando = False
contador_4 = 0

# =========================
# TECLADO
# =========================
def teclado_roleta():
    kb = InlineKeyboardMarkup(row_width=6)
    botoes = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(37)]
    kb.add(*botoes)
    return kb

# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def start(msg):
    if msg.from_user.id not in ADMINS:
        return
    bot.send_message(
        msg.chat.id,
        "🎰 **$Criptoplay$ — Painel Profissional**\n\n"
        "👉 Clique no número que saiu na roleta:",
        reply_markup=teclado_roleta(),
        parse_mode="Markdown"
    )

# =========================
# CLIQUE
# =========================
@bot.callback_query_handler(func=lambda call: True)
def registrar(call):
    global falha_g1, falha_g2, monitorando, contador_4

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "⛔ Apenas ADM")
        return

    n = int(call.data)
    historico.append(n)

    # -------- ALERTA GRUPO 1 --------
    if n in grupo1:
        falha_g1 = 0
    else:
        falha_g1 += 1
        if falha_g1 == 10:
            bot.send_message(call.message.chat.id, "🚨 **ALERTA:** 10 falhas — Grupo 1", parse_mode="Markdown")

    # -------- ALERTA GRUPO 2 --------
    if n in grupo2:
        falha_g2 = 0
    else:
        falha_g2 += 1
        if falha_g2 == 10:
            bot.send_message(call.message.chat.id, "🚨 **ALERTA:** 10 falhas — Grupo 2", parse_mode="Markdown")

    # -------- REPETIÇÃO GRUPO 3 --------
    ultimas_5.append(n)
    if len(ultimas_5) > 5:
        ultimas_5.pop(0)

    qtd = len([x for x in ultimas_5 if x in grupo3])

    if not monitorando and qtd >= 2:
        monitorando = True
        contador_4 = 0

    if monitorando:
        contador_4 += 1
        if n in grupo3:
            bot.send_message(call.message.chat.id, "🚨 **ALERTA:** Repetição confirmada — Grupo 3", parse_mode="Markdown")
            monitorando = False
        elif contador_4 >= 4:
            monitorando = False

    # -------- RELATÓRIO A CADA 10 --------
    if len(historico) == 10:
        analisar(call.message.chat.id)
        historico.clear()

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=teclado_roleta()
    )
    bot.answer_callback_query(call.id)

# =========================
# ANALISE PROFISSIONAL
# =========================
def analisar(chat):
    c = Counter(historico)
    quentes = c.most_common(3)
    frios = sorted([i for i in range(37) if i not in c])

    pares = len([n for n in historico if n != 0 and n % 2 == 0])
    impares = len(historico) - pares

    verm = len([n for n in historico if n in vermelhos])
    pret = len([n for n in historico if n in pretos])

    baixa = len([n for n in historico if 1 <= n <= 18])
    alta  = len([n for n in historico if 19 <= n <= 36])

    col_1 = len([n for n in historico if n in col1])
    col_2 = len([n for n in historico if n in col2])
    col_3 = len([n for n in historico if n in col3])

    d1 = len([n for n in historico if 1 <= n <= 12])
    d2 = len([n for n in historico if 13 <= n <= 24])
    d3 = len([n for n in historico if 25 <= n <= 36])

    msg = (
        "📊 **$Criptoplay$ — RELATÓRIO (10 RODADAS)**\n\n"
        "🎯 **NÚMEROS:**\n"
        f"{' · '.join(map(str, historico))}\n\n"
        "━━━━━━━━━━━━━━\n"
        "🔥 **ZONAS QUENTES**\n" +
        "\n".join([f"{i+1}️⃣ {n} → {q}x" for i, (n, q) in enumerate(quentes)]) +
        "\n\n❄️ **ZONAS FRIAS**\n"
        f"{' · '.join(map(str, frios[:10]))}\n\n"
        "━━━━━━━━━━━━━━\n"
        "⚖️ **PAR / ÍMPAR**\n"
        f"Par: {pares}\nÍmpar: {impares}\n\n"
        "🎨 **COR**\n"
        f"Vermelho: {verm}\nPreto: {pret}\n\n"
        "━━━━━━━━━━━━━━\n"
        "⬆️⬇️ **ALTURA**\n"
        f"0–18: {baixa}\n19–36: {alta}\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 **COLUNAS**\n"
        f"Coluna 1: {col_1}\nColuna 2: {col_2}\nColuna 3: {col_3}\n\n"
        "━━━━━━━━━━━━━━\n"
        "📦 **DÚZIAS**\n"
        f"1ª: {d1}\n2ª: {d2}\n3ª: {d3}\n\n"
        "━━━━━━━━━━━━━━\n"
        "🧠 **LEITURA DO BOT**\n"
        "• Mercado equilibrado\n"
        "• Observe atrasos antes da entrada\n\n"
        "🛑 **Gestão:** Stop Win +20% | Stop Loss −30%"
    )

    bot.send_message(chat, msg, parse_mode="Markdown")

print("🤖 $Criptoplay$ rodando 24h...")
bot.infinity_polling()
