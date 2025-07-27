import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

DATA_FILE = "user_data.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# JSON 파일에서 데이터 불러오기
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# JSON 파일에 데이터 저장
def save_user_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@bot.event
async def on_ready():
    print(f"봇 로그인됨: {bot.user}")
    try:
        guild_id = 1388168041824784457  # 테스트할 디스코드 서버 ID로 바꿔주세요
        guild = discord.Object(id=guild_id)
        synced = await bot.tree.sync(guild=guild)
        print(f"길드 {guild_id}에 슬래시 명령어 {len(synced)}개 동기화 완료")
    except Exception as e:
        print(f"동기화 에러: {e}")

# /계산 명령어
@bot.tree.command(name="계산", description="계산기 명령어")
@app_commands.describe(expression="계산할 수식을 입력하세요")
async def 계산(interaction: discord.Interaction, expression: str):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        await interaction.response.send_message(f'계산 결과: {result}')
    except Exception as e:
        await interaction.response.send_message(f'오류: 올바른 수식을 입력해주세요.\n{e}')

# /저장 명령어
@bot.tree.command(name="저장", description="입력 키와 출력 값을 저장합니다.")
@app_commands.describe(입력="저장할 키", 출력="불러올 때 보여줄 값")
async def 저장(interaction: discord.Interaction, 입력: str, 출력: str):
    user_id = str(interaction.user.id)
    data = load_user_data()

    if user_id not in data:
        data[user_id] = {}
    data[user_id][입력] = 출력
    save_user_data(data)

    await interaction.response.send_message(f"`{입력}`에 대한 값을 저장했습니다: `{출력}`")

# /출력 명령어
@bot.tree.command(name="출력", description="입력 키로 저장된 값을 출력합니다.")
@app_commands.describe(입력="불러올 키")
async def 출력(interaction: discord.Interaction, 입력: str):
    user_id = str(interaction.user.id)
    data = load_user_data()

    if user_id in data and 입력 in data[user_id]:
        await interaction.response.send_message(f"{입력} = {data[user_id][입력]}")
    else:
        await interaction.response.send_message(f"`{입력}`에 해당하는 데이터가 없습니다.")

# /삭제 명령어
@bot.tree.command(name="삭제", description="저장된 키를 삭제합니다.")
@app_commands.describe(입력="삭제할 키")
async def 삭제(interaction: discord.Interaction, 입력: str):
    user_id = str(interaction.user.id)
    data = load_user_data()

    if user_id in data and 입력 in data[user_id]:
        del data[user_id][입력]
        save_user_data(data)
        await interaction.response.send_message(f"`{입력}`에 대한 저장된 값을 삭제했습니다.")
    else:
        await interaction.response.send_message(f"`{입력}`에 해당하는 저장된 값이 없습니다.")

bot.run(TOKEN)