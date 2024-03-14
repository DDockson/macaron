import discord
from discord import app_commands
from discord.ext import commands
import json

def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

class 버튼설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="버튼설정", description="버튼 문구를 설정합니다")
    @app_commands.describe(button = "버튼 문구를 설정합니다")
    async def 버튼설정(self, interaction: discord.Interaction, button: app_commands.Range[str, 1, 20]):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        await interaction.response.send_message(f"`{button}`(을)를 버튼 문구로 설정했습니다!", ephemeral=True)
        asdf['button'] = button
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(버튼설정(bot))
