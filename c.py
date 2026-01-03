# FIRE DROP V4 Ultra Multi — full updated file (with Sticker Spammer integrated)
# Requires: pillow
import asyncio
import json
import os
import time
import logging
import random
import io
import requests
from gtts import gTTS

from typing import Dict, List, Optional, Set

from telegram import Update, Bot as TgBot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# NEW: Pillow for image processing
from PIL import Image, ImageOps

# ---------------------------FIRE DROP
TOKENS = [
    "8061799871:AAHIprGgp0xMf-XM6Tu49TVw0ZofACl__q8",
    "8257005872:AAFlrcpz2u4WJwiBvIKXZQKGpvRqQI2KU90", 
    "8215339883:AAE76TcS8K1t_DX8QSoHCC5nJ4O-JtsSzyo",
    "",
    "",
    ""
]

CHAT_ID = -5066783565
OWNER_ID = 8588747553
SUDO_FILE = "sudo.json"
STICKER_FILE = "stickers.json"
VOICE_CLONES_FILE = "voice_clones.json"
tempest_API_KEY = "sk_e326b337242b09b451e8f18041fd0a7149cc895648e36538"

# ---------------------------
# tempest VOICE CHARACTERS
VOICE_CHARACTERS = {
    1: {
        "name": "Urokodaki",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Deep Indian voice - Urokodaki style",
        "style": "deep_masculine"
    },
    2: {
        "name": "Kanae", 
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "description": "Cute sweet voice - Kanae style",
        "style": "soft_feminine"
    },
    3: {
        "name": "Uppermoon",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "description": "Creepy dark deep voice - Uppermoon style", 
        "style": "dark_creepy"
    },
    4: {
        "name": "Tanjiro",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Heroic determined voice",
        "style": "heroic"
    },
    5: {
        "name": "Nezuko",
        "voice_id": "EXAVITQu4vr4xnSDxMaL", 
        "description": "Cute mute sounds",
        "style": "cute_mute"
    },
    6: {
        "name": "Zenitsu",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "description": "Scared whiny voice",
        "style": "scared_whiny"
    },
    7: {
        "name": "Inosuke",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Wild aggressive voice",
        "style": "wild_aggressive"
    },
    8: {
        "name": "Muzan",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "description": "Evil mastermind voice",
        "style": "evil_calm"
    },
    9: {
        "name": "Shinobu",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "description": "Gentle but deadly voice",
        "style": "gentle_deadly"
    },
    10: {
        "name": "Giyu",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Silent serious voice",
        "style": "silent_serious"
    }
}

# ---------------------------
# TEXTS
RAID_TEXTS = [
    "ᴋɪ sᴀᴛʀᴀɴɢɪ ᴄʜᴜᴛ🤑",
    " ᴋɪ sᴀᴛʀᴀɴɢɪ ᴄʜᴜᴛ🛸",
    " 𝑻ᴇʀɪ 𝑴ᴀ 𝑲𝑎  𝑩ʜᴏsᴅ𝑨ೃ⁀➷🖕🏽",
    "[ ]🍷ᴄʜᴜᴅ кє ᴅᴀꜰᴀɴ🔱",
    "[]>😍< [𝐓𝐌𝐊𝐁]",
    "⭐️  (ｔ𝓂𝓀𝒞) ⃝💫🩵",
    "🗿  (ｔ𝓂𝓀𝒞) ⃝🚀",
    "  ➙ 🇨 ʜꪊᎠ  ɱᥴ ༆ 😡 >",
    "  HTT TMKC 🦥",
    "✦⃝-(𓀐𓂸)- 🇨🇭🇺🇩🇱🇪",
    "✦⃝-(🜏)- 🇷🇦🇳🇩🇮🇰?",
    "✦⃝-(×̷̷͜×̷̷)- 🇹🇲🇷??",
    "✦⃝-(⛧⃝)- ʀᴀɴᴅ",
    " 𝕜ⅈ चुदाई ᴴᴼᴳʸⁱ ⛧☾༺🌐༻☽⛧",
    " 𝕜ⅈ चुदाई ᴴᴼᴳʸⁱ ⛧☾༺🚧༻☽⛧",
]

exonc_TEXTS = [
    "💀", "🔥", "⚡", "🎯", "💥", "🎪", "🍁", "👑", "🔱", "⚜️",
    "💫", "⭐", "🌟", "✨", "🎀", "❤️", "🖤", "💔", "💢", "♨️",
    "💯", "🅱️", "🌀", "🎶", "🎵", "🏆", "🥇", "🎗️", "🎖️", "🏅"
]

