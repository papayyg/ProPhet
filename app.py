async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from utils.locales import get_chats_locales
    await get_chats_locales()

    from utils.commands import set_default_commands
    await set_default_commands(dp)

    from utils.notify import on_startup_notify
    await on_startup_notify(dp)

    from handlers.users.image import on_startup_queue
    await on_startup_queue(dp)

    from utils.contest import on_startup_contest
    await on_startup_contest(dp)

async def on_shutdown(dp):
    from utils.notify import on_shutdown_notify
    await on_shutdown_notify(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)