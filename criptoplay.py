import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

GRUPO_ID = -1003629208122
ADMIN_ID = 8502821738

# ============================================================
# DEFINIÇÃO DE CORES OFICIAIS EUROPEIAS
# ============================================================

VERMELHOS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

PRETOS = {
    2,4,6,8,10,11,13,15,17,
    20,22,24,26,28,29,31,33,35
}

VERDE = {0}

# ============================================================
# LAYOUT OFICIAL EUROPEU (FORMATO MESA)
# ============================================================

LINHA_ZERO = [0]

LINHA_1 = [3,6,9,12,15,18,21,24,27,30,33,36]
LINHA_2 = [2,5,8,11,14,17,20,23,26,29,32,35]
LINHA_3 = [1,4,7,10,13,16,19,22,25,28,31,34]

# ============================================================
# FUNÇÃO PARA IDENTIFICAR COR
# ============================================================

def obter_cor(numero):
    if numero in VERMELHOS:
        return "🔴"
    elif numero in PRETOS:
        return "⚫"
    else:
        return "🟢"

# ============================================================
# CRIAR TECLADO PROFISSIONAL FORMATO MESA
# ============================================================

def criar_teclado_roleta():
    teclado = InlineKeyboardMarkup(row_width=12)

    # Linha do ZERO
    linha_zero_btn = []
    for num in LINHA_ZERO:
        linha_zero_btn.append(
            InlineKeyboardButton(
                f"{obter_cor(num)} {num}",
                callback_data=str(num)
            )
        )
    teclado.row(*linha_zero_btn)

    # Linha Superior (3,6,9...)
    linha1_btn = []
    for num in LINHA_1:
        linha1_btn.append(
            InlineKeyboardButton(
                f"{obter_cor(num)} {num}",
                callback_data=str(num)
            )
        )
    teclado.row(*linha1_btn)

    # Linha do Meio (2,5,8...)
    linha2_btn = []
    for num in LINHA_2:
        linha2_btn.append(
            InlineKeyboardButton(
                f"{obter_cor(num)} {num}",
                callback_data=str(num)
            )
        )
    teclado.row(*linha2_btn)

    # Linha Inferior (1,4,7...)
    linha3_btn = []
    for num in LINHA_3:
        linha3_btn.append(
            InlineKeyboardButton(
                f"{obter_cor(num)} {num}",
                callback_data=str(num)
            )
        )
    teclado.row(*linha3_btn)

    return teclado

# ============================================================
# PAINEL VISUAL
# ============================================================

def painel_texto():
    return """
🎰 PAINEL PROFISSIONAL – ROLETA EUROPEIA

Formato oficial de mesa física
Selecione o número conforme resultado real.
"""

# ============================================================
# COMANDO START
# ============================================================

@bot.message_handler(commands=['start'])
def iniciar(msg):
    if msg.from_user.id != ADMIN_ID:
        return

    bot.send_message(
        GRUPO_ID,
        painel_texto(),
        reply_markup=criar_teclado_roleta()
    )

# ============================================================
# CLIQUE NOS NÚMEROS
# ============================================================

@bot.callback_query_handler(func=lambda call: True)
def receber_numero(call):
    if call.from_user.id != ADMIN_ID:
        return

    numero = int(call.data)

    bot.answer_callback_query(
        call.id,
        text=f"Número selecionado: {numero}"
    )

# ============================================================
# INICIALIZAÇÃO
# ============================================================

print("🎰 PAINEL ROLETA EUROPEIA PROFISSIONAL ATIVO")
bot.infinity_polling()
