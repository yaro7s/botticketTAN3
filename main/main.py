import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="🎟️ Créez un Ticket de Support",
        description=(
            "Tu rencontres un problème, tu as une question ou besoin d’un membre du staff ?\n"
            "Ouvre un ticket en cliquant sur le bouton ci-dessous. Un salon privé sera créé où tu pourras discuter directement avec l’équipe.\n"
            "Merci de bien expliquer ta demande dès le début pour qu’on puisse t’aider le plus vite possible ✅"
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/950038001491275786/1363987096519315506/image.png?ex=68080779&is=6806b5f9&hm=4d9d5a782bd9884701683b3f83d9ee723db4d952383bfee8ef6a54fe717384d0&")

    button = Button(label="Ouvrir un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component and interaction.data['custom_id'] == 'open_ticket':
        guild = interaction.guild
        member = interaction.user

        ticket_channel = await guild.create_text_channel(
            f"ticket-{member.name}",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True),
            }
        )

        embed_ticket = discord.Embed(
            title="Votre Ticket",
            description=f"Salut {member.mention}, voici ton ticket ! Un membre du staff va venir t'aider sous peu.",
            color=discord.Color.green()
        )

        close_button = Button(label="Fermer le Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
        view = View()
        view.add_item(close_button)

        await ticket_channel.send(embed=embed_ticket, view=view)
        await interaction.response.send_message(f"Ton ticket a été créé ici: {ticket_channel.mention}", ephemeral=True)

    elif interaction.type == discord.InteractionType.component and interaction.data['custom_id'] == 'close_ticket':
        channel = interaction.channel
        await channel.delete()
        await interaction.response.send_message("Le ticket a été fermé.", ephemeral=True)

# Garde le bot en ligne grâce à Flask + UptimeRobot
keep_alive()

# Remplace TON_TOKEN_ICI par ton token
bot.run("TON_TOKEN_ICI")
