import os
import pygame.mixer
from statistics import quantiles
import time
import pygame.time
import pickle  # Imports the pickle module for serialization.
import winsound
import random
import pygame
import webbrowser
global location,money,security,player_money
def initialize_steam_api():
    # Placeholder for initializing the Steam API
    steam.init()
def authenticate_user():
    # Placeholder for authenticating the user using Steam API
    user_id = steam.get_user_id()
    if user_id:
        print("User authenticated successfully.\n")
    else:
        print("Failed to authenticate user.")

def text_to_speech(text):
    # Initialize the text-to-speech engine.
    engine = pyttsx3.init()
    # Set properties (optional).
    engine.setProperty('rate', 140)  # Speed of speech.
    engine.setProperty('volume', 0.7)  # Volume (0.0 to 1.0).
    # Convert text to speech
    engine.say(text)
    # Wait for speech to finish.
    engine.runAndWait()

try:
    import pyttsx3
except ImportError:
    print("Error: pyttsx3 module not found.\n")
    text="Error: pyttsx3 module not found."
    text_to_speech(text)
    time.sleep(3.25)
    quit()

#used for opening up external links (what happens if they dont have a browser to open up the link with?).
def open_link(url):
    webbrowser.open(url)

# ANSI color code.
class Colors:
    #standard color palate.
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    # Color-blind friendly color palette.
    # Define alternative colors that are easily distinguishable.
    # Example: RED = '\033[38m', GREEN = '\033[44m', etc.

SAVE_SOUND = "save_sound.wav"
LOAD_SOUND = "load_sound.wav"
SOUND_FILES = ["sound1.wav", "sound2.wav", "sound3.wav", "sound4.wav"]

# Defines initial variables.
iron_gym_security = 0
iron_gym_money = 1000
hacking_level = 1
player_money = 100
apartment_security = 3
apartment_money = 2500
foodnstuff_security = 10
foodnstuff_money = 10000
bank_money = 1000000
bank_security = 100

# Function to save game state
def save_game():
    # Create a dictionary containing the game state.
    game_state = {
        'iron_gym_security': iron_gym_security,
        'iron_gym_money': iron_gym_money,
        'hacking_level': hacking_level,
        'player_money': player_money,
        'apartment_security': apartment_security,
        'apartment_money': apartment_money,
        'foodnstuff_security': foodnstuff_security,
        'foodnstuff_money': foodnstuff_money,
        'bank_money': bank_money,
        'bank_security': bank_security,
        'last_played': time.time()  # Add last played timestamp
    }

    # Opens a file in binary write mode.
    with open('savegame.dat', 'wb') as f:
        # Serializes the game state dictionary and write it to the file.
        pickle.dump(game_state, f)

    print("Game saved.\n")
    winsound.PlaySound(SAVE_SOUND, winsound.SND_FILENAME)

# Function to load game state
def load_game():
    global iron_gym_security, iron_gym_money, hacking_level, player_money, \
        apartment_security, apartment_money, foodnstuff_security, foodnstuff_money,bank_money,bank_security

    if os.path.exists('savegame.dat'):
        # Opens the savegame file in binary read mode.
        with open('savegame.dat', 'rb') as f:
            # Deserializes the data and load the game state dictionary.
            game_state = pickle.load(f)

        # Updates the game variables with the loaded data.
        iron_gym_security = game_state['iron_gym_security']
        iron_gym_money = game_state['iron_gym_money']
        hacking_level = game_state['hacking_level']
        player_money = game_state['player_money']
        apartment_security = game_state['apartment_security']
        apartment_money = game_state['apartment_money']
        foodnstuff_security = game_state['foodnstuff_security']
        foodnstuff_money = game_state['foodnstuff_money']
        bank_money = game_state['bank_money']
        bank_security = game_state['bank_security']
        last_played = game_state.get('last_played', 0)  # Get last played timestamp

        # Calculate idle earnings based on elapsed time since last played
        elapsed_time = time.time() - last_played
        idle_earnings = calculate_idle_earnings(elapsed_time)

        # Add idle earnings to player's money
        player_money += idle_earnings

        print('\033[32m' + "Game loaded.\n" + '\033[0m')
        text = ("Game loaded.")
        text_to_speech(text)
    else:
        print('\033[31m' + "No saved game found.\n" + '\033[0m')
        text = "No saved game found."
        text_to_speech(text)

