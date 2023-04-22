import asyncio

import aiomysql

from data import config


class BotDB:
    async def creatPool(host, user, password, db) -> aiomysql.Pool:
        pool = await aiomysql.create_pool(host=host, port=3306, user=user, password=password, db=db, loop=loop,
                                          autocommit=True, pool_recycle=120)
        return pool

    async def chats_exists(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `id` FROM `chats` WHERE `chat_id` = %s", (chat_id,))
                result = await cursor.fetchone()
                return bool(result)

    async def add_chat(chat_id, first_name):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                print(first_name)
                await cursor.execute("INSERT INTO `chats` (`chat_id`, `first_name`) VALUES (%s, %s)",(chat_id, first_name,))
                await conn.commit()

    async def chat_update(chat_id, first_name):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("UPDATE `chats` SET `first_name` = %s, `join_time` = NOW() WHERE `chat_id` = %s",
                                     (first_name, chat_id,))
                await conn.commit()

    async def check_chat_user(chat_id, user_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = await cursor.execute("SELECT `id` FROM `chat_users` WHERE `chat_id` = %s AND `user_id` = %s",
                                              (chat_id, user_id,))
                return result

    async def check_chat(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = await cursor.execute("SELECT `id` FROM `chat_users` WHERE `chat_id` = %s", (chat_id,))
                return result

    async def add_user(chat_id, user_id, first_name, user_name):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO `chat_users` (`chat_id`, `user_id`, `first_name`, `user_name`) VALUES (%s, %s, %s, %s)",
                    (chat_id, user_id, first_name, user_name,))
                await conn.commit()

    async def remove_user(chat_id, user_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM `chat_users` WHERE `chat_id` = %s AND `user_id` = %s",
                                     (chat_id, user_id,))
                await conn.commit()

    async def all_user(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `user_id`, `first_name` FROM `chat_users` WHERE `chat_id` = %s",
                                     (chat_id), )
                result = await cursor.fetchall()
                return result

    async def check_pidor(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = await cursor.execute("SELECT `id` FROM `pidor` WHERE `chat_id` = %s", (chat_id,))
                return result

    async def add_pidor(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO `pidor` (`chat_id`) VALUES (%s)", (chat_id,))
                await conn.commit()

    async def remove_pidor(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM `pidor` WHERE `chat_id` = %s", (chat_id,))
                await conn.commit()

    async def pick_pidor():
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `chat_id` FROM `pidor`")
                result = await cursor.fetchall()
                return result

    async def users_pidor(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `first_name`, `user_id` FROM `chat_users` WHERE `chat_id` = %s",
                                     (chat_id,))
                result = await cursor.fetchall()
                return result

    async def user_rep(chat, user, first_name):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await cursor.execute("SELECT stat FROM pidor_stats WHERE chat_id = %s AND user_id = %s",
                                        (chat, user,)):
                    await cursor.execute(
                        "UPDATE `pidor_stats` SET `stat` = `stat` + 1 WHERE `chat_id` = %s AND `user_id` = %s",
                        (chat, user,))
                    await conn.commit()
                else:
                    await cursor.execute(
                        "INSERT INTO `pidor_stats` (`stat`, `chat_id`, `user_id`, `first_name`) VALUES (1, %s, %s, %s)",
                        (chat, user, first_name,))
                    await conn.commit()
                return

    async def pidor_stats(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await conn.commit()
                await cursor.execute(
                    "SELECT `first_name`, `stat` FROM `pidor_stats` WHERE `chat_id` = %s ORDER BY `stat` DESC",
                    (chat_id,))
                result = await cursor.fetchall()
                return result

    async def login_exists(user_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = await cursor.execute("SELECT `id` FROM `unibook` WHERE `user_id` = %s", (user_id,))
                return result

    async def add_login(user_id, login, password, uni):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO `unibook` (`user_id`, `login`, `password`, `uni`) VALUES (%s, %s, %s, %s)",
                                     (user_id, login, password, uni,))
                await conn.commit()

    async def remove_login(user_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM `unibook` WHERE `user_id` = %s", (user_id,))
                await conn.commit()

    async def get_login(user_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `login`, `password`, `uni`  FROM `unibook` WHERE `user_id` = %s", (user_id,))
                logpass = await cursor.fetchall()
                login = logpass[0][0]
                password = logpass[0][1]
                uni = logpass[0][2]
                return login, password, uni

    async def all_chats():
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `chat_id` FROM `chats`")
                chats = await cursor.fetchall()
                return chats
    
    async def chats_stat():
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT COUNT(*) FROM `chats`")
                count_chats = await cursor.fetchall()
                await cursor.execute("SELECT COUNT(*) FROM `unibook`")
                count_unibook = await cursor.fetchall()
                return count_chats, count_unibook
    
    async def get_local():
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT `chat_id`, `locales` FROM `chats`")
                chats_locales = await cursor.fetchall()
                return chats_locales
    
    async def locales_exists(chat_id):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                result = await cursor.execute("SELECT `locales` FROM `chats` WHERE `chat_id` = %s", (chat_id,))
                return result
    
    async def insert_lang(chat_id, lang):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("INSERT INTO `chats` (`chat_id`, `locales`) VALUES (%s, %s)",(chat_id, lang,))
                await conn.commit()

    async def set_lang(chat_id, name, lang):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if await cursor.execute("SELECT `locales` FROM chats WHERE chat_id = %s",(chat_id,)):
                    await cursor.execute(
                        "UPDATE `chats` SET `locales` = %s WHERE `chat_id` = %s",(lang, chat_id,))
                    await conn.commit()
                else:
                    await cursor.execute(
                        "INSERT INTO `chats` (`chat_id`, `first_name`, `locales`) VALUES (%s, %s, %s)",(chat_id, name, lang,))
                    await conn.commit()
                return
    
    async def close(self):
        pool.close()
        await pool.wait_closed()


loop = asyncio.get_event_loop()
pool: aiomysql.Pool = loop.run_until_complete(
    BotDB.creatPool(config.DB_HOST, config.DB_USER, config.DB_PASS, config.DATABASE))