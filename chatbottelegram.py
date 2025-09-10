import logging
import g4f
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests


# Configurações
TELEGRAM_BOT_TOKEN = "SEU_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "SUA_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Olá! Sou um bot de IA. Como posso te ajudar?")


async def consultar_cnpj(update: Update, context: CallbackContext) -> None:
    cnpj = update.message.text.strip()
    
    # Verifica se o CNPJ tem 14 dígitos
    if not cnpj.isdigit() or len(cnpj) != 14:
        await update.message.reply_text("⚠️ Envie um CNPJ válido (apenas números, 14 dígitos).")
        return
    
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            await update.message.reply_text("🚫 CNPJ não encontrado ou API indisponível.")
        else:
            resposta = (
                f"📌 **CNPJ:** {data['cnpj']}\n"
                f"🏢 **Nome:** {data['nome']}\n"
                f"📛 **Nome Fantasia:** {data['fantasia']}\n"
                f"📅 **Data de Abertura:** {data['data_situacao']}\n"
                f"📌 **Situação:** {data['situacao']}\n"
                f"🔎 **Atividade Principal:** {data['atividade_principal'][0]['text']} ({data['atividade_principal'][0]['code']})"
            )
            await update.message.reply_text(resposta, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ Erro ao consultar CNPJ. Tente novamente mais tarde.")



async def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    await update.message.reply_text(response)


# Inicializando o bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Rodando o bot
if __name__ == "__main__":
    print("Bot está rodando...")
    app.run_polling()