NCEMO_EMOJIS = [
    "🗿","👑","🩵","🔱","🌷","❤️‍🩹","👞","🤮","🤣","😭","💔","🥺",
    "😁","👿","🚀","🔥","🥹","😬","🙄","😎","👽","👾","😈","👹",
    "🤡","👋🏿","🤞🏿","🙀","👌🏿","🤟🏿","🐒","🦁","🐅","🦓","🐮"
]

# ---------------------------
# GLOBAL STATE
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}

# Initialize data files
if os.path.exists(STICKER_FILE):
    try:
        with open(STICKER_FILE, "r") as f:
            user_stickers = json.load(f)
    except:
        user_stickers = {}
else:
    user_stickers = {}

if os.path.exists(VOICE_CLONES_FILE):
    try:
        with open(VOICE_CLONES_FILE, "r") as f:
            voice_clones = json.load(f)
    except:
        voice_clones = {}
else:
    voice_clones = {}

def save_sudo():
    with open(SUDO_FILE, "w") as f: 
        json.dump(list(SUDO_USERS), f)

def save_stickers():
    # Ensure directory exists
    os.makedirs("stickers", exist_ok=True)
    with open(STICKER_FILE, "w") as f: 
        json.dump(user_stickers, f)

def save_voice_clones():
    with open(VOICE_CLONES_FILE, "w") as f: 
        json.dump(voice_clones, f)

# Global state variables
group_tasks = {}         
spam_tasks = {}
react_tasks = {}
slide_targets = set()    
slidespam_targets = set()
exonc_tasks = {}
sticker_mode = True
apps, bots = [], []
delay = 0.1
spam_delay = 0.5
exonc_delay = 0.05

# Newly declared missing dict for pfp management
pfp_tasks = {}

# Sticker spammer globals (added)
sticker_spam_tasks = {}
sticker_spam_delay = 0.3

logging.basicConfig(level=logging.INFO)

# ---------------------------
# DECORATORS
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            await update.message.reply_text("💢 FIRE DROP PAPA KO BOL ADD KRE  .")
            return
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            await update.message.reply_text("💢 FIRE DROP PAPA KR SKTE HAI BAS .")
            return
        return await func(update, context)
    return wrapper
    
    # ---------------------------
# tempest VOICE FUNCTIONS
async def generate_tempest_voice(text, voice_id, stability=0.5, similarity_boost=0.8):
    """Generate voice using tempest API"""
    url = f"https://api.tempest.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": tempest_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            logging.error(f"tempest API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"tempest request failed: {e}")
        return None

async def generate_multiple_voices(text, character_numbers):
    """Generate voices for multiple characters"""
    voices = []
    
    for char_num in character_numbers:
        if char_num in VOICE_CHARACTERS:
            voice_data = VOICE_CHARACTERS[char_num]
            audio_data = await generate_tempest_voice(text, voice_data["voice_id"])
            if audio_data:
                voices.append({
                    "character": voice_data["name"],
                    "audio": audio_data,
                    "description": voice_data["description"]
                })
    
    return voices

# ---------------------------
# IMAGE / STICKER HELPERS
def process_image_to_webp(img_bytes: bytes, size=512, border_color=None, border_px=16) -> bytes:
    """
    Convert arbitrary image bytes to Telegram sticker WEBP bytes (512x512).
    Optionally add border (color hex or tuple).
    Returns bytes.
    """
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    # Resize while keeping aspect ratio and transparent background/pad
    img.thumbnail((size, size), Image.LANCZOS)
    # Create a transparent canvas 512x512 and paste centered
    canvas = Image.new("RGBA", (size, size), (0,0,0,0))
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    canvas.paste(img, (x, y), img)

    # Optionally add border by expanding and then centering
    if border_color:
        canvas = ImageOps.expand(canvas, border=border_px, fill=border_color)
        # If expanded, resize back to exact size keeping content visible
        canvas = canvas.convert("RGBA")
        canvas.thumbnail((size, size), Image.LANCZOS)
        final_canvas = Image.new("RGBA", (size, size), (0,0,0,0))
        fx = (size - canvas.width) // 2
        fy = (size - canvas.height) // 2
        final_canvas.paste(canvas, (fx, fy), canvas)
        canvas = final_canvas

    # Save to WEBP bytes (lossless)
    out = io.BytesIO()
    canvas.save(out, format="WEBP", lossless=True, quality=100)
    out.seek(0)
    return out.read()

def ensure_user_folder(uid: int):
    path = os.path.join("stickers", str(uid))
    os.makedirs(path, exist_ok=True)
    return path

# ---------------------------
# LOOP FUNCTIONS
async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "gcnc":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:  # ncemo
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(delay)
        except Exception as e:
            await asyncio.sleep(2)

async def ncbaap_loop(bot, chat_id, base):
    """Ultra fast name changer - 5 changes in 0.1 seconds"""
    i = 0
    while True:
        try:
            # Multiple patterns for ultra fast changes
            patterns = [
                f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}",
                f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}",
                f"{base} {exonc_TEXTS[i % len(exonc_TEXTS)]}",
                f"{RAID_TEXTS[i % len(RAID_TEXTS)]} {base}",
                f"{NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]} {base}",
            ]
            
            # Change name multiple times rapidly
            for pattern in patterns[:3]:  # Change 3 times rapidly
                await bot.set_chat_title(chat_id, pattern)
                await asyncio.sleep(0.02)  # Very fast delay
            
            i += 1
            await asyncio.sleep(0.1)  # Main delay
        except Exception as e:
            await asyncio.sleep(1)

