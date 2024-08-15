"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""
import random

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from discord import interactions
import datetime

class Character:
    def __init__(self,name,parts,colors,range,ally):
        self.name = name
        self.parts = parts
        self.colors = colors
        self.range = range
        self.ally = ally

    def GetName(self):
        return self.name
    def GetParts(self):
        return self.parts
    def GetColors(self):
        return self.colors
    def GetRange(self):
        return self.range
    def GetAlly(self):
        return self.ally

    #compare functions return 0 if not the same, 1 if exactly the same, 2 if some are the same
    def CompareName(self,other):
        if self.name == other.name:
            return 1
        else:
            return 0

    def CompareParts(self,other):
        if self.parts == other.parts:
            return 1
        for part in self.parts.split(","):
            if part in other.parts.split(","):
                return 2
        return 0

    def CompareColors(self,other):
        if self.colors == other.colors:
            return 1
        for color in self.colors.split(","):
            if color in other.colors.split(","):
                return 2
        return 0

    def CompareRange(self,other):
        if self.range == other.range:
            return 1
        else:
            return 0
        
    def CompareAlly(self,other):
        if self.ally == other.ally:
            return 1
        else:
            return 0

class CharactersList:
    charArray = [
        #["name",                   "part(s)",  "colors",           "stand range", "alliance"]
        ["Jonathan Joestar",        "1",        "Blue,Brown,Grey",      "N/A", "Hero"],
        ["Will Anthonio Zeppeli",   "1",        "Black,White,Red",      "N/A", "Hero"],
        ["Robert E. O. Speedwagon", "1,2",      "Purple,Green,Yellow",  "N/A", "Hero"],
        ["Dio Brando",              "1,3,6",    "Yellow,Green,Black",   "Close", "Villain"],
        ["Frog",                    "1",        "Green,Black,White",    "N/A", "N/A"],
        ["Straizo",                 "1,2",      "Black,Purple,Red",     "N/A", "N/A"],

        ["Joseph Joestar",          "2,3,4",    "Brown,Green,Blue",     "Close", "Hero"],
        ["Caesar Anthonio Zeppeli", "2",        "White,Blue,Pink",      "N/A", "Hero"],
        ["Lisa Lisa",               "2",        "Black,Red",            "N/A", "Hero"],
        ["Rudol von Stroheim",      "2",        "Black,Green,Yellow",   "N/A", "Hero"],
        ["Smokey Brown",            "2",        "Brown,Gray,Blue",      "N/A", "Hero"],
        ["Suzi Q",                  "2,3",      "Green,Yellow,White",   "N/A", "Hero"],
        ["Kars",                    "2",        "Purple,Pink",          "N/A", "Villain"],
        ["Esidisi",                 "2",        "Blue,Tan",             "N/A", "Villain"],
        ["Wamuu",                   "2",        "Tan,Yellow,Red",       "N/A", "Villain"],

        ["Jotaro Joestar",          "3,4,6",    "Black,Gold,Green",     "Close", "Hero"],
        ["Muhammad Avdol",          "3",        "Red,Gold,Tan",         "Close", "Hero"],
        ["Kakyoin Noriaki",         "3",        "Red,Green,Gold",       "Long", "Hero"],
        ["Jean Pierre Polnareff",   "3,5",      "Grey,Black,Red",       "Close", "Hero"],
        ["Iggy",                    "3",        "Black,White,Yellow",   "Close", "Hero"],
        ["Holy Kujo",               "3",        "Pink,Tan,Yellow",      "Close", "Hero"],
        ["Enya the Hag",            "3",        "Brown,Silver,Yellow",  "Long", "Villain"],
        ["Vanilla Ice",             "3",        "Purple,Pink,Tan",      "Close", "Villain"],
        ["Hol Horse",               "3",        "Yellow, Green, Brown", "Long", "Villain"],
        ["Oingo",                   "3",        "Blue,Red,Green",       "N/A", "Villain"],
        ["Boingo",                  "3",        "Green,Tan,Yellow",     "N/A", "Villain"],
        ["Telence T. D'Arby",       "3",        "Green,White,Purple",   "Close", "Villain"],
        ["Daniel J. D'Arby",        "3",        "Red,White,Pink",       "Close", "Villain"],
        ["Mannish Boy",             "3",        "Tan,Red,Blue",         "Close", "Villain"],
        ["Strength",                "3",        "Black,White,Brown",    "Close", "Villain"],

        ["Josuke Higashikata",      "4",        "Purple,Gold,Black",    "Close", "Hero"],
        ["Koichi Hirose",           "4,5",      "Green,Grey,Gold",      "Long", "Hero"],
        ["Okuyasu Nijimura",        "4",        "Blue,Green,Gold",      "Close", "Hero"],
        ["Rohan Kishibe",           "4",        "Green,White,Pink",     "Close", "Hero"],

        ["Giorno Giovanna",         "5",        "Purple,Yellow,Blue",   "Close", "Hero"],
        ["Bruno Bucciarati",        "5",        "White,Black,Gold",     "Close", "Hero"],
        ["Leone Abbacchio",         "5",        "Black,Purple,Gold",    "Close", "Hero"],
        ["Guido Mista",             "5",        "Orange,Blue,White",    "Long", "Hero"],
        ["Narancia Ghirga",         "5",        "Purple,Orange,Black",  "Long", "Hero"],
        ["Pannacotta Fugo",         "5",        "Green,Blue,Yellow",    "Close", "Hero"],
        ["Trish Una",               "5",        "Pink,Black,Yellow",    "Close", "Hero"],

        ["Jolyne Cujoh",            "6",        "Green,Orange,Yellow", "Close", "Hero"],
        ["Ermes Costello",          "6",        "Green,Brown,Orange", "Close", "Hero"],
        ["Emporio Alnino",          "6",        "White,Blue,Yellow", "N/A", "Hero"],
        ["Foo Fighters",            "6",        "Green,Blue,Yellow", "N/A", "Hero"],
        ["Weather Report",          "6",        "Blue,White,Yellow", "Close", "Hero"],
        ["Narciso Anastasia",       "6",        "Pink,Brown,White", "Close", "Hero"],
        ["Gwess",                   "6",        "Purple,Green,Blue", "Long", "N/A"],
        ["Enrico Pucci",            "6",        "Black,White,Gold", "Long", "Villain"],
        ["Johngalli A.",            "6",        "Purple,White", "Long", "Villain"],
        ["The Green Baby",          "6",        "Green,Red", "Close", "N/A"],

        ["Johnny Joestar",          "7",        "Blue,Yellow,Purple", "Long", "Hero"],
        ["Gyro Zeppeli",            "7",        "Purple,Green,Tan", "Long", "Hero"],
        ["Lucy Steel",              "7",        "Pink,Yellow", "N/A", "Hero"],
        ["Diego Brando",            "7",        "Blue,Yellow,Tan", "N/A", "Villain"],
        ["Hot Pants",               "7",        "Pink,Yellow,Grey", "N/A", "N/A"],
        ["Mountain Tim",            "7",        "Grey,Tan,Yellow", "N/A", "Hero"],
        ["Funny Valentine",         "7",        "Pink,Yellow,Purple", "Close", "Villain"],
        ["Pocoloco",                "7",        "Yellow,Brown,Orange", "Close", "N/A"],
        ["Jesus",                   "7",        "Tan,Brown", "N/A", "N/A"],
        ["Wekapipo",                "7",        "Yellow,Orange,Blue", "N/A", "Villain"],
        ["Sandman",                 "7",        "Green,Brown,Yellow", "Close", "Villain"],
        ["Pork Pie Hat Kid",        "7",        "Green,Yellow,Brown", "Long", "Villain"],
        ["Sugar Mountain",          "7",        "Pink,Black,Purple", "N/A", "N/A"],
        ["Magenta Magenta",         "7",        "Purple", "Close", "Villain"]

                ]
    charObjects = None

    def __init__(self):
        print("init CharactersList")
        self.CheckObjects()

    def CheckObjects(self):
        print("Checking Objects")
        if self.charObjects == None:
            self.charObjects = []
            for char in self.charArray:
                self.charObjects.append(Character(char[0],char[1],char[2],char[3],char[4]))
                #print(f"added char: {char[0]}")
        print("finished Checking Objects")

    def CharCount(self):
        return len(self.charObjects)

    def GetChar(self, index):
        return self.charObjects[index]

