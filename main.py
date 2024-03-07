import discord
from discord import app_commands
from discord.ext import commands
from discord import File
import json
import requests
import asyncio
from datetime import datetime
import os
import re

def is_valid_hex_color(code):
    hex_color_pattern = re.compile(r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return bool(hex_color_pattern.match(code))

def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

with open("token.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
token = config["token"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?",intents = intents)

global cate

with open("cate.json", 'r', encoding='utf-8') as f:
    cate = json.load(f)

@bot.event
async def on_ready():
    print('Ready!')
    bot.loop.create_task(check())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="아프리카"))
    await bot.tree.sync()

@bot.event
async def on_guild_join(guild):
    guildID = guild.id
    if not os.path.exists(f"id/{guildID}.json"):
        restricted_channel = await guild.create_text_channel("🔔ㅣ방송알림")
        await restricted_channel.set_permissions(guild.default_role, send_messages=False)
        with open(f"id/{guildID}.json", 'w', encoding='utf-8') as f:
            json.dump({"id": "macaronbot", "bang": "/뱅온메시지설정", "message": "/메시지설정", "channel": f"{str(restricted_channel.id)}", "button": "/버튼설정", "foot": "/시간메시지설정", "color": "0545b1", "previous": False, "broad": None}, f, ensure_ascii=False)
        print(guildID)

async def check():
    while True:
        guildID = bot.guilds
        for i in range(len(guildID)):
            with open(f"id/{guildID[i].id}.json", 'r', encoding='utf-8') as file:
                global mes
                mes = json.load(file)
                global chan
                chan = int(mes['channel'])
                global id
                id = mes['id']
                global link
                global mess
                mess = mes['message']
                global bang
                bang = mes['bang']
                global but
                but = mes['button']
                global foot
                foot = mes['foot']
                global broad
                broad = mes['broad']
                global previous
                previous = mes['previous']
                global color
                color = mes['color']
            data = requests.get(f'http://bjapi.afreecatv.com/api/{id}/station', headers = {'User-Agent': 'Mozilla/5.0'}).json()
            if 'code' in data:
                mes['previous'] = False
                mes['broad'] = None
                with open(f"id/{guildID[i].id}.json", 'w', encoding='utf-8') as f:
                    json.dump(mes, f, ensure_ascii=False)
            else:
                if type(data['broad']) != type(broad):
                    mes['broad'] = data['broad']
                    mes['previous'] = not previous
                    with open(f"id/{guildID[i].id}.json", 'w', encoding='utf-8') as f:
                        json.dump(mes, f, ensure_ascii=False)

                    if mes['previous'] == True:
                        db = "https://live.afreecatv.com/afreeca/player_live_api.php"
                        dbdata = {"bid": id}
                        response = requests.post(db, data=dbdata)
                        dbdata = response.json()
                        game = dbdata['CHANNEL']['CATE']

                        channel = bot.get_channel(chan)
                        prev = str(data['broad']['broad_no'])
                        link = f"https://play.afreecatv.com/{id}/{prev}"
                        preview = f"https://liveimg.afreecatv.com/h/{prev}.webp"
                        embed=discord.Embed(title=f"{data['broad']['broad_title']}", url=f"{link}", color=int(color, 16))
                        embed.set_author(name=f"{mess}", url=f"{link}", icon_url=f"https:{data['profile_image']}")
                        embed.set_image(url=preview)
                        embed.add_field(name="카테고리", value=f"{cate[game]}", inline=True)
                        embed.add_field(name="시청자", value=f"{data['broad']['current_sum_viewer']}명", inline=True)
                        embed.set_footer(text=f"{foot}")
                        embed.timestamp = datetime.now()
                        await channel.send(content=bang,embed=embed, view=ButtonFunction())

        await asyncio.sleep(30)

class ButtonFunction(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label=f'{but}', url=f"{link}"))