async def spam_loop(bot, chat_id, text):
    while True:
        try:
            await bot.send_message(chat_id, text)
            await asyncio.sleep(spam_delay)
        except Exception as e:
            await asyncio.sleep(2)

async def exonc_godspeed_loop(bot, chat_id, base_text):
    """ULTRA FAST name changer - God Speed mode"""
    i = 0
    while True:
        try:
            # Generate multiple patterns for ultra-fast changes
            patterns = [
                f"{base_text} {exonc_TEXTS[i % len(exonc_TEXTS)]}",
                f"{exonc_TEXTS[i % len(exonc_TEXTS)]} {base_text}",
                f"{base_text}{exonc_TEXTS[i % len(exonc_TEXTS)]}",
                f"{exonc_TEXTS[(i+1) % len(exonc_TEXTS)]} {base_text} {exonc_TEXTS[(i+2) % len(exonc_TEXTS)]}",
                f"{base_text} {exonc_TEXTS[(i+3) % len(exonc_TEXTS)]} {exonc_TEXTS[(i+4) % len(exonc_TEXTS)]}",
            ]
            
            # Change name 5 times in rapid succession
            for j in range(5):
                text = patterns[j % len(patterns)]
                await bot.set_chat_title(chat_id, text)
                await asyncio.sleep(0.01)  # Ultra fast delay between changes
            
            i += 1
            await asyncio.sleep(0.05)  # Main delay
        except Exception as e:
            await asyncio.sleep(0.5)

async def exonc_loop(bot, chat_id, base_text):
    i = 0
    while True:
        try:
            patterns = [
                f"{base_text} {exonc_TEXTS[i % len(exonc_TEXTS)]}",
                f"{exonc_TEXTS[i % len(exonc_TEXTS)]} {base_text}",
                f"{base_text}{exonc_TEXTS[i % len(exonc_TEXTS)]}",
            ]
            text = random.choice(patterns)
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(exonc_delay)
        except Exception as e:
            await asyncio.sleep(1)

async def pfp_loop(bot, chat_id, photo):
    while True:
        try:
            await bot.set_chat_photo(chat_id, photo)
            await asyncio.sleep(0.5)  # delay between changes
        except Exception as e:
            await asyncio.sleep(1)
            
@only_sudo
async def gcpfp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo with /gcpfp")
    
    chat_id = update.message.chat_id
    file_id = update.message.reply_to_message.photo[-1].file_id
    photo = await bots[0].get_file(file_id)
    photo_bytes = await photo.download_as_bytearray()

    if chat_id in pfp_tasks:
        for task in pfp_tasks[chat_id]:
            task.cancel()

    tasks = []
    for bot in bots:
        task = asyncio.create_task(pfp_loop(bot, chat_id, photo_bytes))
        tasks.append(task)

    pfp_tasks[chat_id] = tasks
    await update.message.reply_text("🖼️ GC PFP Auto-Change Started!")

# ---------------------------
# CORE COMMANDS
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪷  V8 Ultra Multi — Commands 🐼\nUse /help")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤍FIRE DROP🤍 TELE CHUDAI BOT MENU 💋

 📛 Name Changers:
/gcnc <name> - 📛 
/ncemo <name> - 💛
/ncbaap <name> -  😺
/stopgcnc - Stop GC changer
/stopncemo - Stop emoji changer  
/stopncbaap - Stop god level
/stopall - Stop everything
/delay <sec> - Set delay

😚 Spam:
/spam <text> - Start spam
/unspam - Stop spam

🤡 React: Not working 😭 
/emojispam <emoji> - Auto react
/stopemojispam - Stop reactions

☺️😈 Slide:
/targetslide (reply) - Target user
/stopslide (reply) - Stop slide
/slidespam (reply) - Slide spam
/stopslidespam (reply) - Stop slide spam

