
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta, timezone

class AdminCommands(commands.Cog):
    #Commands for server administration and moderation
    def __init__(self, bot):
        self.bot = bot
    




    # Function to clear a specified number of messages 
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):

        if amount > 100:
            await ctx.send("You can only delete up to 100 messages at once.")
            return
            
        await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
        confirmation = await ctx.send(f'Cleared {amount} messages.')
        await asyncio.sleep(5)
        await confirmation.delete()
    




    #Function to kick a member from the server 
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked. Reason: {reason or "No reason provided"}')
    




    #Function to ban a member from the server 
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned. Reason: {reason or "No reason provided"}')
    




    # Function to timeout a member for a specified duration 

    @commands.command(name='timeout')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):

        status_msg = await ctx.send(f" Attempting to timeout {member.display_name}...")
        
        # 1. Check member hierarchy
        if member.top_role >= ctx.guild.me.top_role:
            await status_msg.edit(content=f" Cannot timeout: {member.display_name}'s highest role ({member.top_role.name}) is above or equal to my highest role ({ctx.guild.me.top_role.name}).")
            return
            
        # 2. Check admin status
        if member.guild_permissions.administrator:
            await status_msg.edit(content=f" Cannot timeout: {member.display_name} has administrator permissions.")
            return
            
        # 3. Check timeout duration
        if minutes > 40320:  # Max 28 days
            await status_msg.edit(content=" Timeout cannot exceed 28 days (40320 minutes).")
            return
        
        # 4. Convert time with explicit UTC
        try:
            until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
            await status_msg.edit(content=f" Setting timeout until: {until.strftime('%Y-%m-%d %H:%M:%S %Z')}...")
        except Exception as e:
            await status_msg.edit(content=f" Error creating datetime: {str(e)}")
            return
        
        # 5. Apply timeout with extensive error handling
        try:
            # Apply timeout 
            await member.timeout(until, reason=reason)
            
            # Verify timeout was applied
            updated_member = ctx.guild.get_member(member.id)
            if updated_member and updated_member.is_timed_out():
                embed = discord.Embed(
                    title="✅ Member Timed Out",
                    description=f"{member.mention} has been timed out for {minutes} minutes.",
                    color=discord.Color.orange()
                )
                if reason:
                    embed.add_field(name="Reason", value=reason)
                embed.set_footer(text=f"Timed out by {ctx.author}")
                await status_msg.edit(content=None, embed=embed)
            else:
                await status_msg.edit(content=f" API call completed but {member.display_name} is not showing as timed out. This may be a Discord API issue.")
        except discord.Forbidden as e:
            await status_msg.edit(content=f" Permission error: {str(e)}")
        except discord.HTTPException as e:
            await status_msg.edit(content=f" HTTP error: {str(e)}")
        except Exception as e:
            await status_msg.edit(content=f" Unexpected error: {str(e)}")
    





    # Function to setup basic welcome and log channels for the server 	
    @commands.command(name='setup')
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):

        from utils.config import Config
        config = Config()
        
        # Create welcome channel if it doesn't exist
        if not config.get('welcome_channel'):
            welcome_channel = await ctx.guild.create_text_channel('welcome')
            config.set('welcome_channel', welcome_channel.id)
            await ctx.send(f"Created welcome channel: {welcome_channel.mention}")
        
        # Create log channel if it doesn't exist
        if not config.get('log_channel'):
            log_channel = await ctx.guild.create_text_channel('bot-logs')
            config.set('log_channel', log_channel.id)
            await ctx.send(f"Created log channel: {log_channel.mention}")
            
        await ctx.send("Setup complete!")
    





    """------------------------------ Error Handlers ------------------------------"""

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number of messages to delete.")
    

    @kick.error
    @ban.error
    @timeout.error
    async def mod_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found. Please provide a valid mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide valid arguments for the command.")







# Function to add the cog to the bot 	
async def setup(bot):

    await bot.add_cog(AdminCommands(bot))