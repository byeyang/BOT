import datetime
from db import DatabaseManager


def create_demetic(id):
    sql_select = "select * from demetic where user_id = %s"
    demetic = DatabaseManager(cursorclass=True).fetch_one(sql_select, id)
    if not demetic:
        sql_create = 'insert into demetic(user_id) values(%s)'
        DatabaseManager().exeDML(sql_create, id)


def create_user_info(id):
    sql_select = "select * from user_info where user_id = %s"
    user_info = DatabaseManager(cursorclass=True).fetch_one(sql_select, id)
    if not user_info:
        sql_create = 'insert into user_info(user_id) values(%s)'
        DatabaseManager().exeDML(sql_create, id)


def update_user_name(id, name):
    sql = 'update user_info set username=%s where user_id = %s'
    DatabaseManager().exeDML(sql, name, id)

# def update_sell_others(id, sell_others_ip):
#     sql = 'update user_info set sell_others=%s where user_id = %s'
#     DatabaseManager().exeDML(sql, sell_others_ip, id)

def update_user_email(id, email):
    sql = 'update user_info set email=%s where user_id = %s'
    DatabaseManager().exeDML(sql, email, id)


def update_user_transaction_hash(id, email):
    sql = 'update user_info set hash=%s where user_id = %s'
    DatabaseManager().exeDML(sql, email, id)


def update_user_order_info(id, order_info):
    sql = 'update user_info set order_info=%s where user_id = %s'
    DatabaseManager().exeDML(sql, order_info, id)

def update_user_sell_info(id, order_info):
    sql = 'update user_info set sell_info=%s where user_id = %s'
    DatabaseManager().exeDML(sql, order_info, id)


def update_token_address(id, wallet_address):
    sql = 'update demetic set address=%s where user_id = %s'
    DatabaseManager().exeDML(sql, wallet_address, id)


def get_demetic(id):
    sql = 'select * from demetic where user_id = %s'
    demetic_info = DatabaseManager(cursorclass=True).fetch_one(sql, id)
    return demetic_info

def get_user_info(id):
    sql = 'select * from user_info where user_id = %s'
    user_info = DatabaseManager(cursorclass=True).fetch_one(sql, id)
    return user_info


def update_display_wallet(id, wallet_address, private_key, encryption_key, mnemonic_phrase):
    sql = 'update demetic set address=%s, key=%s,key=%s,phrase=%s where user_id = %s'
    DatabaseManager().exeDML(sql, wallet_address, private_key, encryption_key, mnemonic_phrase, id)


def get_is_notifications(user_id):
    sql = 'select * from demetic where user_id = %s'
    user_info = DatabaseManager(cursorclass=True).fetch_one(sql, user_id)
    if user_info["is_node_alerts"] == 0:
        return False
    else:
        return True


def is_node_alerts(user_id):
    sql = 'select * from demetic where user_id = %s'
    user_info = DatabaseManager(cursorclass=True).fetch_one(sql, user_id)
    if user_info["is_node_alerts"] == 0:
        sql_update1 = 'update demetic set alerts = %s where user_id = %s'
        DatabaseManager().exeDML(sql_update1, 1, user_id)
    else:
        sql_update2 = 'update demetic set alerts = %s where user_id = %s'
        DatabaseManager().exeDML(sql_update2, 0, user_id)
