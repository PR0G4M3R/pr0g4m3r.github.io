import os
import discord
from discord.ext import commands
import datetime
import pytz
import random
import sqlite3
import requests
from config import location_module, WEATHER_API

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = WEATHER_API


class weatherModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def kelvin_to_celsius_fahrenheit(self, kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9 / 5) + 32
        return celsius, fahrenheit

    @commands.command(brief='This command gets the weather of a specified location.', name="weather", extras={"category": "Location Commands"})
    async def get_weather(self, ctx, CITY: str):
        if location_module:
            url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
            response = requests.get(url).json()

            if 'main' in response:
                temp_kelvin = response['main']['temp']
                temp_celsius, temp_fahrenheit = self.kelvin_to_celsius_fahrenheit(
                    temp_kelvin)

                feels_like_kelvin = response['main']['feels_like']
                feels_like_celsius, feels_like_fahrenheit = self.kelvin_to_celsius_fahrenheit(
                    feels_like_kelvin)

                wind_speed = response['wind']['speed']
                humidity = response['main']['humidity']
                description = response['weather'][0]['description']
                sunrise_time = datetime.datetime.utcfromtimestamp(
                    response['sys']['sunrise'] + response['timezone'])
                sunset_time = datetime.datetime.utcfromtimestamp(
                    response['sys']['sunset'] + response['timezone'])

                embed = discord.Embed(
                    title=f"Weather in {CITY}",
                    description="Here is the weather for your selected city:",
                    colour=ctx.author.colour
                )

                embed.add_field(name="Temperature", value=f"{
                                temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
                embed.add_field(name="Feels Like", value=f"{feels_like_celsius:.2f}°C or {
                                feels_like_fahrenheit:.2f}°F")
                embed.add_field(name="Humidity", value=f"{humidity}%")
                embed.add_field(name="Wind Speed", value=f"{wind_speed}m/s")
                embed.add_field(name="General Weather", value=description)
                embed.add_field(name="Sunrise Time", value=sunrise_time.strftime(
                    "%H:%M:%S") + " local time")
                embed.add_field(name="Sunset Time", value=sunset_time.strftime(
                    "%H:%M:%S") + " local time")

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Sorry, I couldn't find the weather data for {CITY}.")
        else:
            await ctx.send("Location module is not enabled in the config.")


class TimeModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get a list of available time zones.")
    async def timezones(self, ctx):
        await ctx.send("https://docs.google.com/document/d/1Q4p98dBCpaco0tXXGUFQnwaxTDbJM-Afl5CwOwgWyOM/edit?usp=sharing")

    @commands.command(brief="Get the current time for various time zones.", extras={"category": "Location Commands"})
    async def time(self, ctx, *, location: str):
        if location_module:
            try:
                tz = pytz.timezone(location)
                current_time = datetime.datetime.now(tz)
                time_str = current_time.strftime("%H:%M:%S")

                embed = discord.Embed(title=f"Current Time in {
                                      location}", color=ctx.author.color)
                embed.add_field(name="Time", value=time_str, inline=False)
                await ctx.send(embed=embed)

            except pytz.UnknownTimeZoneError:
                await ctx.send(f"Sorry, I couldn't find the time zone for {location}.")
                print(f"Unknown time zone provided: {location}")
        else:
            await ctx.send("Location module is not enabled in the config.")


def setup(bot):
    bot.add_cog(weatherModule(bot))
    bot.add_cog(TimeModule(bot))
