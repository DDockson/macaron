import discord
from discord import app_commands
from discord.ext import commands
import json
import re

def is_valid_hex_color(code):
    hex_color_pattern = re.compile(r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return bool(hex_color_pattern.match(code))

class 색상설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="색상설정", description="임베드의 색상을 설정합니다")
    @app_commands.describe(color = "0545b1 혹은 #0545B1 형식으로 헥스코드를 입력해주시기 바랍니다")
    async def 색상설정(self, interaction: discord.Interaction, color: str):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        if color[0] == '#':
            color = color[1:]
        if not is_valid_hex_color(color):
            await interaction.response.send_message("해당 형식은 헥스코드 형식이 아닙니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        await interaction.response.send_message(f"`{color}`(을)를 임베드 색상으로 설정했습니다!", ephemeral=True)
        asdf['color'] = color
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(색상설정(bot))
