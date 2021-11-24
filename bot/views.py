import random

from django.shortcuts import render
import profile
import pytz
from .Buttons import *
import datetime
import time

state_register_full_name = 0
state_register_phone_number = 1
state_admin_main = 2
state_user_main = 3
state_zakaz_name = 4
state_zakaz_adress = 5
state_zakaz_image = 6
state_zakaz_weight = 7
state_zakaz_soni = 8
state_zakaz_height = 9
state_zakaz_phone = 10


def start(update, context):
    update.message.reply_html(
        f"Aссалому алайкум {update.effective_user.first_name}\nХитойдан Ўзбекистонга юкларин хисоблашингиз ва бот орқали жўнатишингиз  мумкин.")
    user_id = update.effective_user.id

    profile, bol = Profile.objects.get_or_create(user_id=user_id)

    if bol:
        update.message.reply_html("Сиз ботдан тўлиқ фойдаланишингиз учун аввал Рўйхатдан ўтишингиз керак\n"
                                  "Тўлиқ исм фамилянгизни китиринг", reply_markup=ReplyKeyboardRemove())
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        username = update.effective_user.username

        profile.first_name = first_name
        profile.last_name = last_name
        profile.username = username
        profile.save()

        return state_register_full_name
    else:
        if profile.status == 'admin':
            update.message.reply_html('маин мену', reply_markup=admin_main_button())
            return state_admin_main

        else:
            update.message.reply_html("маин мену", reply_markup=user_main_button())
            return state_user_main


def command_register_full_name(update, context):
    full_name = update.message.text
    profile = Profile.objects.get(user_id=update.effective_user.id)
    profile.full_name = full_name
    profile.save()
    update.message.reply_html("Рўйхатдан муваффақиятли ўтдингиз, Хитойдан Ўзбекистонга юкларингизни шу бот орқали хисоблашингиз мумкин.",reply_markup=user_main_button())

    return state_user_main


def command_zakaz_main(update, context):
    update.message.reply_html("Юбормоқчи бўлган маҳсулотингизнинг номини киритнг", reply_markup=cancel_button())
    return state_zakaz_name


def command_zakaz_name(update, context):
    name = update.message.text
    if name == cancel:
        update.message.reply_html("main manu", reply_markup=user_main_button())
        return state_user_main
    else:
        user = Profile.objects.get(user_id=update.effective_user.id)
        cargo = Cargo.objects.create(user=user, name=name)
        context.user_data['cargo'] = cargo.id
        update.message.reply_html("Маҳсулот расмини юборинг, агар махсулот расми бўлмаса X сўзини қолдиринг.")
        return state_zakaz_image


def command_zakaz_image(update, context):
    cargo = Cargo.objects.get(id=context.user_data['cargo'])
    photo_file = update.message.photo[-1].get_file()
    filename = int(random.random() * 100)
    photo_file.download(f'photo/{filename}.jpg')
    cargo.image = f'photo/{filename}.jpg'
    cargo.save()
    update.message.reply_html(" Махсулот вазнини киритинг.\n"
                              "(Упаковкадан кейинги вазни/GROSS)"
                              "\nМасалан: 24кг")
    return state_zakaz_weight

def command_user_skipimage(update,context):
    update.message.reply_html(" Махсулот вазнини киритинг.\n"
                              "(Упаковкадан кейинги вазни/GROSS)"
                              "\nМасалан: 24кг")
    return state_zakaz_weight


def command_zakaz_weight(update, context):
    weight = update.message.text
    if weight == cancel:
        update.message.reply_html('main manu', reply_markup=user_main_button())
        cargo = Cargo.objects.get(id=context.user_data['cargo'])
        cargo.delete()
        cargo.save()
        return state_user_main
    else:
        if weight.isdigit():
            cargo = Cargo.objects.get(id=context.user_data['cargo'])
            cargo.weight = weight
            cargo.save()
            update.message.reply_html('Упаковка сонини киритинг!')
            return state_zakaz_soni
        else:
            update.message.reply_html("Маҳсулот вазнини қайта сонларда китинг")
            return state_zakaz_weight


