import datetime
import json
import logging
import re
import time

import telebot
from telebot import types


bot = telebot.TeleBot("xxx")

user_account = {}
MAX_PAGE_COUNT = 4
buy_dict = {1: "xx", 2: "xx", 3: "xxl",
            4: "xs"}

sell_dict = {1: "xxs", 2: "l", 3: "m",
             4: "xx"}

# telebot.logger.setLevel(logging.DEBUG)


# DEBUG, INFO, WARNING, ERROR, CRITICAL

class UserState:
    def __init__(self):
        self.state = {}

    def set_state(self, chat_id, command, value):
        if chat_id not in self.state:
            self.state[chat_id] = {}
        self.state[chat_id][command] = value

    def get_state(self, chat_id, command):
        if chat_id in self.state and command in self.state[chat_id]:
            return self.state[chat_id][command]
        return None


@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    start(chat_id)




@bot.message_handler(func=lambda message: True)
def handle_interaction(message):
    chat_id = message.chat.id
    if user_account[chat_id].get_state(chat_id, 'input_hash'):
        if check_hash(message.text):
            update_user_transaction_hash(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, 'input_hash', False)
            text = "*xxx"
            markup_inline = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🔙Back', callback_data='back')
            markup_inline.add(button1)
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)
            user_account[chat_id].set_state(chat_id, 'deposit_done', False)
        else:
            text = "❌*..*"
            bot.send_message(chat_id, text, parse_mode="Markdown")
    elif user_account[chat_id].get_state(chat_id, 'input_name'):
        if message.text:
            user_account[chat_id].set_state(chat_id, '_status_name', message.text)
            update_user_name(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, '_status_name', False)
            text = "🫡*..*"
            bot.send_message(chat_id, text, parse_mode="Markdown")
            user_account[chat_id].set_state(chat_id, '_status_email', True)
            # record_sell(chat_id)
    elif user_account[chat_id].get_state(chat_id, '_status_email'):
        if input_email(message.text):
            user_account[chat_id].set_state(chat_id, 'sell_status_email', message.text)
            update_user_email(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, '_status_email', False)
            text = "xxww."
            markup_inline = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🔙Return', callback_data='back')
            markup_inline.add(button1)
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup_inline)
            user_account[chat_id].set_state(chat_id, 'back_interface', "start")
            record_sell(chat_id)
        else:
            text = "zz"
            bot.send_message(chat_id, text, parse_mode='Markdown')
            user_account[chat_id].set_state(chat_id, 'input_sell_status_email', True)

    elif user_account[chat_id].get_state(chat_id, 'input_wish_sell_ip'):
        if message.text:
            user_account[chat_id].set_state(chat_id, 'sell_status_type', message.text)
            user_account[chat_id].set_state(chat_id, 'input_wish_sell_ip', False)
            text = "🫡*.*"
            bot.send_message(chat_id, text, parse_mode='Markdown')
            user_account[chat_id].set_state(chat_id, 'input_sell_status_name', True)
            # record_sell(chat_id)


    elif user_account[chat_id].get_state(chat_id, 'input_confirm_email'):
        if input_email(message.text):
            update_user_email(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, 'input_contact_email', False)
            text = "xxx"
            bot.send_message(chat_id, text, parse_mode="Markdown")
            user_account[chat_id].set_state(chat_id, 'input_name', True)
        else:
            text = "Plll"
            bot.send_message(chat_id, text, parse_mode='Markdown')
    elif user_account[chat_id].get_state(chat_id, 'input_name'):
        if message.text:
            update_user_name(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, 'input_name', False)
            text = "Cxxx ."
            markup_inline = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🔙 Back', callback_data='back')
            markup_inline.add(button1)
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup_inline)
            user_account[chat_id].set_state(chat_id, 'current_interface', 'start')

    elif user_account[chat_id].get_state(chat_id, 'input_confirm2_email'):
        if input_email(message.text):
            update_user_email(chat_id, message.text)
            user_account[chat_id].set_state(chat_id, 'input_contact_email', False)
            text = """*x"""
            markup_inline = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🔙 Back', callback_data='back')
            markup_inline.add(button1)
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup_inline)
            user_account[chat_id].set_state(chat_id, 'current_interface', 'start')
        else:
            text = "P"
            bot.send_message(chat_id, text, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    if data == 'b_ip':
        buy_ip(chat_id)
    elif data == 'ip_discovery':
        ip_discovery(chat_id)
    elif data == "r":
        user_account[chat_id].set_state(chat_id, 'current_page', 1)
        residential_proxies_browse(chat_id, message_id)

    elif data == "s":
        user_account[chat_id].set_state(chat_id, 'current_page', 2)
        residential_proxies_browse(chat_id, message_id)

    elif data == "d":
        user_account[chat_id].set_state(chat_id, 'current_page', 3)
        residential_proxies_browse(chat_id, message_id)

    elif data == "m":
        user_account[chat_id].set_state(chat_id, 'current_page', 4)
        residential_proxies_browse(chat_id, message_id)

    elif data == "next":
        page = user_account[chat_id].get_state(chat_id, 'current_page')
        user_account[chat_id].set_state(chat_id, 'current_page', page + 1)
        residential_proxies_browse(chat_id, message_id)
    elif data == "previous":
        page = user_account[chat_id].get_state(chat_id, 'current_page')
        user_account[chat_id].set_state(chat_id, 'current_page', page - 1)
        residential_proxies_browse(chat_id, message_id)

    elif data == "sell_status1":
        user_account[chat_id].set_state(chat_id, 'sell_status', 1)
        sell_status(chat_id)
    elif data == "sell_status2":
        user_account[chat_id].set_state(chat_id, 'sell_status', 2)
        sell_status(chat_id)
    elif data == "disable":
        is_node_alerts(chat_id)
        live_alerts(chat_id)
    elif data == "Others":
        Others(chat_id)
    elif data == "help":
        help(chat_id)



def record_sell(chat_id):
    ip_text = user_account[chat_id].get_state(chat_id, 'sell_status_type')
    name = user_account[chat_id].get_state(chat_id, 'sell_status_name')
    email = user_account[chat_id].get_state(chat_id, 'sell_status_email')
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    sell_info_dict = get_user_info(chat_id)["sell_info"]
    if not sell_info_dict:
        sell_info = '{{"{product_name}":"{name},{email},{formatted_time}"}}'.format(product_name=ip_text,
                                                                                    formatted_time=formatted_time,
                                                                                    name=name, email=email)
    else:
        sell_info = json.loads(sell_info_dict)
        sell_info[ip_text] = ",".join([str(name), str(email), str(formatted_time)])
    update_user_sell_info(chat_id, '{}'.format(sell_info).replace("'", '"'))


def deposit(chat_id):
    base_set(chat_id)
    user = get_demetic(chat_id)
    text = deposit_text(user["wallet_address"])
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('✅Deposit Done', callback_data='deposit_done')
    markup_inline.add(button1)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def deposit_done(chat_id):
    text = "*Please  *👇"
    bot.send_message(chat_id, text, parse_mode='Markdown')
    user_account[chat_id].set_state(chat_id, 'input_hash', True)


def confirm(chat_id):
    page = user_account[chat_id].get_state(chat_id, 'current_page')
    product_name = buy_dict[page]

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    order_info_dict = get_user_info(chat_id)["order_info"]

    if not order_info_dict:
        # order_info = '{\"'+product_name+'\":'+'\"'+formatted_time+'\"}'
        order_info = '{{"{product_name}":"{formatted_time}"}}'.format(product_name=product_name,
                                                                      formatted_time=formatted_time)
    else:
        order_info = json.loads(order_info_dict)
        order_info[product_name] = formatted_time

    update_user_order_info(chat_id, '{}'.format(order_info).replace("'", '"'))
    # text = "🎉*Done! \nYour order has been confirmed. Please check your private messages and remain patient while waiting.* ✅"
    # markup_inline = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton('🔙Back', callback_data='back')
    # user_account[chat_id].set_state(chat_id, 'back_interface', "ip_discovery")
    # markup_inline.add(button1)
    # bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)
    text="""🟡*Please provide your email address.*👇"""
    # markup_inline = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton('💴Deposit', callback_data='deposit')
    # markup_inline.add(button1)
    bot.send_message(chat_id, text, parse_mode='Markdown')
    user_account[chat_id].set_state(chat_id, 'input_confirm2_email', True)


def ip_collection(chat_id):
    text = ip_collection_text()
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('🔎IP Discovery', callback_data='ip_discovery')
    button2 = types.InlineKeyboardButton('🔙back', callback_data='back')
    user_account[chat_id].set_state(chat_id, 'back_interface', "buy_ip")
    markup_inline.add(button1, button2)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def wallet_management(chat_id):
    text = wallet_management_text()
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('🔎 View Wallet', callback_data='view_wallet')
    button2 = types.InlineKeyboardButton('🔑Create Wallet', callback_data='create_wallet')
    button3 = types.InlineKeyboardButton('🔙 Back', callback_data='back')
    user_account[chat_id].set_state(chat_id, 'back_interface', "buy_ip")
    markup_inline.add(button1, button2)
    markup_inline.add(button3)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def view_wallet(chat_id):
    user = get_demetic(chat_id)
    if user['wallet_address']:
        eth = total_balance_for_address(user['wallet_address'])
        # usd = eth_to_usd(address)
        # token_purse = get_erc20_token_balance(contract_address, user['wallet_address'])
        text = view_wallet_text(user['wallet_address'], eth)
        user_account[chat_id].set_state(chat_id, 'wallet_address', user['wallet_address'])
        markup_inline = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('💴Deposit', callback_data='deposit')
        button2 = types.InlineKeyboardButton('🔙Back', callback_data='back')
        markup_inline.add(button1, button2)
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup_inline)
        user_account[chat_id].set_state(chat_id, 'back_interface', "start")
    else:
        text = """🥲You currently have no previous packages. Please click "Create" to proceed."""
        markup_inline = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('👮‍♀️Create Wallet', callback_data='create_wallet')
        button2 = types.InlineKeyboardButton('🔙Back')
        user_account[chat_id].set_state(chat_id, 'back_interface', "wallet_management")
        markup_inline.add(button1, button2)
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def sell_ip(chat_id):
    base_set(chat_id)
    text = sell_ip_text()

    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('1️⃣', callback_data='sell_status1')
    button2 = types.InlineKeyboardButton('2️⃣', callback_data='sell_status2')
    button3 = types.InlineKeyboardButton('3️⃣', callback_data='sell_status3')
    button4 = types.InlineKeyboardButton('4️⃣', callback_data='sell_status4')
    button5 = types.InlineKeyboardButton('5️⃣', callback_data='Others')

    markup_inline.add(button1, button2)
    markup_inline.add(button3, button4)
    markup_inline.add(button5)

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def sell_status(chat_id):
    page = user_account[chat_id].get_state(chat_id, 'sell_status')
    user_account[chat_id].set_state(chat_id, 'sell_status_type', sell_dict[page])
    text = "🫡*Please provide your full name, including your first name and last name.*"
    bot.send_message(chat_id, text, parse_mode='Markdown')
    user_account[chat_id].set_state(chat_id, 'inputname', True)



