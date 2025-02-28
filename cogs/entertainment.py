"""
Entertainment commands for the Discord bot.
"""
import discord
from discord.ext import commands
import random
import asyncio

class Entertainment(commands.Cog):
    """
    Fun commands and games.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def roll(self, ctx, dice: str = "1d6"):
        """
        Roll dice in NdN format.
        
        Args:
            dice: Dice to roll in NdN format (default: 1d6)
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send("Dice format must be in NdN format, e.g. 3d6")
            return
        
        if rolls > 100:
            await ctx.send("Cannot roll more than 100 dice at once.")
            return
            
        if limit > 1000:
            await ctx.send("Cannot roll dice with more than 1000 sides.")
            return
            
        results = [random.randint(1, limit) for _ in range(rolls)]
        
        # Format the results
        if len(results) > 1:
            result_str = f"{', '.join(map(str, results))} (Total: {sum(results)})"
        else:
            result_str = str(results[0])
            
        await ctx.send(f"🎲 {ctx.author.mention} rolled {dice}: {result_str}")
    
    @commands.command()
    async def choose(self, ctx, *options):
        """
        Choose between multiple options.
        
        Args:
            options: Options to choose from
        """
        if len(options) < 2:
            await ctx.send("Please provide at least 2 options to choose from.")
            return
            
        chosen = random.choice(options)
        await ctx.send(f"🤔 I choose: **{chosen}**")
    
    @commands.command()
    async def rps(self, ctx):
        """Play rock-paper-scissors against the bot."""
        # Define the possible choices and emojis
        choices = ["rock", "paper", "scissors"]
        emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        
        # Create the message
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description="Click a reaction to play!",
            color=discord.Color.blue()
        )
        
        message = await ctx.send(embed=embed)
        
        # Add reactions
        for choice in choices:
            await message.add_reaction(emojis[choice])
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis.values() and reaction.message.id == message.id
        
        try:
            # Wait for user's choice
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            # Determine the user's choice from emoji
            user_choice = None
            for choice, emoji in emojis.items():
                if str(reaction.emoji) == emoji:
                    user_choice = choice
                    break
            
            # Bot makes its choice
            bot_choice = random.choice(choices)
            
            # Determine the winner
            if user_choice == bot_choice:
                result = "It's a tie!"
            elif (user_choice == "rock" and bot_choice == "scissors") or \
                 (user_choice == "paper" and bot_choice == "rock") or \
                 (user_choice == "scissors" and bot_choice == "paper"):
                result = "You win!"
            else:
                result = "I win!"
            
            # Update the embed with the result
            embed.description = f"You chose: {emojis[user_choice]}\nI chose: {emojis[bot_choice]}\n\n**{result}**"
            await message.edit(embed=embed)
            
        except asyncio.TimeoutError:
            embed.description = "Game cancelled - you didn't respond in time."
            await message.edit(embed=embed)
    
    @commands.command()
    async def trivia(self, ctx):
        """A simple trivia game."""
        # Sample trivia questions with answers
        questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "answer": "Mars"
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                "answer": "Pacific Ocean"
            }
        ]
        
        # Select a random question
        question_data = random.choice(questions)
        question = question_data["question"]
        options = question_data["options"]
        answer = question_data["answer"]
        
        # Create an embed for the question
        embed = discord.Embed(
            title="Trivia Question",
            description=question,
            color=discord.Color.green()
        )
        
        # Add options as fields
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=True)
        
        # Send the question
        message = await ctx.send(embed=embed)
        
        # Add reaction options
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        for i in range(len(options)):
            await message.add_reaction(reactions[i])
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == message.id
        
        try:
            # Wait for user's answer
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
            
            # Get the index of the selected option
            selected_index = reactions.index(str(reaction.emoji))
            selected_option = options[selected_index]
            
            # Check if the answer is correct
            if selected_option == answer:
                result = "✅ Correct! Well done!"
            else:
                result = f"❌ Wrong! The correct answer is: {answer}"
            
            # Update the embed with the result
            embed.add_field(name="Result", value=result, inline=False)
            await message.edit(embed=embed)
            
        except asyncio.TimeoutError:
            embed.add_field(name="Time's up!", value=f"The correct answer was: {answer}", inline=False)
            await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Entertainment(bot))