def command_zakaz_soni(update, context):
    soni = update.message.text
    if soni == cancel:
        update.message.reply_html('main manu', reply_markup=user_main_button())
        cargo = Cargo.objects.get(id=context.user_data['cargo'])
        cargo.delete()
        cargo.save()
        return state_user_main
    else:
        if soni.isdigit():
            cargo = Cargo.objects.get(id=context.user_data['cargo'])
            cargo.soni = soni
            cargo.save()
            update.message.reply_html("Махсулот ўлчўвни киритинг!\n(Упаковка ўлчўви)Ўлчамларни см ларда киритинг\t"
                                      "Масалан: 80х90х110")
            return state_zakaz_height
        else:
            update.message.reply_html("Маҳсулот сонини хато киритдингиз\n"
                                      "Илтимос қайта рақамлар билан киритинг")
            return state_zakaz_soni


def command_zakaz_height(update, context):
    ulchami = update.message.text
    if ulchami == cancel:
        update.message.reply_html('main manu', reply_markup=user_main_button())
        cargo = Cargo.objects.get(id=context.user_data['cargo'])
        cargo.delete()
        cargo.save()
        return state_user_main
    else:
        data = ulchami.split('x')
        if len(data) == 3 and data[0].isdigit() and data[1].isdigit() and data[2].isdigit():
            cargo = Cargo.objects.get(id=context.user_data['cargo'])
            cargo.length = data[0]
            cargo.width = data[1]
            cargo.height = data[2]
            cargo.save()
            update.message.reply_html("Телефон рақамингизни киритинг")
            return state_zakaz_phone
        else:
            update.message.reply_html("Маҳсулот ўлчамини хато киритдингиз\n"
                                      "Илтимос қайта киритинг.Ўлчамларни см ларда киритинг"
                                      "\nМасалан: 80х90х110")
            return state_zakaz_height


def command_zakaz_phone(update, context):
    phone = update.message.text
    if phone == cancel:
        update.message.reply_html('main manu', reply_markup=user_main_button())
        cargo = Cargo.objects.get(id=context.user_data['cargo'])
        cargo.delete()
        cargo.save()
        return state_user_main
    else:
        if phone.isdigit():
            cargo = Cargo.objects.get(id=context.user_data['cargo'])
            cargo.phone_number = phone
            cargo.save()
            update.message.reply_html(" Яшаш манзилингизни танланг!", reply_markup=region_buttons())
            return state_zakaz_adress
        else:
            update.message.reply_html("Телефон рақамингизни хато киритдингиз\n"
                                      "Илтимос қайта рақамлар билан киритинг")
            return state_zakaz_phone


def command_zakaz_adress(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    region = Region.objects.get(name=A)
    cargo = Cargo.objects.get(id=context.user_data['cargo'])
    cargo.region = region
    cargo.cargo_id = f"PB{999999-cargo.id}"
    cargo.save()
    admins = Profile.objects.filter(status='admin')
    for i in admins:
        caption = f"""
<b>Заказ_ид</b>        {cargo.cargo_id}
<b>Номи:</b>           {cargo.name}
<b>оғирлиги:</b>       {cargo.weight}
<b>Сони:</b>           {cargo.soni}
<b>ўлчами:</b>         {cargo.length}x{cargo.width}x{cargo.height} = {cargo.length * cargo.height
                                                               * cargo.width} cm^3
<b>Телефон рақами:</b> {cargo.phone_number}
<b>Манзили:</b>        {cargo.region.name}
<b>Заказ берувчи:</b>  {cargo.user.full_name}
                       {cargo.user.first_name}
                       @{cargo.user.username}
        """
        if cargo.image:
            context.bot.send_photo(chat_id=i.user_id, photo=open(f'{cargo.image}', 'rb'), caption=caption, parse_mode='HTML')
        else:
            context.bot.send_message(chat_id=i.user_id, text=caption)
    query.message.reply_html('Сизнинг заказ муаффақоятли қабул қилинди.'
                             f'Сизнинг Заказ_ид: {cargo.cargo_id}'
                             f'\nСиз билан 24 соат давомида бўғланамиз ва нархларни келтириб утамиз', reply_markup=user_main_button())
    return state_user_main


def command_user_cancel(update, context):
    update.message.reply_html('маин мену', reply_markup=user_main_button())
    cargo = Cargo.objects.get(id=context.user_data['cargo'])
    cargo.delete()
    cargo.save()
    return state_user_main


def command_user_contact(update, context):
    update.message.reply_html(
        "Савол ва таклифлар юзасидан 998503567 рақамига ёки @labbay_admin га мурожаат қилинг!")
    return state_user_main


def command_admin_main(update, context):
    profile = Profile.objects.all()
    cargo = Cargo.objects.all()

    update.message.reply_html(f"Ботдаги фойдаланувчилар сони: {len(profile)}\n"
                              f"Бот орқали заказлар сони: {len(cargo)}")
    return state_admin_main