# Here we name the cog and create a new class for the cog.
class Jojodle(commands.Cog, name="JoJodle"):
    def __init__(self, bot) -> None:
        print("JoJodle init")
        self.bot = bot
        self.charList = CharactersList()
        self.colors = [0xf5462f,0x38eb7d,0xf5ee2f]
        self.SetDay()


    def CompareGuess(self, char1, char2):
        results = []
        results.append(char1.CompareName(char2))
        results.append(char1.CompareParts(char2))
        results.append(char1.CompareColors(char2))
        results.append(char1.CompareRange(char2))
        results.append(char1.CompareAlly(char2))
        return results

    def SetSeed(self, seed):
        self.seed = seed
        random.seed(self.seed)
        self.seedChar = self.charList.GetChar(random.randint(0, self.charList.CharCount() - 1))

    def SetDay(self):
        print("Setting Day")
        self.day = datetime.datetime.now().strftime("%j%Y")
        random.seed(self.day)
        self.curChar = self.charList.GetChar(random.randint(0, self.charList.CharCount() - 1))
        print("Finished Setting Day")

    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)
    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="viewjo",
        description="sends today's current jo",
    )
    async def viewjo(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here
        embed = discord.Embed(description=f"||Today's JoJo's character is {self.curChar.GetName()} from part(s): {self.curChar.GetParts()} their main colors are {self.curChar.GetColors()}||")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="getrandint",
        description="sends today's random integer and the current seed",
    )
    async def getrandint(self, context: Context) -> None:
        seed = datetime.datetime.now().strftime("%j%Y")
        random.seed(seed)
        curInt = random.randint(0, self.charList.CharCount()-1)
        embed = discord.Embed(description=f"||Today's random integer is {curInt} with a seed of {seed}||")
        await context.send(embed=embed)

