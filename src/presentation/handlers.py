from os import getenv

from aiogram.filters.callback_data import CallbackData

from src.logic import Admin, Client, User
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import flags

import src.presentation.kb as kb
import src.presentation.text as text
from src.presentation.callbacks import ClientCallback
from src.presentation.states import Gen, Del, GenConf, DelConf, ConfMenu, UserMenu

router = Router()
admin_id = getenv("ADMIN_TELEGRAM_ID")


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()

    if msg.from_user.username == admin_id:
        await msg.answer(text.hello_admin, reply_markup=kb.admin_menu)
    else:
        await msg.answer(text.hello_clint, reply_markup=kb.client_menu)


@router.callback_query(F.data == "main_menu")
async def menu_handler(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text=text.main_menu, reply_markup=kb.admin_menu)
    else:
        await clbck.message.answer(text=text.main_menu, reply_markup=kb.client_menu)


@router.callback_query(F.data == "get_instructions")
async def get_instructions(clbck: CallbackQuery):
    await clbck.message.answer(text.instructions, reply_markup=kb.instruction_menu)


@router.callback_query(F.data == "add_client")
async def add_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text.client_id_await, reply_markup=kb.iexit_kb)
        await state.set_state(Gen().typing_telegram_id)


@router.message(Gen.typing_telegram_id)
async def get_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text
        await state.update_data(chosen_id=tg_id)
        await msg.answer(text.client_limit_await, reply_markup=kb.iexit_kb)
        await state.set_state(Gen().typing_limit)


@router.message(Gen.typing_limit)
async def get_limit(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        limit = msg.text
        if not limit.isnumeric():
            await state.clear()
            return await msg.answer(text.limit_error, reply_markup=kb.iexit_kb)
        else:
            limit = int(limit)
            user_data = await state.get_data()
            tg_id = user_data['chosen_id']
            User().create(user_id=tg_id, limit=limit)
            await msg.answer("Пользователь успешно добавлен", reply_markup=kb.iexit_kb)
            await state.clear()


@router.callback_query(F.data == "delete_client")
async def delete_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text.client_id_await, reply_markup=kb.iexit_kb)
        await state.set_state(Del().typing_telegram_id)


@router.message(Del.typing_telegram_id)
async def delete_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text

        try:
            User().delete(user_id=tg_id)
            await msg.answer("Пользователь успешно удален", reply_markup=kb.iexit_kb)
            await state.clear()
        except:
            await state.clear()
            return await msg.answer(text.telegram_id_error, reply_markup=kb.iexit_kb)



@router.callback_query(F.data == "create_config")
async def add_config(clbck: CallbackQuery):
    user_id = str(clbck.from_user.username)
    if User().get(user_id) is None:
        return await clbck.message.answer(text.user_not_defined, reply_markup=kb.iexit_kb)
    if not User().allowed_to_create_client(user_id):
        return await clbck.message.answer(text.user_limit_exited, reply_markup=kb.iexit_kb)
    client_id = Client().create(user_id=user_id)
    client = Client().get(client_id)
    uri = client.conn_str
    await clbck.message.answer(text=uri, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "conf_list")
async def config_list(clbck: kb.EmailPageCallbackFactory):
    await kb.show_clients_pages(clbck)


@router.callback_query(kb.EmailCallbackFactory.filter())
async def client_choosing(callback_query: CallbackQuery, callback_data: kb.EmailCallbackFactory,
                          state: FSMContext):
    email = callback_data.email
    await state.update_data(email=email)
    await state.set_state(ConfMenu.choosing_action)
    await callback_query.message.edit_text(f"Выберите действие, которое вы хотите совершить с туннелем {email}",
                                           reply_markup=kb.config_sub_menu)


@router.callback_query(F.data == "get_config")
async def get_config(clbck: CallbackQuery, state: FSMContext):
    email = await state.get_data()
    email = email['email']
    await clbck.message.answer(Client().get(email).conn_str, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "delete_config")
async def delete_config(clbck: CallbackQuery, state: FSMContext):
    email = await state.get_data()
    email = email['email']
    Client().delete(email)
    await clbck.message.answer("Клиент удалён", reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "user_list")
async def config_list(clbck: kb.EmailPageCallbackFactory):
    await kb.show_users_pages(clbck)


@router.callback_query(kb.UserCallbackFactory.filter())
async def client_choosing(callback_query: CallbackQuery, callback_data: kb.UserCallbackFactory,
                          state: FSMContext):
    user = callback_data.user
    await state.update_data(user=user)
    await state.set_state(UserMenu.choosing_action)
    await callback_query.message.answer(f"Выберите действие, которое вы хотите совершить с пользователем {user}",
                                        reply_markup=kb.config_sub_menu)


@router.callback_query(F.data == "change_limit")
async def change_limit(clbck: CallbackQuery, state: FSMContext):
    user = await state.get_data()
    user = user['user']
    User().get(user).limit = 10  # TODO
    await clbck.message.answer("Новый лимит - 10 (доделать)", reply_markup=kb.iexit_kb)


# @router.callback_query(F.data == "delete_user")
# async def delete_user(clbck: CallbackQuery, state: FSMContext):
#     user = await state.get_data()
#     user = user['email']
#     User().delete(user)
#     await clbck.message.answer("Пользователь удалён", reply_markup=kb.iexit_kb)
#

@router.callback_query(kb.EmailPageCallbackFactory.filter(F.action.in_(["prev", "next"])))
async def query_email_page(callback_query: kb.EmailPageCallbackFactory, callback_data: kb.EmailPageCallbackFactory):
    current_page = int(callback_data.page)
    action = callback_data.action
    if action == "prev":
        page = current_page - 1
    elif action == "next":
        page = current_page + 1
    else:
        page = current_page
    if page != current_page:
        await kb.show_clients_pages(callback_query, page)
    else:
        await callback_query.answer('Вы уже на этой странице!')


@router.callback_query(kb.UserPageCallbackFactory.filter(F.action.in_(["prev", "next"])))
async def query_user_page(callback_query: kb.UserPageCallbackFactory, callback_data: kb.UserPageCallbackFactory):
    current_page = int(callback_data.page)
    action = callback_data.action
    if action == "prev":
        page = current_page - 1
    elif action == "next":
        page = current_page + 1
    else:
        page = current_page
    if page != current_page:
        await kb.show_clients_pages(callback_query, page)
    else:
        await callback_query.answer('Вы уже на этой странице!')


@router.callback_query(kb.EmailCallbackFactory.filter())
async def query_item(callback_query: CallbackQuery, callback_data: kb.EmailCallbackFactory):
    email = callback_data.email
    await callback_query.message.answer(Client().get(email).conn_str, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "get_config")
async def get_conf(clbck: CallbackQuery, state: FSMContext):
    client_data = await state.get_data()
    client_id = client_data['client_id']
    client = Client().get(client_id)
    await clbck.message.answer(text=client.conn_str, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "delete_config")
async def delete_config(clbck: CallbackQuery, state: FSMContext):
    client_data = await state.get_data()
    client_id = client_data['client_id']
    Client().delete(client_id)
    await clbck.message.answer(text=text.config_is_deleted, reply_markup=kb.iexit_kb)
