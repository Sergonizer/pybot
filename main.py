import discord
import asyncio
import datetime
import random
import requests
import json
import config
from discord.ext import commands

from discord.ext import tasks
from discord.ext.commands import has_permissions
from discord.utils import get
from random import randint

from discord.ext.commands import has_permissions, MissingPermissions
import decimal
from decimal import Decimal


intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=['ñ?', 'Ñ?', 'fn?'], intents=intents, help_command=None, case_insensitive=True)
vc = bot.get_channel(884408053980614696)

"""
@tasks.loop(minutes=5)
async def mytask():
    global vc
    editvc = bot.get_channel(907970607575076926)
    #memvc = bot.get_channel(884481831792169041)
    max = 0
    for channel in editvc.guild.channels:
        if str(channel.type).lower() == "voice" and channel.id != 907970607575076926:
            if len(channel.members) > max:
                vc = channel
                max = len(channel.members)
    if max == 0:
        vc = bot.get_channel(884408053980614696)
    rec = f"({max}🗣️) {vc.name} (click)"
    if rec != editvc.name:
        await editvc.edit(name=rec)
    #player = 0
    #nonbots = 0
    #for memb in memvc.guild.members:
    #    if not memb.bot:
    #        nonbots += 1
    #    for activ in memb.activities:
    #        if activ.name:
    #            if activ.name.lower() == "geometry dash":
    #                player += 1
    #count = f"{player}/{nonbots} playing gd"
    #if count != memvc.name:
    #    await memvc.edit(name=count)
"""

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    dms = await bot.get_user(341846440760573955).create_dm()
    await dms.send("Ñ in da chat")
    mytask.start()

async def send_notify_reply(content, original_message, delay=10):
    reply = await original_message.reply(content)
    await asyncio.sleep(delay)
    await reply.delete()
    await original_message.delete()