#User Commands

    #autocomplete choices for all guess commands
    async def guess_autocomplete(self,
                               interaction: discord.Interaction,
                               current: str,
                               ) -> [app_commands.Choice[str]]:
        choices = []
        for char in self.charList.charObjects:
            choices.append(char.GetName())
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

    #standard daily guess command
    @app_commands.command(
        name="guess",
        description="make a guess for today's JoJodle"
    )
    @app_commands.autocomplete(choices=guess_autocomplete)
    async def guess(self, i: discord.Interaction, choices: str):
        if datetime.datetime.now().strftime("%j%Y") != self.day:
            self.SetDay()
        charGuess = None
        results = []
        choices = choices.lower()
        for char in self.charList.charObjects:
            if char.GetName().lower() == choices:
                charGuess = char
                results = self.CompareGuess(char, self.curChar)
        # rest of your command
        embeds = []
        embeds.append(discord.Embed(description=f"||You guessed {charGuess.GetName()}||", color=self.colors[results[0]]))
        embeds.append(discord.Embed(description=f"||Part(s): {charGuess.GetParts()}||", color=self.colors[results[1]]))
        embeds.append(discord.Embed(description=f"||Colors: {charGuess.GetColors()}||", color=self.colors[results[2]]))
        embeds.append(discord.Embed(description=f"||Stand range: {charGuess.GetRange()}||", color=self.colors[results[3]]))
        embeds.append(discord.Embed(description=f"||Alliance: {charGuess.GetAlly()}||", color=self.colors[results[4]]))
        await i.response.send_message(embeds=embeds)

    #seeded guess command
    @app_commands.command(
        name="seededguess",
        description="make a guess for today's JoJodle"
    )
    @app_commands.autocomplete(choices=guess_autocomplete)
    async def seededguess(self, i: discord.Interaction, choices: str, seed: str = None):
        if seed != None:
            self.SetSeed(seed)
        charGuess = None
        results = []
        choices = choices.lower()
        for char in self.charList.charObjects:
            if char.GetName().lower() == choices:
                charGuess = char
                results = self.CompareGuess(char, self.seedChar)
        # rest of your command
        embeds = []
        embeds.append(discord.Embed(description=f"||You guessed {charGuess.GetName()}||", color=self.colors[results[0]]))
        embeds.append(discord.Embed(description=f"||Part(s): {charGuess.GetParts()}||", color=self.colors[results[1]]))
        embeds.append(discord.Embed(description=f"||Colors: {charGuess.GetColors()}||", color=self.colors[results[2]]))
        embeds.append(discord.Embed(description=f"||Stand range: {charGuess.GetRange()}||", color=self.colors[results[3]]))
        embeds.append(discord.Embed(description=f"||Alliance: {charGuess.GetAlly()}||", color=self.colors[results[4]]))
        await i.response.send_message(embeds=embeds)