def Others(chat_id):
    text = "🫡*Please enter the type of IP you wish to sell.👇*"
    bot.send_message(chat_id, text, parse_mode='Markdown')
    user_account[chat_id].set_state(chat_id, 'inpuip', True)


def help(chat_id):
    base_set(chat_id)
    text = help_text()
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('✅Live Alerts', callback_data='Live Alerts')
    button2 = types.InlineKeyboardButton('✅Social media', callback_data='Social media')
    button3 = types.InlineKeyboardButton('✅Contact us', callback_data='Contact us')
    button4 = types.InlineKeyboardButton('🔙Return', callback_data='back')
    markup_inline.add(button1)
    markup_inline.add(button2)
    markup_inline.add(button3)
    markup_inline.add(button4)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)
    user_account[chat_id].set_state(chat_id, 'back_interface', "start")


def live_alerts(chat_id):
    is_notifications = get_is_notifications(chat_id)
    text = live_alerts_text(is_notifications)

    if is_notifications:
        button1 = types.InlineKeyboardButton('Notifications', callback_data='disable')
    else:
        button1 = types.InlineKeyboardButton('Notifications', callback_data='disable')

    button2 = types.InlineKeyboardButton('🔙Back', callback_data='back')
    user_account[chat_id].set_state(chat_id, 'back_interface', "start")

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(button1)
    markup_inline.add(button2)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def social_media(chat_id):
    text = social_media_text()
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('✅', url="https:")
    button2 = types.InlineKeyboardButton('✅', url="https:")
    button3 = types.InlineKeyboardButton('✅', url="https:")
    markup_inline.add(button1)
    markup_inline.add(button2)
    markup_inline.add(button3)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup_inline)