⚡💥 exonc:
/exonc <name> - Fast name change
/exoncfast <name> - Faster
/exoncgodspeed <name> - God speed
/stopexonc - Stop exonc

💕 Sticker System:
/newsticker (reply photo) - Create sticker
/delsticker - Delete stickers
/stickerstatus - Sticker status
/multisticker (reply photo) - Create 5 stickers
/stickerspam - Start sending saved stickers in loop
/stopstickerspam - Stop sticker spam

🎧 Voice Features:
/animevn <characters> <text> - Anime voice (1-10)
/voices - List voices
/tempest <text> - Default voice

👑 SUDO:
/addsudo (reply) - Add sudo
/delsudo (reply) - Remove sudo  
/listsudo - List sudo users

💅 Misc:
/myid - Your ID
/ping - Check bot
/status - Show status
    """
    await update.message.reply_text(help_text)

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end = time.time()
    await msg.edit_text(f"🏓 Pong! {int((end-start)*1000)}ms")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# ---------------------------
# NAME CHANGER COMMANDS
@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /gcnc <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "gcnc"))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🔄 Gc ka name change start hai FIRE DROP Ji!!😋")

@only_sudo
async def ncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemo <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemo"))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🍁 Emoji Name Changer Started FIRE DROP Jii ! ")

@only_sudo
async def ncbaap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """GOD LEVEL Name Changer - 5 changes in 0.1 seconds"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncbaap <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start ultra fast tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(ncbaap_loop(bot, chat_id, base))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("💀🔥 GOD LEVEL NCBAAP ACTIVATED! 5 NC in 0.1s! Kar diya FIRE DROP 🚀")

@only_sudo
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ Rok diya is greeb ka chudai 😋!")
    else:
        await update.message.reply_text("💢 Kisi ki chudai nhi ho rhi ")

@only_sudo
async def stopncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ Emoji changer wali chuda ro Diya God FIRE DROP!")
    else:
        await update.message.reply_text("💢 Emoji changer wali chudai nhi ho rhi FIRE DROP Sir! ")

@only_sudo
async def stopncbaap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ GOD LEVEL NCBAAP Stopped!")
    else:
        await update.message.reply_text("💢 No active ncbaap")

# ---------------------------
# exonc COMMANDS
@only_sudo
async def exonc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exonc <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("💀 exonc Mode Activated!")

@only_sudo
async def exoncfast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exonc_delay
    exonc_delay = 0.03
    
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exoncfast <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("⚡ Faster exonc Activated!")

@only_sudo
async def exoncgodspeed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ULTRA FAST GOD SPEED MODE"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exoncgodspeed <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    # Start GOD SPEED tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_godspeed_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("👑🔥 GOD SPEED exonc ACTIVATED! 5 NC in 0.05s! 🚀")

@only_sudo
async def stopexonc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
        del exonc_tasks[chat_id]
        await update.message.reply_text("🛑 exonc Stopped!")
    else:
        await update.message.reply_text("💢 No active exonc")
        # ---------------------------
# SPAM COMMANDS
@only_sudo
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /spam <text>")
    
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing spam
    if chat_id in spam_tasks:
        for task in spam_tasks[chat_id]:
            task.cancel()
    
    # Start new spam
    tasks = []
    for bot in bots:
        task = asyncio.create_task(spam_loop(bot, chat_id, text))
        tasks.append(task)
    
    spam_tasks[chat_id] = tasks
    await update.message.reply_text("💥 GERRBO PE SPAM STARTED!")

@only_sudo
async def unspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        for task in spam_tasks[chat_id]:
            task.cancel()
        del spam_tasks[chat_id]
        await update.message.reply_text("🛑 Spam Stopped!")
    else:
        await update.message.reply_text("💢 No active spam")

# ---------------------------
# SLIDE COMMANDS
@only_sudo
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slide_targets.add(target_id)
    await update.message.reply_text(f"🎯 IS GREEB KI BHI CHUDAI START: {target_id}")

@only_sudo
async def stopslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slide_targets.discard(target_id)
    await update.message.reply_text(f"🛑 Slide stopped: {target_id}")

@only_sudo
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slidespam_targets.add(target_id)
    await update.message.reply_text(f"💥 IS GREEB KI CHUDAI SLIDE SPAM SE HOGI : {target_id}")

@only_sudo
async def stopslidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slidespam_targets.discard(target_id)
    await update.message.reply_text(f"🛑 Slide spam stopped: {target_id}")

