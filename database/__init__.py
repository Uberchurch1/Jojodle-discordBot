"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""
import time

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

    #add daily highscore time and/or count TODO: copy seeded
    async def add_daily_hs(
        self, user_id: int, server_id: int, time: float = None, count: int = None
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        #add score to all scores db
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

        #adding to dleaderboard
        rows = await self.connection.execute(
            "SELECT created_at FROM dleaderboard WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        #checks if there is any highscore otherwise makes a new one
        async with rows as cursor:
            # TODO: check rank
            rank = -1
            if await cursor.fetchone() == None:
                await self.connection.execute(
                    "INSERT INTO dleaderboard(user_id, server_id, type, time, count, rank) VALUES (?, ?, 0, ?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time,
                        count,
                        # TODO: add rank
                        rank
                    ),
                )
                await self.connection.execute(
                    "INSERT INTO dleaderboard(user_id, server_id, type, time, count, rank) VALUES (?, ?, 1, ?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time,
                        count,
                        # TODO: add rank
                        rank
                    ),
                )
                await self.connection.commit()
                return 0
        # find a greater(worse score) time
        rows = await self.connection.execute(
            "SELECT created_at FROM dleaderboard WHERE user_id=? AND server_id=? AND time >= ? AND type = 0",
            (
                user_id,
                server_id,
                time
            ),
        )
        async with rows as cursor:
            # TODO: check rank
            rank = -1
            if await cursor.fetchone() != None:
                # update current high score
                await cursor.execute(
                    "UPDATE dleaderboard SET time = ?, count = ?, rank = ? WHERE user_id = ? AND server_id=? AND type=0",
                    (
                        time,
                        count,
                        rank,
                        user_id,
                        server_id
                        # TODO: add rank
                    ),
                )

        # find a greater(worse score) count
        rows = await self.connection.execute(
            "SELECT created_at FROM dleaderboard WHERE user_id=? AND server_id=? AND count >= ? AND type = 1",
            (
                user_id,
                server_id,
                count
            ),
        )
        async with rows as cursor:
            # TODO: check rank
            rank = -1
            if await cursor.fetchone() != None:
                # update current high score
                await cursor.execute(
                    "UPDATE dleaderboard SET time = ?, count = ?, rank = ? WHERE user_id = ? AND server_id=? AND type=1",
                    (
                        time,
                        count,
                        rank,
                        user_id,
                        server_id
                        # TODO: add rank
                    ),
                )

        await self.connection.commit()
        return 1
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
        #add to personal all scores
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

        #check if is high score and add to sleaderboard
        rows = await self.connection.execute(
            "SELECT created_at FROM sleaderboard WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        # checks if there is any highscore otherwise makes a new one
        async with rows as cursor:
            #TODO: check rank
            rank = -1
            if await cursor.fetchone() == None:
                await self.connection.execute(
                    "INSERT INTO sleaderboard(user_id, server_id, type, time, count, rank) VALUES (?, ?, 0, ?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time,
                        count,
                        #TODO: add rank
                        rank
                    ),
                )
                await self.connection.execute(
                    "INSERT INTO sleaderboard(user_id, server_id, type, time, count, rank) VALUES (?, ?, 1, ?, ?, ?)",
                    (
                        user_id,
                        server_id,
                        time,
                        count,
                        # TODO: add rank
                        rank
                    ),
                )
                await self.connection.commit()
                return 0
        #find a greater(worse score) time
        rows = await self.connection.execute(
            "SELECT created_at FROM sleaderboard WHERE user_id=? AND server_id=? AND time >= ? AND type = 0",
            (
                user_id,
                server_id,
                time
            ),
        )
        async with rows as cursor:
            # TODO: check rank
            rank = -1
            if await cursor.fetchone() != None:
                #update current high score
                await cursor.execute(
                    "UPDATE sleaderboard SET time = ?, count = ?, rank = ? WHERE user_id = ? AND server_id=? AND type=0",
                    (
                        time,
                        count,
                        rank,
                        user_id,
                        server_id
                        # TODO: add rank
                    ),
                )

        # find a greater(worse score) count
        rows = await self.connection.execute(
            "SELECT created_at FROM sleaderboard WHERE user_id=? AND server_id=? AND count >= ? AND type = 1",
            (
                user_id,
                server_id,
                count
            ),
        )
        async with rows as cursor:
            # TODO: check rank
            rank = -1
            if await cursor.fetchone() != None:
                # update current high score
                await cursor.execute(
                    "UPDATE sleaderboard SET time = ?, count = ?, rank = ? WHERE user_id = ? AND server_id=? AND type=1",
                    (
                        time,
                        count,
                        rank,
                        user_id,
                        server_id
                        # TODO: add rank
                    ),
                )

        await self.connection.commit()
        return 1

    #TODO: MAKE CHECK RANK LEADERBOARD FUNCTION

    #get highscores daily and/or seeded
    async def get_scores(self, user_id: int, server_id: int, all:bool = False) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """

        # ----------------------------#
        fdaily = []
        fseeded = []

        #get daily (high)scores
        if all:
            dhscores = await self.connection.execute(
                "SELECT time, count, created_at FROM dhs WHERE user_id=? AND server_id=? ORDER BY created_at DESC",
                (
                    user_id,
                    server_id,
                ),
            )
            async with dhscores as cursor:
                results = await cursor.fetchall()
                if results == None:
                    fdaily = None
                else:
                    for result in results:
                        fdaily.append(result)
        # ----------------------------#

        #----------------------------#
        rows = await self.connection.execute(
            "SELECT time, count, created_at, rank FROM dleaderboard WHERE user_id=? AND server_id=? ORDER BY type",
            (
                user_id,
                server_id,
            )
        )
        async with rows as cursor:
            results = await cursor.fetchall()
            try:
                dhtime = results[0]
                dhcount = results[1]
            except:
                dhtime = None
                dhcount = None
        # ----------------------------#

        # get seeded (high)scores
        if all:
            shscores = await self.connection.execute(
                "SELECT time, count, created_at FROM shs WHERE user_id=? AND server_id=? ORDER BY created_at DESC",
                (
                    user_id,
                    server_id,
                ),
            )
            async with shscores as cursor:
                results = await cursor.fetchall()
                if results == None:
                    fseeded = None
                else:
                    for result in results:
                        fseeded.append(result)
        # ----------------------------#
        # ----------------------------#
        rows = await self.connection.execute(
            "SELECT time, count, created_at, rank FROM sleaderboard WHERE user_id=? AND server_id=? ORDER BY type",
            (
                user_id,
                server_id,
            )
        )
        async with rows as cursor:
            results = await cursor.fetchall()
            try:
                shtime = results[0]
                shcount = results[1]
            except:
                shtime = None
                shcount = None
        # ----------------------------#

        #       #all daily scores   #all seeded scores  #daily high score   #seeded high score
        #       return[0][i][x]     return[1][i][x]     return[2][t][x]        return[3][t][x]
        #       [0]time, [1]count, [2]created_at        [0]time, [1]count, [2]created_at, [3]rank
        return [fdaily,             fseeded,            [dhtime, dhcount],  [shtime, shcount]]

    async def reset_comp(self, date: time.struct_time):
        await self.connection.execute(
            "UPDATE gtracker SET completed = 0.0, time = 0, count = 0, date=? WHERE type=0 AND date<>?",
            (
                date,
                date
            )
        )
        await self.connection.commit()

    async def track_guess(self, user_id: int, server_id: int, time: time.struct_time, date: time.struct_time, correct: bool = False) -> [float, int]:
        completed = 0
        rows = await self.connection.execute(
            "SELECT time, count, completed FROM gtracker WHERE user_id=? AND server_id=? AND type=0",
            (
                user_id,
                server_id,
            )
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            print(result)
            if result == None:
                print("inserting")
                await self.connection.execute(
                    "INSERT INTO gtracker (user_id, server_id, type, time, count, completed, date) VALUES (?, ?, 0, ?, 1, 0,?)",
                    (
                        user_id,
                        server_id,
                        time,
                        date
                    ),
                )
            elif result[2] == 0:
                print("update")
                completed = time - result[0]
                await self.connection.execute(
                    "UPDATE gtracker SET time=?, count=?, completed=? WHERE user_id=? AND server_id=? AND type=0",
                    (
                        time if result[0] == 0 else result[0],
                        result[1] + 1,
                        completed if correct else 0,
                        user_id,
                        server_id,
                    )
                )
            else:
                return [result[2], result[1]]
            print('commit')
            await self.connection.commit()
            if correct:
                await self.add_daily_hs(user_id, server_id, time=completed, count=result[1] + 1)
            return [completed, result[1]+1 if result != None else 1]