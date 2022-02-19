# Formula 1 Discord Bot 

Due to the off season, the bot is disabled. Feel free to come back when the F1 2022 season starts.

Join the server and try it out for yourself: https://discord.gg/kcBUXGfR

This project allows you to write commands to discord bot which sends back the most important information about latest Formula 1 events inlcuding:
* last race results ⟶ !last-race
* last quailfying results ⟶ !last-quali
* constructor standings ⟶ !constructor-standings
* drivers standings ⟶ !drivers-standings
* schedule of events ⟶ !schedule
* next race information ⟶ !next-race

![](images/quali.PNG)

# Functionality to implement
* betting race winners on discord with full leaderboard to play in close communities
* sending notifications about incoming events

# Technologies
All of the data about races is gathered from Ergast Developer API - http://ergast.com/mrd/
- python
- docker
- docker-compose
## Python modules
* requests
* discord.py
* BeautifulSoup

## Docker and docker-compose

This bot on my discord server is running in docker container on local raspberry pi 24/7.