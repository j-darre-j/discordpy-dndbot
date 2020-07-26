# bot.py
# imports for various discord.py functions and existing python functions
import os
import random
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

# ENV file to securely process discord token information.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!') # defining bot command prefix (ie: "!help")
bot.remove_command('help') # removing default "!help" command

# Role definition for assigning user roles.
init_role = "Aspiring Applicant"
accept_role = "Accepted Applicant"

# Print to console that bot has connected
@bot.event
async def on_ready():
    guild = discord.Guild
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print (f'Bot is connected to the server!')

# When a member joins, display a message then assign a nickname and a role. Also check to ensure message is sent to the correct channel.
@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name = init_role)
    init_embed=discord.Embed(title="Subject: Potential Employment", colour=discord.Colour(0x3DC8FF), description="Hello, this job invitation is the beginning of our correspondance. "
                             "Accepting this message implies that you are accepting employment from Regal Enterprises. Employment is subject to immediate termination if found in violation of company policy. Do you __**!accept**__ or __**!deny**__?")
    init_embed.set_thumbnail(url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    init_embed.set_author(name="From: REGAL ENTERPRISES", icon_url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    init_embed.set_footer(text="All correspondance should be contained to your private computer. Sharing this information will result in termination. "
                          "By reading this disclaimer, you agree to abide by these terms and conditions.", icon_url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    await member.edit(nick ="Nameless Person")
    await member.add_roles(role)
    for channel in member.guild.channels:
        if str(channel) == "incoming-transmission": # Checking message will be in #incoming-transmission      
            await channel.send(embed=init_embed)

# Remade 'help' command, formatted into a nice embed message.
@bot.command(pass_context=True)
async def help(ctx):
        embed = discord.Embed(title="TERMINAL COMMANDS", description="!help will refresh this page.")
        embed.add_field(name="!info", value="Displays this menu.")
        embed.add_field(name="!funfact", value="Displays a funfact from our Great History.")
        embed.add_field(name="!accept", value="Accepts invitations or messages.")
        embed.add_field(name="!deny", value="Denies invitations or messages.")
        embed.add_field(name="!info", value="Lets you pass arguments and I will repeat them to you. (!info arg1 arg2 ...)")
        embed.add_field(name="!purge", value="Deletes all messages in a channel. Please be careful with this.")
        await ctx.send(content=None, embed=embed)
        
# When user types "!accept", print message and change role
@bot.command(pass_context = True)
async def accept(ctx):
    role = get(ctx.guild.roles, name = accept_role)
    role_first = get(ctx.guild.roles, name = init_role)
    user = ctx.message.author
    accept_embed=discord.Embed(title="Subject: Employment Offer", colour=discord.Colour(0x3DC8FF), description = "Welcome to REGAL, recruit. We are very excited to have you join our "
                             "newest branch. A qualified candidate such as yourself should have no problems passing both the physical and psychological evaluations. At your earliest " 
                             "convenience, please head down to the nearest REGAL ENTERPRISES office to have both tests performed. Please be well rested and completely honest with any "
                             "and all questions. Do not hesitate to contact **Mr. XYZ** at __**abc.xyz@regal.ent**__ if you have any questions or concerns.")
    accept_embed.set_author(name="From: REGAL ENTERPRISES", icon_url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    accept_embed.set_thumbnail(url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    accept_embed.set_footer(text="All correspondance should be contained to your private computer. Sharing this information will result in termination."
                          "By reading this disclaimer, you agree to abide by these terms and conditions.", icon_url="https://cblproperty.blob.core.windows.net/production/assets/blt93f46e23c3b4b3d1-Regal_Cinemas_Logo.png")
    await ctx.send(embed=accept_embed)   
    await user.add_roles(role)
    await user.remove_roles(role_first)
    
# If user types "!deny", open DM with user and kick them from the server. Then purge all messages in channel.
@bot.command(pass_context=True)
async def deny(ctx, amount = 500):
    user2 = ctx.message.author # Defines user as the message author
    await user2.create_dm() # Creates DM
    goodbye_embed=discord.Embed(title="From: REGAL ENTERPRISES", description="Subject: Employment Denied", color=0xFF2E3B)
    goodbye_embed.set_footer(text="Regal thanks you for your interest. At your request, you have denied employment. All communications will now cease. Good bye.")
    await user2.send(embed=goodbye_embed)
    await ctx.guild.kick(user2) 
    await ctx.channel.purge(limit = amount) 
    await ctx.send(f'Regal has purged {user2.display_name} from all available records.') # Validate purge and kick was successful (no exception handling)

# Prints a stupid funfact. Made to test embed messages and commands. Chooses a quote at random.
@bot.command(name='funfact')
async def fun_fact(ctx):
    global terminal_quotes
    terminal_quotes = [
        '**// Fun fact: in 2208 Elon Musk\'s corpse was recovered for reproductive purposes.**',
        '**// Popular architect Andres Gil was murdered by a swimmer whose name has been scrubbed from history. Only his spine was found.**',
        '**// In 2033, Forest Ranger Taylor Brown found the first evidence of extraterrestrial life. It was a small meteor embed with a message.**',
        '**// Spaceforce General Brandon Nguyen flew the first aircraft that could leave Earth and return. This was in 2085.**',
        '**// Famous artist Allison Landaker painted the first image of the Aliues, the First Contacts.**',
        '**// Doctor Jeremy Dumdumaya is responsible for the COVID-29 vaccine. He would also go on to create several other vaccines.**',
        '**// Doctor Ian Torrence invented the first artifical skin replacement. This would lead to a breakthrough in cosmetic surgeries.**',
        '**// President of the LDS Church Joshua Purvis was sent on a solo colonization mission after leading LDS church members to their death in an attempt to walk the Pacific Ocean.**',
        '**// Doctor Alyssa McAdams is responsible for the leading CPR technique still used to date. She discovered this by accident while trying to save her partner, Blake.**',
        '**// The 58th President Eric Denoe was the first crippled President.**',
        '**// Aislynn Brown, prestigious esport streamer, beat the world record for time spent streaming continuously at 168 hours.**',

        (
            '**// Fun fact: in 2498, Edison Ind. launched the last rocket from the surface of Earth, '
            'leaving approximately 2.7 million civillians. These civillians would not join the Spacers.**'
        ),
        (
            '**// There was a decorated swimmer and esport professional who, in 2031, swam across every large lake in the United States.'
            ' Unfortunately, he would later go on to miss the game winning Insec at the League of Legends World Championship (season 2033)'
            ', resulting in a 2-3 loss for the first ever North American team to reach the final bracket. North America would never'
            ' reach another finals up until the esport ended in 2040. League of Legends was the United State\'s primary esport.**'
        ),
    ]
    response = random.choice(terminal_quotes)
    await ctx.send(response)
  
# Deletes all messages in a channel.  
@bot.command(pass_context = True)
async def purge(ctx):
    await ctx.channel.purge()
    
# Test command to see how arguments are parsed by the bots.
@bot.command(pass_context=True)
async def info(ctx, *args):
    await ctx.send('{} The information you provided is: {}'.format(len(args), ', '.join(args)))

bot.run(TOKEN)