import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration from environment variables
TWITTER_CHANNEL_ID = int(os.getenv('TWITTER_CHANNEL_ID', '1326211329844969533'))
TWITTER_ROLE_ID = int(os.getenv('TWITTER_ROLE_ID', '1332445630160961587'))
TIKTOK_CHANNEL_ID = int(os.getenv('TIKTOK_CHANNEL_ID', '1332675349003370506'))
TIKTOK_ROLE_ID = int(os.getenv('TIKTOK_ROLE_ID', '1332675394964291708'))

def create_twitter_embed(text, image_url=None, author_name="Twitter User", author_avatar="https://abs.twimg.com/icons/apple-touch-icon-192x192.png"):
    """Create a stylized Twitter notification embed"""
    embed = discord.Embed(
        description=text, 
        color=0x1DA1F2,  # Twitter blue
        timestamp=datetime.now()
    )
    embed.set_author(
        name=author_name, 
        icon_url=author_avatar
    )
    if image_url:
        embed.set_image(url=image_url)
    embed.set_footer(text="Twitter", icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png")
    return embed

def create_tiktok_embed(text, video_url=None, author_name="TikTok Creator", author_avatar="https://sf16-scmcdn-sg.ibytedtos.com/goofy/tiktok/web/node/_next/static/media/logo.1f506ab5.svg"):
    """Create a stylized TikTok notification embed"""
    embed = discord.Embed(
        description=text, 
        color=0x000000,  # TikTok black
        timestamp=datetime.now()
    )
    embed.set_author(
        name=author_name, 
        icon_url=author_avatar
    )
    if video_url:
        embed.set_image(url=video_url)
    embed.set_footer(text="TikTok", icon_url="https://sf16-scmcdn-sg.ibytedtos.com/goofy/tiktok/web/node/_next/static/media/logo.1f506ab5.svg")
    return embed

@bot.command(name='tweet')
async def simulate_tweet(ctx, *, content):
    """Advanced Twitter notification simulation"""
    # Split content into optional parts
    parts = content.split('|')
    tweet_text = parts[0].strip()
    image_url = parts[1].strip() if len(parts) > 1 else None
    author_name = parts[2].strip() if len(parts) > 2 else "Twitter User"
    
    # Get Twitter channel and role
    twitter_channel = bot.get_channel(TWITTER_CHANNEL_ID)
    twitter_role = twitter_channel.guild.get_role(TWITTER_ROLE_ID)

    # Create embed
    embed = create_twitter_embed(
        text=tweet_text, 
        image_url=image_url if image_url and image_url.startswith('http') else None,
        author_name=author_name
    )

    # Send notification
    await twitter_channel.send(twitter_role.mention, embed=embed)
    await ctx.message.delete()

@bot.command(name='tiktok')
async def simulate_tiktok(ctx, *, content):
    """Advanced TikTok notification simulation"""
    # Split content into optional parts
    parts = content.split('|')
    tiktok_text = parts[0].strip()
    video_url = parts[1].strip() if len(parts) > 1 else None
    author_name = parts[2].strip() if len(parts) > 2 else "TikTok Creator"
    
    # Get TikTok channel and role
    tiktok_channel = bot.get_channel(TIKTOK_CHANNEL_ID)
    tiktok_role = tiktok_channel.guild.get_role(TIKTOK_ROLE_ID)

    # Create embed
    embed = create_tiktok_embed(
        text=tiktok_text, 
        video_url=video_url if video_url and video_url.startswith('http') else None,
        author_name=author_name
    )

    # Send notification
    await tiktok_channel.send(tiktok_role.mention, embed=embed)
    await ctx.message.delete()

@tasks.loop(seconds=60)
async def change_status():
    """Alternate between TikTok and Twitter status"""
    activities = [
        discord.Game("a scroller sur TikTok"),
        discord.Game("a lire des Twittos")
    ]
    current_activity = next(activities_cycle)
    await bot.change_presence(activity=current_activity)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    # Initialize the cycle and start changing status
    global activities_cycle
    activities = [
        discord.Game("a scroller sur TikTok"),
        discord.Game("a lire des Twittos")
    ]
    activities_cycle = iter(activities)
    change_status.start()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
