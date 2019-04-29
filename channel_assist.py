from models import user, product, photo, request
from utils.connections import *
from utils.db_handler import *
from utils.utils import *
from texts import filters
from texts import deftxt
from logger import logger
import time


# Both of success and failure functions are optional
def success(response, user_data):
    logger.info(user_data)
    logger.info('send_message success response: %s' % response)


def failure(response, user_data):
    logger.info(user_data)
    logger.error('send_message failure response: %s' % response)


def admin_restricted(func):
    def restricted_function(*args, **kwds):
        update = kwds.get('update')
        if not update:
            update = args[1]
        if update and str(get_user_id(update)) in public.root_admins:
            return func(*args, **kwds)
        else:
            return user_menu(*args, **kwds)

    return restricted_function


creat_table_if_not_exist(engine, product.products)
creat_table_if_not_exist(engine, user.users)
creat_table_if_not_exist(engine, photo.photos)
creat_table_if_not_exist(engine, request.requests)

continue_btn = TemplateMessageButton(text=deftxt.continue_btn, value=filters.continue_btn, action=0)
state_view_btn = TemplateMessageButton(text=deftxt.state_view_btn, value=filters.state_view_btn, action=0)
insert_product_btn = TemplateMessageButton(text=deftxt.insert_product_btn, value=filters.insert_product_btn, action=0)
# sales_report_btn = TemplateMessageButton(text=deftxt.sales_report_btn, value=filters.sales_report_btn, action=0)
buy_btn = TemplateMessageButton(text=deftxt.buy_btn, value=filters.buy_btn, action=0)
cancel_btn = TemplateMessageButton(text=deftxt.cancel_btn, value=filters.cancel_btn, action=0)


@dispatcher.message_handler(filters=TextFilter(keywords=filters.start))
def welcom(bot, update):
    add_user_if_not_exist(update)
    message = TextMessage(deftxt.start_and_welcom)
    btn_list = [
        continue_btn
    ]
    user_peer = get_user(update)
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[filters.continue_btn]))
@admin_restricted
def admin_menu(bot, update):
    message = TextMessage(deftxt.admin_menu)
    btn_list = [
        buy_btn, state_view_btn, insert_product_btn,  # sales_report_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


def user_menu(bot, update):
    message = TextMessage(deftxt.user_menu)
    btn_list = [
        buy_btn, state_view_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[filters.buy_btn]))
def buy_conversation(bot, update):
    message = TextMessage(deftxt.get_prd_id)
    btn_list = [
        cancel_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), get_count),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=filters.cancel_btn),
                                                            function_cancel)])


def get_count(bot, update):
    prd_id = arabic_to_eng_number(get_message_text(update))
    if prd_id.isdigit():
        prd = select_prd(prd_id)
        user_peer = get_user(update)
        if prd:
            dispatcher.set_conversation_data(update=update, key='prd_id', value=prd_id)
            message = TextMessage(deftxt.get_count)
            btn_list = [
                cancel_btn
            ]
            template_message = TemplateMessage(general_message=message, btn_list=btn_list)
            bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
            dispatcher.register_conversation_next_step_handler(update,
                                                               [MessageHandler(TextFilter(), send_Purchase_Message),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords=filters.cancel_btn),
                                                                    function_cancel)])
        else:
            bad_prd_id(bot, update)
    else:
        bad_prd_id(bot, update)


def send_Purchase_Message(bot, update):
    user_peer = get_user(update)
    count = arabic_to_eng_number(get_message_text(update))
    prd_id = dispatcher.get_conversation_data(update, 'prd_id')
    photo_id = select_prd(prd_id).photo_id
    if count.isdigit():
        if int(count) > 0:
            photo = select_photo_id(photo_id)
            prd = select_prd(prd_id)
            amount = str(int(count) * int(prd.amount))
            account_number = str(public.admins_card_number)
            photo_file_id = photo.file_id
            photo_name = photo.name
            photo_access_hash = photo.access_hash
            photo_file_size = str(photo.file_size)
            photo_ext_width = photo.ext_width
            photo_ext_height = photo.ext_height

            photo_message = PhotoMessage(file_id=photo_file_id, access_hash=photo_access_hash,
                                         name=photo_name, file_size=photo_file_size,
                                         caption_text=TextMessage('*{}*'.format(prd.name)
                                                                  + '\n' + deftxt.prd_id
                                                                  + ': *{}*'.format(prd_id)
                                                                  + '\n' + deftxt.offer_number
                                                                  + ': *{}*'.format(eng_to_arabic_number(count))
                                                                  + '\n' + deftxt.unit_price
                                                                  + ': *{}*'.format(
                                             eng_to_arabic_number("{:,}".format(prd.amount)))),
                                         mime_type="image/jpeg", width=89, height=90,
                                         file_storage_version=1, ext_width=photo_ext_width,
                                         ext_height=photo_ext_height,
                                         thumb='')
            purchase_message = PurchaseMessage(
                msg=photo_message, account_number=account_number,
                amount=amount, money_request_type=MoneyRequestType.normal)
            bot.send_message(purchase_message, user_peer, success_callback=success, failure_callback=failure)
            dispatcher.finish_conversation(update)
        else:
            bad_input(bot, update)
    else:
        bad_input(bot, update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[filters.insert_product_btn]))
