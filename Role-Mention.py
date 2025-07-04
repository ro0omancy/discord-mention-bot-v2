
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # ضروري للوصول لقائمة الأعضاء
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ بوت المنشن شغال: {bot.user}")
    # تحميل cog المنشن
    await bot.load_extension("cogs.mentioner")

bot.run(os.environ["MENTIONER_TOKEN"])
