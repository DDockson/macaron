import discord
from discord import app_commands
from discord.ext import commands

class 사용법(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="사용법", description="봇 사용 가이드를 보냅니다")
    async def 사용법(self, interaction: discord.Interaction):
        await interaction.response.send_message("`봇 사용 가이드:` <https://zrr.kr/OZGf>", ephemeral=True)

async def setup(bot):
    await bot.add_cog(사용법(bot))
