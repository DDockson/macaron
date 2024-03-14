import discord
from discord import app_commands
from discord.ext import commands
import json

class 채널설정(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="채널설정", description="공지용 채널을 설정해보세요.")
    @app_commands.describe(channel='방송을 공지할 채널을 선택해주세요.')
    async def 채널설정(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("명령어는 DM에서 사용할 수 없습니다.", ephemeral=True)
            return
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
            await interaction.response.send_message("명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return
        guildID = interaction.guild.id
        with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
            asdf = json.load(file)
        await interaction.response.send_message(f"<#{channel.id}> 채널을 공지용 채널로 설정했습니다!", ephemeral=True)
        asdf['channel'] = channel.id
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
            json.dump(asdf, file, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(채널설정(bot))
