import discord
from discord import app_commands
from discord.ext import commands
import json
import re

class 뱅온메시지설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="뱅온메시지설정", description="방송 공지를 할 때 쓰일 뱅온 메시지를 설정합니다")
    @app_commands.describe(bang = "방송 공지를 할 때 쓰일 뱅온 메시지를 설정합니다")
    async def 뱅온메시지설정(self, interaction: discord.Interaction, bang: app_commands.Range[str, 1, 100]):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        await interaction.response.send_message(f"`{bang}`(으)로 뱅온 메시지를 설정했습니다!", ephemeral=True)
        asdf['bang'] = bang
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(뱅온메시지설정(bot))
