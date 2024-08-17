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
        self, user_id: int, server_id: int, time: float = None, count: int = None
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT created_at FROM dhs WHERE user_id=? AND server_id=? ORDER BY created_at DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            await self.connection.execute(
                "INSERT INTO dhs(user_id, server_id, time, count) VALUES (?, ?, ?, ?)",
                (
                    user_id,
                    server_id,
                    time,
                    count
                ),
            )
            await self.connection.commit()
        #TODO: check if is high score and add to sleaderboard

    #add seeded highscore time and/or count
    async def add_seeded_hs(
        self, user_id: int, server_id: int, time: float = None, count: int = None
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT created_at FROM shs WHERE user_id=? AND server_id=? ORDER BY created_at DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            await self.connection.execute(
                "INSERT INTO shs(user_id, server_id, time, count) VALUES (?, ?, ?, ?)",
                (
                    user_id,
                    server_id,
                    time,
                    count
                ),
            )
            await self.connection.commit()

        #TODO: check if is high score and add to sleaderboard
        rows = await self.connection.execute(
            "SELECT created_at FROM sleaderboard WHERE user_id=? AND server_id=? ORDER BY created_at DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            #TODO: check rank
            rank = -1
            if await cursor.fetchone() == None:
                await self.connection.execute(
                    "INSERT INTO sleaderboard(user_id, server_id, time, count, rank) VALUES (?, ?, ?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time,
                        count,
                        #TODO: add rank
                        rank
                    ),
                )
            else:
                await self.connection.execute(
                    "UPDATE sleaderboard SET time = ?, count = ?, rank = ? WHERE user_id = ?",
                    (
                        time,
                        count,
                        rank,
                        user_id
                        # TODO: add rank
                    ),
                )
            await self.connection.commit()

    #TODO: MAKE CHECK RANK LEADERBOARD FUNCTION

    #get highscores daily and/or seeded
    async def get_highscores(self, user_id: int, server_id: int, all:bool = False) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        #set up return variables
        fdtimeL = []
        fdcountL = []
        fstimeL = []
        fscountL = []
        dhtime = None
        dhcount = None
        shtime = None
        shcount = None

        #get daily (high)scores
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
                #get all scores
                dhtime_list = []
                dhcount_list = []
                #TODO: fix ['time'].values
                for time in dhresults['time'].values[0]:
                    dhtime_list.append(time)
                for count in dhresults['count'].values[0]:
                    dhcount_list.append(count)
                #append results
                for result in dhtime_list:
                    fdtimeL.append(result)
                for result in dhcount_list:
                    fdcountL.append(result)
            #get high scores TODO: CHANGE TO LEADERBOARD DB
            for time in dhresults['time'].values[0]:
                dhtime = time if (dhtime > time) or (dhtime == None) else dhtime
            for count in dhresults['count'].values[0]:
                dhcount = count if (dhcount > count) or (dhcount == None) else dhcount

        #repeat with seeded (high)scores
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
                #get all scores
                shtime_list = []
                shcount_list = []
                for time in shresults['time'].values[0]:
                    shtime_list.append(time)
                for count in shresults['count'].values[0]:
                    shcount_list.append(count)
                #append results
                for result in shtime_list:
                    fstimeL.append(result)
                for result in shcount_list:
                    fscountL.append(result)
            #get high scores TODO: CHANGE TO LEADERBOARD DB
            for time in shresults['time'].values[0]:
                shtime = time if (shtime > time) or (shtime == None) else shtime
            for count in shresults['count'].values[0]:
                shcount = count if (shcount > count) or (shcount == None) else shcount

        #reorganizes all scores to be accessed better
        fdaily = []
        for i in range(len(fdtimeL)):
            fdaily.append([fdtimeL[i], fdcountL[i]])
        fseeded = []
        for i in range(len(fstimeL)):
            fseeded.append([fstimeL[i], fscountL[i]])
        #       #all daily scores   #all seeded scores  #daily high score   #seeded high score
        #       return[0][i][x]     return[1][i][x]     return[2][x]        return[3][x]
        return [fdaily,             fseeded,            [dhtime, dhcount],  [shtime, shcount]]