# ---------------------------
# VOICE COMMANDS
@only_sudo
async def animevn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Anime voice with tempest"""
    if len(context.args) < 2:
        return await update.message.reply_text("⚠️ Usage: /animevn <character_numbers> <text>\FIRE DROPmple: /animevn 1 2 3 Hello world")
    
    try:
        # Parse character numbers
        char_numbers = []
        text_parts = []
        
        for arg in context.args:
            if arg.isdigit() and int(arg) in VOICE_CHARACTERS:
                char_numbers.append(int(arg))
            else:
                text_parts.append(arg)
        
        if not char_numbers:
            return await update.message.reply_text("💢 Please provide valid character numbers (1-10)")
        
        text = " ".join(text_parts)
        if not text:
            return await update.message.reply_text("💢 Please provide text to speak")
        
        await update.message.reply_text(f"🍁 Generating voices for characters: {', '.join([VOICE_CHARACTERS[num]['name'] for num in char_numbers])}...")
        
        # Generate voices
        voices = await generate_multiple_voices(text, char_numbers)
        
        if not voices:
            # Fallback to gTTS if tempest fails
            tts = gTTS(text=text, lang='ja', slow=False)
            voice_file = io.BytesIO()
            tts.write_to_fp(voice_file)
            voice_file.seek(0)
            
            character_names = [VOICE_CHARACTERS[num]['name'] for num in char_numbers]
            await update.message.reply_voice(
                voice=voice_file, 
                caption=f"🎀 {' + '.join(character_names)}: {text}"
            )
        else:
            # Send each voice
            for voice in voices:
                await update.message.reply_voice(
                    voice=voice["audio"],
                    caption=f"🎀 {voice['character']}: {text}\n{voice['description']}"
                )
                await asyncio.sleep(1)  # Delay between voices
        
    except Exception as e:
        await update.message.reply_text(f"💢 Voice error: {e}")

@only_sudo
async def tempest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Default tempest voice"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /tempest <text>")
    
    text = " ".join(context.args)
    
    # Use Urokodaki voice as default
    audio_data = await generate_tempest_voice(text, VOICE_CHARACTERS[1]["voice_id"])
    
    if audio_data:
        await update.message.reply_voice(
            voice=audio_data,
            caption=f"🎙️ {VOICE_CHARACTERS[1]['name']}: {text}"
        )
    else:
        # Fallback to gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        voice_file = io.BytesIO()
        tts.write_to_fp(voice_file)
        voice_file.seek(0)
        await update.message.reply_voice(voice=voice_file, caption=f"🗣️ Fallback TTS: {text}")

@only_sudo
async def voices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List available voices"""
    voice_list = "🍁 Available Anime Voices:\n\n"
    for num, voice in VOICE_CHARACTERS.items():
        voice_list += f"{num}. {voice['name']} - {voice['description']}\n"
    
    voice_list += "\n🎀 Usage: /animevn 1 2 3 Hello world"
    await update.message.reply_text(voice_list)

@only_sudo
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /music <song>")
    
    song = " ".join(context.args)
    await update.message.reply_text(f"🎶 Downloading: {song}")

@only_sudo
async def clonevn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a voice message")
    
    await update.message.reply_text("🎤 Voice cloning started...")

@only_sudo
async def clonedvn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /clonedvn <text>")
    
    text = " ".join(context.args)
    await update.message.reply_text(f"🎙️ Speaking in cloned voice: {text}")

# ---------------------------
# REACT COMMANDS
@only_sudo
async def emojispam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /emojispam <emoji>")
    
    emoji = context.args[0]
    chat_id = update.message.chat_id
    
    async def react_loop(bot, chat_id, emoji):
        # Placeholder loop — this bot uses on_message reply behavior instead of reactions
        while True:
            await asyncio.sleep(1)
    
    if chat_id in react_tasks:
        for task in react_tasks[chat_id]:
            task.cancel()
    
    tasks = []
    for bot in bots:
        task = asyncio.create_task(react_loop(bot, chat_id, emoji))
        tasks.append(task)
    
    react_tasks[chat_id] = tasks
    await update.message.reply_text(f"🍁 Auto-reaction: {emoji}")

@only_sudo
async def stopemojispam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in react_tasks:
        for task in react_tasks[chat_id]:
            task.cancel()
        del react_tasks[chat_id]
        await update.message.reply_text("🛑 Reactions Stopped!")
    else:
        await update.message.reply_text("💢 No active reactions")