#highscore commands
    #manually add highscores
    @app_commands.command(
        name="addhs",
        description="Shows the highscores of a user in the server.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @app_commands.describe(user="The user you want to get the warnings of.")
    @commands.is_owner()
    async def addhs(self, i: discord.Interaction, user: discord.User, time:float, count:int, daily: bool = False) -> None:
        member = i.guild.get_member(user.id) or await i.guild.fetch_member(
            user.id
        )
        if daily:
            await self.bot.database.add_daily_hs(user.id, i.guild.id, time, count)
        else:
            await self.bot.database.add_seeded_hs(user.id, i.guild.id, time, count)
        type = "daily" if daily else "seeded"
        embed = discord.Embed(description=f"added {member}'s {type} highscore( time: {time}, count: {count})")
        await i.response.send_message(embed=embed)

    #get highscores(XX-type 0 = daily, type 1 = seeded, type 2 = both-XX, all (show all scores))
    @app_commands.command(
        name="highscores",
        description="Shows the highscores of a user in the server.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def highscores(self, i: discord.Interaction, user: discord.User, all:bool = False) -> None:
        """
        Shows the warnings of a user in the server.

        :param context: The hybrid command context.
        :param user: The user you want to get the warnings of.
        """
        #       #all daily scores   #all seeded scores  #daily high score   #seeded high score
        #       return[0][x][i]     return[1][x][i]     return[2][x]        return[3][x]
        highscore_results = await self.bot.database.get_highscores(user.id, i.guild.id, all)
        embed = discord.Embed(title=f"Highscores of {user}", color=0xe483ff)
        '''description = ""
        if highscore_results == -1:
            description = "This user has no highscores."
        else:
            description += f"*|         Daily       Highscores         |* *|         Seeded      Highscores         |*\n"
            description += "*| time: {dtime:<8}s - count: {dcount:<4}guesses |* *| time: {stime:<8}s - count: {scount:<4}guesses |*\n".format(
                dtime = highscore_results[2][0],
                dcount = highscore_results[2][1],
                stime = highscore_results[3][0],
                scount = highscore_results[3][1]
            )
            if all:
                description += f"*|       All     Daily      scores        |* *|       All     Seeded      scores       |*\n"
                rows = []
                for daily in highscore_results[0]:
                    rows.append("*| time: {dtime:<8}s - count: {dcount:<4}guesses |*".format(
                        dtime = daily[0],
                        dcount = daily[1]
                    ))
                for i in range(len(highscore_results[1])):
                    try:
                        rows[i] += " *| time: {stime:<8}s - count: {scount:<4}guesses |*\n".format(
                            stime=highscore_results[1][i][0],
                            scount=highscore_results[1][i][1]
                        )
                    except:
                        rows.append("                                           *| time: {stime:<8}s - count: {scount:<4}guesses |*\n".format(
                            stime=highscore_results[1][i][0],
                            scount=highscore_results[1][i][1]
                        ))'''
        description = highscore_results
        embed.description = description
        await i.response.send_message(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Jojodle(bot))