# Function to calculate idle earnings based on elapsed time
def calculate_idle_earnings(elapsed_time):
    # Define your idle earnings logic here
    # Example: Earn 1 money every hour
    eph = 1
    return (elapsed_time / 3600) * eph



@staticmethod
def dice_roll():
    #defines the dice roll game that is the minigame that pops up when you use the hack command.
    print("Welcome to the Dice Rolling Mini-Game!\n")
    print("Roll the dice and guess if the result will be odd or even.")
    
    roll = random.randint(1, 6)
    guess = input("Enter your guess (odd/even): ").lower()

    if (guess == "odd" and roll % 2 != 0) or (guess == "even" and roll % 2 == 0):
        print('\033[32m'+f"The dice rolled a {roll}. You win!")
        player_money += 0.1 * money
        money *= 0.9
        security *= 1.1
        hacking_level += 0.1
        print("Let the hacking commence.\n")
        delay_animation()
        print("You now have", player_money,"$.\n")
        save_game()
        location()          
    else:
        print(f"The dice rolled a {roll}. You lose!\n")
        show_map()

def shop():
    global hacking_level, player_money
    buy = input("1 hacking level - 1000$\n"
                "99 $ - 100$\n"
                "EPH (Idle earnings per hour) + 1 - 100$\n"
                "Type map to go back to the map.\n").lower()
    if buy == "1 hacking level" or buy == "hacking level" or buy == "level":
        if player_money >= 1000:
            player_money-=1000
            hacking_level += 1
            save_game()
            shop()
    elif buy == "99$" or buy == "99" or buy == "$":
        if player_money >= 100:
            player_money -= 1
            save_game()
            shop()
    elif buy == "map":
        show_map()
    elif buy== "eph" or buy=="eph(earningsperhour)" or buy == "earningsperhour":
        eph+=1 
        shop()
         
    else:
        print('\033[31m' +"That is not a item in the shop.\n"+'\033[0m')
        shop()
        
def clear_screen():
    # Clears the screen.
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def delay_animation():
    print("-")
    time.sleep(0.5)
    clear_screen()
    print("--")
    time.sleep(0.5)
    clear_screen()
    print("---")
    time.sleep(0.5)
    clear_screen()
    print("----")
    time.sleep(0.5)
    clear_screen()
    
class MiniGames:
    @staticmethod
    def memory_match():
        print("Welcome to the Memory Matching Mini-Game!\n")
        print("Try to match pairs of cards in as few attempts as possible.\n")

        cards = ["A", "B", "C", "D", "E", "F"] * 2
        random.shuffle(cards)
        revealed = [False] * len(cards)

        attempts = 0
        matched_pairs = 0

        while matched_pairs < len(cards) // 2:
            print(" ".join(card if revealed[i] else "?" for i, card in enumerate(cards)))

            indices = input("Enter the indices of two cards (e.g., '0 1'):\n").split().lower()
            if len(indices) != 2:
                print('\033[31m' +"Invalid input. Please enter two indices separated by a space.\n"+'\033[0m')
                continue

            index1, index2 = map(int, indices)

            if index1 == index2 or revealed[index1] or revealed[index2]:
                print('\033[31m' +"Invalid selection. Please choose two unrevealed cards.\n"+'\033[0m')
                continue

            if cards[index1] == cards[index2]:
                matched_pairs += 1
                print('\033[32m'+"Match found!\n"+'\033[0m')
            else:
                print("No match.")

            revealed[index1] = revealed[index2] = True
            attempts += 1

        print('\033[32m'+f"Congratulations! You completed the game in {attempts} attempts.\n"+'\033[0m')
        show_map()



