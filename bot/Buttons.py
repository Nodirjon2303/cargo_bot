from .models import *
from telegram import ReplyKeyboardMarkup, \
    InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

zakaz_qoldirish = '➕Заказ қолдириш'
boglanish = 'Боғланиш'
status = '📝Статистика'
cancel = 'Бекор қилиш'

def user_main_button():
    button = [
        [zakaz_qoldirish],
        [boglanish]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True)

def admin_main_button():
    button = [
        [status]
    ]

    return ReplyKeyboardMarkup(button, resize_keyboard=True)


def cancel_button():
    button = [
        [cancel]
    ]
    return ReplyKeyboardMarkup(button)

def region_buttons():
    button = []
    regions = Region.objects.all()
    res = []
    for i in regions:
        res.append(InlineKeyboardButton(f'{i.name}', callback_data=f'{i.name}'))
        if len(res) == 2:
            button.append(res)
            res = []
    if len(res) > 0:
        button.append(res)
    return InlineKeyboardMarkup(button)
