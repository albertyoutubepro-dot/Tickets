import discord
from discord.ext import commands
from discord import app_commands
import logging
from utils.helpers import utc_to_gmt
from utils.database import user_has_support_role
import time
from datetime import datetime, timezone

logger = logging.getLogger('discord')

class HelpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.hybrid_command(name="help", description="Display help information and available commands.")
    async def help_command(self, ctx: commands.Context):
        invoker = ctx.author if isinstance(ctx, commands.Context) else ctx.user
        logger.info(f"Help command invoked by {invoker}")
        try:
            is_interaction = isinstance(ctx, discord.Interaction)

            if is_interaction and not ctx.response.is_done():
                await ctx.response.defer(ephemeral=True)

            current_time = datetime.now(timezone.utc)

            embed = discord.Embed(
                title="❓ Support Bot Help Center",
                description=f"Welcome to {self.bot.user.name} - your  support system! Select a category below to get detailed information about features and commands.",
                color=0x00D4FF,
                timestamp=current_time
            )

            embed.add_field(
                name="🔧 Need Setup Help?",
                value="Select 'Setup Guide' from the dropdown for a complete walkthrough of configuring your support system.",
                inline=False
            )

            embed.add_field(
                name="🎫 Managing Tickets?",
                value="Choose 'Ticket Commands' to learn about all ticket management features and commands.",
                inline=False
            )

            embed.add_field(
                name="🚀 Quick Start",
                value="New to the bot? Start with our Quick Start guide to get up and running in minutes!",
                inline=False
            )

            embed.add_field(
                name="🆘 **Need Additional Help?**",
                value=f"Join our support server for 24/7 assistance:\n[**Support Server**](https://discord.gg/kmGn5bh8Kf)\n\n• Expert help from our team\n• Community discussions\n• Feature requests & feedback",
                inline=False
            )

            embed.set_footer(text=f"{self.bot.user.name} Support System • Select Category Below")
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

            help_view = HelpCategoryView(self.bot, invoker.id)

            if is_interaction:
                if ctx.response.is_done():
                    await ctx.followup.send(embed=embed, view=help_view, ephemeral=True)
                else:
                    await ctx.response.send_message(embed=embed, view=help_view, ephemeral=True)
            else:
                await ctx.send(embed=embed, view=help_view)

        except Exception as e:
            logger.error(f"Error in help command: {e}")
            raise e

    @commands.hybrid_command(name="info", description="Display bot information, links, and resources.")
    async def info(self, ctx: commands.Context):
        try:
            if isinstance(ctx, discord.Interaction):
                await ctx.response.defer()

            embed = discord.Embed(
                title=f"🎫 {self.bot.user.name}",
                description="Your all-in-one Discord support ticket system.\nFast, reliable, and easy to set up.",
                color=0x000000,
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(
                name="🔗 Links",
                value=(
                    f"🌐 **[Website](https://deathhh.netlify.app/)**\n"
                    f"💬 **[Support Server](https://discord.gg/kmGn5bh8Kf)**\n"
                    f"🤖 **[Invite Bot](https://discord.com/oauth2/authorize?client_id=1512703087645556766&permissions=8&integration_type=0&scope=bot)**"
                ),
                inline=True
            )

            embed.add_field(
                name="📋 Commands",
                value=(
                    f"`,help` — full command list\n"
                    f"`,setup-tickets` — setup wizard\n"
                    f"`,send-panel` — deploy ticket panel"
                ),
                inline=True
            )

            embed.add_field(
                name="✨ Features",
                value=(
                    "🎫 Ticket categories & priorities\n"
                    "⭐ Rating & feedback system\n"
                    "📋 Transcripts & logging\n"
                    "✨ Auto-response triggers"
                ),
                inline=False
            )

            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.set_footer(text=f"Prefix: ,  •  Use ,help for all commands")

            if isinstance(ctx, discord.Interaction):
                await ctx.followup.send(embed=embed)
            else:
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in info command: {e}")
            raise e

    @commands.hybrid_command(name="botinfo", description="Display information about the bot.")
    @app_commands.describe()
    async def botinfo(self, ctx: commands.Context):
        logger.info(f"Botinfo command invoked by {ctx.author if isinstance(ctx, commands.Context) else ctx.user}")
        try:
            if isinstance(ctx, discord.Interaction):
                await ctx.response.defer(ephemeral=True)

            current_time = datetime.now(timezone.utc)

            embed = discord.Embed(
                title=f"❓ {self.bot.user.name} Information",
                description="Detailed information about this bot.",
                color=0x00D4FF,
                timestamp=current_time
            )

            embed.add_field(
                name="📊 **General Information**",
                value=f"• **Bot Name:** {self.bot.user.name}\n"
                      f"• **Bot ID:** {self.bot.user.id}\n"
                      f"• **Created At:** {utc_to_gmt(self.bot.user.created_at).strftime('%Y-%m-%d %H:%M:%S GMT')}",
                inline=False
            )

            embed.add_field(
                name="📋 **Technical Details**",
                value=f"• **Discord.py Version:** {discord.__version__}\n"
                      f"• **Python Version:** {__import__('platform').python_version()}\n"
                      f"• **Total Servers:** {len(self.bot.guilds)}",
                inline=False
            )

            embed.set_footer(text=f" Support System • Bot Information")
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

            if isinstance(ctx, discord.Interaction):
                await ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in botinfo command: {e}")
            raise e

    @commands.hybrid_command(name="ping", description="Check the bot's latency and connection status.")
    async def ping(self, ctx: commands.Context):
        logger.info(f"Ping command invoked by {ctx.author if isinstance(ctx, commands.Context) else ctx.user}")
        try:
            if isinstance(ctx, discord.Interaction):
                await ctx.response.defer(ephemeral=True)

            latency = round(self.bot.latency * 1000)

            if latency < 50:
                status_text = "Excellent"
                status_emoji = "🟢"
                color = 0x00FF88
                description = f"🚀 **Lightning Fast!** - {latency}ms response time"
            elif latency < 100:
                status_text = "Very Good"
                status_emoji = "🟢"
                color = 0x00D4FF
                description = f"📈 **Excellent Performance** - {latency}ms response time"
            elif latency < 150:
                status_text = "Good"
                status_emoji = "🟡"
                color = 0xFFAA00
                description = f"🔧 **Stable Connection** - {latency}ms response time"
            elif latency < 250:
                status_text = "Fair"
                status_emoji = "🟡"
                color = 0xFF8C00
                description = f"🎯 **Moderate Delays** - {latency}ms response time"
            else:
                status_text = "Poor"
                status_emoji = "❌"
                color = 0xFF6B6B
                description = f"❌ **High Latency Detected** - {latency}ms response time"

            embed = discord.Embed(
                title="📊 Real-Time Connection Status",
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(
                name="🔄 **Ping Latency**",
                value=f"```{latency}ms```",
                inline=True
            )

            embed.add_field(
                name="📈 **Connection Quality**",
                value=f"{status_emoji} **{status_text}**",
                inline=True
            )

            embed.add_field(
                name="🤖 **WebSocket Status**",
                value="🟢 **Online**",
                inline=True
            )

            if latency < 50:
                embed.add_field(
                    name="🚀 **Performance Analysis**",
                    value="Perfect for gaming and real-time applications!",
                    inline=False
                )
            elif latency < 100:
                embed.add_field(
                    name="📈 **Performance Analysis**",
                    value="Excellent for all Discord operations",
                    inline=False
                )
            elif latency < 150:
                embed.add_field(
                    name="🔧 **Performance Analysis**",
                    value="Good for normal Discord usage",
                    inline=False
                )
            elif latency < 250:
                embed.add_field(
                    name="🎯 **Performance Analysis**",
                    value="May notice slight delays in responses",
                    inline=False
                )
            else:
                embed.add_field(
                    name="❌ **Performance Analysis**",
                    value="Experiencing significant delays - check connection",
                    inline=False
                )

            embed.add_field(
                name="🕐 **Response Time Details**",
                value=f"• **API Latency:** {latency}ms\n• **WebSocket:** Connected\n• **Status:** {status_text}",
                inline=False
            )

            embed.set_footer(text="Live connection metrics • Updated every request")

            if isinstance(ctx, discord.Interaction):
                await ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in ping command: {e}")
            raise e

    @commands.hybrid_command(name="status", description="Update the bot's activity status. (Bot owner only)")
    @app_commands.describe(
        activity_type="The type of activity to display",
        text="The status text to display"
    )
    @app_commands.choices(activity_type=[
        app_commands.Choice(name="Playing", value="PLAYING"),
        app_commands.Choice(name="Watching", value="WATCHING"),
        app_commands.Choice(name="Listening", value="LISTENING"),
        app_commands.Choice(name="Streaming", value="STREAMING"),
    ])
    async def set_status(self, ctx: commands.Context, activity_type: str, *, text: str):
        if not await self.bot.is_owner(ctx.author):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="Only the bot owner can use this command.",
                color=0xFF6B6B,
                timestamp=datetime.now(timezone.utc)
            )
            if isinstance(ctx, discord.Interaction):
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed, ephemeral=True)
            return

        try:
            if isinstance(ctx, discord.Interaction):
                await ctx.response.defer(ephemeral=True)

            activity_type = activity_type.upper()

            if activity_type == "STREAMING":
                activity = discord.Streaming(name=text, url="https://discord.gg/kmGn5bh8Kf")
            elif activity_type == "PLAYING":
                activity = discord.Game(name=text)
            elif activity_type == "WATCHING":
                activity = discord.Activity(type=discord.ActivityType.watching, name=text)
            elif activity_type == "LISTENING":
                activity = discord.Activity(type=discord.ActivityType.listening, name=text)
            else:
                activity = discord.Activity(type=discord.ActivityType.watching, name=text)

            await self.bot.change_presence(activity=activity, status=discord.Status.online)

            embed = discord.Embed(
                title="🔄 Bot Status Updated",
                description=f"The bot's status has been updated successfully.",
                color=0x00D4FF,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="🚀 **Activity Type**", value=f"`{activity_type.capitalize()}`", inline=True)
            embed.add_field(name="📋 **Status Text**", value=f"`{text}`", inline=True)
            embed.set_footer(text=f"Updated by {ctx.author if isinstance(ctx, commands.Context) else ctx.user}")

            if isinstance(ctx, discord.Interaction):
                await ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in status command: {e}")
            raise e

    @commands.hybrid_command(name="stats", description="Display server statistics and bot performance metrics.")
    async def stats(self, ctx: commands.Context):
        logger.info(f"Stats command invoked by {ctx.author if isinstance(ctx, commands.Context) else ctx.user}")
        try:
            if isinstance(ctx, discord.Interaction):
                await ctx.response.defer(ephemeral=True)

            current_time = datetime.now(timezone.utc)


            embed = discord.Embed(
                title="📊 Server Statistics & Bot Performance",
                description="Real-time server analytics and bot performance metrics.",
                color=0x00D4FF,
                timestamp=current_time
            )

            guild = ctx.guild
            embed.add_field(
                name="❓ **Server Information**",
                value=f"• **Server Name:** {guild.name}\n"
                      f"• **Server ID:** {guild.id}\n"
                      f"• **Created:** {guild.created_at.strftime('%Y-%m-%d')}\n"
                      f"• **Owner:** {guild.owner.mention if guild.owner else 'Unknown'}\n"
                      f"• **Members:** {guild.member_count:,}",
                inline=False
            )

            embed.add_field(
                name="🚀 **Bot Performance**",
                value=f"• **Latency:** {round(self.bot.latency * 1000)}ms\n"
                      f"• **Guilds:** {len(self.bot.guilds):,}\n"
                      f"• **Users:** {len(self.bot.users):,}\n"
                      f"• **Commands:** {len(self.bot.commands)}",
                inline=False
            )

            embed.add_field(
                name="📈 **Member Statistics**",
                value=f"• **Total Members:** {guild.member_count:,}\n"
                      f"• **Online Members:** {len([m for m in guild.members if m.status != discord.Status.offline]):,}\n"
                      f"• **Bots:** {len([m for m in guild.members if m.bot]):,}\n"
                      f"• **Humans:** {len([m for m in guild.members if not m.bot]):,}",
                inline=True
            )

            embed.add_field(
                name="🎫 **Channel Statistics**",
                value=f"• **Text Channels:** {len(guild.text_channels)}\n"
                      f"• **Voice Channels:** {len(guild.voice_channels)}\n"
                      f"• **Categories:** {len(guild.categories)}\n"
                      f"• **Total Channels:** {len(guild.channels)}",
                inline=True
            )

            embed.set_footer(text="Live Statistics • Updated in Real-Time")
            embed.set_thumbnail(url=guild.icon.url if guild.icon else self.bot.user.display_avatar.url)

            if isinstance(ctx, discord.Interaction):
                await ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in stats command: {e}")
            raise e

    

