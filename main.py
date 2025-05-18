import discord #importações do bot
from discord.ext import commands
from discord import app_commands
from humanfriendly import parse_timespan, InvalidTimespan
from typing import Optional
from datetime import timedelta
from discord.ui import Modal, TextInput
from discord import TextStyle



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.' , intents=intents)

def is_owner(interaction: discord.Integration) ->bool:
    return interaction.user.id == 1218039180341411910


class TicketModal(Modal):
    def __init__(self):
        super().__init__(title="Abrir ticket")

    titulo = TextInput(label="Resuma o seu ticket")
    descricao = TextInput(label="Descreva melhor o seu ticket",
    style=TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
       categoria_ticket = discord.utils.get(interaction.guild.categories, id=1305545865896792084)
       ticket_canal = await interaction.guild.create_text_channel(f"TICKET {interaction.user.name}", category=categoria_ticket)
       await ticket_canal.set_permissions(interaction.user, view_channel=True)
       await ticket_canal.send(f"Ticket de {interaction.user.mention}\n## {self.titulo}\n{self.descricao}")
       embed = discord.Embed(title="✅ Ticket criado. ✅", description=f"Seu ticket foi criado em {ticket_canal}", color=0x00ff00)
       await interaction.response.send_message(embed=embed)


@bot.event #definimos um evento
async def on_ready():
    activity = discord.Game(name="Call of Duty:Black Ops 6", type=3)
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print('Pronto para uso')
    print(bot.user)
    print(f"Ping: {round (bot.latency * 1000)}")
    await bot.tree.sync()
   
    




@bot.tree.command(description="Expulsar um membro.")
@app_commands.describe(member="Membro expulso do server.")
@app_commands.describe(reason="Motivo pela expulsão.")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
    await member.kick(reason=reason)
    embed = discord.Embed(title="👟💥🏃‍♂️ Kickado!", description=f"{member.mention} Você foi Kickado por {reason}", color=0xff0000)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description="Banir um membro.")
@app_commands.describe(member="Membro banido do server.")
@app_commands.describe(reason="Motivo pelo banimento.")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨🚫 Banido!", description=f"{member.mention} Você foi Banido por {reason}",color=0xff0000)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(description="Mutar membros do server.")
@app_commands.describe(member="Membro mutado do server.")
@app_commands.describe(reason="Motivo pelo mute.")
@app_commands.describe(duration="Duração do mute.")
@commands.has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: Optional[str], duration: Optional[str] ="14d"):
    try:
        duration = parse_timespan(duration)
    except InvalidTimespan:
        return await interaction.response.send_message(f"{duration} não é um tempo válido. (5s, 5m, 5h, 5d)")
    await member.timeout(timedelta(seconds=duration), reason=reason)
    embed = discord.Embed(title="🔇🚫 Mutado!", description=f"{member.mention} Você foi Castigado por {reason}",color=0xff0000)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(description="Desmutar membros do server.")
@app_commands.describe(member="Membro desmutado do server.")
@app_commands.describe(reason="Motivo pelo desmute.")
async def unmute(interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
    if not member.is_timed_out():
        embed = discord.Embed(title="🔊✅ Desmutado!", description=f"{member.mention} Você foi tirado do Castigo por {reason}",color=0x00ff00)
        return await interaction.response.send_message(embed=embed)
    await member.timeout(None, reason=reason)
    embed = discord.Embed(title="🔊✅ Desmutado!", description=f"{member.mention} Você foi tirado do Castigo por {reason}",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Apagar mensagens")
@app_commands.describe(amount="Quantidade de mensagens que deseja apagar")
@app_commands.describe(reason="Motivo por apagar as mensagens")
async def purge(interaction: discord.Interaction, amount: int, reason: Optional[str]):
    if amount > 100:
        embed = discord.Embed(
            title="Você mencionou!",
            description=f"{amount}\n  \n Por favor, insira um número abaixo de 100!",
            color=0xff0000
        )
        return await interaction.response.send_message(embed=embed)

    # Deferindo a resposta para evitar o erro de tempo
    await interaction.response.defer()

    # Apagando as mensagens
    deleted = await interaction.channel.purge(limit=amount, reason=reason)

    # Respondendo após a exclusão
    await interaction.followup.send(f"{len(deleted)} mensagens foram apagadas por {reason or 'nenhuma razão especificada'}")








 
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int, *, reason="Bem-Vindo de Volta!"):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(title="✅ **Desbanido com Sucesso!** ✅", description=f"{user.mention} Você foi Desbanido!.", color=0x00ff00)
        await ctx.send(embed=embed)
    except discord.NotFound:
        embed = discord.Embed(title="Erro", description=f"Usuário com ID {user_id} Não Encontrado.", color=0x00ff00)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Erro", description="Você Não Permissãos para Desbanir este Usuário.", color=0x00ff00)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Erro", description=str(e), color=0x00ff00)
        await ctx.send(embed=embed)


@bot.tree.command(description="Ver donos do servidor")
async def donos(interaction : discord.Interaction):
    embed = discord.Embed(title="Donos do Servidor\n \n \n", description= "\n \n \n👑Founder GBL👑\n \n🎩Owner Leozera🎩\n \n🎩Owner Tuta🎩\n  \n🎩Owner Paulo🎩", color=0x00ff00)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description="Status do server")