@bot.event
async def on_message(message):
    prohibited_list = ["your mother so. hot I hhh im omg god holy fuck AAA mmrhfhj"]

    if message.channel.id == 884196890407731212 and not message.author.guild_permissions.manage_messages:
        allowed_platform = ["twitch.tv", "youtube.com/clip"]

        if not any([platform in message.content for platform in allowed_platform]):
            await message.delete()
 
    if any([text in message.content for text in prohibited_list]):
        await message.delete()

    if message.channel.category_id == 899473682353758269:
        await message.delete()
            
    if message.content.lower().startswith("dead chat, wake up") and message.author.guild_permissions.mention_everyone:
        await message.reply("Alright man, @everyone", mention_author=False)
    
    if message.author.id == 323630372531470346 and "beat 3sh" in message.content:
        await message.reply("gg")

    if "this is my easy" in message.content.lower():
        if message.author.id == 669383539875381258:
            await message.reply("No it's not, this is your max", mention_author=True)
        else:
            await message.reply("You're not kehni", mention_author=True)

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    global vc
    sendfl = 0
    emb = discord.Embed()
    emb2 = discord.Embed()
    vclog = bot.get_channel(911567672083357696)
    hislog = bot.get_channel(937100830316855356)
    if vc == None:
        vc = bot.get_channel(884408053980614696)
    
    line = ""
    if (before.channel in vclog.guild.channels or not before.channel) and (after.channel in vclog.guild.channels or not after.channel):
        state = ""
        if after.self_mute or after.mute:
            state = " (muted)"
        if after.self_deaf or after.deaf:
            state = " (deaf)"
    
        emb.set_author(name=f"{member.name}#{member.discriminator}", url="https://youtube.com/c/Sergonizer", icon_url=member.avatar_url)

        if before.channel == after.channel:
            if before.self_mute and not after.self_mute:
                sendfl = 1
                line = (line + f"Unmuted")
            elif not before.self_mute and after.self_mute:
                sendfl = 1
                line = (line + f"Muted")
            elif before.self_deaf and not after.self_deaf:
                sendfl = 1
                line = (line + f"Undeafened")
            elif not before.self_deaf and after.self_deaf:
                sendfl = 1
                line = (line + f"Deafened")
            elif before.mute and not after.mute:
                sendfl = 1
                line = (line + f"Was unmuted")
            elif not before.mute and after.mute:
                sendfl = 1
                line = (line + f"Was muted")
            elif before.deaf and not after.deaf:
                sendfl = 1
                line = (line + f"Was undeafened")
            elif not before.deaf and after.deaf:
                sendfl = 1
                line = (line + f"Was deafened")
            elif not before.self_stream and after.self_stream:
                sendfl = 1
                line = (line + f"Started streaming")
            elif before.self_stream and not after.self_stream:
                sendfl = 1
                line = (line + f"Stopped streaming")
            elif not before.self_video and after.self_video:
                sendfl = 1
                line = (line + f"Turned on camera")
            elif before.self_video and not after.self_video:
                sendfl = 1
                line = (line + f"Turned off camera")
                
        elif after.afk:
            sendfl = 1
            line = (line + f"Was moved to afk channel {after.channel.mention}")
        elif (before.channel == None or before.channel.id == 907970607575076926) and after.channel != None and after.channel.id != 907970607575076926:
            sendfl = 1
            line = (line + f"Joined {after.channel.mention}{state}")
        elif before.channel != None and before.channel.id != 907970607575076926 and (after.channel == None or after.channel.id == 907970607575076926):
            sendfl = 1
            line = (line + f"Left {before.channel.mention}")
        elif before.channel != None and after.channel != None:
            sendfl = 1
            line = (line + f"Moved from {before.channel.mention} to {after.channel.mention}{state}")
        
        line2 = ""
        if sendfl:
            if before.channel != after.channel:
                if before.channel and before.channel.id != 907970607575076926:
                    if len(before.channel.members) == 1: line2 = line2 + "1 member left"
                    else: line2 = line2 + f"{len(before.channel.members)} members left"
                    if after.channel and after.channel.id != 907970607575076926:
                        line2 = line2 + ", "
                if after.channel and after.channel.id != 907970607575076926:
                    if len(after.channel.members) == 1: line2 = line2 + "1 member now"
                    else: line2 = line2 + f"{len(after.channel.members)} members now"
                emb.set_footer(text=line2)
            emb.description = line
            emb.colour = member.colour

            beflist = aftlist = []

            if ("left" in line2 or "," in line2) and len(before.channel.members) > 0:
                for mem in before.channel.members:
                    mmstate = mem.voice
                    state = ""
                    if mmstate.self_mute or mmstate.mute:
                        state = " (muted)"
                    if mmstate.self_deaf or mmstate.deaf:
                        state = " (deaf)"
                    beflist.append(mem.mention + f"{state}")
                if len(beflist) > 0: 
                    emb2.add_field(name = f"Members in {before.channel.name}:", value = "\n".join(beflist))
               

            if ("now" in line2 or "," in line2) and len(after.channel.members) > 0:
                for mem in after.channel.members:
                    mmstate = mem.voice
                    state = ""
                    if mmstate.self_mute or mmstate.mute:
                        state = " (muted)"
                    if mmstate.self_deaf or mmstate.deaf:
                        state = " (deaf)"
                    aftlist.append(mem.mention + f"{state}")
                if len(aftlist) > 0:
                    emb2.add_field(name = f"Members in {after.channel.name}:", value = "\n".join(aftlist))

            emb.timestamp = emb2.timestamp = datetime.datetime.now()
            if len(beflist) + len(aftlist) > 0: 
                msg = await hislog.send(embed = emb2)
                emb.title = "Members list"
                emb.url = msg.jump_url
            await vclog.send(embed = emb)


    if after.channel != None:
        if after.channel.id == 907970607575076926:
            if vc.permissions_for(member).connect:
                await member.move_to(vc)
            else:
                await member.move_to(None)
                dms = await member.create_dm()
                await dms.send(f"You have no perms to join {vc.name}!")
    
@bot.event
async def on_raw_reaction_add(payload):
    relog = bot.get_channel(935670107785543781)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.guild_id == relog.guild.id:
        member = payload.member
        
        emb = discord.Embed()
        emb.description = f"[Message Link]({message.jump_url})"
        emb.title = f"Added reaction {payload.emoji}"
        emb.timestamp = datetime.datetime.now()
        emb.set_author(name=f"{member.name}#{member.discriminator}", url="https://youtube.com/c/Sergonizer", icon_url=member.avatar_url)
        emb.colour = member.colour
        await relog.send(embed = emb)

