"""
MIT License
Copyright (c) 2020 GamingGeek

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from discord.ext import commands
from fire.push import pushbullet
from fire import exceptions
import functools
import asyncio
import discord
import traceback


class guildRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.loop.run_in_executor(None, func=functools.partial(self.bot.datadog.increment, 'guilds.leave'))
        fire = self.bot.get_guild(564052798044504084)
        await fire.edit(description=f'The official server for the Fire Discord bot, used in {len(self.bot.guilds)} servers.')
        self.bot.logger.info(f"$REDFire left the guild $BLUE{guild.name}({guild.id}) $REDwith $BLUE{guild.member_count} $REDmembers! Goodbye o/")
        try:
            await pushbullet("link", "Fire left a guild!", f"Fire left {guild.name}({guild.id}) with {guild.member_count} members! Goodbye o/", f"https://api.gaminggeek.dev/guild/{guild.id}")
        except exceptions.PushError as e:
            self.bot.logger.warn(f'$YELLOWFailed to send guild leave notification!')


def setup(bot):
    if bot.dev:
        return
    try:
        bot.add_cog(guildRemove(bot))
        bot.logger.info(f'$GREENLoaded event $BLUEguildRemove!')
    except Exception as e:
        # errortb = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        bot.logger.error(f'$REDError while loading event $BLUE"guildRemove"', exc_info=e)
