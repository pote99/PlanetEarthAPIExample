import discord
import requests


# 봇 토큰
TOKEN = ''

# API 키
API_KEY = ''

# 역할 ID
ROLE_ID = ''


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    if message.content.startswith('!auth'):
        
        # SENDER id 가져오기
        author_id = message.author.id

        # API
        api_url = f'https://planetearth.kr/api/discord.php?key={API_KEY}&discord={author_id}'
        pe_request = requests.get(api_url)
        data = pe_request.json()

        # SUCCESS인지 확인
        if data['status'] == 'SUCCESS':

            pe_data = data['data'][0]
            #account_id = pe_data['discord'] 디스코드 ID
            uuid = pe_data['uuid'] # 마인크래프트 UUID

            # 인게임 닉네임 가져오기
            mojang_url = f'https://api.mojang.com/user/profile/{uuid}'
            mc_request = requests.get(mojang_url)
            minecraft = mc_request.json()
            ign = minecraft['name']

            # 역할 가져오기
            guild = message.guild
            role = discord.utils.get(guild.roles, id=int(ROLE_ID))

            # 역할 부여, 성공 메시지 전송, IGN으로 별명 변경
            await message.channel.send("플래닛어스 디스코드에 인증된 유저입니다! 권한을 지급합니다.")
            await message.author.add_roles(role)
            await message.author.edit(nick=ign)
        else:
            # 실패 메시지 전송
            await message.channel.send("플래닛어스 디스코드에 인증되지 않은 유저입니다. 관리자에게 문의해주세요.")


client.run(TOKEN)