@bot.event
async def on_raw_reaction_remove(payload):
    relog = bot.get_channel(935670107785543781)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.guild_id == relog.guild.id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        emb = discord.Embed()
        emb.description = f"[Message Link]({message.jump_url})"
        emb.title = f"Removed reaction {payload.emoji}"
        
        emb.timestamp = datetime.datetime.now()
        emb.set_author(name=f"{member.name}#{member.discriminator}", url="https://youtube.com/c/Sergonizer", icon_url=member.avatar_url)
        emb.colour = member.colour
        await relog.send(embed = emb)

@bot.command(pass_context=True, aliases=['?'])
async def ñ(ctx):
    await ctx.send("ñ")

@bot.command(pass_context=True, aliases=['??'])
async def perms(ctx, permission):
    if not(permission.lower() in dir(ctx.message.author.guild_permissions)):
        await ctx.send("There is no perm like this...")
    else:
        memlist = []
        for member in ctx.guild.members:
            if eval("member.guild_permissions." + str(permission).lower()):
                if not member.bot:
                    if member.guild_permissions.administrator:
                        memlist.insert(0, "(Admin) " + member.display_name)
                    else:
                        memlist.append(member.display_name)
                else:
                    if member.guild_permissions.administrator:
                        memlist.insert(0, "[Bot] (Admin) " + member.display_name)
                    else:
                        memlist.append("[Bot] " + member.display_name)
        if len(", ".join(memlist)) > 2000:
            await ctx.send("Lots of members (" + str(len(memlist)) + ") have this perm!")
        elif len(memlist) < 1:
            await ctx.send("Bru, no one has this perm.")
        else:
            await ctx.send(embed=discord.Embed(title=f"List of members with {permission.upper()} perm ({len(memlist)} of them):", description="\n".join(memlist)))
           
@bot.command(pass_context=True, aliases=['???'])
async def chanperms(ctx, permission, pass_id):
    permchan = -1
    if not(permission.lower() in dir(ctx.message.author.guild_permissions)):
        await ctx.send("There is no perm like this...")
    else:
        for chan in ctx.message.guild.channels:
            if chan.id == int(pass_id):
                permchan = chan
        if permchan == -1:
            await ctx.send("Bruh, the channel does not exist")
        else:
            memlist = []
            for member in ctx.guild.members:
                if getattr(permchan.permissions_for(member), permission.lower()):
                    if not member.bot:
                        if member.guild_permissions.administrator:
                            memlist.insert(0, "(Admin) " + member.display_name)
                        else:
                            memlist.append(member.display_name)
                    else:
                        if member.guild_permissions.administrator:
                            memlist.insert(0, "[Bot] (Admin)" + member.display_name)
                        else:
                            memlist.append("[Bot] " + member.display_name)
            if len(", ".join(memlist)) > 2000:
                await ctx.send("Lots of members (" + str(len(memlist)) + ") have this perm!")
            elif len(memlist) < 1:
                await ctx.send("Bru, no one has this perm.")
            else:
                await ctx.send(embed=discord.Embed(title=f"List of members with {permission.upper()} perm in #{permchan.name} ({len(memlist)} of them):", description="\n".join(memlist)))
           
@bot.command(pass_context=True)
async def chanroleperms(ctx, permission, pass_id):
    permchan = -1
    if not(permission.lower() in dir(ctx.message.author.guild_permissions)):
        await ctx.send("There is no perm like this...")
    else:
        for chan in ctx.message.guild.channels:
            if chan.id == int(pass_id):
                permchan = chan
        if permchan == -1:
            await ctx.send("Bruh, the channel does not exist")
        else:
            rolelist = []
            for role in ctx.guild.roles:
                if getattr(permchan.overwrites_for(role), permission.lower()) is True or (getattr(permchan.overwrites_for(role), permission.lower()) is None and getattr(permchan.overwrites_for(ctx.guild.default_role), permission.lower()) is True) or (getattr(permchan.overwrites_for(role), permission.lower()) is None and getattr(permchan.overwrites_for(ctx.guild.default_role), permission.lower()) is None and getattr (role.permissions, permission.lower()) is True):
                    if role.permissions.administrator:
                        rolelist.insert(0, "(Admin) " + role.name)
                    else:
                        rolelist.append(role.name)
            if len(", ".join(rolelist)) > 2000:
                await ctx.send("Lots of roles (" + str(len(rolelist)) + ") have this perm!")
            elif len(rolelist) < 1:
                await ctx.send("Bru, no roles have this perm.")
            else:
                await ctx.send(embed=discord.Embed(title=f"List of roles with {permission.upper()} perm in #{permchan.name} ({len(rolelist)} of them):", description="\n".join(rolelist)))
           
