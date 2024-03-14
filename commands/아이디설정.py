import discord
from discord import app_commands
from discord.ext import commands
import json
import re

class 아이디설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="아이디설정", description="아프리카 아이디를 설정합니다")
    @app_commands.describe(id = "bj.afreecatv.com/macaronbot/123456789에서 'macaronbot' 부분")
    async def 아이디설정(self, interaction: discord.Interaction, id: str):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        if not re.match("^[a-zA-Z0-9]+$", id):
            await interaction.response.send_message(f"올바른 아프리카 아이디 형식이 아닙니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        await interaction.response.send_message(f"`{id}`(을)를 아프리카 아이디로 설정했습니다!", ephemeral=True)
        asdf['id'] = id
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(아이디설정(bot))
