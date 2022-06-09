############################# [ IMPORTS ] #############################

import discord, asyncio, os

from discord.ext import commands

import functions, pdf_generator as pdf


############################# [ FUNCTIONS ] #############################

class ab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ab")  # Main command
    async def ab(self, ctx, *args):  # Create a by-default command
        # print(args)

        # Handling each scenario
        if args == ():  # Check if there is no args => trying to know how to use it
            await ctx.send(
                f"Hi {ctx.author.mention} :sparkles:,\nTo get the user manual please type `$ab -h` or `$ab help`",
                delete_after=5)
        else:
            def check(msg):  # Only to check the validity of the argument sent
                return msg.author.id == ctx.author.id and msg.channel == ctx.channel

            if len(args) > 1:
                # print(len(args))
                await ctx.send(
                    f" Arrrrggghh {ctx.author.mention} :confounded:,\nDon't overload me, please type `$ab -h` or `$ab help` for help",
                    delete_after=2)
            else:
                if args[0] in ['help', '-h']:  # Help argument
                    dm = await ctx.author.create_dm()  # Create a dm channel
                    await dm.send("\nHello dear *Sky Lover* :milky_way:"
                                  "\nYou asked for help to use me and here I am ... "
                                  "\nas efficient as a N130/900 :wink:"
                                  "\n========================================"
                                  "\n`$ab help` or `$ab -h` : To get this manual"
                                  "\n`$ab coords` or `$ab -c` : To enter coordinates of your choice"
                                  "\n`$ab place` or `$ab -p` : To enter the place of your choice"
                                  "\n========================================"
                                  "\nI was developed by *Wyv3rn#3154*, go tell him about bugs or compliments :grin:")  # Send a private message

                elif args[0] in ['coords', '-c']:  # Coodrinates argument
                    try:
                        await ctx.send('Please enter coordinates ({lat} {lon}): ')
                        usrInput = await self.bot.wait_for('message', check=check,
                                                           timeout=30)  # get the input and check if the sender and the channel are the right
                        lat, lon = str(usrInput.content).split(
                            " ")  # Try to get latitude and longitude entered by the user
                        lat = float(lat)
                        lon = float(lon)

                        @commands.Cog.listener()  # Delete all the message concerning the request
                        async def on_message(message):
                            if message.author.id == ctx.author.id:
                                await asyncio.sleep(2)
                                await message.delete()

                        try:  # Check if values are legit coordinates
                            await ctx.send("Valid values", delete_after=2)
                            await ctx.send(
                                f'You just entered the coordinates: \nlattitude = **{lat}**, longitude = **{lon}**',
                                delete_after=2)

                            # Waiting for creation
                            embed = discord.Embed(title=":clock8: I'm in creation...",
                                                  description="Please wait a second, I'm creating your pdf",
                                                  color=0x0f056b)
                            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                            embed.set_image(
                                url="https://www.nasa.gov/sites/default/files/thumbnails/image/sombrero-galaxy.jpg")
                            embed.set_footer(text="Made by *Wyv3rn#3154*")
                            await ctx.send(embed=embed, delete_after=2)

                            # Creation
                            city = functions.getCity(lat, lon)
                            # print(lat,lon)
                            pdf.Vars().set_lat(lat)  # Setting all variables into a Vars() class
                            pdf.Vars().set_lon(lon)
                            pdf.Vars().set_place(city)

                            pdf.PDFgen(lat, lon, city)  # Create a pdf with the vars in the class

                            # Send the PDF
                            embed = discord.Embed(title=":star: PDF of your location",
                                                  description="This is a pdf that contains the near future astronomical events of your position",
                                                  color=0x0f056b)
                            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                            embed.set_footer(text="Made by *Wyv3rn#3154*")
                            await ctx.send(embed=embed, delete_after=2)
                            filename = pdf.vars.get_filename()
                            await ctx.send(file=discord.File(r"pdf/{}.pdf".format(filename)),
                                           content=f"{ctx.author.mention}", delete_after=2)
                            os.remove(f"pdf/{filename}.pdf")
                        except ValueError:
                            await ctx.send("Invalid values", delete_after=2)
                            await ctx.send(
                                f'You just entered the coordinates: \nlattitude = **{lat}**, longitude = **{lon}**',
                                delete_after=5)

                    except asyncio.TimeoutError:  # Timeout error => user quit
                        await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!", delete_after=2)

                elif args[0] in ['place', '-p']:  # Place argument
                    try:
                        await ctx.send('Please enter a city name: ', delete_after=30)
                        usrInput = await self.bot.wait_for('message', check=check, timeout=30)
                        city = str(usrInput.content).lower()  # Make the input in lowercase

                        @commands.Cog.listener()  # Delete all the message concerning the request
                        async def on_message(message):
                            if message.author.id == ctx.author.id:
                                await asyncio.sleep(2)
                                await message.delete()

                        if not any(char.isdigit() for char in city):  # Check if it doesn't contain any digit
                            invalidChars = list("!@#$%^&*()+?=,<>/")
                            if not any(char in invalidChars for char in city) : # Check if it doesn't contain special chars except ' ','_' and '-'
                                await ctx.send("Valid value", delete_after=2)
                                await ctx.send(f'You just entered the city: **{city}**', delete_after=2)

                                # Waiting for creation
                                embed = discord.Embed(title=":clock8: I'm in creation...",
                                                      description="Please wait a second, I'm creating your pdf",
                                                      color=0x0f056b)
                                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                                embed.set_image(
                                    url="https://www.nasa.gov/sites/default/files/thumbnails/image/sombrero-galaxy.jpg")
                                embed.set_footer(text="Made by *Wyv3rn#3154*")
                                await ctx.send(embed=embed, delete_after=2)

                                # Creation
                                lat, lon = functions.getCoords(city)
                                # print(lat,lon)
                                pdf.vars.set_lat(lat)  # Setting all variables into a Vars() class
                                pdf.vars.set_lon(lon)
                                pdf.vars.set_place(city)

                                pdf.PDFgen(lat, lon, city)  # Create a pdf with the vars in the class

                                # Send the PDF
                                embed = discord.Embed(title=":star: PDF of your location",
                                                      description="This is a pdf that contains the near future astronomical events of your position",
                                                      color=0x0f056b)
                                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                                embed.set_footer(text="Made by *Wyv3rn#3154*")
                                await ctx.send(embed=embed, delete_after=2)
                                filename = pdf.vars.get_filename()
                                await ctx.send(file=discord.File(r"pdf/{}.pdf".format(filename)),
                                               content=f"{ctx.author.mention}", delete_after=5)
                                os.remove(f"pdf/{filename}.pdf")
                            else:
                                await ctx.send("Invalid value", delete_after=5)
                                await ctx.send(f'You just entered the city: **{city}**', delete_after=5)
                        else:
                            await ctx.send("Invalid value", delete_after=5)
                            await ctx.send(f'You just entered the city: **{city}**', delete_after=5)

                    except asyncio.TimeoutError:  # Timeout error => user quit
                        await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!", delete_after=2)

                else:  # Ununderstable argument
                    await ctx.send("I don't think I understood you, please type `$ab -h` or `$ab help` for help",
                                   delete_after=2)

    @commands.Cog.listener()
    async def on_ready(self):
        print('     [+] cogs.ab')


def setup(bot):
    bot.add_cog(ab(bot))