@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member, *, reason = "existing"):
    if ctx.message.author.guild_permissions.ban_members:
        if ctx.message.author.id != member.id:
            await ctx.send("{0.mention} was banned from \"**{1}**\". Reason: {2}.".format(member, ctx.guild, reason))
        else:
            await ctx.send("{0.mention}, you can't ban yourself dude (but I can ping you if you wish)".format(member))
    else:
        await ctx.send("You have no permission to do that")

@bot.command(pass_context=True)
async def hate(ctx, member: discord.Member, *, reason = "existing"):
    if ctx.message.author.guild_permissions.ban_members:
        await ctx.send("Hating {0.mention}. Reason: {1}.".format(member, reason))

@bot.command(pass_context=True)
async def rolemems(ctx, *, rolename):
    role = -1
    flag = 0
    for checkrole in ctx.message.guild.roles:
        if checkrole.name.lower().startswith(rolename.lower()):
            if role == -1 or checkrole.name.lower() == rolename.lower():
                role = checkrole
                if checkrole.name.lower() == rolename.lower():
                    break
            else:
                flag = 1
                break
    if flag:
        await ctx.send("Specify the role name plz")
    elif not role:
        await ctx.send("No role exist with this name, typo probably?")
    else:
        memlist = []
        for memb in ctx.message.guild.members:
            if role in memb.roles:
                if memb.guild_permissions.administrator:
                    memlist.insert(0, "(Admin) " + memb.display_name)
                else:
                    memlist.append(memb.display_name)
        if len(", ".join(memlist)) > 2000:
            await ctx.send("Lots of members (" + str(len(memlist)) + ") have this role!")
        elif len(memlist) < 1:
            await ctx.send("Bru, no one has this role.")
        else:
            await ctx.send(embed=discord.Embed(title=f"List of members with {role.name} role ({len(memlist)} of them):", description="\n".join(memlist)))

@bot.command(pass_context=True)    
async def ex(ctx, *, comm):
    if ctx.author.id == 341846440760573955:
        comm = comm.replace('`','').split('\n')
        comm = '\n'.join([*map(lambda x: '\t\t'+x, comm)])
        fcode = f"""
import discord
import math
import asyncio
import datetime
import requests
import json
import random
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import has_permissions
from discord.utils import get
from random import randint

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=['ñ?', 'Ñ?', 'fn?'], intents=intents, help_command=None, case_insensitive=True)

async def inline():
{comm}


try:
    loop.create_task(inline())
except Exception as e:
    loop.create_task(ctx.send(e))
"""
        try:
            exec(fcode, {'ctx': ctx, 'loop': asyncio.get_running_loop()})
        except Exception as e:
            code = []
            dms = await bot.get_user(341846440760573955).create_dm()
            emb = discord.Embed(title = "Exception!", description = e)
            await dms.send(embed = emb)
            excode = fcode.split('\n')
            i = 1
            for line in excode:
                line = (str(i) + '.').ljust(4) + "\t" + line
                i += 1
                code.append(line)
            code = '\n'.join(code)
            await dms.send(code)
              
@bot.command(pass_context=True)
async def rng(ctx, a1, b1, step1=1.0):
    a = float(a1)
    b = float(b1)
    step = float(step1)
    await ctx.send(round((random.randint(a, b-1) + random.random())/step)*step)
      
