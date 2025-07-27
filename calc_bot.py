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

client.run(TOKEN)