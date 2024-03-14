import discord
from discord import app_commands
from discord.ext import commands
import json

class 시간메시지설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="시간메시지설정", description="방송 시작 시간 옆에 쓰일 메시지를 설정합니다")
    @app_commands.describe(time = "방송 시작 시간 옆에 쓰일 메시지를 설정합니다")
    async def 시간메시지설정(self, interaction: discord.Interaction, time: app_commands.Range[str, 1, 20]):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        await interaction.response.send_message(f"`{time}`(을)를 시간 메시지로 설정했습니다!", ephemeral=True)
        asdf['foot'] = time
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(시간메시지설정(bot))
