import discord
from discord.ext import commands
from discord.ui import Button, View, Select

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ------------------------------
# SELECT MENU (KATEGORIE)
# ------------------------------
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Zakup", emoji="🎫", description="Ticket dotyczący zakupu"),
            discord.SelectOption(label="Odbiór nagrody", emoji="🎁", description="Ticket do odebrania nagrody"),
            discord.SelectOption(label="Zgłoszenie problemu", emoji="❓", description="Problem lub błąd"),
            discord.SelectOption(label="Status", emoji="🧧", description="Informacja o statusie"),
            discord.SelectOption(label="Kontakt z Administracją", emoji="📞", description="Kontakt z administracją")
        ]
        super().__init__(placeholder="Wybierz kategorię ticketu...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        guild = interaction.guild
        user = interaction.user

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        channel = await guild.create_text_channel(
            f"ticket-{category.replace(' ', '-').lower()}-{user.name}",
            overwrites=overwrites
        )

        await channel.send(
            f"**Ticket otwarty!**\nKategoria: **{category}**\n\nKliknij poniżej, aby zamknąć ticket:",
            view=CloseButton()
        )

        await interaction.response.send_message(
            f"Ticket utworzony! ➜ {channel.mention}",
            ephemeral=True
        )


# VIEW do menu
class TicketMenu(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# ------------------------------
# PRZYCISK ZAMYKANIA TICKETA
# ------------------------------
class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="🔒 Zamknij ticket", style=discord.ButtonStyle.red, custom_id="close_ticket"))


@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")


# ------------------------------
# KOMENDA DO WYSŁANIA PANELU
# ------------------------------
@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="🎟️ System Ticketów",
        description="Wybierz kategorię ticketu z menu poniżej.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketMenu())


# ------------------------------
# OBSŁUGA PRZYCISKÓW
# ------------------------------
@bot.event
async def on_interaction(interaction):
    if interaction.data.get("custom_id") == "close_ticket":
        await interaction.response.send_message("Zamykanie ticketu...", ephemeral=True)
        await interaction.channel.delete()


# ------------------------------
# START BOTA
# ------------------------------
bot.run("MTQ0NTA4NzY0OTIyMzQxMzk0Mg.GY5Wna.0U-KeZGKMYw0JhoQqZDX8sPEd-10yxSbFB6AY8")
