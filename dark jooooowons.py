from typing import Mapping
import os
import discord
import sqlite3
import random
import asyncio

master_ids = [874871785898786878]
client = discord.Client()

@client.event
async def on_ready():
    print("Login")
    while True:
         game = discord.Game("주인에게 잔소리를")
         await client.change_presence(status=discord.Status.online, activity=game)
@client.event
async def on_message(message):
    if not isinstance(message.channel, discord.channel.DMChannel):
        if (message.author.guild_permissions.administrator or message.author.id in master_ids):
            try:
                if message.content == "ㄷ등록":
                    con = sqlite3.connect(str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("CREATE TABLE users (id INTEGER, money INTEGER, pickax INTEGER, NextPickax INTEGER);")
                    con.commit()
                    cur.execute("CREATE TABLE mineral (id INTEGER, iron INTEGER, gold INTEGER, emerald INTEGER, ruby INTEGER, diamond INTEGER, reddiamond INTEGER);")
                    con.commit()
                    embed = discord.Embed(title="등록 성공", description="성공적으로 등록이 완료되었습니다.", color=0xffffff)
                    await message.channel.send(embed=embed)
            except sqlite3.OperationalError:
                embed = discord.Embed(description="서버가 이미 등록되어있습니다.", color=0xff0000)
                await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content.startswith("ㄷ가입"):
            try:
                con = sqlite3.connect(str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()
                if (user_info == None):
                    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", (message.author.id, 5000, "플라스틱 곡괭이", "철곡괭이"))
                    con.commit()
                    embed = discord.Embed(title="가입 성공", description="가입 선물로 5000원이 지급됩니다.", color=0xffffff)
                    await message.channel.send(embed=embed)
                    cur.execute("INSERT INTO mineral VALUES(?, ?, ?, ?, ?, ?, ?);", (message.author.id, 0, 0, 0, 0, 0, 0))
                    con.commit()
                    con.close()
                else:
                    embed = discord.Embed(description="이미 가입을 하셨습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)
            except sqlite3.OperationalError:
                embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content == "ㄷ정보":
            try:
                con = sqlite3.connect(str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()
                if (user_info == None):
                    embed = discord.Embed(description="가입이 되어있지 않습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)
                else:
                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                    user = cur.fetchone()
                    cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                    mineral = cur.fetchone()
                    embed = discord.Embed(title=f"{message.author.name}님의 정보", color=0xffffff)
                    embed.add_field(name="자금", value=user[1], inline=False)
                    embed.add_field(name="곡괭이", value=user[2], inline=False)
                    embed.add_field(name="광물", value=f"철: {mineral[1]}개\n금: {mineral[2]}개\n에메랄드: {mineral[3]}개\n루비: {mineral[4]}개\n다이아몬드: {mineral[5]}개\n레드 다이아몬드: {mineral[6]}개")
                    await message.channel.send(embed=embed)
                    con.close()
            except sqlite3.OperationalError:
                embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)
    
    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content == "ㄷ곡괭이 강화":
            try:
                con = sqlite3.connect(str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()
                if (user_info == None):
                    embed = discord.Embed(description="가입이 되어있지 않습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)
                else:
                    con = sqlite3.connect(str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                    pickax = cur.fetchone()
                    if pickax[2] == "플라스틱 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 2000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("철 곡괭이", "금 곡괭이", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(200000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="다음 곡괭이: 금 곡괭이\n강화비용: 50000원", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 20000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "철 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 50000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("금 곡괭이", "에메랄드 곡괭이", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(500000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="다음 곡괭이: 에메랄드 곡괭이\n강화비용: 100000원", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 50000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "금 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 200000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("에메랄드 곡괭이", "루비 곡괭이", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(2000000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="다음 곡괭이: 에메랄드 곡괭이\n강화비용: 200000원", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 200000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "에메랄드 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 400000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("루비 곡괭이", "다이아몬드 곡괭이", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(4000000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="다음 곡괭이: 다이아몬드 곡괭이\n강화비용: 800000원", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 400000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "루비 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 800000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("다이아몬드 곡괭이", "레드 다이아몬드 곡괭이", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(8000000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="다음 곡괭이: 다이아몬드 곡괭이\n강화비용: 1400000원", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 800000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "다이아몬드 곡괭이":
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        money = cur.fetchone()
                        if money[1] >= 1400000:
                            cur.execute("UPDATE users SET pickax = ?, NextPickax = ? WHERE id == ?;", ("레드 다이아몬드 곡괭이", "더이상 강화 가능한 곡괭이가 없습니다.", message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (int(money[1]) - int(14000000), message.author.id))
                            con.commit()
                            embed = discord.Embed(title="곡괭이 강화 성공", description="더이상 강화 가능한 곡괭이가 없습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="곡괭이 강화 실패", description="잔액이 부족합니다.\n강화비용: 1400000원", color=0xff0000)
                            await message.channel.send(embed=embed)
                    if pickax[2] == "레드 다이아몬드 곡괭이":
                        embed = discord.Embed(title="곡괭이 강화 실패", description="더이상 강화 가능한 곡괭이가 없습니다.", color=0xff0000)
                        await message.channel.send(embed=embed)
            except sqlite3.OperationalError:
                embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content == "ㄷ광질":
            try:
                con = sqlite3.connect(str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()
                if (user_info == None):
                    embed = discord.Embed(description="가입이 되어있지 않습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="광질 시작", description=f"5초를 기다려주세요.", color=0xffffff)
                    await message.channel.send(embed=embed)
                    con = sqlite3.connect(str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                    pickax = cur.fetchone()
                    if pickax[2] == "플라스틱 곡괭이":
                        number = random.choice([1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10])
                        mineral_kind = random.choice(["철", "철", "철", "철", "철", "철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "철 곡괭이":
                        number = random.choice([2, 2, 2, 2, 2, 2, 4, 4, 4, 6, 6, 8, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 18, 20])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "금 곡괭이":
                        number = random.choice([4, 4, 4, 4, 4, 4, 8, 8, 8, 9, 9, 16, 16, 20, 20, 24, 24, 28, 28, 32, 32, 36, 36, 40])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "에메랄드 곡괭이":
                        number = random.choice([8, 8, 8, 8, 8, 8, 16, 16, 16, 24, 24, 32, 32, 40, 40, 48, 48, 56, 56, 64, 64, 72, 72, 80])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "루비 곡괭이":
                        number = random.choice([16, 16, 16, 16, 16, 16, 32, 32, 32, 48, 48, 64, 64, 80, 80, 96, 96, 112, 112, 128, 128, 142, 142, 160])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "다이아몬드 곡괭이":
                        number = random.choice([32, 32, 32, 32, 32, 32, 64, 64, 64, 96, 96, 128, 128, 160, 160, 192, 192, 224, 224, 264, 264, 284, 284, 320])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "다이아몬드 곡괭이":
                        number = random.choice([50, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 200, 300, 300, 300, 300, 500, 500, 500, 500, 500, 500, 1000])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
                    if pickax[2] == "레드 다이아몬드 곡괭이":
                        number = random.choice([100, 100, 100, 100, 100, 100, 400, 400, 400, 400, 400, 800, 800, 1200, 1200, 1200, 1200, 1600, 1600, 2400, 2400, 2400, 2400, 10000])
                        mineral_kind = random.choice(["철", "금", "금", "금", "금", "금", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "에메랄드", "루비", "루비", "루비", "루비", "다이아몬드", "다이아몬드", "다이아몬드", "레드 다이아몬드"])
                        await asyncio.sleep(5)
                        if mineral_kind == "철":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            iron = int(mineral[1]) + int(number)
                            cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (iron, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "금":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            gold = int(mineral[2]) + int(number)
                            cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (gold, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "에메랄드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            emerald = int(mineral[3]) + int(number)
                            cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (emerald, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "루비":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            ruby = int(mineral[4]) + int(number)
                            cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (ruby, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            diamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (diamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        if mineral_kind == "레드 다이아몬드":
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            mineral = cur.fetchone()
                            reddiamond = int(mineral[5]) + int(number)
                            cur.execute("UPDATE reddiamond SET diamond = ? WHERE id == ?;", (reddiamond, message.author.id))
                            con.commit()
                            embed = discord.Embed(title="채굴 성공", description=f"{mineral_kind} {number}개를 얻으셨습니다.", color=0xffffff)
                            await message.channel.send(embed=embed)
                        con.close()
            except sqlite3.OperationalError:
                embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content == "ㄷ광물 가격":
            embed = discord.Embed(title="광물 가격", description="철: 1000원\n금: 1500원\n에메랄드: 2000원\n루비: 2500원\n다이아몬드: 3000원\n레드 다이아몬드: 6000원", color=0xffffff)
            await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content.startswith("ㄷ판매"):
            con = sqlite3.connect(str(message.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if (user_info == None):
                embed = discord.Embed(description="가입이 되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)
            else:
                try:
                    main = message.content[4:]
                    mineral = main.split(" ")[0]
                    if mineral == "레드":
                        mineral = "레드 다이아몬드"
                        number = main.split(" ")[2]
                        if mineral == "레드 다이아몬드":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[6]):
                                cur.execute("UPDATE mineral SET reddiamond = ? WHERE id == ?;", (int(iron_number[6]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 6000 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="레드 다이아몬드", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(6000 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                    else:
                        number = main.split(" ")[1]
                        if mineral == "철":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[1]):
                                cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (int(iron_number[1]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 1000 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="철", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(1000 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                        if mineral == "금":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[2]):
                                cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (int(iron_number[2]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 1500 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="금", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(1500 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                        if mineral == "에메랄드":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[3]):
                                cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (int(iron_number[3]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 2000 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="에메랄드", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(2000 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                        if mineral == "루비":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[4]):
                                cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (int(iron_number[4]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 2500 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="루비", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(2500 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                        if mineral == "다이아몬드":
                            con = sqlite3.connect(str(message.guild.id) + ".db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                            iron_number = cur.fetchone()
                            if int(number) <= int(iron_number[5]):
                                cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (int(iron_number[5]) - int(number), message.author.id))
                                con.commit()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                money = cur.fetchone()
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + 3000 * int(number)), message.author.id))
                                con.commit()
                                embed = discord.Embed(title="판매 성공", color=0xffffff)
                                embed.add_field(name="판매 광물", value="다이아몬드", inline=False)
                                embed.add_field(name="판매 갯수", value=str(number) + "개", inline=False)
                                embed.add_field(name="판매금", value=str(3000 * int(number)) + "원", inline=False)
                                await message.channel.send(embed=embed)
                                con.close()
                            else:
                                embed = discord.Embed(title="판매 실패", description="가지고 계신 갯수보다 더 많이 입력하셨습니다.", color=0xff0000)
                                await message.channel.send(embed=embed)
                except sqlite3.OperationalError:
                    embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if message.content == ("ㄷ전부 판매"):
            con = sqlite3.connect(str(message.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if (user_info == None):
                embed = discord.Embed(description="가입이 되어있지 않습니다.", color=0xff0000)
                await message.channel.send(embed=embed)
            else:
                try:
                    cur.execute("SELECT * FROM mineral WHERE id == ?;", (message.author.id,))
                    minerals = cur.fetchone()
                    iron = int(minerals[1]) * 1000
                    gold = int(minerals[2]) * 1500
                    emerald = int(minerals[3]) * 2000
                    ruby = int(minerals[4]) * 2500
                    diamond = int(minerals[5]) * 3000
                    reddiamond = int(minerals[6]) * 6000
                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                    money = cur.fetchone()
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (str(int(money[1]) + int(iron) + int(gold) + int(emerald) + int(ruby) + int(diamond) + int(reddiamond)), message.author.id))
                    con.commit()
                    cur.execute("UPDATE mineral SET iron = ? WHERE id == ?;", (0, message.author.id))
                    cur.execute("UPDATE mineral SET gold = ? WHERE id == ?;", (0, message.author.id))
                    cur.execute("UPDATE mineral SET emerald = ? WHERE id == ?;", (0, message.author.id))
                    cur.execute("UPDATE mineral SET ruby = ? WHERE id == ?;", (0, message.author.id))
                    cur.execute("UPDATE mineral SET diamond = ? WHERE id == ?;", (0, message.author.id))
                    cur.execute("UPDATE mineral SET reddiamond = ? WHERE id == ?;", (0, message.author.id))
                    con.commit()
                    embed = discord.Embed(title="판매 성공", description="판매 금액: " + str(int(iron) + int(gold) + int(emerald) + int(ruby) + int(diamond) + int(reddiamond)) + "원",color=0xffffff)
                    await message.channel.send(embed=embed)
                    con.close()
                except sqlite3.OperationalError:
                    embed = discord.Embed(description="서버가 등록되어있지 않습니다.", color=0xff0000)
                    await message.channel.send(embed=embed)
access_token = os.environ["BOT TOKEN"]
client.run(access_token)
