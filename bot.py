import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# -----------------------------
# ВСТАВЬ СВОИ ДАННЫЕ
# -----------------------------
TOKEN = "8545036459:AAEfbDRAOba2qvH7_UKdHe44-LSVmEySIzg"
ADMIN_ID = 5697252704

# -----------------------------
# НАСТРОЙКА БОТА
# -----------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Состояние для команды /post
class PostState(StatesGroup):
    waiting_for_text = State()

# Кнопка отмены
cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_post")]
    ]
)

# -----------------------------
# КОМАНДА /start (красивые кнопки)
# -----------------------------
@dp.message(Command("start"))
async def start_cmd(message: Message):

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Отправить пост")],
            [KeyboardButton(text="🖼 Фото Серёги")],
            [KeyboardButton(text="📌 Пример поста")]
        ],
        resize_keyboard=True
    )

    await message.answer_photo(
        photo="https://media.discordapp.net/attachments/1434894166160183296/1463634046516199595/IMG_20260121_233908_095.jpg?ex=69728aed&is=6971396d&hm=7ffe4a23a2610e0c0a10b23eb0fd3e35d1a7ede5a2d11a1a0b0d8307e7b38cea&=&format=webp&width=968&height=968",
        caption="Здраствуйте, это я Серёга! Сдесь вы можете отправить мемы с мной или взять фото с мной. А то нахуй 2 поставлю",
        reply_markup=keyboard
    )

# -----------------------------
# ОБРАБОТЧИКИ КНОПОК
# -----------------------------
@dp.message(F.text == "📤 Отправить пост")
async def btn_post(message: Message, state: FSMContext):
    await post_cmd(message, state)

@dp.message(F.text == "🖼 Фото Серёги")
async def btn_image(message: Message):
    await image_cmd(message)

@dp.message(F.text == "📌 Пример поста")
async def btn_refens(message: Message):
    await refens_cmd(message)

# -----------------------------
# КОМАНДА /post
# -----------------------------
@dp.message(Command("post"))
async def post_cmd(message: Message, state: FSMContext):
    await message.answer(
        "Стоп-стоп! А ты уже /refens поглянул? если да то жду твой пост",
        reply_markup=cancel_kb
    )
    await state.set_state(PostState.waiting_for_text)

@dp.callback_query(F.data == "cancel_post")
async def cancel_post(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Отправка отменена.")
    await state.clear()

# -----------------------------
# ОБРАБОТКА ПОСТА (исправлено, без None)
# -----------------------------
@dp.message(PostState.waiting_for_text)
async def receive_post(message: Message, state: FSMContext):
    sender = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name

    # Фото
    if message.photo:
        caption = f"Новый пост от {sender}:"
        if message.caption:
            caption += f"\n{message.caption}"
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)

    # Видео
    elif message.video:
        caption = f"Новый пост от {sender}:"
        if message.caption:
            caption += f"\n{message.caption}"
        await bot.send_video(ADMIN_ID, message.video.file_id, caption=caption)

    # Документ
    elif message.document:
        caption = f"Новый пост от {sender}:"
        if message.caption:
            caption += f"\n{message.caption}"
        await bot.send_document(ADMIN_ID, message.document.file_id, caption=caption)

    # Текст
    elif message.text:
        await bot.send_message(
            ADMIN_ID,
            f"Новый пост от {sender}:\n{message.text}"
        )

    # Неизвестный тип
    else:
        await bot.send_message(
            ADMIN_ID,
            f"Новый пост от {sender}:\n⚠️ Неизвестный тип сообщения"
        )

    await message.answer("✅ Сообщение отправлено админу!")
    await state.clear()

# -----------------------------
# КОМАНДА /refens
# -----------------------------
@dp.message(Command("refens"))
async def refens_cmd(message: Message):
    await message.answer_photo(
        photo="https://cdn.discordapp.com/attachments/1434894166160183296/1463936530698735689/IMG_20260122_193922_774.jpg?ex=6973a4a3&is=69725323&hm=cb63d94b845cc88b47d0f81e54b236282a3cc52a09e2b54d96af1b1f9e31bd37&",
        caption="Вот так должен выглядить пост"
    )

# -----------------------------
# КОМАНДА /image — 10 изображений
# -----------------------------
@dp.message(Command("image"))
async def image_cmd(message: Message):
    photos = [
        "https://media.discordapp.net/attachments/1434894166160183296/1463633283706519622/sHMpsmQHvyXvLQczJg1E_HxQvbpOAY7h1hXMDnmJGXRtfuMt1W1hoBlEkn6jAwIvtq5HdC9O9sp62t5YhEH6ICLJ.jpg?ex=69728a37&is=697138b7&hm=b130758a0c74633e6146ed022900643be7f305c0e5b4d7042a88523eb9fbd008&=&format=webp&width=647&height=864",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633284243132700/X1IXcZ37tMCa1HgY4-4al1czu_macQZbHug8JJcaQLQ2fD3ipRGEQ9f-aIXz_hag4NR05v31rF3JnI2ldH7x761t.jpg?ex=69728a37&is=697138b7&hm=fd9ef30f62d3a63c6c970b3c1f1c32145a1a43b4b0269b2fecf7177a9bdc3b86&=&format=webp&width=864&height=864",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633284901896363/9hYqek0DUOfj1oll9AhKWitA8Q8ntsYllvj-XwatHnnCbuFjLvrCrv_uno5BS2kDgYJJzwF-AZxLG3jkbvZST4Ws.jpg?ex=69728a38&is=697138b8&hm=6340e9426fe79aa072f2882cebd001243a7c51fb27979989c69fa4af0336f798&=&format=webp&width=864&height=864",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633285472194570/IMG_20260120_161551_906.jpg?ex=69728a38&is=697138b8&hm=497304f37b9e28ae7b468e0eb776947be8febb51540ff5b09cbdfb2d06c1fa43&=&format=webp",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633286185353326/IMG_20251106_115909_177.jpg?ex=69728a38&is=697138b8&hm=2e470f8f7edd86f404e2b0e94c31448c2ce5c75bcc609a2502090c016b5a90fe&=&format=webp",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633286604656660/IMG_20251105_224645_935.jpg?ex=69728a38&is=697138b8&hm=d7f1789e8242c2d5cb06e2adba7761f175578bb2ba7fb14c7cd2d6c2e704f0ff&=&format=webp",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633287217156219/IMG_20251105_224525_810.jpg?ex=69728a38&is=697138b8&hm=9c99ab8026c67f4f38df3b2eeae5742ecd7199f9477b51d00b728f41000584ff&=&format=webp&width=582&height=863",
        "https://media.discordapp.net/attachments/1434894166160183296/1463633287581929566/IMG_20251105_140313_824.jpg?ex=69728a38&is=697138b8&hm=be589b0eae8294c3adcf68004b1d2489d2db5762bb797fbcfc47ff12df931936&=&format=webp",
        "https://cdn.discordapp.com/attachments/1434894166160183296/1463633393031057600/IMG_20260121_233628_929.jpg?ex=69728a51&is=697138d1&hm=d7e7308fc5d011868565572d0cb3107d18d56a37ac2d6c28c4714f84b948df32&"
    ]

    media = [InputMediaPhoto(media=url) for url in photos]
    await message.answer_media_group(media)

# -----------------------------
# ЗАПУСК
# -----------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