@bot.command()
async def savedata(message):
    if (message.user.guild_permissions.administrator or message.user.id == 439421870857519104) and not isinstance(message.channel, discord.DMChannel):
        serverID = message.guild.id
        user_data_file = f'id/{serverID}.json'
        if os.path.exists(user_data_file):
            await message.channel.send(file=File(user_data_file))
        else:
            await message.channel.send('Unknown')

@bot.tree.command(name="아이디설정", description="아프리카 아이디를 설정합니다")
@app_commands.describe(id = "bj.afreecatv.com/macaronbot/123456789에서 'macaronbot' 부분")
async def 아이디설정(interaction: discord.Interaction, id: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    if not re.match("^[a-zA-Z0-9]+$", id):
        await interaction.response.send_message(f"올바른 아프리카 아이디 형식이 아닙니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{id}`(을)를 아프리카 아이디로 설정했습니다!", ephemeral=True)
    asdf['id'] = id
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="뱅온메시지설정", description="방송 공지를 할 때 쓰일 뱅온 메시지를 설정합니다")
@app_commands.describe(bang = "방송 공지를 할 때 쓰일 뱅온 메시지를 설정합니다")
async def 뱅온메시지설정(interaction: discord.Interaction, bang: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{bang}`(으)로 뱅온 메시지를 설정했습니다!", ephemeral=True)
    asdf['bang'] = bang
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="메시지설정", description="프로필 사진 옆에 뜨는 메시지를 설정합니다")
@app_commands.describe(message = "프로필 사진 옆에 뜨는 메시지를 설정합니다")
async def 메시지설정(interaction: discord.Interaction, message: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{message}`(으)로 메시지를 설정했습니다!", ephemeral=True)
    asdf['message'] = message
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="채널설정", description="방송 공지용 채널을 설정합니다")
@app_commands.describe(id = "디스코드 설정 - 고급 - 개발자 모드 활성화 후, 원하늘 채널 우클릭 - 채널 ID 복사하기 클릭")
async def 채널설정(interaction: discord.Interaction, id: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    if not is_convertible_to_int(id):
        await interaction.response.send_message(f"올바른 채널 ID 형식이 아닙니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"<#{id}> 채널을 공지용 채널로 설정했습니다!", ephemeral=True)
    asdf['channel'] = id
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="버튼설정", description="버튼 문구를 설정합니다")
@app_commands.describe(button = "버튼 문구를 설정합니다")
async def 버튼설정(interaction: discord.Interaction, button: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{button}`(을)를 버튼 문구로 설정했습니다!", ephemeral=True)
    asdf['button'] = button
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="시간메시지설정", description="방송 시작 시간 옆에 쓰일 메시지를 설정합니다")
@app_commands.describe(time = "방송 시작 시간 옆에 쓰일 메시지를 설정합니다")
async def 시간메시지설정(interaction: discord.Interaction, time: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
        return
    guildID = interaction.guild.id
    with open(f"id/{guildID}.json", 'r', encoding='utf-8') as file:
        asdf = json.load(file)
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == 439421870857519104):
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{time}`(을)를 시간 메시지로 설정했습니다!", ephemeral=True)
    asdf['foot'] = time
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

@bot.tree.command(name="색상설정", description="임베드의 색상을 설정합니다")
@app_commands.describe(color = "0545b1 혹은 #0545B1 형식으로 헥스코드를 입력해주시기 바랍니다")
async def 색상설정(interaction: discord.Interaction, color: str):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"명령어는 DM에서 사용하실 수 없습니다.", ephemeral=True)
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
        await interaction.response.send_message(f"명령어를 사용하실 권한이 없습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"`{color}`(을)를 임베드 색상으로 설정했습니다!", ephemeral=True)
    asdf['color'] = color
    with open(f"id/{guildID}.json", 'w', encoding='utf-8') as file:
        json.dump(asdf, file, ensure_ascii=False)

bot.run(token)