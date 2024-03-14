import discord
from discord import app_commands
from discord.ext import commands

class 세이브데이터(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="세이브데이터", description="세이브데이터를 보냅니다.")
    async def 세이브데이터(self, interaction: discord.Interaction):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        file_path = f"id/{guildID}.json"
        await interaction.response.send_message(file=discord.File(file_path), ephemeral=True)

async def setup(bot):
    await bot.add_cog(세이브데이터(bot))
