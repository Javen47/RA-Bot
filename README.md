# RA-Bot
A discord bot for handling the responsibilities of a college Resident Assistant (RA).

This project is the core functionality of a discord bot. Meaning, the commands or the "brain" of the bot are included here. Whoever uses this project still must create the "shell" of the bot (the bot profile that is shown on the discord server). This is not a hard task to do, and there are plenty of tutorials online.

How to setup the bot:

  0.) Prerequisites:
  
        - Python interpreter
        - Python pip installer
        - A dedicated machine for running the RA-bot script

  1.) Set up the following discord components to create the "shell" of the bot:
  
      - An account (an existing account is fine)
      - A developer application (free and easy to do)
      - A bot (through the developer application)
      - An actual discord server (also referred to as a guild)

  2.) Run the following pip commands in the command line to be able to run the project:
  
      - pip install -U python-dotenv
      - pip install -U discord.py
  
  3.) Download or clone the project.
  
  4.) Edit the '.env' file within the project folder:
    
        - 'DISCORD_TOKEN' is where the unique token from your bot in the discord application will go.
        - 'DISCORD_GUILD' is the exact name of your discord server.
  
  4.) Open command line in the directory of your project folder.
  
  5.) Run the following command:
  
    python bot.py
    
    