def insert_prd_conv(bot, update):
    message = TextMessage(deftxt.get_prd_name)
    btn_list = [
        cancel_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), get_prd_amount),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=filters.cancel_btn),
                                                            function_cancel)])


def get_prd_amount(bot, update):
    prd_name = get_message_text(update)
    dispatcher.set_conversation_data(update, key='prd_name', value=prd_name)
    message = TextMessage(deftxt.get_prd_amount)
    btn_list = [
        cancel_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), get_prd_photo),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=filters.cancel_btn),
                                                            function_cancel)])


def get_prd_photo(bot, update):
    prd_amount = get_message_text(update)
    dispatcher.set_conversation_data(update=update, key='prd_amount', value=prd_amount)
    message = TextMessage(deftxt.get_prd_photo)
    btn_list = [
        cancel_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(PhotoFilter(), insert_prd_done),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=filters.cancel_btn),
                                                            function_cancel)])


def insert_prd_done(bot, update):
    prd_photo = get_message_obj(update)
    photo_file_id = prd_photo.file_id
    photo_access_hash = prd_photo.access_hash
    photo_name = prd_photo.name
    photo_file_size = prd_photo.file_size
    photo_mime_type = prd_photo.mime_type
    photo_width = prd_photo.width
    photo_height = prd_photo.height
    photo_ext_width = prd_photo.ext_width
    photo_ext_height = prd_photo.ext_height

    insert_photo(
        file_id=photo_file_id, access_hash=photo_access_hash, name=photo_name, file_size=photo_file_size,
        mime_type=photo_mime_type, width=photo_width, height=photo_height, ext_width=photo_ext_width,
        ext_height=photo_ext_height)

    prd_name = dispatcher.get_conversation_data(update, 'prd_name')
    prd_amount = dispatcher.get_conversation_data(update, 'prd_amount')
    prd_photo_id = select_photo_file_id(photo_file_id)

    insert_product(name=prd_name, amount=arabic_to_eng_number(prd_amount), photo_id=prd_photo_id)

    message = TextMessage(deftxt.get_prd_done)
    btn_list = [
        continue_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(BankMessageFilter())
def get_purchase_request_payment(bot, update):
    user_id = get_user_id(update)
    if int(user_id) > 100:
        receipt = get_receipt_obj(update)
        time_stamp = str(time.time()).split('.')[0]
        request_id = '{}_{}'.format(receipt.payer, time_stamp)
        count = int(receipt.regarding.split('\n')[2].split()[2].split("*")[1])
        amount = receipt.amount
        description = receipt.description
        logger.info(
            'get_purchase_request_payment :{user_id : %s, receipt: %s, request_id: %s}' % user_id, receipt, request_id
        )
        insert_request(user_id=user_id, request_id=request_id, count=count, amount=amount, description=description)
        message = TextMessage(deftxt.payment_done)
        btn_list = [
            continue_btn
        ]
        template_message = TemplateMessage(general_message=message, btn_list=btn_list)
        user_peer = get_user(update)
        bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
        bot.send_message(TextMessage('*' + request_id + '*'), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[filters.state_view_btn]))
def purchase_state_request(bot, update):
    message = TextMessage(deftxt.get_request_id)
    btn_list = [
        cancel_btn
    ]
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    user_peer = get_user(update)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), send_state_request),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=filters.cancel_btn),
                                                            function_cancel)])


def send_state_request(bot, update):
    req_id = get_message_text(update)
    if req_id.split('_')[0].isdigit():
        req_state = select_state(req_id)
        if req_state:
            message = TextMessage(deftxt.send_request_state.format(req_state))
            btn_list = [
                continue_btn
            ]
            template_message = TemplateMessage(general_message=message, btn_list=btn_list)
            user_peer = get_user(update)
            bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
            dispatcher.finish_conversation(update)
        else:
            bad_prd_id(bot, update)
    else:
        bad_input(bot, update)


def function_cancel(bot, update):
    user_peer = get_user(update)
    btn_list = [
        continue_btn
    ]
    message = TextMessage(deftxt.cancel)
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


def bad_input(bot, update):
    logger.error('bad inputted.')
    user_peer = get_user(update)
    btn_list = [
        cancel_btn
    ]
    message = TextMessage(deftxt.bad_input)
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


def bad_prd_id(bot, update):
    user_peer = get_user(update)
    logger.error('bad product id inputted.')
    btn_list = [
        cancel_btn
    ]
    message = TextMessage(deftxt.prd_not_exist)
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


def bad_req_id(bot, update):
    user_peer = get_user(update)
    logger.error('bad request id inputted.')
    btn_list = [
        cancel_btn
    ]
    message = TextMessage(deftxt.req_not_exist)
    template_message = TemplateMessage(general_message=message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)


# Run the bot!
updater.run()