def actions(location, security, money):
    global hacking_level, player_money
    action = input("Type 'help' for a list of commands and their functions.\n").lower()
    if action == "map":
            show_map()
    elif action == "hack":
            if hacking_level > security:
                dice_roll()
            else:
                print('\033[31m' +"Oops, that did not work. It seems that your hacking level of", hacking_level,
                      "is not high enough.\n"+'\033[0m')
                actions(location, money, security)
    elif action == "weaken":
            delay_animation()
            security *= 0.95
            hacking_level += 0.05
            save_game()
            actions(location, money, security)
    elif action == "grow":
            if hacking_level>security:
                q=input("The minigame for the grow command is still under development, so for now ill let you decide if you want to play the mingame, do you want to play the minigame?\n").lower()
                if q== "yes" or q== "y":
                    delay_animation()
                    run_snake_game()
                else:
                    money *= 1.1
                    security*=1.1
                    hacking_level+=0.05
                    save_game()
                    actions(location, money, security)
               
    elif action == "stats":
            print("Money:", player_money,"$.\n")
            print("Hacking level:", hacking_level,".\n")
            print("Apartment security:", apartment_security,".\n")
            print("Apartment money:", apartment_money,"$.\n")
            print("Iron gym security:", iron_gym_security,".\n")
            print("Iron gym money:", iron_gym_money,"$.\n")
            print("Foodnstuff security:", foodnstuff_security,".\n")
            print("Foodnstuff money:", foodnstuff_money,"$.\n")
            print("Bank security:", bank_security,".\n")
            print("Bank money:", bank_money,"$.\n" )
            print("Your current location is", location,".\n")
            actions(location, money, security)
    elif action == "def stats" or action == "def stat" or action == "def statistics":
            print("The statistics command shows your hacking level, your money, the security of places,"
                  "the amount of money places have, and your current location.")
            actions(location, money, security)
    elif action == "def def":
            print("This is the command that you are using right now. It provides more in-depth information "
                  "on commands from the help menu.")
            actions(location, money, security)
    elif action == "def hack":
            print("This is a basic command that is used to hack into places' accounts to take their money.\n"
                  "The formula for money gained is 0.1 times the current money of said location.\n"
                  "The security of the place then goes up by 10% and you gain 10% of a level.")
            actions(location, money, security)
    elif action == "save":
            save_game()
            print("Sending you to the console.")
            console()
    elif action == "load":
            load_game()
            print("Sending you to the console.")
            console()
    elif action == "def load":
            print("This commands loads your most recent game save.")
            print("Sending you to the console.")
            console()
    elif action == "def save":
            print("This command saves your current gamestate for use later.")
            print("Sending you to the console.")
            console()
    elif action == "def grow":
            print("This command increases the amount of money in the target by 10% but also increases the\n "
                  "security level by the same amount, and you gain 5% of a level.\n")
            actions(location, money, security)
    elif action == "def weaken":
            print("This command weakens the target security level by 5%, and gives you 5% of a level.\n")
            actions(location, money, security)
    elif action == "def console":
            print("This command opens up the console witch you can use to perform commands that are not\n"
                  "specific to the place that you are in.\n")
            console()
    elif action == "console":
            print("Sending you to the console.")
            console()
    elif action == "help":
            print_help()
    else:
            print('\033[31m' +"You can't do that.\n"+'\033[0m')
            print_help()


