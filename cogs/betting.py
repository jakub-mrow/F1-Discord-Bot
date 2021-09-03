import discord
import json
import requests
from discord.ext import commands
from discord import Embed
from graphics.emojis import Emoji
import mysql.connector
from mysql.connector import Error

class Betting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "bet")
    async def bet(self, ctx, *, bet):
        if ctx.channel.id == 872137469318029393:
            db = mysql.connector.connect(
                host = "192.168.1.39",
                user = get_login(),
                passwd = get_login(),
                database = "F1Bot"
            )
            mycursor = db.cursor(buffered=True)
            round_num = get_last_round()
            gp_name = get_gp_name(round_num)
            user_name = ctx.message.author.name

            # Creating tables with one to many hiararchy
            #mycursor.execute("CREATE TABLE Users (userID int PRIMARY KEY AUTO_INCREMENT, name varchar(50) UNIQUE, points int DEFAULT 0)")
            #mycursor.execute("CREATE TABLE Bets (betID int PRIMARY KEY AUTO_INCREMENT, userID int, bet varchar(50), raceName varchar(50), FOREIGN KEY (userID) REFERENCES Users(userID), UNIQUE (userID, raceName))")

            # # Inserting new Users
            try:
                mycursor.execute("INSERT INTO Users (name, points) VALUES (%s, %s)", (user_name, "DEFAULT"))
                db.commit()
            except Error as e:
                print(e)

            # # # # Selecting userID from Users table
            mycursor.execute("SELECT userID FROM Users WHERE name = '{}'".format(user_name))
            userID = int(mycursor.fetchone()[0])

            # # #Inserting bet data into Bets Table
            try:
                mycursor.execute("INSERT INTO Bets (userID, bet, raceName) VALUES (%s, %s, %s)", (userID, bet, gp_name))
                db.commit()
            except Error as e:
                print(e)

            # # Printing actual tables
            mycursor.execute("SELECT * FROM Users")
            for x in mycursor:
                print(x)
            print("---------------------------------")
            mycursor.execute("SELECT * FROM Bets")
            for x in mycursor:
                print(x)
    

def setup(client):  
    client.add_cog(Betting(client))

def get_login():
    with open("cogs\database.txt", "r") as file:
        lines = file.readlines()
        return lines[0].strip()

def get_gp_name(round_num):
    response = requests.get("http://ergast.com/api/f1/current.json")
    my_json = response.text
    parsed = json.loads(my_json)
    gp_name = parsed["MRData"]["RaceTable"]["Races"][round_num]["raceName"]
    return gp_name

def get_last_round():
    response = requests.get("http://ergast.com/api/f1/current/last/results.json")
    my_json = response.text
    parsed = json.loads(my_json)
    round_num = int(parsed["MRData"]["RaceTable"]["Races"][0]["round"])
    return round_num