async def server(interaction: discord.Interaction):
    embed = discord.Embed(title="****Cargos do Servidor****", description="\n \n👑Founder GBL👑\n \n🎩Owner Leozera🎩\n \n🎩Owner Tuta🎩\n  \n🎩Owner Paulo🎩 \n \n \n  ****Supreme do Servidor**** \n \n 🃏KelLyall🃏 \n \n \n ****Master do Servidor****\n \n 🕵MIBR Motz. ᵀᴴᴱ ᴳᴼᴬᵀ🕵\n \n \n ****Adm do Servidor**** \n \n 🗿gabriel - droop🗿\n \n \n ****V1p do Servidor**** \n \n 💎CRN 0 elthonbragga💎", color=0x00ff00 )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description="Regras do Servidor")
async def regras(interaction: discord.Interaction):
    embed = discord.Embed(title="❗Siga nossas Regras❗\n \n ", description="\n \n https://discord.com/channels/1218039180341411910/1304001845378682890",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Anuncios de Jogos Grátis")
async def jogos(interaction: discord.Interaction):
    embed = discord.Embed(title=" 🎮 Anúncios de Jogos Grátis 🎮 \n \n ", description= "https://discord.com/channels/1218039180341411910/1304394564458774578",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Anuncios de Eventos")
async def even(interaction: discord.Interaction):
    embed = discord.Embed(title="🎊 Anúncios de Eventos 🎊\n \n ", description= "https://discord.com/channels/1218039180341411910/1304367806497947670",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Avisos")
async def avs(interaction: discord.Interaction):
    embed = discord.Embed(title="📅 Fique por Dentro dos Avisos 📅\n \n ", description= "https://discord.com/channels/1218039180341411910/1304236483141697636",color=0x00ff00)
    await interaction.response.send_message(embed=embed)
        
@bot.tree.command(description="Anúncios")
async def anun(interaction: discord.Interaction):
    embed = discord.Embed(title="📣 Fique por Dentro dos Anúncios 📣\n \n ", description= "https://discord.com/channels/1218039180341411910/1304225841932406854",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Chat de banidos")
async def banidos(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Relatório dos Banidos 📋\n \n ", description= "https://discord.com/channels/1218039180341411910/1304235763214323712",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Chat sala Adm")
async def salaadm(interaction: discord.Interaction):
    embed = discord.Embed(title="💡 Sugestôes Sobre Adm do Server 💡\n \n ", description= "https://discord.com/channels/1218039180341411910/1304223761272148120",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Chat-Geral")
async def chat(interaction: discord.Interaction):
    embed = discord.Embed(title="😁 Participe do Nosso Chat-Geral 😁\n \n ", description= "https://discord.com/channels/1218039180341411910/1304006005104836689",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Chat da sala Zoeira")
async def zoeira(interaction: discord.Interaction):
    embed = discord.Embed(title="🤣 Gastação sem Limites 🤣\n \n ", description= "https://discord.com/channels/1218039180341411910/1218039180341411913",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Novidades do Cs2")
async def cs2(interaction: discord.Interaction):
    embed = discord.Embed(title="✅ Atualizações CS2 ✅\n \n ", description= "https://discord.com/channels/1218039180341411910/1304539000190533743",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Novidades do Fortnite")
async def fort(interaction: discord.Interaction):
    embed = discord.Embed(title="✅ Atualizações Fortnite ✅\n \n ", description= "https://discord.com/channels/1218039180341411910/1304539030804893729",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Novidades do Valorant")
async def val(interaction: discord.Interaction):
    embed = discord.Embed(title="✅ Atualizações Valorant ✅\n \n ", description= "https://discord.com/channels/1218039180341411910/1304539052426395750",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Novidades do Warzone")
async def cod(interaction: discord.Interaction):
    embed = discord.Embed(title="✅ Atualizações Warzone✅\n \n ", description= "https://discord.com/channels/1218039180341411910/1304539072554860616",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Cfg dos Pros cs2")
async def cfgcs2(interaction: discord.Interaction):
    embed = discord.Embed(title="🧑‍💻 Configurações dos Proplayers CS2 🧑‍💻\n \n ", description= "https://discord.com/channels/1218039180341411910/1303989296755113984",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Cfg dos Pros Fortnite")
async def cfgfort(interaction: discord.Interaction):
    embed = discord.Embed(title="🧑‍💻 Configurações dos Proplayers Fortnite🧑‍💻\n \n ", description= "https://discord.com/channels/1218039180341411910/1304537917347069982",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Cfg dos Pros Valorant")
async def cfgval(interaction: discord.Interaction):
    embed = discord.Embed(title="🧑‍💻 Configurações dos Proplayers Valorant🧑‍💻\n \n ", description= "https://discord.com/channels/1218039180341411910/1304537999211630652",color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Cfg dos Pro Warzone")
async def cfgcod(interaction: discord.Interaction):
    embed = discord.Embed(title="🧑‍💻 Configurações dos Proplayers Warzone🧑‍💻\n \n ", description= "https://discord.com/channels/1218039180341411910/1304538039950901339",color=0x00ff00)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(description="Abrir ticket")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_modal(TicketModal())




@bot.tree.command(description="Fechar ticket")
async def fechar_ticket(interaction: discord.Interaction):
    categoria_ticket = discord.utils.get(interaction.guild.categories, id=1305545865896792084)
    if categoria_ticket != interaction.channel.category:
        embed = discord.Embed(title="❌ Erro. ❌", description=f"Você só pode usar este comando em um ticket.", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return
    everyone= interaction.guild.default_role
    await interaction.channel.set_permissions(everyone, send_messages=False)
    embed = discord.Embed(title="✅ Ticket Fechado. ✅", description=f"Ticket fechado com sucesso!.", color=0x00ff00)
    await interaction.response.send_message(embed=embed)



bot.run("MTMwNDYxNDQzNDgzNjMyMDMzOA.GWMvZd.ghFvrB76ysOpMwI7QFlifahxaJYHOKcA-Z-UGg")





        

    