from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from django.conf import settings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler

from bot.views import *


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )
        conv_hand = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text, start)
            ],
            states={
                state_register_full_name: [
                    MessageHandler(Filters.text, command_register_full_name)
                ],
                state_user_main: [
                    MessageHandler(Filters.regex('^(' + zakaz_qoldirish + ')$'), command_zakaz_main),
                    MessageHandler(Filters.regex('^(' + boglanish + ')$'), command_user_contact),

                ],
                state_admin_main:[
                    MessageHandler(Filters.regex('^(' + status + ')$'), command_admin_main)
                ],
                state_zakaz_name: [
                    MessageHandler(Filters.text, command_zakaz_name)
                ],
                state_zakaz_image: [
                    MessageHandler(Filters.regex('^(' + cancel + ')$'), command_user_cancel),
                    MessageHandler(Filters.photo, command_zakaz_image)
                ],
                state_zakaz_weight: [
                    MessageHandler(Filters.text, command_zakaz_weight)
                ],
                state_zakaz_soni: [
                    MessageHandler(Filters.text, command_zakaz_soni)
                ],
                state_zakaz_height: [
                    MessageHandler(Filters.text, command_zakaz_height)
                ],
                state_zakaz_phone: [
                    MessageHandler(Filters.text, command_zakaz_phone)
                ],
                state_zakaz_adress: [
                    MessageHandler(Filters.regex('^(' + cancel + ')$'), command_user_cancel),
                    CallbackQueryHandler(command_zakaz_adress)
                ]

            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )
        updater.dispatcher.add_handler(conv_hand)

        updater.start_polling()
        updater.idle()