import openai
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp
import keyboards.default as kb

openai.api_key = "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"


class TextGeneration(StatesGroup):
    waiting_for_text = State()


@dp.message_handler(commands='chatgpt')
async def cmd_start(message: types.Message):
    await message.reply("Задай мені будь яке питання і я спробую на нього відповісти", reply_markup=kb.cancel_fsm)
    await TextGeneration.waiting_for_text.set()


@dp.message_handler(Text(equals="📤 Скасувати"), state=TextGeneration)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ви завершили спілкування, якщо є ще якісь питання, я чекаю на тебе.",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=TextGeneration.waiting_for_text)
async def generate_text(message: types.Message, state: FSMContext):
    msg = await message.answer("Зачекайте, я подумаю над вашими словами.")
    try:
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message.text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completions.choices[0].text
        if "\n" in response:
            response = response.splitlines()
            await message.answer(response[2])
        else:
            await message.answer(response)
        await TextGeneration.waiting_for_text.set()
        await msg.delete()
    except Exception as e:
        print(str(e))
        await message.answer("Сталась помилка. Спробуйте написати мені пізніше.")
