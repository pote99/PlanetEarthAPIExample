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
    
    # !auth를 쳤을때
    if message.content.startswith('!auth'):
        
        # SENDER id 가져오기
        author_id = message.author.id

        # 디스코드 API
        discord_url = f'https://planetearth.kr/api/discord.php?key={API_KEY}&discord={author_id}'
        discord_request = requests.get(discord_url)
        discord_json = discord_request.json()

        # 서버, 역할 가져오기
        guild = message.guild
        role = discord.utils.get(guild.roles, id=int(ROLE_ID))

        # SUCCESS인지 확인
        if discord_json['status'] == 'SUCCESS':

            discord_data = discord_json['data'][0]
            #account_id = discord_data['discord'] 디스코드 ID
            uuid = discord_data['uuid'] # 마인크래프트 UUID

            # 인게임 API, 만약 군인 랭크에게 디스코드 군인 역할을 지급하고 싶다면 nation-ranks를 가져오면 됩니다.
            town_url = f'https://planetearth.kr/api/resident.php?key={API_KEY}&uuid={uuid}'
            town_request = requests.get(town_url)
            town_json = town_request.json()
            town_data = town_json['data'][0]
            town_name = town_data['town']

            # 마을 이름이 같을 때
            if town_name == 'Dev_Island':

                # IGN가져오기
                ign = town_data['name']

                # 역할 부여, 성공 메시지 전송, IGN으로 별명 변경
                await message.channel.send("인증에 성공했습니다! 권한을 지급합니다.")
                # await message.channel.send(f"마을 {town_name}")
                await message.author.add_roles(role)
                await message.author.edit(nick=ign)

            # FAILED인지 확인
            elif town_json['status'] == 'FAILED':
            
                # 실패 메시지 전송
                await message.channel.send("타우니 데이터를 가져올 수 없습니다.")

            # 마을 이름이 같지 않을 때
            elif town_name != 'Dev_Island':

                # 실패 메시지 전송
                await message.channel.send("마을에 가입되지 않은 플레이어입니다.")

            else:

                # 오류 메시지 전송
                await message.channel.send("오류가 발생했습니다. 관리자에게 문의해주세요.")

        # FAILED인지 확인
        elif discord_json['status'] == 'FAILED':

            # 실패 메시지 전송
            await message.channel.send("플래닛어스 디스코드에 인증되지 않은 유저입니다.")

        else:

            # 오류 메시지 전송
            await message.channel.send("오류가 발생했습니다. 관리자에게 문의해주세요.")
    
client.run(TOKEN)
