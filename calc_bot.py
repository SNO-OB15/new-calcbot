import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.tree.sync()  # 슬래시 커맨드 동기화

client = MyClient()

@client.tree.command(name="calc", description="계산기 명령어")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(expression="계산할 수식을 입력하세요")
async def calc(interaction: discord.Interaction, expression: str):
    try:
        # eval 조심! 보안상 문제 생길 수 있음. 간단한 수식 정도만 허용.
        result = eval(expression, {"__builtins__": None}, {})
        await interaction.response.send_message(f'계산 결과: {result}')
    except Exception as e:
        await interaction.response.send_message(f'오류: 올바른 수식을 입력해주세요.\n{e}')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 사용자별 데이터 저장 딕셔너리
user_data = {}

@bot.event
async def on_ready():
    print(f"봇 로그인됨: {bot.user}")
    try:
        await bot.tree.sync()
        print("슬래시 커맨드 동기화 완료")
    except Exception as e:
        print(f"에러 발생: {e}")

# /저장 입력 키 출력 값
@bot.tree.command(name="저장", description="입력 키와 출력 값을 저장합니다.")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(입력="저장할 키", 출력="불러올 때 보여줄 값")
async def 저장(interaction: discord.Interaction, 입력: str, 출력: str):
    user_id = str(interaction.user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][입력] = 출력
    await interaction.response.send_message(f"`{입력}`에 대한 값을 저장했습니다: `{출력}`")

# /출력 키
@bot.tree.command(name="출력", description="입력 키로 저장된 값을 출력합니다.")
@app_commands.describe(입력="불러올 키")
async def 출력(interaction: discord.Interaction, 입력: str):
    user_id = str(interaction.user.id)
    if user_id in user_data and 입력 in user_data[user_id]:
        await interaction.response.send_message(f"`{입력}`의 값: `{user_data[user_id][입력]}`")
    else:
        await interaction.response.send_message(f"`{입력}`에 해당하는 데이터가 없습니다.")


client.run(TOKEN)