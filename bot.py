import os

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from database.database import save_message
from indexer.index_server import index_guild
from ingestion.pipeline import ingest_message
from vector_db.chroma_db import add_message
from rag.pipeline import answer

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.tree.command(name="ask", description="Ask a question to the AI investigator.")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()

    response = answer(question)

    await interaction.followup.send(response)
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

    except Exception as e:
        print(e)
    #Enable to index the server on startup if bot was not present when the server was created. This will index all messages in the server.
    #guild = bot.guilds[0]
    #await index_guild(guild)
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if not message.content:
        return

    save_message(message)
    add_message(message)
    ingest_message(message)
    await bot.process_commands(message)
    print(f"{message.author}: {message.content}")

bot.run(TOKEN)