def contact_us(chat_id):
    text = """🟡Please provide your email address.👇"""
    bot.send_message(chat_id, text, parse_mode='Markdown')
    user_account[chat_id].set_state(chat_id, 'input_contact_email', True)



def base_set(chat_id):
    if not user_account.get(chat_id, False):
        user_account[chat_id] = UserState()
        create_demetic(chat_id)
        create_user_info(chat_id)


def start(chat_id):
    base_set(chat_id)
    text = start_text()
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('🔆B', callback_data='b_ip')
    button2 = types.InlineKeyboardButton('💴  S', callback_data='s_ip')
    button3 = types.InlineKeyboardButton('🔎H', callback_data='help')
    markup_inline.add(button1, button2)
    markup_inline.add(button3)
    photo = open('static/pic_start.png', 'rb')  # 替换 'path/to/image.jpg' 为你的图片路径
    bot.send_photo(chat_id, photo, text, parse_mode="Markdown", reply_markup=markup_inline)
    photo.close()  # 记得关闭文件


def check_hash(text):
    if '/' in text:
        text = text.split('/')[-1]
        return bool(re.match(r'^0x([A-Fa-f0-9]{64})$', text))
    else:
        return bool(re.match(r'^0x([A-Fa-f0-9]{64})$', text))


def input_email(input_data):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, input_data):
        return True
    else:
        return False