def print_help():
    print(
        "Hack - Allows you to infiltrate a system and take some of their money. For more information on how this command works, use the command 'def {command name}'.\n"
        "Weaken - This command weakens the target security system.\n"
        "Grow - This command increases the amount of money in the target's bank accounts, thus allowing you to take more money.\n"
        "Map - Redirects you back to the map.\n"
        "Stats - Shows your current statistics.\n"
        "Def - Gives you more specific information on commands.\n"
        "Save - Saves your current game.\n"
        "Load - Loads your last save, if you want to make a new save then just don't load your last save and save on the new game.\n"
        "Console - Opens a screen for you to run general commands.\n")
    time.sleep(5)
    actions(location, security, money)
    

def com():
    command = input("Type the commands that you wish to use; note that you cannot use the hack, grow, and weaken commands, uh, I guess also the console command.\n").lower()
    if command == "stats" or command == "stat" or command == "statistics":
        print("Money:", player_money,"$.\n")
        print("Hacking level:", hacking_level,".\n")
        print("Apartment security:", apartment_security,".\n")
        print("Apartment money:", apartment_money,"$.\n")
        print("Iron gym security:", iron_gym_security,".\n")
        print("Iron gym money:", iron_gym_money,"$.\n")
        print("Foodnstuff security:", foodnstuff_security,".\n")
        print("Foodnstuff money:", foodnstuff_money,"$.\n")
        print("Bank money:",bank_money,"$.\n")
        print("Bank security:",bank_security,".\n")
        show_map()
    elif command == "help":
        print_help()
    elif command == "def stats":
        print("The statistics command shows your hacking level, your money, the security of places, the amount of money places have, and your current location.")
        com()
    elif command == "def def":
        print("This is the command that you are using right now. It provides more in-depth information on commands from the help menu.\n")
        print_help()
    elif command == "def help":
        print("This is a basic command that is used to hack into places' accounts to take their money. The formula for money gained is 0.1 times the current money of said "
              "location.\n")
        print("The security of the place then goes up by 10% and you gain 10% of a level.\n")
        com()
    elif command == "save":
        save_game()  # Corrected function call.
        console()
    elif command == "load":
        load_game()
        console()
    elif command == "credits" or command == "credit":
        print ("Made by Casper aka: Julie.\n")
        print("Inspired by Bitsburner.\n")
        print ("Bug tested by Casper, Freinds, Family, And ChatGPT.\n")
        print("Made in python.\n")
        print("Played by you (:\n")
        show_map()
    elif command =="def credits" or command == "def credit":
        print("Opens up the credits.\n")
        actions(location,security,money)
    elif command == "def load":
        print("This commands loads your most recent game save.\n")
        com()
    elif command == "def save":
        print("This command saves your current game-state for use later.\n")
        com()
    elif command == "def grow":
        print("This command increases the amount of money in the target by 10% but also increases the security level by the same amount, and you gain 5% of a level.\n")
        com()
    elif command == "def weaken":
        print("This command weakens the target security level by 5%, and gives you 5% of a level.\n")
        com()
    elif command == "def console":
        print("This command opens up the console witch you can use to perform commands that are not specific to the place that you are in.\n")
        com()
    elif command == "map":
        show_map()
    elif command == "def map":
        print("This command opens up the map.\n")
        com()
    else:
        print('\033[31m' +"That is not a valid command.\n"+'\033[0m')
        print_help()

