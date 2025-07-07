import discord
from discord.ext import commands
import asyncio

ALLOWED_ROLE_IDS = [
    1069172391156125807,
    787033561521061939,
    800835255379427378
]

def has_allowed_role():
    async def predicate(ctx):
        return any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)
    return commands.check(predicate)

class Mentioner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_allowed_role()
    async def mention(self, ctx, role_id: int):
        try:
            role = ctx.guild.get_role(role_id)
            if not role:
                await ctx.send("❌ ما لقيت الرول. تأكد من الـ Role ID.")
                return

            # استخدم role.members بدل فحص كل الأعضاء
            members = [m for m in role.members if not m.bot]
            if not members:
                await ctx.send("❌ ما فيه أحد عنده الرول.")
                return

            batch_size = 50
            delay = 3
            total = len(members)
            digits = len(str(total))

            for i in range(0, total, batch_size):
                batch = members[i:i+batch_size]
                current_message = f"📣 منشن للرول: {role.mention}\n\n"

                for idx, member in enumerate(batch, start=i+1):
                    number = str(idx).zfill(digits)
                    mention_line = f"{number}. {member.mention}\n"

                    if len(current_message) + len(mention_line) < 2000:
                        current_message += mention_line
                    else:
                        await ctx.channel.send(current_message)
                        await asyncio.sleep(delay)
                        current_message = f"📣 منشن للرول: {role.mention}\n\n{mention_line}"

                if current_message.strip():
                    await ctx.channel.send(current_message)

                if i + batch_size < total:
                    separator = "||--------------------------------||"
                    await ctx.channel.send(separator)
                    await asyncio.sleep(delay)

        except ValueError:
            await ctx.send("❌ الـ Role ID غير صحيح. تأكد من كتابة الأرقام فقط.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("🚫 هذا الأمر مخصص لرولات معيّنة فقط.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Mentioner(bot))