class HelpCategoryView(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.user_id = user_id

    @discord.ui.select(
        placeholder="Select a help category...",
        options=[
            discord.SelectOption(
                label="Setup Guide",
                value="setup",
                emoji="🔧",
                description="Complete setup walkthrough"
            ),
            discord.SelectOption(
                label="Ticket Commands",
                value="tickets",
                emoji="🎫",
                description="All ticket management commands"
            ),
            discord.SelectOption(
                label="Admin Commands",
                value="admin",
                emoji="🛡️",
                description="Administrator commands & features"
            ),
            discord.SelectOption(
                label="Trigger Commands",
                value="triggers",
                emoji="✨",
                description="Keyword triggers & auto-responses"
            ),
            discord.SelectOption(
                label="General Commands",
                value="general",
                emoji="❓",
                description="General bot commands & info"
            )
        ]
    )
    async def help_category_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            category = select.values[0]
            current_time = utc_to_gmt(datetime.now(timezone.utc))

            if category == "setup":
                embed = discord.Embed(
                    title="🔧 Setup Guide",
                    description="Complete guide to setting up your support system.",
                    color=0x00D4FF,
                    timestamp=current_time
                )

                embed.add_field(
                    name="🚀 **Quick Setup**",
                    value="`setup-tickets` - Launch the complete setup wizard\n"
                          "This command will guide you through configuring categories, roles, and channels.",
                    inline=False
                )

                embed.add_field(
                    name="📋 **Category Management**",
                    value="`add-category <name>` - Add a new support category\n"
                          "`remove-category <name>` - Remove an existing category\n"
                          "`list-categories` - View all configured categories",
                    inline=False
                )

                embed.add_field(
                    name="🎯 **Panel Deployment**",
                    value="`send-panel dropdown` - Send panel with dropdown menu\n"
                          "`send-panel button` - Send panel with individual buttons",
                    inline=False
                )

            elif category == "tickets":
                embed = discord.Embed(
                    title="🎫 Ticket Commands",
                    description="All commands for managing support tickets.",
                    color=0x00D4FF,
                    timestamp=current_time
                )

                embed.add_field(
                    name="🎯 **Ticket Management**",
                    value="`close-ticket` - Close the current ticket with transcript\n"
                          "`claim-ticket` - Claim a ticket for support\n"
                          "`transfer-ticket @user` - Transfer ticket to another staff member\n"
                          "`priority <level>` - Change ticket priority level\n"
                          "`add-user @user` - Add a user to the current ticket\n"
                          "`remove-user @user` - Remove a user from the ticket\n"
                          "`rename <name>` - Rename the current ticket channel",
                    inline=False
                )

                embed.add_field(
                    name="🕐 **Priority & Status**",
                    value="`priority <level>` - Set ticket priority (low/medium/high/critical)\n"
                          "`claim` - Claim a ticket for support handling",
                    inline=False
                )

                embed.add_field(
                    name="💡 **User Features**",
                    value="• Create tickets using the support panel\n"
                          "• Rate your support experience when ticket closes\n"
                          "• Receive automatic transcripts in DMs",
                    inline=False
                )

            elif category == "admin":
                embed = discord.Embed(
                    title="🛡️ Admin Commands",
                    description="Administrator commands and features.",
                    color=0x00D4FF,
                    timestamp=current_time
                )

                embed.add_field(
                    name="🔧 **System Setup**",
                    value="`setup-tickets` - Configure the entire support system\n"
                          "`send-panel <type>` - Deploy support panels\n"
                          "`reset-categories` - Reset all categories to default",
                    inline=False
                )

                embed.add_field(
                    name="👥 **Support Role Management**",
                    value="`support-role-add @role` - Add additional support role\n"
                          "`support-role-remove @role` - Remove additional support role\n"
                          "`support-role-list` - List all support roles",
                    inline=False
                )

                embed.add_field(
                    name="📊 **Analytics & Stats**",
                    value="`stats` - View comprehensive server statistics",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ **Permissions Required**",
                    value="Most admin commands require **Administrator** permission or designated **Support Staff** role.",
                    inline=False
                )

            elif category == "triggers":
                embed = discord.Embed(
                    title="✨ Trigger Commands",
                    description="Manage keyword triggers and automatic responses.",
                    color=0x00D4FF,
                    timestamp=current_time
                )

                embed.add_field(
                    name="🔧 **Trigger Management**",
                    value="`add-trigger <keyword> <message>` - Create a new keyword trigger\n"
                          "`remove-trigger <keyword>` - Remove an existing trigger\n"
                          "`trigger-get <keyword>` - View trigger response message",
                    inline=False
                )

                embed.add_field(
                    name="📋 **Trigger Information**",
                    value="`list-triggers` - View all triggers in this server\n"
                          "• Triggers respond automatically when keywords are detected\n"
                          "• Keywords are case-insensitive and match partial text",
                    inline=False
                )

                embed.add_field(
                    name="🛡️ **Permissions Required**",
                    value="• `add-trigger` and `remove-trigger` require **Administrator** permission\n• `trigger-get` and `list-triggers` can be used by anyone",
                    inline=False
                )

            else:  # general
                embed = discord.Embed(
                    title="❓ General Commands",
                    description="General bot commands and information.",
                    color=0x00D4FF,
                    timestamp=current_time
                )

                embed.add_field(
                    name="📊 **Bot Information**",
                    value="`ping` - Check bot latency and status\n"
                          "`botinfo` - View detailed bot information\n"
                          "`help` - Display this help menu",
                    inline=False
                )

                embed.add_field(
                    name="❓ **Support Resources**",
                    value="`faq` - Frequently asked questions\n"
                          "`stats` - Server statistics (if you have permissions)",
                    inline=False
                )

                embed.add_field(
                    name="🚀 **Need More Help?**",
                    value="Join our support server: [Support Server](https://discord.gg/kmGn5bh8Kf)\n"
                          "Create a support ticket using the panel for personalized assistance!",
                    inline=False
                )

            embed.set_footer(text=" Support System • Help")
            view = HelpCategoryView(self.bot, self.user_id)
            await interaction.response.edit_message(embed=embed, view=view)

        except Exception as e:
            logger.error(f"Error in help category select: {e}")
            from utils.error_handler import GlobalErrorHandler
            handler = GlobalErrorHandler(self.bot)
            await handler.handle_view_error(interaction, e)

async def setup(bot):
    await bot.add_cog(HelpSystem(bot))