def show_map():
    print('\033[0m'+"Welcome to a Text-Based Hacker Adventure Game!\n")
    print("You find yourself in a bustling town. Your goal is to navigate through different locations and hack into systems to earn money.")
    location = input("\n|"
                     "\n|"
                     "\n+--------+------+-------+---------+"
                     "\n| Iron   | Home | Foodn | bank    |"
                     "\n| Gym    |      | stuff |         |"
                     "\n+--------+------+-------+---------+"
                     "\n| Apart  | shop |   unfinished    |"
                     "\n| Ment   |      |   lot           |"
                     "\n| Complex|      |                 |"
                     "\n|        |      |                 |"
                     "\n+--------+------+-----------------+"
                     "\n|        "
                     "\n|        "
                     "\n|        "
                     "\n|"
                     "\n|"
                     "\n|"
                     "\n|"
                     "\n|"
                     "\nThis is a map of the town. Type in the name of the place where you would like to do stuff, or type help for a list of commands.\n"
                     '\033[1m'+"Important: if you use the help menu after going to a location you will have to return to that location in order to run commands.\n"+'\033[0m').lower()
    if location == "iron gym" or location == "irongym":
        print('\033[34m'+"You arrive at the Iron Gym. Once a bustling hub for fitness enthusiasts, now it stands abandoned and overrun by hackers looking to exploit its neglected security systems for financial gain.\n"+'\033[0m')
        actions(location, iron_gym_security, iron_gym_money)
    elif location == "apartment complex":
        print('\033[34m'+"You arrive at the Apartment Complex. This area is known for its high level of security, but rumors suggest that its digital defenses might have vulnerabilities waiting to be exploited.\n"+'\033[0m')
        actions(location, apartment_security, apartment_money)
    elif location == "foodnstuff" or location == "food n stuff":
        print('\033[34m'+"You find yourself at FoodnStuff. It's a massive supermarket chain with a robust security system to protect its valuable assets.\n"+'\033[0m')
        actions(location, foodnstuff_security, foodnstuff_money)
    elif location == "bank":
        print("You arrive at the bank, its a bank; what do you expect it has alot of money and a very high security system. Hackers have been trying to infiltrate this bank for years and only 2 people have been succesfull.\n")
        print("Now that I think about it that's actually alot.\n")
        actions(location, bank_security, bank_money)     
    elif location == "home":
        print('\033[34m'+"You go back to your house and store your winnings for the day.\n"+'\033[0m')
        print("Jeez maybe you could get some hacking levels and unlock something here, who knows?\n")
        time.sleep(5)
        if hacking_level>=11:
            print('\033[1m'+"There is a easteregg that you can access in on the map by typing something.\n"+'\033[0m') 
            show_map()
        else:
            a=input("\nWould you like to go back to the console or back to the map?\n").lower()
            if a== "console":
                console()
            elif a== "map":
                show_map() 
            else:
                show_map() 
     #If you look at this part of the code it will ruin the easter egg ):
    elif location == "easter egg" or location == "easteregg":
        print('\033[32m'+"Congratulations, you have found an Easter egg!\n"+'\033[0m')
        minigame = input("Now you can play a secret mini-game. Select the difficulty (1-10).\n").lower()
        try:
            minigame = int(minigame)
            if 1 <= minigame <= 10:
                lockpicking_mini_game(minigame)
            else:
                print('\033[31m' +"Sorry, but that difficulty is not allowed.\n"+'\033[0m')
                show_map()
        except ValueError:
            print('\033[31m' +"Invalid input. Please enter a number between 1 and 10.\n"+'\033[0m')
            print("Returning you back to the map.\n")
            delay_animation()
            show_map()

    elif location == "console":
        console()
    elif location == "rickroll" or location == "rick roll":
        url= "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        open_link(url)
        show_map()
    elif location == "help":
        print_helpmap()
    elif location =="shop":
        place = input("Would you like to buy some upgrades?\n").lower()
        if place == "yes":
            shop()
        else:
            print("Ok then.\n")
            show_map()
    else:
        print('\033[31m' +"That is not a place in the town.\n"+'\033[0m')
        print("Returning you to the map.\n")
        delay_animation()
        show_map()


def console():
    clear_screen()
    com()