# ---------------------------
# STICKER SYSTEM (UPDATED)
@only_sudo
async def newsticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Create a sticker from a replied photo:
    - Resize & convert to WEBP 512x512
    - Save file to stickers/<user_id>/
    - Send sticker back to user
    """
    global sticker_mode
    if not sticker_mode:
        return await update.message.reply_text("💢 Sticker system is disabled by owner.")
    
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo with /newsticker")
    
    user_id = update.effective_user.id
    file_id = update.message.reply_to_message.photo[-1].file_id
    try:
        file_obj = await bots[0].get_file(file_id)
        img_bytes = await file_obj.download_as_bytearray()
    except Exception as e:
        return await update.message.reply_text(f"💢 Failed to download photo: {e}")
    
    # Process image -> webp
    try:
        webp_bytes = process_image_to_webp(bytes(img_bytes))
    except Exception as e:
        return await update.message.reply_text(f"💢 Image processing failed: {e}")
    
    # Save to user folder
    folder = ensure_user_folder(user_id)
    index = len(user_stickers.get(str(user_id), [])) + 1
    filename = os.path.join(folder, f"sticker_{index}.webp")
    with open(filename, "wb") as f:
        f.write(webp_bytes)
    
    # Update JSON index
    user_stickers.setdefault(str(user_id), []).append(filename)
    save_stickers()
    
    # Send sticker back
    try:
        await update.message.reply_sticker(sticker=io.BytesIO(webp_bytes))
        await update.message.reply_text("✅ Sticker created and saved!")
    except Exception:
        # fallback: send file
        await update.message.reply_document(document=io.BytesIO(webp_bytes), filename=f"sticker_{index}.webp")
        await update.message.reply_text("✅ Sticker created (sent as file).")

@only_sudo
async def delsticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Delete all saved stickers for the calling user.
    """
    user_id = update.effective_user.id
    key = str(user_id)
    if key in user_stickers:
        # Remove files
        for fp in user_stickers[key]:
            try:
                if os.path.exists(fp):
                    os.remove(fp)
            except:
                pass
        # Remove folder if empty
        try:
            folder = os.path.join("stickers", key)
            if os.path.exists(folder) and not os.listdir(folder):
                os.rmdir(folder)
        except:
            pass
        del user_stickers[key]
        save_stickers()
        await update.message.reply_text("✅ Your stickers deleted!")
    else:
        await update.message.reply_text("💢 No stickers found")

