"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""
import datetime
import time

import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection
        
#JOJODLE DB COMMANDS

    #add daily highscore time and/or count TODO: copy seeded
    async def add_daily_hs(
        self, user_id: int, server_id: int, time: float = None, count: int = None
    ) -> int:
        """
        This function will add a score to the daily database.

        :param user_id: The ID of the user that should be warned.
        :param time: The time score.
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
        This function will add a score to the seeded database.

        :param user_id: The ID of the user that should be warned.
        :param time: The time score.
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
        This function will get all the scores of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the scores of the user.
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

    async def leaderboard(self, server_id: int, number:int = 10) -> list:
        # get daily leaderboard
        # get time scores
        dtime=[]
        results = await self.connection.execute(
            "SELECT rank, user_id, time, count, created_at FROM dleaderboard WHERE server_id=? AND type=0 ORDER BY rank",
            (server_id,),
        )
        async with results as cursor:
            results = await cursor.fetchall()
            nrange = number if number < len(results) else len(results)
            for i in range(nrange):
                dtime.append(results[i])
        # get count scores
        dcount = []
        results = await self.connection.execute(
            "SELECT rank, user_id, time, count, created_at FROM dleaderboard WHERE server_id=? AND type=1 ORDER BY rank",
            (server_id,),
        )
        async with results as cursor:
            results = await cursor.fetchall()
            nrange = number if number < len(results) else len(results)
            for i in range(nrange):
                dcount.append(results[i])

        # get seeded leaderboard
        # get time scores
        stime = []
        results = await self.connection.execute(
            "SELECT rank, user_id, time, count, created_at FROM sleaderboard WHERE server_id=? AND type=0 ORDER BY rank",
            (server_id,),
        )
        async with results as cursor:
            results = await cursor.fetchall()
            nrange = number if number < len(results) else len(results)
            for i in range(nrange):
                stime.append(results[i])
        # get count scores
        scount = []
        results = await self.connection.execute(
            "SELECT rank, user_id, time, count, created_at FROM sleaderboard WHERE server_id=? AND type=1 ORDER BY rank",
            (server_id,),
        )
        async with results as cursor:
            results = await cursor.fetchall()
            nrange = number if number < len(results) else len(results)
            for i in range(nrange):
                scount.append(results[i])

        #      daily leaderboard by time, by count, seeded leaderboard by time, by count
        #      [0]rank, [1]user_id, [2]time, [3]count, [4]created_at
        return [dtime, dcount, stime, scount]

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

    async def track_sguess(self, user_id: int, server_id: int, time: float, seed: str, correct: bool = False) -> [float, int]:
        completed = 0
        rows = await self.connection.execute(
            "SELECT time, count, completed FROM gtracker WHERE user_id=? AND server_id=? AND type=1 AND seed=?",
            (
                user_id,
                server_id,
                seed
            )
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            print(result)
            if result == None:
                print("inserting")
                await self.connection.execute(
                    "INSERT INTO gtracker (user_id, server_id, type, time, count, completed, seed, date) VALUES (?, ?, 1, ?, 1, 0,?,'none')",
                    (
                        user_id,
                        server_id,
                        time,
                        seed
                    ),
                )
            elif result[2] == 0:
                print("update")
                completed = time - result[0]
                await self.connection.execute(
                    "UPDATE gtracker SET time=?, count=?, completed=? WHERE user_id=? AND server_id=? AND type=1",
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
                await self.add_seeded_hs(user_id, server_id, time=completed, count=result[1] + 1)
            return [completed, result[1]+1 if result != None else 1]

    async def upd_ranks(self):
        # update daily ranks
        # upd time ranks
        results = await self.connection.execute(
            "SELECT user_id, server_id FROM dleaderboard WHERE type=0 ORDER BY time, count"
        )
        async with results as cursor:
            results = await cursor.fetchall()
            for i in range(len(results)):
                await self.connection.execute(
                    "UPDATE dleaderboard SET rank=? WHERE user_id=? AND server_id=? AND type=0",
                    (
                        i+1,
                        results[i][0],
                        results[i][1]
                    )
                )
        # upd count ranks
        results = await self.connection.execute(
            "SELECT user_id, server_id FROM dleaderboard WHERE type=1 ORDER BY count, time"
        )
        async with results as cursor:
            results = await cursor.fetchall()
            for i in range(len(results)):
                await self.connection.execute(
                    "UPDATE dleaderboard SET rank=? WHERE user_id=? AND server_id=? AND type=1",
                    (
                        i+1,
                        results[i][0],
                        results[i][1]
                    )
                )

        # update seeded ranks
        # upd time ranks
        results = await self.connection.execute(
            "SELECT user_id, server_id FROM sleaderboard WHERE type=0 ORDER BY count, time"
        )
        async with results as cursor:
            results = await cursor.fetchall()
            for i in range(len(results)):
                await self.connection.execute(
                    "UPDATE sleaderboard SET rank=? WHERE user_id=? AND server_id=? AND type=0",
                    (
                        i+1,
                        results[i][0],
                        results[i][1]
                    )
                )
        # upd count ranks
        results = await self.connection.execute(
            "SELECT user_id, server_id FROM sleaderboard WHERE type=1 ORDER BY time, count"
        )
        async with results as cursor:
            results = await cursor.fetchall()
            for i in range(len(results)):
                await self.connection.execute(
                    "UPDATE sleaderboard SET rank=? WHERE user_id=? AND server_id=? AND type=1",
                    (
                        i+1,
                        results[i][0],
                        results[i][1]
                    )
                )
        await self.connection.commit()