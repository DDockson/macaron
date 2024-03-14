import discord
from discord.ext import commands
import json
import requests
import asyncio
from datetime import datetime
import os

with open("token.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
token = config["token"]

intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="?",intents = intents)

bot.remove_command("help")

global cate

with open("cate.json", 'r', encoding='utf-8') as f:
    cate = json.load(f)

async def load():
    for filename in os.listdir("./commands"):
        if filename.endswith("py"):
            await bot.load_extension(f"commands.{filename[:-3]}")

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
        bot_role = guild.get_member(bot.user.id)
        await restricted_channel.set_permissions(bot_role, send_messages=True)
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

asyncio.run(load())

bot.run(token)