@only_sudo
async def multisticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Create 5 variations from replied photo (different border colors).
    Saves them and sends them as stickers.
    """
    global sticker_mode
    if not sticker_mode:
        return await update.message.reply_text("💢 Sticker system is disabled by owner.")
    
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo with /multisticker")
    
    user_id = update.effective_user.id
    file_id = update.message.reply_to_message.photo[-1].file_id
    try:
        file_obj = await bots[0].get_file(file_id)
        img_bytes = await file_obj.download_as_bytearray()
    except Exception as e:
        return await update.message.reply_text(f"💢 Failed to download photo: {e}")
    
    border_colors = ["#00eaff", "#ff6b6b", "#7dff7d", "#ffd166", "#c084fc"]
    saved_paths = []
    try:
        for i, col in enumerate(border_colors, start=1):
            webp = process_image_to_webp(bytes(img_bytes), border_color=col, border_px=20)
            folder = ensure_user_folder(user_id)
            filename = os.path.join(folder, f"sticker_multi_{int(time.time())}_{i}.webp")
            with open(filename, "wb") as f:
                f.write(webp)
            user_stickers.setdefault(str(user_id), []).append(filename)
            saved_paths.append((filename, webp))
        save_stickers()
    except Exception as e:
        return await update.message.reply_text(f"💢 Failed creating stickers: {e}")
    
    # Send each sticker
    sent = 0
    for fp, webp_bytes in saved_paths:
        try:
            await update.message.reply_sticker(sticker=io.BytesIO(webp_bytes))
            sent += 1
        except Exception:
            await update.message.reply_document(document=io.BytesIO(webp_bytes), filename=os.path.basename(fp))
            sent += 1
        await asyncio.sleep(0.4)
    await update.message.reply_text(f"✅ Created and sent {sent} stickers!")

@only_sudo
async def stickerstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_stickers = sum(len(stickers) for stickers in user_stickers.values())
    await update.message.reply_text(f"📊 Sticker Status: {total_stickers} stickers total")

@only_owner
async def stopstickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sticker_mode
    sticker_mode = False
    await update.message.reply_text("🛑 Stickers disabled")

@only_owner
async def startstickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sticker_mode
    sticker_mode = True
    await update.message.reply_text("✅ Stickers enabled")

# ---------------------------
# STICKER SPAMMER (ADDED)
async def sticker_spam_loop(bot, chat_id, sticker_paths):
    i = 0
    while True:
        try:
            path = sticker_paths[i % len(sticker_paths)]
            # read file and send
            with open(path, "rb") as f:
                await bot.send_sticker(chat_id, sticker=f)
            i += 1
            await asyncio.sleep(sticker_spam_delay)
        except Exception:
            await asyncio.sleep(1)


@only_sudo
async def stickerspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in user_stickers or len(user_stickers[user_id]) == 0:
        return await update.message.reply_text("💢 You have no saved stickers.")

    chat_id = update.message.chat_id
    sticker_list = user_stickers[user_id]

    # Stop old task
    if chat_id in sticker_spam_tasks:
        for t in sticker_spam_tasks[chat_id]:
            t.cancel()

    tasks = []
    for bot in bots:
        task = asyncio.create_task(sticker_spam_loop(bot, chat_id, sticker_list))
        tasks.append(task)

    sticker_spam_tasks[chat_id] = tasks
    await update.message.reply_text(f"🔥 Sticker spam started! ({len(sticker_list)} stickers looping)")


@only_sudo
async def stopstickerspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id in sticker_spam_tasks:
        for t in sticker_spam_tasks[chat_id]:
            t.cancel()
        del sticker_spam_tasks[chat_id]

        await update.message.reply_text("🛑 Sticker spam stopped!")
    else:
        await update.message.reply_text("💢 No sticker spam running.")
# ---------------------------
# CONTROL COMMANDS
@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Stop all tasks
    for chat_tasks in group_tasks.values():
        for task in chat_tasks:
            task.cancel()
    group_tasks.clear()
    
    for chat_tasks in spam_tasks.values():
        for task in chat_tasks:
            task.cancel()
    spam_tasks.clear()
    
    for chat_tasks in react_tasks.values():
        for task in chat_tasks:
            task.cancel()
    react_tasks.clear()
    
    for chat_tasks in exonc_tasks.values():
        for task in chat_tasks:
            task.cancel()
    exonc_tasks.clear()
    
    slide_targets.clear()
    slidespam_targets.clear()
    
    # stop sticker spam too
    for chat_tasks in sticker_spam_tasks.values():
        for task in chat_tasks:
            task.cancel()
    sticker_spam_tasks.clear()
    
    await update.message.reply_text("⏹ ALL ACTIVITIES STOPPED!")

@only_sudo
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args:
        return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    
    try:
        delay = max(0.1, float(context.args[0]))
        await update.message.reply_text(f"✅ Delay set to {delay}s")
    except:
        await update.message.reply_text("💢 Invalid number")

# ---------------------------
# STATUS COMMANDS
@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_text = f"""
📊 FIRE DROP BOTS Status:

🎀 Name Changers: {sum(len(tasks) for tasks in group_tasks.values())}
⚡ exonc Sessions: {sum(len(tasks) for tasks in exonc_tasks.values())}
😹 Spam Sessions: {sum(len(tasks) for tasks in spam_tasks.values())}
🪐 Reactions: {sum(len(tasks) for tasks in react_tasks.values())}
🪼 Slide Targets: {len(slide_targets)}
💥 Slide Spam: {len(slidespam_targets)}

