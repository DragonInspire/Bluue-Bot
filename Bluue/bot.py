import discord 
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Select, View
from dotenv import load_dotenv
import os
from overlayImage import overlayImage
from guildList import guildList
from get_online_farplane import get_online_farplane
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Create a bot instance with a command prefix and all intents enabled
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# List of ranks for the uniform selection
ranks = ["resident", "buke", "bushi", "shogun", "yako"]

# Event: Bot is ready
@bot.event
async def on_ready():
    print("bot is running")
    try:
        # Attempt to sync the commands with the server
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
    farplane_online_edit.start()

# Command: Display help information
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(
        '''```
Commands
    /uniform
    /farplane_list
        ```
        ''')

@tasks.loop(minutes=1)
async def farplane_online_edit():
    channel = bot.get_channel(1131996950548467782)
    message = await channel.fetch_message(1131998219673538640)
    online_peoples = get_online_farplane()
    printable_online = "**Online members of The Farplane guild**$```$"

    for world in online_peoples:
        printable_online += world
        printable_online += "$"
        for player in online_peoples[world]:
            printable_online += "   "
            printable_online += player
            printable_online += "$"
    printable_online += "```"
    printable_online += f"$Last update at {datetime.now()} UTC time"
    printable_online = printable_online.replace("$", "\n")
    await message.edit(content=printable_online)

@bot.tree.command(name="farplane_list")
async def farplane_list(interaction: discord.Interaction):
    memberList = guildList()

    try:
        await interaction.response.send_message(f"farplane members {memberList}")
    except:
        await interaction.response.send_message(f"sorry the member list was too long, discord only supports 2000 characters")

# Command: Choose a uniform rank
@bot.tree.command(name="uniform")
@app_commands.describe(username="Username:")
async def uniform(interaction: discord.Interaction, username: str):
    # Create a list of SelectOption for each rank
    optionList = list(map(lambda rankInList: discord.SelectOption(label=rankInList), ranks))
    
    # Create a Select component with the options
    select = Select(options=optionList)
    
    # Callback function for the selection
    async def my_callback(interaction):
        # Get the selected rank from the Select component
        choice = select.values[0]
        
        # Generate the uniform image and create a Discord file
        file = discord.File(overlayImage(username, choice), filename="uniform.png")
        
        # Send a message with the uniform image
        await interaction.response.send_message(f"hey {username} here is your {choice} uniform", file=file)

    # Set the callback for the Select component
    select.callback = my_callback
    
    # Create a View with the Select component
    view = View()
    view.add_item(select)
    
    # Send a message with the Select component to choose a rank
    await interaction.response.send_message("choose a rank", view=view)

try: 
    # Run the bot with the provided Discord token
    bot.run(DISCORD_TOKEN)
except discord.HTTPException as e: 
    if e.status == 429: 
        print("The Discord servers denied the connection for making too many requests") 
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests") 
    else: 
        raise e
