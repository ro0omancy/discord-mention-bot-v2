import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_ID = 1230055223939174420  # ← غيّرها لرقم الكاتيجوري حق التكتات

@bot.event
async def on_ready():
    print(f"✅ البوت شغّال: {bot.user}")

@bot.command(name="sendT")
@commands.has_permissions(administrator=True)
async def send_transcript(ctx):
    category = discord.utils.get(ctx.guild.categories, id=CATEGORY_ID)
    if not category:
        await ctx.send("❌ ما لقيت الكاتيجوري.")
        print("⚠️ الكاتيجوري غير موجود.")
        return

    sent = 0
    for channel in category.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.send("/transcript")
                sent += 1
            except Exception as e:
                print(f"⚠️ خطأ في {channel.name}: {e}")
    await ctx.send(f"✅ تم إرسال /transcript في {sent} قناة.")

@bot.command(name="deleteT")
@commands.has_permissions(administrator=True)
async def delete_tickets(ctx):
    category = discord.utils.get(ctx.guild.categories, id=CATEGORY_ID)
    if not category:
        await ctx.send("❌ ما لقيت الكاتيجوري.")
        print("⚠️ الكاتيجوري غير موجود.")
        return

    deleted = 0
    for channel in category.channels:
        try:
            await channel.delete()
            deleted += 1
        except Exception as e:
            print(f"⚠️ خطأ في حذف {channel.name}: {e}")
    await ctx.send(f"✅ تم حذف {deleted} قناة في `{category.name}`")

bot.run(os.environ["DISCORD_TOKEN"])