⏱ Delay: {delay}s
⚡ exonc Delay: {exonc_delay}s
🤖 Active Bots: {len(bots)}
👑 SUDO Users: {len(SUDO_USERS)}
🍁 Voice Characters: {len(VOICE_CHARACTERS)}
    """
    await update.message.reply_text(status_text)

# ---------------------------
# SUDO MANAGEMENT
@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user")
    
    uid = update.message.reply_to_message.from_user.id
    SUDO_USERS.add(uid)
    save_sudo()
    await update.message.reply_text(f"✅ SUDO added: {uid}")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user")
    
    uid = update.message.reply_to_message.from_user.id
    if uid in SUDO_USERS:
        SUDO_USERS.remove(uid)
        save_sudo()
        await update.message.reply_text(f"🗑 SUDO removed: {uid}")
    else:
        await update.message.reply_text("💢 User not in SUDO")

@only_sudo
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sudo_list = "\n".join([f"👑 {uid}" for uid in SUDO_USERS])
    await update.message.reply_text(f"👑 SUDO Users:\n{sudo_list}")

# ---------------------------
# AUTO REPLY HANDLER
from telegram.helpers import mention_html

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    name = update.message.from_user.full_name
    mention = mention_html(uid, name)

    # Slide normal mode — mention user
    if uid in slide_targets:
        for text in RAID_TEXTS[:3]:
            await update.message.reply_html(f"{mention} {text}")
            await asyncio.sleep(0.1)

    # Slide spam mode — mention user fast
    if uid in slidespam_targets:
        for text in RAID_TEXTS:
            await update.message.reply_html(f"{mention} {text}")
            await asyncio.sleep(0.05)

# ---------------------------
# BOT SETUP
def build_app(token):
    app = Application.builder().token(token).build()
    
    # Core commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("status", status_cmd))
    
    # Name changer commands
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(CommandHandler("ncemo", ncemo))
    app.add_handler(CommandHandler("ncbaap", ncbaap))
    app.add_handler(CommandHandler("stopgcnc", stopgcnc))
    app.add_handler(CommandHandler("stopncemo", stopncemo))
    app.add_handler(CommandHandler("stopncbaap", stopncbaap))
    app.add_handler(CommandHandler("stopall", stopall))
    app.add_handler(CommandHandler("delay", delay_cmd))
    
    # exonc commands
    app.add_handler(CommandHandler("exonc", exonc))
    app.add_handler(CommandHandler("exoncfast", exoncfast))
    app.add_handler(CommandHandler("exoncgodspeed", exoncgodspeed))
    app.add_handler(CommandHandler("stopexonc", stopexonc))
    
    # Spam commands
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("unspam", unspam))
    
    # React commands
    app.add_handler(CommandHandler("emojispam", emojispam))
    app.add_handler(CommandHandler("stopemojispam", stopemojispam))
    
    # Slide commands
    app.add_handler(CommandHandler("targetslide", targetslide))
    app.add_handler(CommandHandler("stopslide", stopslide))
    app.add_handler(CommandHandler("slidespam", slidespam))
    app.add_handler(CommandHandler("stopslidespam", stopslidespam))
    
    # Sticker commands
    app.add_handler(CommandHandler("newsticker", newsticker))
    app.add_handler(CommandHandler("delsticker", delsticker))
    app.add_handler(CommandHandler("multisticker", multisticker))
    app.add_handler(CommandHandler("stickerstatus", stickerstatus))
    app.add_handler(CommandHandler("stopstickers", stopstickers))
    app.add_handler(CommandHandler("startstickers", startstickers))
    
    # Sticker spam handlers (ADDED)
    app.add_handler(CommandHandler("stickerspam", stickerspam))
    app.add_handler(CommandHandler("stopstickerspam", stopstickerspam))
    
    # Voice commands
    app.add_handler(CommandHandler("animevn", animevn))
    app.add_handler(CommandHandler("tempest", tempest_cmd))
    app.add_handler(CommandHandler("music", music))
    app.add_handler(CommandHandler("clonevn", clonevn))
    app.add_handler(CommandHandler("clonedvn", clonedvn))
    app.add_handler(CommandHandler("voices", voices))
    
    # SUDO management
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("listsudo", listsudo))
    
    # Auto replies
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    
    return app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if not token.strip():
            continue

        # small sanity check — skip obviously malformed tokens to avoid immediate crash
        if ":" not in token or len(token.split(":")[0]) < 5:
            print(f"⚠️ Skipping malformed token: {token[:10]}...")
            continue

        try:
            app = build_app(token)
            apps.append(app)
            # app.bot may not be ready until initialize/start — keep reference after initialize
            bots.append(app.bot)
            print(f"✅ Bot initialized: {token[:10]}...")
        except Exception as e:
            print(f"💢 Failed building app: {e}")

    # Start all bots
    for app in apps:
        try:
            await app.initialize()
            await app.start()
            # PTB v20+ supports run_polling; older versions may have updater
            if hasattr(app, "updater") and getattr(app, "updater") is not None:
                # safe attempt for older APIs
                try:
                    await app.updater.start_polling()
                except Exception:
                    # fallback to run_polling
                    try:
                        await app.run_polling()
                    except Exception as e:
                        print(f"💢 Polling failed: {e}")
            else:
                try:
                    await app.run_polling()
                except Exception as e:
                    print(f"💢 run_polling failed: {e}")
            print(f"🚀 Bot started successfully!")
        except Exception as e:
            print(f"💢 Failed starting app: {e}")

    print(f"🎉 FIRE DROP V4 Ultra Multi is running with {len(bots)} bots!")
    print("📊 Chat ID:", CHAT_ID)
    print("🤖 Active Bots:", len(bots))
    print("💀 NCBAAP Mode: READY (5 NC in 0.1s)")
    print("👑 GOD SPEED Mode: READY (5 NC in 0.05s)")
    print("🍁 tempest Voices: ✅ ACTIVE WITH YOUR API KEY")
    print("⚡ All Features: ACTIVATED")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        print("\n🛑 FIRE DROP V4 Shutting Down...")
    except Exception as e:
        print(f"💢 Error: {e}")
