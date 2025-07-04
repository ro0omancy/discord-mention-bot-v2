import discord
from discord.ext import commands
import asyncio

class Mentioner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mention(self, ctx, role_id: int):
        """أمر لمنشن جميع الأعضاء في رول معين باستخدام Role ID"""
        try:
            role = ctx.guild.get_role(role_id)
            if not role:
                await ctx.send("❌ ما لقيت الرول. تأكد من الـ Role ID.")
                return

            # جلب الأعضاء اللي عندهم الرول (بدون البوتات)
            members = [m for m in ctx.guild.members if role in m.roles and not m.bot]

            if not members:
                await ctx.send("❌ ما فيه أحد عنده الرول.")
                return

            batch_size = 70  # عدد المنشنات في كل رسالة
            delay = 3  # تأخير بين الرسائل بالثواني
            total = len(members)
            digits = len(str(total))  # لترقيم الأعضاء

            for i in range(0, total, batch_size):
                batch = members[i:i+batch_size]
                mentions = []

                for idx, member in enumerate(batch, start=i+1):
                    number = str(idx).zfill(digits)
                    mentions.append(f"{number}. {member.mention}")

                message = f"📣 منشن للرول: {role.mention}\n\n" + "\n".join(mentions)
                await ctx.channel.send(message)

                # إضافة فاصل بين المجموعات
                if i + batch_size < total:
                    separator = "||--------------------------------||"
                    await ctx.channel.send(separator)
                    await asyncio.sleep(delay)

        except ValueError:
            await ctx.send("❌ الـ Role ID غير صحيح. تأكد من كتابة الأرقام فقط.")

async def setup(bot):
    await bot.add_cog(Mentioner(bot))