@bot.command(pass_context=True)
@commands.has_permissions(manage_guild=True)
async def addinfo(ctx, msgid, *, addition):
    addition = addition.replace('`','')
    msg = await ctx.channel.fetch_message(msgid)
    emb = msg.embeds[0]
    if emb.description:
        emb.description = emb.description + addition
    else:
        emb.description = addition
    await msg.edit(embed = emb)

@bot.command(pass_context=True)
@commands.has_permissions(add_reactions=True)
async def ratio(ctx):
    msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    await msg.add_reaction("🇷")
    await msg.add_reaction("🇦")
    await msg.add_reaction("🇹")
    await msg.add_reaction("🇮")
    await msg.add_reaction("🇴")

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def randreact(ctx, msgid):
    reactioners = []
    msg = await ctx.channel.fetch_message(msgid)
    for reaction in msg.reactions:
        async for user in reaction.users():
            if not (user in reactioners):
                reactioners.append(user)
    await ctx.send("{0.mention} has been chosen by random, congrats!".format(reactioners[randint(0, len(reactioners) - 1)]))

async def checkreact(ctx, mesgid, num, price):
    numb = int(num)
    msg = await ctx.channel.fetch_message(mesgid)
    reactioners = []
    for reaction in msg.reactions:
        async for user in reaction.users():
            if not (user in reactioners) and not user.bot:
                reactioners.append(user)
    if numb > len(reactioners):
        numb = len(reactioners)
    emb = discord.Embed()
    emb.colour = ctx.author.colour
    emb.title = "Giveaway finished!"
    winners = []
    for i in range(numb):
        r = randint(0, len(reactioners) - 1)
        winners.append(f"{reactioners[r].mention}")
        reactioners.pop(r)
    emb.add_field(name = f"Winners of {price}:", value = "\n".join(winners))
    emb.set_footer(text = "Giveaway comm created by Sergonizer#2120", icon_url = "https://cdn.discordapp.com/avatars/341846440760573955/36e17daf3756292fe17de192c73a4214.webp?size=1024")
    await ctx.send(embed=emb)
    await ctx.send(f"{ctx.author.mention}")


#@bot.command(pass_context=True)
#@commands.has_permissions(kick_members=True)
async def giveaway(ctx, time, numb, price = "500xp"):
    emb = discord.Embed()
    if float(time) > 10080:
        emb = discord.Embed()
        emb.colour = ctx.author.colour
        emb.title = "Wrong time range!"
        emb.description = "You can't set the time range over 1 week!"
        emb.set_footer(text = "Giveaway comm created by Sergonizer#2120", icon_url = "https://cdn.discordapp.com/avatars/341846440760573955/36e17daf3756292fe17de192c73a4214.webp?size=1024")
        await ctx.send(embed=emb)
    elif float(time) < 1:
        emb = discord.Embed()
        emb.colour = 0xFF0000
        emb.title = "Wrong time range!"
        emb.description = "You can't set the time range less than 1 minute!"
        emb.set_footer(text = "Giveaway comm created by Sergonizer#2120", icon_url = "https://cdn.discordapp.com/avatars/341846440760573955/36e17daf3756292fe17de192c73a4214.webp?size=1024")
        await ctx.send(embed=emb)
    else:
        #await ctx.send("{0.mention}".format(get(ctx.guild.roles, id=904483840360349726)))
        emb.colour = 0x00FFFF
        emb.title = "Giveaway!"
        if float(time) == 1.0:
            emb.description = f"{ctx.author} decided to make a giveaway of {price} with {numb} winners, it's your time! (actually your time is 1 minute)"
        else:
            emb.description = f"{ctx.author} decided to make a giveaway of {price} with {numb} winners, it's your time! (actually your time is {time} minutes)"
        emb.add_field(name = "Some info:", value = "If we don't reach enough reactions, everyone will become winners!")
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.thumbnail.url = "https://freepikpsd.com/file/2019/10/clock-emoji-png-1-Transparent-Images-Free.png"
        emb.set_footer(text = "Giveaway comm created by Sergonizer#2120", icon_url = "https://cdn.discordapp.com/avatars/341846440760573955/36e17daf3756292fe17de192c73a4214.webp?size=1024")
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("✅")
        await asyncio.sleep(int(float(time) * 60))
        await checkreact(ctx, msg.id, numb, price)

bot.run(config.token)
