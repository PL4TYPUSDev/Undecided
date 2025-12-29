import discord
from discord.ext import commands
import requests
import os

# =====================
# CONFIG
# =====================
TOKEN = os.getenv("TOKEN")

WELCOME_CHANNEL_ID = 1455076752907829349
RULES_CHANNEL_ID = 1455073160406765642

# =====================
# BOT SETUP
# =====================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# =====================
# READY
# =====================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# =====================
# AUTO WELCOME
# =====================
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.TextChannel):
        return

    embed = discord.Embed(
        title="👋 Welcome!",
        description=(
            f"Welcome {member.mention}!\n\n"
            f"📜 Please read <#{RULES_CHANNEL_ID}> before chatting."
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await channel.send(embed=embed)

# =====================
# /ROBux COMMAND
# =====================
@bot.command()
async def robux(ctx, amount: int):
    tax = int(amount * 0.30)
    receive = amount - tax

    embed = discord.Embed(
        title="💰 Robux Calculator",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Original Robux", value=amount, inline=False)
    embed.add_field(name="Tax (30%)", value=tax, inline=False)
    embed.add_field(name="You Receive", value=receive, inline=False)

    await ctx.send(embed=embed)

# =====================
# /GAMEPASS COMMAND
# =====================
@bot.command()
async def gamepass(ctx, gamepass_id: int):
    url = f"https://billowing-sky-14c1.macheterbx.workers.dev/?id={gamepass_id}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except:
        await ctx.send("❌ Failed to fetch gamepass data.")
        return

    embed = discord.Embed(
        title="🎮 Gamepass Information",
        color=discord.Color.orange()
    )
    embed.add_field(name="Name", value=data["name"], inline=False)
    embed.add_field(name="Price", value=f'{data["priceInRobux"]} Robux', inline=False)
    embed.add_field(name="Regional Pricing", value=data["regionalPricing"], inline=False)

    await ctx.send(embed=embed)

# =====================
# /COMMANDS COMMAND (DM ONLY)
# =====================
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="📖 Command List",
        description="Here are all available commands:",
        color=discord.Color.purple()
    )
    embed.add_field(name="/commands", value="Shows this help menu", inline=False)
    embed.add_field(name="/robux <amount>", value="Calculates Robux after 30% tax", inline=False)
    embed.add_field(name="/gamepass <id>", value="Shows gamepass name, price & regional pricing", inline=False)

    try:
        await ctx.author.send(embed=embed)
        await ctx.reply("📬 Check your DMs for the command list!", delete_after=5)
    except:
        await ctx.reply("❌ I can't DM you. Please enable DMs.", delete_after=5)

# =====================
# UNKNOWN COMMAND HANDLER
# =====================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❓ Unknown Command",
            description="Here are the available commands:",
            color=discord.Color.red()
        )
        embed.add_field(name="/commands", value="Show all commands", inline=False)
        embed.add_field(name="/robux <amount>", value="Robux calculator", inline=False)
        embed.add_field(name="/gamepass <id>", value="Gamepass info", inline=False)

        try:
            await ctx.author.send(embed=embed)
            await ctx.reply("❌ Unknown command. Check your DMs 📬", delete_after=5)
        except:
            await ctx.reply("❌ Unknown command. Enable DMs to see help.", delete_after=5)

# =====================
# RUN BOT
# =====================
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERROR: TOKEN environment variable not set. Please set your Discord bot token.")
