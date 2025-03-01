import discord
from discord.ext import commands

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='tts')
    async def text_to_speech(self, ctx, *, message=None):
        """
        Converts text to speech and plays it in the voice channel.
        Usage: !tts <message>
        """
        # Check if a message was provided
        if message is None:
            embed = discord.Embed(
                title="⚠️ Error",
                description="Please provide a message to convert to speech.",
                color=discord.Color.red()
            )
            embed.add_field(name="Usage", value="`!tts <message>`", inline=False)
            await ctx.send(embed=embed)
            return
            
        # Check if the message is too long (Discord has limits)
        if len(message) > 200:
            embed = discord.Embed(
                title="⚠️ Error",
                description="Your message is too long. Please keep it under 200 characters.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
            
        try:
            # Send the TTS message
            await ctx.send(message, tts=True)
            
            # Send a confirmation embed
            embed = discord.Embed(
                title="🔊 Text-to-Speech",
                description=f"TTS message sent by {ctx.author.mention}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Message", value=message, inline=False)
            await ctx.send(embed=embed)
            
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="⚠️ Error",
                description=f"Failed to send TTS message: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Error",
                description=f"An unexpected error occurred: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))