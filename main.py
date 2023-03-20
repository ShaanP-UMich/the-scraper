import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_API_TOKEN = os.environ.get('DISCORD_API_TOKEN')

OUTPUT_DIR = 'output'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

# @bot.event
# async def on_message(message):
#     if message.channel.name == "bot-testing":
#         print(f'{message.author.name}: {message.content}')


@bot.command(name='last')
async def last_n_messages(context, limit=10, channel_id=None):
    print(context.channel)
    channel = context.channel

    if channel_id != None:
        channel = await bot.fetch_channel(channel_id)

    async for message in channel.history(limit=limit):
        reply = f'{message.author.name}: {message.content}'
        print(reply)
        # await context.send(reply, delete_after=10, silent=True)


@bot.command(name='last_years')
async def last_year_messages(context, years=1, channel_id=None):
    channel = context.channel

    if channel_id != None:
        channel = await bot.fetch_channel(channel_id)

    timeframe = datetime.datetime.now() - datetime.timedelta(weeks=years*52)
    file_name = f'{context.guild.name}-{channel.name}-output-{years}.txt'
    output_file = os.path.join(OUTPUT_DIR, file_name)

    with open(output_file, 'w') as f:
        print(f"Beginning output to {output_file}")
        async for message in channel.history(after=timeframe, limit=None):
            f.write(
                f'{message.created_at} | {message.author.name}: {message.content}\n')
        # await context.send("Done writing to output file", delete_after=10, silent=True)
        print(f'Outputted to {output_file}')


@bot.command(name='last_all')
async def last_year_messages(context, channel_id=None):
    channel = context.channel

    if channel_id != None:
        channel = await bot.fetch_channel(channel_id)

    file_name = f'{context.guild.name}-{channel.name}-output-all.txt'
    output_file = os.path.join(OUTPUT_DIR, file_name)

    with open(output_file, 'w') as f:
        print(f"Beginning output to {output_file}")
        async for message in channel.history(limit=None):
            f.write(
                f'{message.created_at} | {message.author.name}: {message.content}\n')
        # await context.send("Done writing to output file", delete_after=10, silent=True)
        print(f'Outputted to {output_file}')


bot.run(DISCORD_API_TOKEN)
