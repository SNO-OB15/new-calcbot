import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 봇이 로그인되었습니다!")

@bot.command()
async def calc(ctx, *, expression: str):
    try:
        # eval은 위험할 수 있으니 꼭 신뢰할 수 있는 수식만 쓰세요.
        result = eval(expression, {"__builtins__": None}, {})
        await ctx.send(f"계산 결과: {result}")
    except Exception as e:
        await ctx.send(f"수식 오류: {e}")

bot.run(TOKEN)