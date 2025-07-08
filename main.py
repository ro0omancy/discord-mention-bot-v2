import discord
from discord.ext import commands
import os
import asyncio
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# رقم الكاتيجوري الخاص بالتكتات
CATEGORY_ID = 1230055223939174420

# الرولات المسموح لهم باستخدام أمر المنشن
ALLOWED_ROLE_IDS = [
    1069172391156125807,
    787033561521061939,
    1229787664132214795
]

# المستخدمين المسموح لهم باستخدام أمر المنشن (User IDs)
ALLOWED_USER_IDS = [
    836444737942323200,
    816569640834039818,
    919176925870714890
]

def has_allowed_role():
    async def predicate(ctx):
        return (
            ctx.author.id in ALLOWED_USER_IDS or
            any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)
        )
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"✅ البوت شغّال: {bot.user}")

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
        if channel.name.startswith("closed-"):
            try:
                await channel.delete()
                deleted += 1
            except Exception as e:
                print(f"⚠️ خطأ في حذف {channel.name}: {e}")
    await ctx.send(f"✅ تم حذف {deleted} قناة تبدأ بـ `closed-` في `{category.name}`")

@bot.command()
@has_allowed_role()
async def mention(ctx, role_id: int):
    try:
        role = ctx.guild.get_role(role_id)
        if not role:
            await ctx.send("❌ ما لقيت الرول. تأكد من الـ Role ID.")
            return

        members = [m for m in role.members if not m.bot]
        if not members:
            await ctx.send("❌ ما فيه أحد عنده الرول.")
            return

        batch_size = 50
        delay = 3
        total = len(members)
        digits = len(str(total))

        for i in range(0, total, batch_size):
            batch = members[i:i + batch_size]
            list_number = (i // batch_size) + 1
            current_message = (
                f"📢: {role.mention}\n"
                f"🎖️ : {role.name}\n"
                f"━━━━━━({list_number})━━━━━━\n\n"
            )
            for idx, member in enumerate(batch, start=i + 1):
                number = str(idx).zfill(digits)
                current_message += f"{number}. {member.mention}\n"

            if i + batch_size >= total:
                current_message += "**-------DONE :white_check_mark: ------**"
            else:
                current_message += "||--------------------------------||"

            await ctx.channel.send(current_message)

            if i + batch_size < total:
                await asyncio.sleep(delay)

    except ValueError:
        await ctx.send("❌ الـ Role ID غير صحيح. تأكد من كتابة الأرقام فقط.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 هذا الأمر مخصص لرولات معيّنة فقط.")
    else:
        raise error

# aiohttp webserver to keep bot alive on Replit
async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.router.add_get("/", handle)

async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    print(f"🌐 Webserver started on port {os.environ.get('PORT', 8080)}")

async def main():
    await start_webserver()
    await bot.start(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
