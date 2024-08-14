"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
        
#JOJODLE DB COMMANDS

    #add daily highscore time and/or count
    async def add_daily_hs(
        self, user_id: int, server_id: int, time: int = None, count: int = None
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM dhs WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            if time is not None:
                await self.connection.execute(
                    "INSERT INTO dhs(user_id, server_id, time) VALUES (?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time
                    ),
                )
            if count is not None:
                await self.connection.execute(
                    "INSERT INTO dhs(user_id, server_id, count) VALUES (?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        count
                    ),
                )
            await self.connection.commit()

    #add seeded highscore time and/or count
    async def add_seeded_hs(
        self, user_id: int, server_id: int, time: int = None, count: int = None
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM shs WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            if time is not None:
                await self.connection.execute(
                    "INSERT INTO shs(user_id, server_id, time) VALUES (?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time
                    ),
                )
            if count is not None:
                await self.connection.execute(
                    "INSERT INTO shs(user_id, server_id, count) VALUES (?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        count
                    ),
                )
            await self.connection.commit()

    #get highscores daily and/or seeded
    async def get_highscores(self, user_id: int, server_id: int, type:int = 2, all:bool = False) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        dhscores = await self.connection.execute(
            "SELECT user_id, server_id, time, count FROM dhs WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with dhscores as cursor:
            dhresults = await cursor.fetchall()
            if all:
                dhresult_list = []
                for row in dhresults:
                    dhresult_list.append(row)
                #return result_list
            else:
                dhtime = None
                dhcount = None
                for time in dhresults['time'].values[0]:
                    dhtime = time if (dhtime > time) or (dhtime == None) else dhtime
                for count in dhresults['count'].values[0]:
                    dhcount = count if (dhcount > count) or (dhcount == None) else dhcount
                #return [dhtime, dhcount]
        #repeat with shs
        shscores = await self.connection.execute(
            "SELECT user_id, server_id, time, count FROM shs WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with shscores as cursor:
            shresults = await cursor.fetchall()
            if all:
                shresult_list = []
                for row in dhresults:
                    shresult_list.append(row)
                #return result_list
            else:
                shtime = None
                shcount = None
                for time in shresults['time'].values[0]:
                    shtime = time if (shtime > time) or (shtime == None) else shtime
                for count in shresults['count'].values[0]:
                    shcount = count if (shcount > count) or (shcount == None) else shcount
                #return [dhtime, dhcount]
        
        final = []
        if all:
            if type == 0 or type == 2:
                for i in dhresult_list:
                    final.append(i)
            if type == 1 or type == 2:
                for i in shresult_list:
                    final.append(i)
        else:
            if type == 0 or type == 2:
                final.append(dhcount, dhtime)
            if type == 1 or type == 2:
                final.append(shcount, shtime)
        return final