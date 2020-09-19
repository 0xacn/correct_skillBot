import discord 
from discord import Member
from typing import Optional
from datetime import datetime
from config import STAFF_LOGS_CHANNEL_ID
from discord.ext.commands import (Cog, MemberConverter,
                                  command, has_permissions, 
                                  bot_has_permissions, 
                                  CheckFailure, Greedy)
                                  
                                  
class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @command(name="kick",brief='kicks member')
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets : Greedy[Member], *, reason : Optional[str] = "no reason provied."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing")
        else:
            for target in targets:
    
                if (ctx.guild.me.top_role.position > target.top_role.position 
                    and not target.guild_permissions.administrator):
    
                    await target.kick(reason=reason)
                    embed = discord.Embed(title=f"kicked {target.display_name} {reason}",
                                        colour=discord.Color.blurple(),
                                        timestamp=datetime.utcnow())
                    fields = [("Actioned By", ctx.author.display_name, False)]
                    await self.log_channel.send(embed=embed)
                else:
                    await ctx.send(f"{target.display_name} could not be kicked.")
            await self.log_channel.send("Action completed.")
    
    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You dont have the permission to do this. -_-")

    @command(name="ban", brief="bans member")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, targets : Greedy[Member], *, reason : Optional[str] = "no reason provied."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing")
    
        else:
    
            for target in targets:
    
                if (ctx.guild.me.top_role.position > target.top_role.position 
                    and not target.guild_permissions.administrator):
    
                    await target.ban(reason=reason)
                    embed = discord.Embed(title=f"banned {target.display_name} {reason}",
                                        colour=discord.Color.blurple(),
                                        timestamp=datetime.utcnow())
                    fields = [("Actioned By", ctx.author.display_name, False)]
                    await self.log_channel.send(embed=embed)
                else:
                     await ctx.send(f"{target.display_name} could not be banned.")
            await self.log_channel.send("Action completed.")
   
    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You dont have the permission to do this. -_-")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")
            self.log_channel = self.bot.get_channel(STAFF_LOGS_CHANNEL_ID)

def setup(bot):
    bot.add_cog(Mod(bot))