def lockpicking_mini_game(difficulty):
    print("Welcome to the lockpicking mini-game!\n")
    print("You are attempting to pick a lock of difficulty level",difficulty,".\n")
    print("You must turn the lock's tumblers to the correct positions to unlock it.\n")

    # Generate a random combination for the lock based on difficulty.
    lock_combination = [random.randint(0, 9) for _ in range(difficulty)]

    # Player's attempt at picking the lock.
    player_attempt = []

    # Allow the player to attempt to pick the lock.
    for tumbler_index in range(difficulty):
        print("Tumbler", tumbler_index + 1)
        player_guess = int(input("Enter a number (0-9) to turn the tumbler:\n "))
        player_attempt.append(player_guess)

    # Check if the player's attempt matches the lock combination.
    if player_attempt == lock_combination:
        print ('\033[32m'+"Congratulations! You successfully picked the lock!\n"+'\033[0m')
        player_money+=500*difficulty
        hacking_level+=0.1*difficulty
        show_map()
    else:
        print('\033[31m' +"Sorry, the lock remains locked. Better luck next time.\n"+'\033[0m')
    show_map()
def print_helpmap():
    print(
        "Hack - Allows you to infiltrate a system and take some of their money. For more information on how this command works, use the command 'def {command name}'.\n"
        "Weaken - This command weakens the target security system.\n"
        "Grow - This command increases the amount of money in the target's bank accounts, thus allowing you to take more money.\n"
        "Map - Redirects you back to the map.\n"
        "Stats - Shows your current statistics.\n"
        "Def - Gives you more specific information on commands.\n"
        "Save - Saves your current game.\n"
        "Load - Loads your last save, if you want to make a new save then just don't load your last save and save on the new game.\n"
        "Console - Opens a screen for you to run general commands.\n"
        "Credits - Opens up the credits menu.\n")
    time.sleep(5)
    show_map

# Define screen dimensions and colors.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define directions.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class, the class for snakes.
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED

    def get_head_position(self):
        # Return the position of the snake's head.
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False  # Snake collided with itself.
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))


# Food class, the class for food.
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (0, 255, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

def run_snake_game():
    # Initialize Pygame.
    pygame.init()

    # Create screen.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')

    # Set up the game clock.
    clock = pygame.time.Clock()

    # Create snake and food objects.
    snake = Snake()
    food = Food()

    # Set initial food count and win condition.
    food_count = 0
    win_condition = 10

    # Set the snake update frequency (updates per second).
    snake_update_frequency = 250

    # Boolean variable to track invincibility.
    invincible = True
    # Other methods of the Snake class...

# Modify the main loop to use the updated Snake class.
    # Main loop.
    running = True
    while running:
        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Check for the first control input to end invincibility.
                if invincible:
                    invincible = False
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        # Update snake movement periodically based on update frequency.
        if pygame.time.get_ticks() % (1000 // snake_update_frequency) == 0:
            # Check for invincibility before moving the snake.
            if not invincible:
                head_position=snake.get_head_position()
                if (head_position[0] <= 0 or head_position[0] >= SCREEN_WIDTH or
                head_position[1] <= 0 or head_position[1] >= SCREEN_HEIGHT or
                snake.hits_self()):
                    running = False
                    pygame.quit()
                    show_map()
                # Check if snake eats food.
                if snake.get_head_position() == food.position:
                    snake.length += 1
                    food.randomize_position()
                    food_count += 1

        # Draw everything.
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()

        # Limits the frame rate.
        clock.tick(80)  # Adjust frame rate as needed.

        # Check win condition.
        if food_count >= win_condition:
            font = pygame.font.SysFont(None, 36)
            text = font.render('You Win!', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            food_count = 0
            win_condition = 10
            pygame.time.wait(2000)  # Display "You Win!" message for 2 seconds.
            money *= 1.1
            security *= 1.1
            hacking_level += 0.05
            save_game()
            pygame.quit()
            actions(location, money, security)



# Entry point for the program.
if __name__ == "__main__":
    show_map()
    while True:
        game_result = run_snake_game()  # Run the Snake game.
        if not game_result:
            print("You lost the game!\n")
            food_count = 0
            win_condition = 10
            show_map()  # Return to the show_map function.
def start_game():
    init_steam() 
    show_map()

# Used to start the game and also used to show the map as the name of the defined function implies.
start_game()