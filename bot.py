import discord
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

intents = discord.Intents.all()

intents.members = True

# bot = commands.Bot(command_prefix="!fight", intents=intents)

# @bot.hybrid_command(name="first_slash")
# async def first_slash(ctx): 
#    await ctx.send("You executed the slash command!") #respond no longer works, so i changed it to send

# @bot.event
# async def on_ready():
#    await bot.sync() #sync the command tree
#    print("Bot is ready and online")

# bot.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord import app_commands
import os
from battle_simulation import fair_fight_decider
import json

guild_id = os.getenv("GUILD_ID")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=guild_id), name = 'help', description='Intro and info') #guild specific slash command
async def help(interaction: discord.Interaction):

    message = """\
    I am a Battle Simulator! Train, get stronger and rise up the leaderboard!

    Features:
    1. Create your character/class (/class)

    2. Two User fights (/fight me)

    3. Train (or Win) to get stronger (/train)

    4. View Leaderboard (/lb)"""

    await interaction.response.send_message(message, ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'lb', description='Show figher leaderboard')
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.send_message(f" \
            Leaderboard: to be implemented", ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'class', description='Create or Change your character\'s class')
async def modify_character_class(interaction: discord.Interaction, character_class: str):
    
    try:
        if fair_fight_decider(character_class):
        
            Player = interaction.user.name
            
            # Check if the user exists
            with open('battle_data.json', 'r') as f:
                stats = json.load(f)

            if interaction.user in stats: # user exists
                stats[Player]['Class'] = character_class
                with open('battle_data.json', 'w') as f:
                    json.dump(stats, f)

                await interaction.response.send_message(f"{interaction.user.mention}, changing you class to: {character_class}")
                
            else: # user does not exist
                stats[Player] = dict()
                stats[Player]['Class'] = character_class
                stats[Player]['Wins'] = 0
                stats[Player]['CritNumber'] = 2

                with open('battle_data.json', 'w') as f:
                    json.dump(stats, f)

                await interaction.response.send_message(f" Welcome {interaction.user.mention} to the Discord BattleSim! Your class is: {character_class}", ephemeral = False)
        else:
            await interaction.response.send_message(f"{interaction.user.mention}, your class was not approved. Try again.")
    except Exception as e:
        print(e)


@tree.command(guild = discord.Object(id=guild_id), name = 'fight', description='Enter fighting arena!')
async def fight(interaction: discord.Interaction):
    await interaction.response.send_message(f" \
            {interaction.user.mention} entered the fight! (Work in progress)", ephemeral = False) 

client.run(os.getenv("DISCORD_TOKEN"))
