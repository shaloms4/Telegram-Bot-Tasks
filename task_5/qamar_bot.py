import logging
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
print(f'token: {TOKEN}')

moon_router = Router()

class MoonMissionQuiz(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    result = State()


@moon_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(MoonMissionQuiz.question_1)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="A. Neil Armstrong")],
            [KeyboardButton(text="B. Buzz Aldrin")],
            [KeyboardButton(text="C. Michael Collins")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Hello! I’m Qamar, your Moon guide 🌙.\nLet's see how much you know about the historic moon missions!\n\nFirst question: Who was the first person to walk on the Moon?",
        reply_markup=keyboard,
    )


@moon_router.message(MoonMissionQuiz.question_1)
async def process_question_1(message: Message, state: FSMContext) -> None:
    answer = message.text.lower()

    await state.update_data(question_1_answer=answer)

    if answer == "a. neil armstrong":
        await state.set_state(MoonMissionQuiz.question_2)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="A. Apollo 11")],
                [KeyboardButton(text="B. Apollo 13")],
                [KeyboardButton(text="C. Apollo 12")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "Correct! Next, which mission was the first to land on the Moon?\n\nA. Apollo 11\nB. Apollo 13\nC. Apollo 12",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Hmm, that's not quite right. The correct answer is 'Neil Armstrong'. Try again!",
            reply_markup=ReplyKeyboardRemove(),
        )


@moon_router.message(MoonMissionQuiz.question_2)
async def process_question_2(message: Message, state: FSMContext) -> None:
    answer = message.text.lower()

    await state.update_data(question_2_answer=answer)

    if answer == "a. apollo 11":
        await state.set_state(MoonMissionQuiz.question_3)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="A. USA")],
                [KeyboardButton(text="B. USSR")],
                [KeyboardButton(text="C. China")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "Nice! Last question, which country was the first to send a spacecraft to the Moon?\n\nA. USA\nB. USSR\nC. China",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Oops, that's not quite right. The correct answer is 'Apollo 11'. Try again!",
            reply_markup=ReplyKeyboardRemove(),
        )


@moon_router.message(MoonMissionQuiz.question_3)
async def process_question_3(message: Message, state: FSMContext) -> None:
    answer = message.text.lower()

    await state.update_data(question_3_answer=answer)

    if answer == "b. ussr":
        await state.set_state(MoonMissionQuiz.result)
        await show_results(message, state)
    else:
        await message.answer(
            "Oops, that's not quite right. The correct answer is 'USSR'. Try again!",
            reply_markup=ReplyKeyboardRemove(),
        )


async def show_results(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    score = 0
    if data.get("question_1_answer") == "a. neil armstrong":
        score += 1
    if data.get("question_2_answer") == "a. apollo 11":
        score += 1
    if data.get("question_3_answer") == "b. ussr":
        score += 1

    result_text = f"Quiz Over! 🌙\nYou scored {score} out of 3!\n\nHere's a summary of your answers:\n"
    result_text += f"1. Who was the first person to walk on the Moon? You answered: {data.get('question_1_answer')}\n"
    result_text += f"2. Which mission was the first to land on the Moon? You answered: {data.get('question_2_answer')}\n"
    result_text += f"3. Which country was the first to send a spacecraft to the Moon? You answered: {data.get('question_3_answer')}\n"

    await message.answer(result_text, reply_markup=ReplyKeyboardRemove())


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(moon_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
