#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = "8581315644:AAH4fKp73bLFWu8J4qjfxqese-e0N1RmQJ8"
ADMIN_ID = 5784333126

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")

usuarios = {}  # Mapeia message_id_encaminhado -> (user_id, user_nome)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Bem-vindo(a) ao suporte do *KDrama Max*!\n\n"
        "💬 Me manda sua mensagem — sugestão de série, pedido ou dúvida — "
        "e responderei o mais rápido possível! 🎬",
        parse_mode="Markdown"
    )


async def receber_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    user_id = user.id

    if user_id == ADMIN_ID:
        return  # Admin não se manda mensagem

    nome = user.first_name or "Usuário"
    username = f"@{user.username}" if user.username else "sem @"

    texto_encaminhado = (
        f"📩 *Nova mensagem do grupo KDrama Max*\n"
        f"👤 {nome} ({username})\n"
        f"🆔 `{user_id}`\n\n"
        f"💬 {msg.text or '[mídia]'}\n\n"
        f"_Responda esta mensagem para responder o usuário._"
    )

    enviado = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=texto_encaminhado,
        parse_mode="Markdown"
    )

    usuarios[enviado.message_id] = (user_id, nome)

    await msg.reply_text(
        "✅ Mensagem recebida! Responderei em breve. 😊"
    )


async def responder_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.from_user.id != ADMIN_ID:
        return

    if not msg.reply_to_message:
        await msg.reply_text("↩️ Para responder, use *Reply* na mensagem do usuário.", parse_mode="Markdown")
        return

    msg_id_original = msg.reply_to_message.message_id
    dados = usuarios.get(msg_id_original)

    if not dados:
        await msg.reply_text("⚠️ Não encontrei o usuário desta mensagem. Pode ter reiniciado o bot.")
        return

    user_id, nome = dados

    await context.bot.send_message(
        chat_id=user_id,
        text=f"📬 *Resposta do KDrama Max:*\n\n{msg.text}",
        parse_mode="Markdown"
    )

    await msg.reply_text(f"✅ Resposta enviada para {nome}!")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_ID) & filters.REPLY, responder_usuario))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_usuario))

    print("🤖 KDrama Max Bot rodando...")
    app.run_polling()
