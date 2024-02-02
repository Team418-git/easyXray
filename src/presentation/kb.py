from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logic import Client, User

items_per_page = 7

admin_menu = [
    [InlineKeyboardButton(text="-----ADMIN PANEL-----")],
    [InlineKeyboardButton(text="➕ Добавить юзера", callback_data="add_client"),
     InlineKeyboardButton(text="❌ Удалить юзера", callback_data="delete_client")],
    # [InlineKeyboardButton(text="📋 Список юзеров", callback_data="user_list")],
    [InlineKeyboardButton(text="---------------------", callback_data="spare_callback")],
    # [InlineKeyboardButton(text="📃 Мои конфигурации", callback_data="conf_list")],
    [InlineKeyboardButton(text="🔧 Запросить конфигурацию", callback_data="create_config")],
    [InlineKeyboardButton(text="🔍 Инструкции", callback_data="get_instructions")]
]

client_menu = [
    # [InlineKeyboardButton(text="📃 Мои конфигурации", callback_data="conf_list")],
    [InlineKeyboardButton(text="🔧 Запросить конфигурацию", callback_data="create_config")],
    [InlineKeyboardButton(text="🔍 Инструкции", callback_data="get_instructions")]
]

instruction_menu = [
    [InlineKeyboardButton(text="iOS", url="https://telegra.ph/Instrukciya-dlya-iOS-01-11"),
     InlineKeyboardButton(text="Android", url="https://telegra.ph/Instrukciya-dlya-Android-01-11")],
    [InlineKeyboardButton(text="MacOS", url="https://telegra.ph/Instrukciya-dlya-MacOS-01-11"),
     InlineKeyboardButton(text="Windows", url="https://telegra.ph/Instrukciya-dlya-Windows-01-11")],
    [InlineKeyboardButton(text="Linux", url="https://telegra.ph/Instrukciya-dlya-Linux-Ubuntu-AppImage-01-11")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]

config_sub_menu = [
    [InlineKeyboardButton(text="Запросить URI", callback_data="get_config")],
    [InlineKeyboardButton(text="Удалить конфигурацию", callback_data="delete_config")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]

user_sub_menu = [
    [InlineKeyboardButton(text="Изменить лимит", callback_data="change_limit")],
    [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_menu)
client_menu = InlineKeyboardMarkup(inline_keyboard=client_menu)
instruction_menu = InlineKeyboardMarkup(inline_keyboard=instruction_menu)
config_sub_menu = InlineKeyboardMarkup(inline_keyboard=config_sub_menu)
user_sub_menu = InlineKeyboardMarkup(inline_keyboard=user_sub_menu)

iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]])


class TunnelPagination(StatesGroup):
    showing_items = State()


#
# class UsersPagination(StatesGroup):
#     showing_items = State()


class EmailPageCallbackFactory(CallbackData, prefix="fabnum_email"):
    action: str
    page: int


class UserPageCallbackFactory(CallbackData, prefix="fabnum_user"):
    action: str
    page: int


class EmailCallbackFactory(CallbackData, prefix="fabemail"):
    email: str


class UserCallbackFactory(CallbackData, prefix="fabuser"):
    user: str


async def get_emails_page_keyboard(emails_on_page: list, page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    for email in emails_on_page:
        builder.row(InlineKeyboardButton(text=email, callback_data=EmailCallbackFactory(email=email).pack()))
    if total_pages != 1:
        builder.row(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="ignore"))
    if page > 1:
        builder.add(InlineKeyboardButton(text="<<", callback_data=EmailPageCallbackFactory(action="prev", page=page).pack()))
    if page < total_pages:
        builder.add(InlineKeyboardButton(text=">>", callback_data=EmailPageCallbackFactory(action="next", page=page).pack()))
    builder.row(InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu"))
    return builder.as_markup()


async def get_users_page_keyboard(users_on_page: list, page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    for user in users_on_page:
        builder.row(InlineKeyboardButton(text=user, callback_data=UserCallbackFactory(user=user).pack()))
    if total_pages != 1:
        builder.row(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="ignore"))
    if page > 1:
        builder.add(InlineKeyboardButton(text="<<", callback_data=UserPageCallbackFactory(action="prev", page=page).pack()))
    if page < total_pages:
        builder.add(InlineKeyboardButton(text=">>", callback_data=UserPageCallbackFactory(action="next", page=page).pack()))
    builder.row(InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu"))
    return builder.as_markup()


async def show_clients_pages(clbck: EmailPageCallbackFactory, page: int = 1):
    user_id = clbck.from_user.username
    emails = Client().get_by_user(user_id)
    if len(emails) == 0:
        return await clbck.message.answer("У вас пока нет туннелей", reply_markup=iexit_kb)
    total_pages = len(emails) // items_per_page + (len(emails) % items_per_page > 0)
    text = f"Выберите туннель:"
    start = (page - 1) * items_per_page
    end = start + items_per_page
    emails_on_page = emails[start:end]
    keyboard = await get_emails_page_keyboard(emails_on_page, page, total_pages)
    await clbck.message.answer(text, reply_markup=keyboard)


async def show_users_pages(clbck: UserPageCallbackFactory, page: int = 1):
    users = [user.id for user in User().get_all()]
    if len(users) == 0:
        return await clbck.message.answer("Пока нет юзеров", reply_markup=iexit_kb)
    total_pages = len(users) // items_per_page + (len(users) % items_per_page > 0)
    text = f"Выберите пользователя, которому хотите обновить лимит:"
    start = (page - 1) * items_per_page
    end = start + items_per_page
    emails_on_page = users[start:end]
    keyboard = await get_users_page_keyboard(emails_on_page, page, total_pages)
    await clbck.message.answer(text, reply_markup=keyboard)