def residential_proxies_browse(chat_id, message_id):
    page = user_account[chat_id].get_state(chat_id, 'current_page')
    text = proxies_text(chat_id, page)
    markup_inline = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('✅Pick', callback_data='pick')
    button2 = types.InlineKeyboardButton('Next✳️', callback_data='next')
    button3 = types.InlineKeyboardButton('❇️Previous', callback_data='previous')
    button4 = types.InlineKeyboardButton('🔙Back', callback_data='back')
    user_account[chat_id].set_state(chat_id, 'back_interface', "ip_discovery")

    if page == MAX_PAGE_COUNT:
        markup_inline.add(button1)
        markup_inline.add(button3, button4)
    elif page == 1:
        markup_inline.add(button1, button2)
        markup_inline.add(button4)
    else:
        markup_inline.add(button1, button2)
        markup_inline.add(button3, button4)

    photo = open(f'static/pic_{page}.png', 'rb')

    if page != 1:
        bot.delete_message(chat_id, message_id)

    bot.send_photo(chat_id, photo, text, parse_mode="HTML", reply_markup=markup_inline)
    photo.close()



def back_interface(chat_id):
    function_map = {
        'buy_ip': buy_ip,
        'ip_discovery': ip_discovery,
        'pick': pick,
        'start': start,
        "wallet_management": wallet_management
    }
    back_interface_function_name = user_account[chat_id].get_state(chat_id, 'back_interface')
    function_map[back_interface_function_name](chat_id)


def start_run_bot():
    bot.polling()

if __name__ == '__main__':
    start_run_bot()
