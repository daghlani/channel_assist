def arabic_to_eng_number(mynum):
    mynum = str(mynum)
    return mynum.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def eng_to_arabic_number(number):
    number = str(number)
    return number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


def get_message_obj(update):
    return update.get_effective_message()


def get_receipt_obj(update):
    return get_message_obj(update).get_receipt()


def get_message_text(update):
    return update.get_effective_message().text.strip()


def get_user_id(update):
    return update.get_effective_user().peer_id


def get_user(update):
    return update.get_effective_user()
