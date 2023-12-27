import random
import time
import os
from replit import db
import json
import requests
import colorama
from colorama import Fore, Back, Style
import datetime
import threading
import time

user_money = 0
used=False
used_T=False

ADMINS = ['Cluefixx',"AFK"]

def account_authentication():
  def get_username():
    if "logged_in_user" in db:
        print(f"User '{db['logged_in_user']}' is already logged in.")
        return db["logged_in_user"]
    else:
        username = input("Please enter your username: ")
        db["logged_in_user"] = username
        return username

  def check_banned_status(username, json_file):
      with open(json_file, 'r') as file:
          data = json.load(file)

      for entry in data.get("bans", []):
          if entry["user"] == username:
              exit(print(f"{Fore.RED}You are banned from using this game for: {Fore.BLUE} {entry['reason']}{Fore.RESET}"))
              #original: exit(print(f"{colorama.Fore.RED}You are banned from using this game for: {banned_users[USER]}{colorama.Fore.RESET}"))

  username = get_username()

  json_file_path = 'bans.json'

  check_banned_status(username, json_file_path)

def start_program():
  account_authentication()

#ads

ads = [
    "Want your own Ad? Type it in the comments! 50 slots left",

    "Want your own Ad? Type it in the comments! 50 slots left",

    "Want your own Ad? Type it in the comments! 50 slots left",

    "Want your own Ad? Type it in the comments! 50 slots left",
]

def display_ad():
    while True:
        ad = random.choice(ads)

        print(f"Ad: {ad}")

        time.sleep(600)

ad_thread = threading.Thread(target=display_ad)
ad_thread.daemon = True
ad_thread.start()

#ads
os.system('clear')
if os.name in ["nt", "dos"]:
  USER = str(os.getlogin())
elif os.name in ["posix"]:
  USER = str(os.environ.get("REPL_OWNER"))
else:
  USER = str(os.environ.get("USERNAME"))
  if USER == "None":
      USER = str(os.path.expanduser("~"))
      if USER == "None":
          USER = "User"
USERidhash_step1 = hash(USER)
USERidhash = bin(USERidhash_step1)
SER_KEY = USER + '_user_money'
INVENTORY_KEY = USER + '_inventory'
SAVE_FILE = 'inventory_save.json'
api_url = "http://example.com"
response = requests.get(api_url)
data = response.text
s = data[:-1]

def load_game():
  global user_money, total_money_spent, inventory
  saved_data = db.get(SER_KEY)
  if saved_data:
      try:
          data = json.loads(saved_data)
          user_money = data.get('user_money', 0)
          used_T = data.get('used_T', "")
          total_money_spent = data.get('total_money_spent', 0)

          inventory = data.get('inventory', [])
      except json.JSONDecodeError:
          user_money = 0
          total_money_spent = 0
          inventory = []
          print("Error loading game data. Starting new game.")
  else:
      print("No saved game found. Starting new game.")
      user_money = 0
      used_T=False
      total_money_spent = 0
      inventory = []
load_game()
def load_cases_from_file(file_name):
  cases = {}
  with open(file_name, 'r') as file:
      data = file.read()
      cases = eval('{' + data + '}')
  return cases

file_name = 'cases_data.txt'
Cases = load_cases_from_file(file_name)

def display_message(message):
    input(f'{message} [Press Enter to continue]')
    os.system('clear')


def tutorial_guide():
    print(f"Playid: {hash(USER)}")
    ask = input(f"Do you want a tutorial {Fore.BLUE}y{Fore.LIGHTGREEN_EX}/{Fore.RED}n{Fore.RESET}: ")

    if ask.lower() == 'y':
        os.system('clear')

        print("Welcome! Here's a quick guide to get started:\n")
        print("1. To open a case, use commands like:")
        print("\\ open freecase / .|. \\ open casename / .|. \\ open casename x<amount> /")
        display_message('Try the commands for opening cases')

        print("2. Lock and unlock items using:")
        print("\\ lock /  - This prevents items from being sold")
        print("\\ unlock / - Unlock the items for selling")
        display_message('Learn how to lock and unlock items')

        print("3. Check your leaderboard position with:")
        print("\\ leaderboard /")
        display_message('Explore the leaderboard feature')

        print("4. View your inventory and sell items:")
        print("\\ inv / - See your inventory\n\\ sell x1-inf / - Sell items")
        print("\\ sellall / - Sell all your items")
        display_message('Check inventory and learn to sell items')

        print("5. Visit the shop for rare items:")
        print("\\ shop / - Purchase rare items")
        display_message('Explore the shop feature')

        print("6. Obtain data about an item using:")
        print("\\ data itemname /")
        display_message('Learn how to retrieve item data')

        print("7. Interact with bots using items:")
        print("\\ jackpot item_name /")
        display_message('Use items with bots')

        print("8. Clear excess text on the screen:")
        print("\\ cls /")
        display_message('Clear the screen')

        print("9. Wipe your data:")
        print("\\ wipe /")
        display_message('Learn to wipe data')

        print("10. Check total spent:")
        print("\\ total spent /")
        display_message('Check total spent amount')

        os.system('clear')
    else:
      pass
      os.system('clear')

tutorial_guide()
amount = {}
with open('add.txt', 'r') as file:
    lines = file.readlines()

with open('add.txt', 'w') as file:
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            username = parts[0]
            money = float(parts[1])
            amount[username] = money

            if username == USER:
                print(f"An Admin Gave you: {colorama.Fore.YELLOW}{money}{colorama.Fore.GREEN}${colorama.Fore.RESET}")
                user_money += money
            else:
                file.write(line)

if USER not in amount:
    pass

def open_case(case_name, quantity=1, luck_boost=0, speeden=25):
  global user_money, total_money_spent, inventory

  if case_name == 'freecase' and quantity > 1:
      print(colorama.Fore.RED + "You can only open one FreeCase at a time." + colorama.Fore.RESET)
      return

  if case_name.lower() in Cases:
      for _ in range(quantity):
          if Cases[case_name]['cost'] > user_money:
              print(colorama.Fore.RED + "You don't have enough money to open this case." + colorama.Fore.RESET)
              return
          else:
              user_money -= Cases[case_name]['cost']
              total_money_spent += Cases[case_name]['cost']
              print(f"You opened {case_name} for {Cases[case_name]['cost']}$")

          spinning_time = 3.2 - (speeden * 0.1)
          start_time = time.time()

          spinning_items = Cases[case_name]['items']
          landing_item = None

          while time.time() - start_time < spinning_time:
              os.system('cls' if os.name == 'nt' else 'clear')

              landing_item = random.choices(
                  spinning_items, weights=[item['chance'] + luck_boost for item in spinning_items]
              )[0]
              print(f"[{' ' * 5}{landing_item['icon']} {landing_item['name']}{' ' * 5}]")
              time.sleep(0.1)

          time.sleep(1)

          if landing_item:
              found_time = datetime.datetime.utcnow().isoformat()
              item_with_details = landing_item.copy()
              item_with_details.update({
                  'found_time': found_time,
                  'origin_case': case_name,
                  'locked': False
              })
              print(f"You found a {landing_item['icon']} {landing_item['name']} worth {landing_item['value']}$ with a {landing_item['chance'] + luck_boost}% chance")

              inventory.append(item_with_details)

              inventory[:] = [item for item in inventory if item.get('name') != case_name]
          else:
              print(colorama.Fore.RED + "There was an issue determining the item. Please try again." + colorama.Fore.RESET)

  else:
      print(f"{colorama.Fore.RED}{case_name} is not a valid case{colorama.Fore.RESET}")



def show_inventory():
  global user_money, total_value

  print(f"Money: ${user_money}")

  total_value = user_money

  print("Inventory:")
  for item in inventory:
      print(f"{item['icon']} {item['name']} worth ${item['value']}")
      total_value += item['value']

  print(f"Net Worth: ${total_value}")


def sell_item(item_name, quantity=None):
  global user_money
  sold_items = 0
  total_value = 0

  items_to_remove = []

  for item in list(inventory):
      if item['name'] == item_name:
          if quantity is None or (quantity is not None and sold_items < quantity):
              items_to_remove.append(item)
              total_value += item['value']
              sold_items += 1

  for item in items_to_remove:
      inventory.remove(item)

  if sold_items > 0:
      print(f"Sold {sold_items} {item_name}(s) for a total of {total_value}$")
      user_money += total_value
  else:
      print(f"You don't have {item_name} in your inventory or try adding x quantity.")
def sell_all_items():
      global user_money, inventory

      total_value = sum(item['value'] for item in inventory if not item.get('locked')) 
      user_money += total_value
      print(f"Sold all unlock items in your inventory for a total of {total_value}$")
      inventory = [item for item in inventory if item.get('locked')]

def preview_case(case_name):

      if case_name in Cases:
          case_items = Cases[case_name]['items']
          for item in case_items:
              print(f"{item['icon']} {item['name']} valued at {item['value']}$ with a {item['chance']}% chance")
      else:
          print(f"{colorama.Fore.RED}{case_name} is not a valid case{colorama.Fore.RESET}")
def show_cases():
      sorted_cases = sorted(Cases.items(), key=lambda item: item[1]['cost'])
      for case_name, case_details in sorted_cases:
          print(f"{case_name} - Cost: {case_details['cost']}$")
def show_total_money_spent():
      global total_money_spent
      print(f"Total money spent: ${total_money_spent}")

def wipe_data():
  global inventory, user_money, total_money_spent, life_time_money_lost
  user_money = 0
  total_money_spent = 0
  life_time_money_lost = 0
  inventory.clear()

def lock_item():
  global inventory
  item_name = input("Enter the name of the item to lock: ")
  found_items = [item for item in inventory if item['name'] == item_name and not item.get('locked')]

  if not found_items:
      new_item = {'name': item_name, 'locked': True}
      print(f"{colorama.Fore.GREEN}{item_name} has been added to the inventory and locked.{colorama.Fore.RESET}")
      return

  if len(found_items) == 1:
      found_item = found_items[0]
      found_item['locked'] = True
      print(f"{colorama.Fore.GREEN}{item_name} has been locked.{colorama.Fore.RESET}")
  else:
      print(f"Multiple unlocked items found with the name '{item_name}':")
      for index, item in enumerate(found_items, start=1):
          print(f"{index}. {item['name']}")

      choice = input("Enter the number of the item(s) to lock or 'all' to lock all of them: ")

      if choice.lower() == 'all':
          for item in found_items:
              item['locked'] = True
          print(f"All '{item_name}' items have been locked.")
      elif choice.isdigit() and 1 <= int(choice) <= len(found_items):
          found_item = found_items[int(choice) - 1]
          found_item['locked'] = True
          print(f"{found_item['name']} has been locked.")
      else:
          print("Invalid choice.")

def jackpot(item_name):

  global inventory, total_money_spent

  user_item = next((item for item in inventory if item['name'] == item_name), None)

  if user_item is None:
      print(f"{colorama.Fore.RED}You don't have {item_name} in your inventory.{colorama.Fore.RESET}")
      return

  print(f"{colorama.Fore.YELLOW}Jackpot started for {item_name}!{colorama.Fore.RESET}")

  inventory.remove(user_item)


  bot_names = ['Dawg', 'Big', f'{colorama.Fore.MAGENTA}Cluefix{colorama.Fore.RESET}', f'{colorama.Fore.MAGENTA}LoganPaxton3{colorama.Fore.RESET}', 'Joe', 'Benji', 'Tatanka', 'Yatzil', 'Lucky', 'animal' , 'switch' , 'route' , 'coin', 'flu', 'power', 'forum', 'gloom', 'thoughtful', 'spoil', 'applied', 'marble', 'talk', 'foundation', 'ideal', 'decide', 'flow']
  bot_items = [
      {'name': 'money bag', 'value': 2, 'icon': '💰', 'chance': 0.0},
      {'name': 'rare stamp', 'value': 12, 'icon': '📬', 'chance': 0.0},
      {'name': 'marble', 'value': 15, 'icon': '🔵', 'chance': 0.0},
      {'name': 'pen', 'value': 4, 'icon': '🖊️', 'chance': 0.0},
      {'name': 'silver ring', 'value': 10, 'icon': '💍', 'chance':  0.0},
      {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance':  0.0},
      {'name': 'antique vase', 'value': 15, 'icon': '🏺', 'chance':  0.0},
      {'name': 'pickaxe', 'value': 5, 'icon': '⛏️', 'chance':  0.0},
      {'name': 'rare stamp', 'value': 12, 'icon': '📬', 'chance':  0.0},
      {'name': 'rusty nail', 'value': 0.5, 'icon': '🔩', 'chance': 0.0},
      {'name': 'marble', 'value': 15, 'icon': '🔵', 'chance': 0.0},
      {'name': 'book', 'value': .25, 'icon': '📒', 'chance': 0.0},
      {'name': 'lock', 'value': .50, 'icon': '🔒', 'chance': 0.0},
      {'name': 'crayon', 'value': 3, 'icon': '🖍️ ', 'chance': 0.0},
      {'name': 'axe', 'value': 5, 'icon': '🪓', 'chance': 0.0},
      {'name': 'pen', 'value': 4, 'icon': '🖊️ ', 'chance': 0.0},
      {'name': 'fountain pen', 'value': 7, 'icon': '🖋️ ', 'chance': 0.0},
      {'name': 'black nib', 'value': 10, 'icon': '✒️ ', 'chance': 0.0},
      {'name': 'keyboard', 'value': 5, 'icon': '⌨️ ', 'chance': 0.0},
      {'name': 'plug', 'value': 6, 'icon': '🔌', 'chance': 0.0},
      {'name': 'floppy disk', 'value': 5, 'icon': '💾', 'chance': 0.0},
      {'name': 'computer mouse', 'value': 5, 'icon': '🖱️ ', 'chance': 0.0},
      {'name': 'silver ring', 'value': 10, 'icon': '💍', 'chance': 0.0},
      {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance': 0.0},
      {'name': 'copper coin', 'value': 2, 'icon': '💰', 'chance': 0.0},
      {'name': 'small gem', 'value': 8, 'icon': '💎', 'chance': 0.0},
      {'name': 'old key', 'value': 1, 'icon': '🔑', 'chance': 0.0},
      {'name': 'rubber duck', 'value': 4, 'icon': '🦆', 'chance': 0.0},
      {'name': 'glass marble', 'value': 12, 'icon': '🔮', 'chance': 0.0},
      {'name': 'playing card', 'value': 3.5, 'icon': '🃏', 'chance': 0.0},
      {'name': 'trash', 'value': 5, 'icon': '🗑️ ', 'chance': 0.0},
      {'name': 'trash', 'value': 10, 'icon': '🗑️ ', 'chance': 0.0},
      {'name': 'trash', 'value': 2, 'icon': '🗑️ ', 'chance': 0.0},
      {'name': 'trash', 'value': 1, 'icon': '🗑️ ', 'chance': 0.0},

  ]

  user_item_value = user_item.get('value', 0)
  if user_item_value >= 1500:
    bot_items.append({'name': 'ice cube', 'value': 2500, 'icon': '🧊', 'chance': 0.0})
    bot_items.append({'name': 'snowFlake', 'value': 500, 'icon': '❄️', 'chance': 0.0})
    bot_items.append({'name': 'trash', 'value': 500, 'icon': '🗑️ ', 'chance': 0.0})
  user_item_value = user_item.get('value', 0)
  if user_item_value >= 500:
    bot_items.append({'name': 'snowFlake', 'value': 500, 'icon': '❄️', 'chance': 0.0})
    bot_items.append({'name': 'trash', 'value': 500, 'icon': '🗑️ ', 'chance': 0.0})

  user_item_value = user_item.get('value', 0)
  if user_item_value >= 100000:
      bot_items.append({'name': 'mystic tome', 'value': 100000, 'icon': '📖', 'chance': 0.0})
      bot_items.append({'name': 'alien specimen', 'value': 120000, 'icon': '👽', 'chance': 0.0})
      bot_items.append({'name': 'crystal ball', 'value': 150000, 'icon': '🔮', 'chance': 0.0})
      bot_items.append({'name': 'enchanted relic', 'value': 120000, 'icon': '🔮', 'chance': 0.0})
  user_item_value = user_item.get('value', 0)
  if user_item_value >= 65000:
      bot_items.append({'name': 'ancient scroll', 'value': 80000, 'icon': '📜', 'chance': 0.0})
      bot_items.append({'name': 'phantom amulet', 'value': 85000, 'icon': '🧿', 'chance': 0.0})
      bot_items.append({'name': 'magic potion', 'value': 65000, 'icon': '🧪', 'chance': 0.0})
      bot_items.append({'name': 'ancient scroll', 'value': 80000, 'icon': '📜', 'chance': 0.0})
  user_item_value = user_item.get('value', 0)
  if user_item_value >= 150:
      bot_items.append({'name': 'knitting yarn', 'value': 150, 'icon': '🧶', 'chance': 0.0})
      bot_items.append({'name': 'model paint', 'value': 350, 'icon': '🎨', 'chance': 0.0})
      bot_items.append({'name': 'beach ball', 'value': 150, 'icon': '🏐', 'chance': 0.0})
      bot_items.append({'name': 'sunglasses', 'value': 250, 'icon': '🕶️', 'chance': 0.0})
      bot_items.append({'name': 'hiking boots', 'value': 250, 'icon': '🥾', 'chance': 0.0})
      bot_items.append({'name': 'binoculars', 'value': 300, 'icon': '🔭', 'chance': 0.0})
      bot_items.append({'name': 'gold necklace', 'value': 200, 'icon': '⛓️', 'chance': 0.0})

      bot_items.append({'name': 'gold necklace', 'value': 200, 'icon': '⛓️', 'chance': 0.0})
      bot_items.append({'name': 'trash', 'value': 300, 'icon': '🗑️ ', 'chance': 0.0})
      bot_items.append({'name': 'apple laptop', 'value': 250, 'icon': '💻', 'chance': 0.0})
      bot_items.append({'name': 'gold necklace', 'value': 200, 'icon': '⛓️', 'chance':  0.0})

  user_item_value = user_item.get('value', 0)
  if user_item_value >= 70:
      bot_items.append({'name': 'toy car', 'value': 100, 'icon': '🚗', 'chance': 0.0})
      bot_items.append({'name': 'compass', 'value': 100, 'icon': '🧭', 'chance': 0.0})
      bot_items.append({'name': 'basketball', 'value': 120, 'icon': '🏀', 'chance': 0.0})
      bot_items.append({'name': 'computer screen', 'value': 100, 'icon': '🖥️ ', 'chance': 0.0})
      bot_items.append({'name': 'skateboard', 'value': 150, 'icon': '🛹', 'chance': 0.0})
      bot_items.append({'name': 'trash', 'value': 100, 'icon': '🗑️ ', 'chance': 0.0})

  user_item_value = user_item.get('value', 0)
  if user_item_value >= 20:
      bot_items.append({'name': 'graffiti cans', 'value': 50, 'icon': '🎨', 'chance': 0.0})
      bot_items.append({'name': 'sunscreen', 'value': 59, 'icon': '🧴', 'chance': 0.0})
      bot_items.append({'name': 'printer', 'value': 40, 'icon': '🖨️ ', 'chance': 0.0})
      bot_items.append({'name': 'phone', 'value': 25, 'icon': '📱', 'chance': 0.0})
      bot_items.append({'name': 'mic', 'value': 20, 'icon': '🎙️ ', 'chance': 0.0})
      bot_items.append({'name': 'toy soldier', 'value': 25, 'icon': '⚔️ ', 'chance': 10})

  user_item_value = user_item.get('value', 0)
  if user_item_value >= 50000:
      bot_items.append({'name': 'frosty', 'value': 11000, 'icon': '☃️', 'chance': 0.0})
      bot_items.append({'name': 'oven mitts', 'value': 2000, 'icon': '🧤', 'chance': 0.0})
      bot_items.append({'name': 'rolling pin', 'value': 3000, 'icon': '🧑‍🍳', 'chance': 0.0})
      bot_items.append({'name': 'mixing bowl', 'value': 1000, 'icon': '🥣', 'chance': 0.0})
      bot_items.append({'name': 'spacesuit', 'value': 20000, 'icon': '🧑‍🚀', 'chance': 0.0})
      bot_items.append({'name': 'moon rock', 'value': 50000, 'icon': '🌑', 'chance': 0.0})
      bot_items.append({'name': 'constellation map', 'value': 45000, 'icon': '🌌', 'chance': 0.0})
      bot_items.append({'name': 'trash', 'value': 10000, 'icon': '🗑️ ', 'chance': 0.0})
      bot_items.append({'name': 'ice cold', 'value': 19000, 'icon': '🥶', 'chance': 0.0})
      bot_items.append({'name': 'nnow mountain', 'value': 24000, 'icon': '🗻', 'chance': 0.0})

  participants = [{'name': 'You', 'item': item_name, 'value': user_item_value, 'chance': 0.0, 'icon': user_item.get('icon', '')}]
  total_value = participants[0]['value']

  num_bots = random.randint(1, 26)
  for i in range(num_bots):
      bot_name = random.choice(bot_names)
      bot_item = random.choice(bot_items)
      bot_names.remove(bot_name)
      bot_chance = 0.0
      participants.append({'name': bot_name, 'item': bot_item['name'], 'value': bot_item['value'], 'chance': bot_chance, 'icon': bot_item.get('icon', '')})
      total_value += bot_item['value']

  for participant in participants:
      participant['chance'] = participant['value'] / total_value

  print("Participants:")

  for participant in participants:
      item_icon = participant.get('icon', '') 
      print(f"{participant['name']} - Item: {participant['item']} - Value: {participant['value']} - Chance: {participant['chance'] * 100:.2f}% - Icon: {item_icon}")
      print('')
  total_value = sum(participant['value'] for participant in participants)
  print(f'total: {total_value}$')
  print("Jackpot ending in 10 seconds...")
  time.sleep(10)

  winner = None
  winning_number = random.random()
  current_probability = 0.0

  for participant in participants:
      current_probability += participant['chance']
      if winning_number <= current_probability:
          winner = participant
          break

  if winner is None:
      print("No winner was determined.")
      return

  if winner['name'] == 'You':
    print(f"{colorama.Fore.YELLOW}Congratulations! You won all the items with a {participants[0]['chance'] * 100:.2f}% chance!{colorama.Fore.RESET}")
    for participant in participants:
        if participant['name'] != 'You':
            inventory.append({'name': participant['item'], 'value': participant['value'], 'icon': participant.get('icon', '')})
    inventory.append(user_item)
  else:
     print(f"{colorama.Fore.YELLOW}The winner of the jackpot is: {winner['name']}, with {winner['item']} and a {winner['chance'] * 100:.2f}% chance!{colorama.Fore.RESET}")

shop_items = [
  {'name': 'small health potion', 'value': 5, 'icon': '❤️ '},
  {'name': 'sword', 'value': 15, 'icon': '⚔️'},
  {'name': 'shield', 'value': 10, 'icon': '🛡️'},
  {'name': 'book', 'value': .25, 'icon': '📒', 'chance': 50},
  {'name': 'lock', 'value': .50, 'icon': '🔒', 'chance': 30},
  {'name': 'crayon', 'value': 3, 'icon': '🖍️ ', 'chance': 15},
  {'name': 'axe', 'value': 5, 'icon': '🪓', 'chance': 10},
  {'name': 'crystal ball', 'value': 70, 'icon': '🔮', 'chance': 0.1},
  {'name': 'silver ring', 'value': 10, 'icon': '💍', 'chance': 40},
  {'name': 'gold necklace', 'value': 200, 'icon': '⛓️', 'chance': 0.1},
  {'name': 'trash', 'value': 2, 'icon': '🗑️ ', 'chance': 30},
  {'name': 'copper coin', 'value': 2, 'icon': '💰', 'chance': 50},
  {'name': 'small gem', 'value': 15, 'icon': '💎', 'chance': 10},
  {'name': 'old key', 'value': 1, 'icon': '🔑', 'chance': 90},
  {'name': 'antique vase', 'value': 15, 'icon': '🏺', 'chance':  15},
  {'name': 'pickaxe', 'value': 5, 'icon': '⛏️', 'chance': 45},
  {'name': 'rare stamp', 'value': 12, 'icon': '📬', 'chance': 25},
  {'name': 'rusty nail', 'value': 0.5, 'icon': '🔩', 'chance': 30},
  {'name': 'marble', 'value': 15, 'icon': '🔵', 'chance': 30},
  {'name': 'toy soldier', 'value': 25, 'icon': '⚔️ ', 'chance': 10},
  {'name': 'rare mail box', 'value': 560, 'icon': '📬', 'chance': 0.1},
  {'name': 'rubber duck', 'value': 4, 'icon': '🦆', 'chance': 50},
  {'name': 'glass marble', 'value': 12, 'icon': '🔮', 'chance': 20},
  {'name': 'playing card', 'value': 3.5, 'icon': '🃏', 'chance': 70},
  {'name': 'pen', 'value': 4, 'icon': '🖊️ ', 'chance': 55},
  {'name': 'fountain pen', 'value': 7, 'icon': '🖋️ ', 'chance': 45},
  {'name': 'black nib', 'value': 10, 'icon': '✒️ ', 'chance': 45},
  {'name': 'glass marble', 'value': 100, 'icon': '🔮', 'chance': 0.1},
  {'name': 'computer screen', 'value': 100, 'icon': '🖥️ ', 'chance': 1},
  {'name': 'keyboard', 'value': 5, 'icon': '⌨️ ', 'chance': 50},
  {'name': 'mic', 'value': 20, 'icon': '🎙️ ', 'chance': 30},
  {'name': 'plug', 'value': 6, 'icon': '🔌', 'chance': 45},
  {'name': 'floppy disk', 'value': 5, 'icon': '💾', 'chance': 45},
  {'name': 'computer mouse', 'value': 5, 'icon': '🖱️ ', 'chance': 50},
  {'name': 'printer', 'value': 40, 'icon': '🖨️ ', 'chance': 5},
  {'name': 'phone', 'value': 25, 'icon': '📱', 'chance': 25},
  {'name': 'apple laptop', 'value':250, 'icon': '💻', 'chance': 0.1},
  {'name': 'diamond ring', 'value': 200, 'icon': '💍', 'chance': 50},
  {'name': 'platinum watch', 'value': 300, 'icon': '⌚', 'chance': 50},
  {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance': 50},
  {'name': 'yacht', 'value': 10000, 'icon': '🛥️', 'chance': 10},
  {'name': 'private jet', 'value': 20000, 'icon': '✈️', 'chance': 1},
  {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance': 10},
  {'name': 'mansion', 'value': 100000, 'icon': '🏰', 'chance': 0.1},
  {'name': 'luxury car', 'value': 50000, 'icon': '🚗', 'chance': 5},
  {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance': 94.9},
  {'name': 'snowFlake', 'value': 500, 'icon': '❄️ ', 'chance': 92.8},
  {'name': 'ice cube', 'value': 2500, 'icon': '🧊', 'chance': 6},
  {'name': 'frosty', 'value': 11000, 'icon': '☃️ ', 'chance': 1},
  {'name': 'nnow Mountain', 'value': 24000, 'icon': '🗻', 'chance': 0.1},
  {'name': 'ice Cold', 'value': 19000, 'icon': '🥶', 'chance': 0.1},
  {'name': 'Fire extinguisher', 'value': 10000, 'icon': '🧯', 'chance': 48},
  {'name': 'fire', 'value': 15000, 'icon': '🔥', 'chance': 30},
  {'name': 'mad', 'value': 35000, 'icon': '🤬', 'chance': 15},
  {'name': 'volcano', 'value': 50000, 'icon': '🌋', 'chance': 5},
  {'name': 'wave', 'value': 150, 'icon': '🌊', 'chance': 0.1},
  {'name': 'water', 'value': 10, 'icon': '💦', 'chance': 5},
  {'name': 'trash', 'value': 0.1, 'icon': '🗑️ ', 'chance': 65.2},
  {'name': 'compass', 'value': 15, 'icon': '🧭', 'chance': 50},
  {'name': 'map', 'value': 10, 'icon': '🗺️ ', 'chance': 55},
  {'name': 'tent', 'value': 80, 'icon': '⛺', 'chance': 10},
  {'name': 'crystal ball', 'value': 150000, 'icon': '🔮', 'chance': 1},
  {'name': 'magic potion', 'value': 65000, 'icon': '🧪', 'chance': 5},
  {'name': 'ancient scroll', 'value': 80000, 'icon': '📜', 'chance': 3},
  {'name': 'trash', 'value': 100, 'icon': '🗑️ ', 'chance': 30},
  {'name': 'immortality elixir', 'value': 500000, 'icon': '⚗️', 'chance': 1},
  {'name': 'eternal flame', 'value': 100000, 'icon': '🔥', 'chance': 20},
  {'name': 'time crystal', 'value': 200000, 'icon': '⏳', 'chance': 10},
  {'name': 'trash', 'value': 20000, 'icon': '🗑️ ', 'chance': 69},
  {'name': 'hoverboard', 'value': 80000, 'icon': '🛹', 'chance': 20},
  {'name': 'cybernetic implant', 'value': 200000, 'icon': '🤖', 'chance': 5},
  {'name': 'intergalactic spaceship', 'value': 1000000, 'icon': '🚀', 'chance': 1},
  {'name': 'trash', 'value': 500, 'icon': '🗑️ ', 'chance': 74},
  {'name': 'excalibur', 'value': 3000000, 'icon': '⚔️', 'chance': 1},
  {'name': 'holy grail', 'value': 2500000, 'icon': '🏺', 'chance': 2},
  {'name': 'mysticamulet', 'value': 600000, 'icon': '🔗', 'chance': 15},
  {'name': 'trash', 'value': 10000, 'icon': '🗑️ ', 'chance': 50},
  {'name': 'dragon', 'value': 100000, 'icon': '🐉', 'chance': 1},
  {'name': 'phoenix', 'value': 50000, 'icon': '🔥', 'chance': 10},
  {'name': 'unicorn', 'value': 30000, 'icon': '🦄', 'chance': 20},
  {'name': 'trash', 'value': 1000, 'icon': '🗑️ ', 'chance': 69},
  {'name': 'vampire fang', 'value': 100000, 'icon': '🧛', 'chance': 10},
  {'name': 'werewolf claw', 'value': 80000, 'icon': '🐺', 'chance': 20},
  {'name': 'ghostly apparition', 'value': 120000, 'icon': '👻', 'chance': 5},
  {'name': 'trash', 'value': 200, 'icon': '🗑️ ', 'chance': 65},
  {'name': 'constellation map', 'value': 45000, 'icon': '🌌', 'chance': 15},
  {'name': 'moon rock', 'value': 50000, 'icon': '🌑', 'chance': 5},
  {'name': 'spacesuit', 'value': 20000, 'icon': '🧑‍🚀', 'chance': 50},
  {'name': 'alien specimen', 'value': 120000, 'icon': '👽', 'chance': 0.1},
  {'name': 'star  fragment', 'value': 80000, 'icon': '🌠', 'chance': 2},
  {'name': 'trash', 'value': 500, 'icon': '🗑️ ', 'chance': 22.5},
  {'name': 'portal gun', 'value': 25000, 'icon': '🔫', 'chance': 10},
  {'name': 'dimension shard', 'value': 75000, 'icon': '💎', 'chance': 1},
  {'name': 'time loop coil', 'value': 55000, 'icon': '♾️', 'chance': 7},
  {'name': 'trash', 'value': 1000, 'icon': '🗑️ ', 'chance': 70},
  {'name': 'gold bar', 'value': 25000, 'icon': '🏆', 'chance': 5},
  {'name': 'sapphire gem', 'value': 35000, 'icon': '💠', 'chance': 1},
  {'name': 'pirate sword', 'value': 7000, 'icon': '🗡️', 'chance': 40},
  {'name': 'trash', 'value': 200, 'icon': '🗑️ ', 'chance': 20},
  {'name': 'enchanted relic', 'value': 120000, 'icon': '🔮', 'chance': 10},
  {'name': 'mystic tome', 'value': 100000, 'icon': '📖', 'chance': 3},
  {'name': 'phantom amulet', 'value': 85000, 'icon': '🧿', 'chance': 5},
  {'name': 'trash', 'value': 300, 'icon': '🗑️ ', 'chance': 82},
  {'name': 'ancient armour', 'value': 40000, 'icon': '🛡️', 'chance': 20},
  {'name': 'forged sword', 'value': 30000, 'icon': '⚔️', 'chance': 30},
  {'name': 'warrior flag', 'value': 25000, 'icon': '🏴‍☠', 'chance': 25},
  {'name': 'trash', 'value': 100, 'icon': '🗑️ ' , 'chance': 25},
  {'name': 'earth crystal', 'value': 35000, 'icon': '🌍', 'chance': 20},
  {'name': 'air orb', 'value': 40000, 'icon': '💨', 'chance': 15},
  {'name': 'water talisman', 'value': 30000, 'icon': '💧', 'chance': 25},
  {'name': 'fire essence', 'value': 70000, 'icon': '🔥', 'chance': 5},
  {'name': 'trash', 'value': 500, 'icon': '🗑️ ', 'chance': 35},
  {'name': 'graffiti cans', 'value': 50, 'icon': '🎨', 'chance': 60},
  {'name': 'skateboard', 'value': 150, 'icon': '🛹', 'chance': 30},
  {'name': 'basketball', 'value': 120, 'icon': '🏀', 'chance': 50},
  {'name': 'trash', 'value': 5, 'icon': '🗑️ ', 'chance': 60},
  {'name': 'binoculars', 'value': 300, 'icon': '🔭', 'chance': 40},
  {'name': 'hiking boots', 'value': 250, 'icon': '🥾', 'chance': 35},
  {'name': 'compass', 'value': 100, 'icon': '🧭', 'chance': 50},
  {'name': 'trash', 'value': 10, 'icon': '🗑️ ', 'chance': 75},
  {'name': 'flower seeds', 'value': 50, 'icon': '🌼', 'chance': 50},
  {'name': 'watering can', 'value': 80, 'icon': '🚿', 'chance': 20},
  {'name': 'garden gnome', 'value': 100, 'icon': '🧙', 'chance': 15},
  {'name': 'trash', 'value': 5, 'icon': '🗑️ ', 'chance': 65},
  {'name': 'sunglasses', 'value': 250, 'icon': '🕶️', 'chance': 25},
  {'name': 'beach ball', 'value': 150, 'icon': '🏐', 'chance': 35},
  {'name': 'sunscreen', 'value': 59, 'icon': '🧴', 'chance': 60},
  {'name': 'trash', 'value': 2, 'icon': '🗑️ ', 'chance': 80},
  {'name': 'mixing bowl', 'value': 1000, 'icon': '🥣', 'chance': 1},
  {'name': 'rolling pin', 'value': 3000, 'icon': '🧑‍🍳', 'chance': 1},
  {'name': 'oven mitts', 'value': 2000, 'icon': '🧤', 'chance': 1},
  {'name': 'trash', 'value': 1, 'icon': '🗑️ ', 'chance': 99.9},
  {'name': 'game tokens', 'value': 250, 'icon': '🎟️', 'chance': 5},
  {'name': 'plush toy', 'value': 125, 'icon': '🧸', 'chance': 28},
  {'name': 'arcade ticket', 'value': 90, 'icon': '🎫', 'chance': 65},
  {'name': 'trash', 'value': 2, 'icon': '🗑️ ', 'chance': 85},
  {'name': 'model paint', 'value': 350, 'icon': '🎨', 'chance': 50},
  {'name': 'knitting yarn', 'value': 150, 'icon': '🧶', 'chance': 50},
  {'name': 'toy car', 'value': 100, 'icon': '🚗', 'chance': 50},
  {'name': 'guitar pick', 'value': 00.1, 'icon': '🎸', 'chance': 99.9},
  {'name': 'sheet music', 'value': 4000, 'icon': '🎼', 'chance': 0.1},
  {'name': 'microphone', 'value': 5000, 'icon': '🎤', 'chance': 0.1},
  {'name': 'chef hat', 'value': 25, 'icon': '🧑‍🍳', 'chance': 25},
  {'name': 'spatula', 'value': 15, 'icon': '🍳', 'chance': 60},
  {'name': 'apron', 'value': 10, 'icon': '👨‍🍳', 'chance': 75},
  {'name': 'game controller', 'value': 500, 'icon': '🎮', 'chance': 25},
  {'name': 'headset', 'value': 800, 'icon': '🎧', 'chance': 5},
  {'name': 'gaming mouse', 'value': 250, 'icon': '🖱️ ', 'chance': 45},
  {'name': 'canvas', 'value': 50, 'icon': '🖼️', 'chance': 50},
  {'name': 'brushes', 'value': 30, 'icon': '🖌️', 'chance': 70},
  {'name': 'easel', 'value': 85, 'icon': '🎨', 'chance': 25},
  {'name': 'dumbbell', 'value': 350, 'icon': '🏋️', 'chance': 70},
  {'name': 'yoga mat', 'value': 300, 'icon': '🧘', 'chance': 75},
  {'name': 'jump rope', 'value': 600, 'icon': '➰', 'chance': 5},
  {'name': 'floppy disk', 'value': 550, 'icon': '💾', 'chance': 55},
  {'name': 'smart watch', 'value': 900, 'icon': '⌚', 'chance': 15},
  {'name': 'tablet', 'value': 1000, 'icon': '📱', 'chance': 5},
  {'name': 'fountain pen', 'value': 40, 'icon': '✒️', 'chance': 70},
  {'name': 'notebook', 'value': 50, 'icon': '📓', 'chance': 80},
  {'name': 'typewriter', 'value': 180, 'icon': '🖨️', 'chance': 25},
  {'name': 'rare coin', 'value': 800, 'icon': '🥮', 'chance': 10},
  {'name': 'stamps', 'value': 680, 'icon': '📬', 'chance': 25},
  {'name': 'vintage toy', 'value': 400, 'icon': '🧸', 'chance': 65},
  {'name': 'backpack', 'value': 1500, 'icon': '🎒', 'chance': 1},
  {'name': 'travel guide', 'value': 750, 'icon': '📚', 'chance': 15},
  {'name': 'world map', 'value': 450, 'icon': '🗺️', 'chance': 45},
  {'name': 'fishing rod', 'value': 100, 'icon': '🎣', 'chance': 15},
  {'name': 'tackle box', 'value': 85, 'icon': '🧰', 'chance': 25},
  {'name': 'fishing hat', 'value': 54, 'icon': '👒', 'chance': 50},
  {'name': 'wrench', 'value': 90, 'icon': '🔧', 'chance': 25},
  {'name': 'screwdriver', 'value': 60, 'icon': '🖋️', 'chance': 60},
  {'name': 'car battery', 'value': 150, 'icon': '🔋', 'chance': 15},
  {'name': 'camera lens', 'value': 260, 'icon': '📸', 'chance': 10},
  {'name': 'tripod', 'value': 200, 'icon': '📷', 'chance': 15},
  {'name': 'memory card', 'value': 130, 'icon': '💳', 'chance': 75},
  {'name': 'bicycle helmet', 'value': 70, 'icon': '⛑️', 'chance': 10},
  {'name': 'bike pump', 'value': 25, 'icon': '🗜️', 'chance': 50},
  {'name': 'water bottle', 'value': 10, 'icon': '🚰', 'chance': 55},
  {'name': 'cape', 'value': 300, 'icon': '🦸', 'chance': 50},
  {'name': 'mask', 'value': 250, 'icon': '🦹', 'chance': 60},
  {'name': 'utility belt', 'value': 450, 'icon': '🧗', 'chance': 40},
  {'name': 'ancient manuscript', 'value': 40000, 'icon': '📜', 'chance': 20},
  {'name': 'rare artifact', 'value': 100000, 'icon': '🏺', 'chance': 10},
  {'name': 'antique jewelry', 'value': 75000, 'icon': '💍', 'chance': 15},
  {'name': 'stock certificates', 'value': 200000, 'icon': '📈', 'chance': 7},
  {'name': 'gold ingot', 'value': 150000, 'icon': '🥇', 'chance': 20},
  {'name': 'luxury watch', 'value': 85000, 'icon': '⌚', 'chance': 30},
  {'name': 'priceless painting', 'value': 70000, 'icon': '🖼️', 'chance': 5},
  {'name': 'sculpture masterpiece', 'value': 50000, 'icon': '🗿', 'chance': 10},
  {'name': 'vintage art supplies', 'value': 25000, 'icon': '🖌️', 'chance': 30},
  {'name': 'diamond chips', 'value': 120000, 'icon': '💎', 'chance': 35},
  {'name': 'platinum card', 'value': 190000, 'icon': '💳', 'chance': 20},
  {'name': 'luxury car keys', 'value': 350000, 'icon': '🚗', 'chance': 5},
  {'name': 'moon alien', 'value': 250000, 'icon': '👽', 'chance': 15},
  {'name': 'space shuttle model', 'value': 150000, 'icon': '🚀', 'chance': 25},
  {'name': 'astronaut autograph', 'value': 80000, 'icon': '✍️ ', 'chance': 35},
  {'name': 'iced', 'value': 1000000, 'icon': '🥶 ', 'chance': 1},
  {'name': 'mad', 'value': 670000, 'icon': '🤬', 'chance': 10},
  {'name': 'uncolored face', 'value': 120000, 'icon': '☹', 'chance': 90},
  {'name': 'dino dna', 'value': 10000000, 'icon': '🧬', 'chance': 10},
  {'name': 'really old scroll', 'value': 7000000, 'icon': '📜', 'chance': 25},
  {'name': '1352 news paper', 'value': 5000000, 'icon': '📰', 'chance': 35},
  {'name': 'gold_dvd', 'value': 15000000, 'icon': '📀', 'chance': 40},
  {'name': 'floppy disk', 'value': 1200000, 'icon': '💾', 'chance': 60},
  {'name': 'gold/coal building', 'value': 1953942552, 'icon': '🕋 ', 'chance': 1},
  {'name': 'plane', 'value': 73477343, 'icon': '🚅', 'chance': 50},
  {'name': 'building', 'value': 1200400, 'icon': '🏛', 'chance': 70},
  {'name': 'crown ewels', 'value': 50000, 'icon': '👑', 'chance': 20},
  {'name': 'royal scepter', 'value': 30000, 'icon': '🏰', 'chance': 30},
  {'name': 'throne', 'value': 25000, 'icon': '🪑', 'chance': 25},
  {'name': 'latest martphone', 'value': 15000, 'icon': '📱', 'chance': 50},
  {'name': 'high-end laptop', 'value': 60000, 'icon': '💻', 'chance': 2},
  {'name': 'smart home system', 'value': 45000, 'icon': '🏠', 'chance': 15},
  {'name': 'luxury briefcase', 'value': 10000, 'icon': '💼', 'chance': 50},
  {'name': 'business jet model', 'value': 30000, 'icon': '✈️', 'chance': 20},
  {'name': 'goldbar', 'value': 25000, 'icon': '🥇', 'chance': 30},
  {'name': 'model villa', 'value': 20000, 'icon': '🏘️', 'chance': 20},
  {'name': 'private island map', 'value': 40000, 'icon': '🏝️', 'chance': 15},
  {'name': 'luxury apartment keys', 'value': 30000, 'icon': '🔑', 'chance': 25},
  {'name': 'start up hares', 'value': 60000, 'icon': '📈', 'chance': 20},
  {'name': 'investment portfolio', 'value': 15000, 'icon': '🗂️', 'chance': 30},
  {'name': 'networking club membership', 'value': 25000, 'icon': '🔗', 'chance': 50},


]
sorted_items = sorted(shop_items, key=lambda x: x['value'])
if USER == "Cluefixx":
  USER = "AFK"
else:
  pass
def shop():
  global user_money, inventory

  print("Welcome to the Shop!")
  print("Available Items:")
  for index, item in enumerate(sorted_items, start=1):
      print(f"{index}. {item['name']} - Cost: ${item['value']} - Icon: {item['icon']}")

  try:
      choice = int(input("Enter the number of the item you want to buy (0 to cancel): "))
      if choice == 0:
          print(colorama.Fore.RED+"Purchase cancelled."+colorama.Fore.RESET)
          return

      selected_item = sorted_items[choice - 1]

      if user_money >= selected_item['value']:
          user_money -= selected_item['value']
          inventory.append(selected_item)
          print(f"{colorama.Fore.YELLOW}You bought a {selected_item['name']} for ${selected_item['value']}!{colorama.Fore.RESET}")
      else:
          print(colorama.Fore.RED+"Insufficient funds to buy the item."+colorama.Fore.RESET)

  except (ValueError, IndexError):
      print(colorama.Fore.RED+"Invalid choice. Please enter a valid number."+colorama.Fore.RESET)
def unlock_item(item_name):
  global inventory
  found_items = [item for item in inventory if item['name'] == item_name and item.get('locked')]

  if not found_items:
      new_item = {'name': item_name, 'locked': False}
      inventory.append(new_item)
      print(f"{colorama.Fore.GREEN}{item_name} has been added to the inventory and locked.{colorama.Fore.RESET}")
      return

  if len(found_items) == 1:
      found_item = found_items[0]
      found_item['locked'] = False
      print(f"{colorama.Fore.YELLOW}{item_name} has been unlocked.{colorama.Fore.RESET}")
  else:
      print(f"Multiple locked items found with the name '{item_name}':")
      for index, item in enumerate(found_items, start=1):
          print(f"{index}. {item['name']}")

      choice = input("Enter the number of the item(s) to unlock or 'all' to unlock all of them: ")

      if choice.lower() == 'all':
          for item in found_items:
              item['locked'] = False
          print(f"All '{item_name}' items have been unlocked.")
      elif choice.isdigit() and 1 <= int(choice) <= len(found_items):
          found_item = found_items[int(choice) - 1]
          found_item['locked'] = False
          print(f"{found_item['name']} has been unlocked.")
      else:
          print("Invalid choice.")

def item_data(item_name):
  found = False
  for item in inventory:
      if item['name'] == item_name:
          found = True
          locked_status = "locked 🔐" if item.get('locked') else "unlocked 🔓"
          found_time = item.get('found_time', 'Unknown time')
          origin_case = item.get('origin_case', 'Unknown case')
          print(f"{item['icon']} {item['name']} - Worth: {item['value']}$ - Status: {locked_status} - Found: {found_time} from {origin_case}")
          break
  if not found:
      print(f"No item named '{item_name}' found in inventory.")
def save_game():
  while True:
        data = {
            'user_money': user_money,
            'total_money_spent': total_money_spent,
            'used_T' : used_T,
            'inventory': inventory
        }
        db[SER_KEY] = json.dumps(data)
        time.sleep(1)

save_thread = threading.Thread(target=save_game)
save_thread.daemon = True
save_thread.start()
def send_player_data():
  total_valueS = user_money
  for item in inventory:
      total_valueS += item['value']

  player_data = {
      "player": USER,
      "money": user_money,
      "net_worth": total_valueS,
      "most_valued_item": total_money_spent,
      "inventory": inventory
  }

  try:
      response = requests.post("https://leaderboard.cluefixx.repl.co/add", json=player_data)
      if response.status_code == 200:
          pass
      else:
          pass
  except requests.RequestException as e:
      print(f"Error sending player data: {e}")
def backup():
  global inventory, user_money, total_money_spent
def retrieve_leaderboard_data():
  try:
      response = requests.get("https://leaderboard.cluefixx.repl.co/leaderboard_json")
      if response.status_code == 200:
          leaderboard_data = response.json()
          print("Leaderboard:")
          for rank, player in enumerate(leaderboard_data, start=1):
              username = player.get('player', 'Unknown')
              money = player.get('money', 'N/A')
              net_worth = player.get('net_worth', 'N/A')
              total_valueX = player.get('Total Money Spent', 'N/A')
              inventory = ", ".join(player.get('Inventory', []))
              print(f"{rank}. @{username} - Money: {colorama.Fore.GREEN}{money}${colorama.Fore.RESET}, Net Worth: {net_worth}{colorama.Fore.RESET}, Total Money Spent: {colorama.Fore.GREEN}{total_valueX}{colorama.Fore.RESET}, Inventory: {inventory}")
      else:
          print(f"Failed to retrieve leaderboard data. Status code: {response.status_code}")
  except requests.RequestException as e:
      print(f"Error retrieving leaderboard data: {e}")
  except:
      print(f"Unknown Error Occured: {e}")


def send_data_repeatedly():
  while True:
      send_player_data()
      time.sleep(60)

data_thread = threading.Thread(target=send_data_repeatedly)
data_thread.daemon = True
data_thread.start()

def flip(bet_amount):
  global user_money

  if not isinstance(bet_amount, (int, float)) or bet_amount <= 0:
      print(colorama.Fore.RED + "Please enter a valid positive number for your bet." + colorama.Fore.RESET)
      return

  if '-' in str(bet_amount) or '+' in str(bet_amount):
      print(colorama.Fore.RED + "Invalid characters detected in your bet. Please enter a valid positive number." + colorama.Fore.RESET)
      return

  if bet_amount > user_money:
      print(colorama.Fore.RED + "You don't have enough money for this bet." + colorama.Fore.RESET)
      return

  coin_flip_result = random.randint(1, 2)
  if coin_flip_result == 1:
      print(colorama.Fore.YELLOW + "You Won! Check your Money" + colorama.Fore.RESET)
      user_money += bet_amount
  else:
      user_money -= bet_amount
      print(colorama.Fore.RED + "You Lost." + colorama.Fore.RESET)

def add_money(username, amount):
    with open("balances.txt", "a") as file:
        file.write(f"{username}, {amount}\n")

def askapicode(code):
    global inventory
    player_data = {
        "code": code,
    }
    try:
        response = requests.post("https://redeem.cluefixx.repl.co/redeem", json=player_data)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data.get("item") == "Titanic Snowman":
                print('Thank you for Supporting us Here is a Titanic Snowman.')
                inventory.append({'name': 'titanic snowman ????', 'value': 100000, 'icon': '⛄', 'chance': 100})
            elif data.get("item") == "Titanic Santa":
                print('Thank you for Supporting us Here is a Titanic Santa.')
                inventory.append({'name': 'titanic santa ????', 'value': 100000, 'icon': '🎅', 'chance': 100})
            elif data.get("item") == "Huge Penguin":
                print('Thank you for Supporting us Here is a Huge Penguin.')
                inventory.append({'name': 'huge penguin ???', 'value': 100000, 'icon': '🐧', 'chance': 100})
            elif data.get("item") == "Dev Robot":
                print('Thank you for Supporting us Here is a Dev Robot.')
                inventory.append({'name': 'dev robot ?????', 'value': 100000, 'icon': '🤖', 'chance': 100})
            elif data.get("item") == "Casegift":
                print('Thank you for Supporting us Here is a Limited case You can open.')
                inventory.append({'name': 'case', 'value': 100000, 'icon': '🤖', 'chance': 100})
            else:
                pass
        else:
            print(f"Unsuccessful request. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending player data: {e}")


while True:
  command = input("> ").lower()
  if command == "inv":
      show_inventory()
  elif command == "wipe":
      ask = input('Do you want to wipe your data? (y/n) ').lower() 
      if ask == 'y':
          wipe_data()
          print(colorama.Fore.RED + 'Data wiped successfully' + colorama.Fore.RESET)
  elif command == 'unlock':
      item_name = input("Enter the name of the item to unlock: ")
      unlock_item(item_name)
  elif command.startswith('lock'):
      lock_item()

  elif command == "total spent":
      show_total_money_spent()
  elif command == "help":
      print("inv - Show your inventory")
      print("open <case_name> x<quantity> - Open a case")
      print("sell <item_name> [x<quantity>] - Sell an item with an optional quantity")
      print("sellall - Sell all items in your inventory")
      print("cases - Show available cases")
      print("Preview <Case> - Preview the items in a case")
      print("total spent - Show the total money spent")
      print("data <item_name> - Display details about a specific item if in inventory")
      print("unlock - Unlock a specific item if in inventory")
      print("lock - Lock a specific item if in inventory")
      print("total cost - Tells you how much you have spent")
      print("wipe - Wipe all game data")
      print("cls - Clear the screen")
      print("jackpot <item_name> - Start a jackpot with a specified item")
      print("shop - Visit the shop to buy items")
      print("help - Show this help message")
      print("leaderboard - View the leaderboard")
  elif command == "leaderboard":
    retrieve_leaderboard_data()
  elif command == "sellall":
        sell_all_items()
  elif command.startswith("open "):
    parts = command.split(" ")
    case_name = parts[1].lower()
    quantity = 1
    if len(parts) > 2 and parts[2].startswith("x"):
        try:
            quantity = int(parts[2][1:])
        except ValueError:
            print(colorama.Fore.RED+"Invalid quantity format. Please use 'x<number>' for quantity."+colorama.Fore.RESET)


    case_names = {name.lower(): data for name, data in Cases.items()}
    if case_name in case_names:
        open_case(case_name, quantity)
    else:
        print(f"{colorama.Fore.RED}Case '{case_name}' not found.{colorama.Fore.RESET}")
  elif command == "shop":
       shop()
  elif command == "code":
        X=(input("Enter the code: "))
        askapicode(code=X)
  elif command.startswith("data "):
    parts = command.split(" ")
    if len(parts) > 1:
        item_name = ' '.join(parts[1:])
        item_data(item_name)
  elif command.startswith("flip "):
      parts = command.split(" ")
      if len(parts) > 1:
          try:
              datad = int(parts[1])
              flip(datad)
          except ValueError:
              print(colorama.Fore.RED+"Invalid input. Please enter a valid amount to bet."+colorama.Fore.RESET)
      else:
          print(colorama.Fore.RED+"Invalid input. Please enter a valid amount to bet."+colorama.Fore.RESET)
  elif command.startswith("jackpot "):
    parts = command.split(" ")
    if len(parts) > 1:
        item_name = ' '.join(parts[1:])
        jackpot(item_name)
    else:
        print(colorama.Fore.RED+"Invalid input. Please specify an item for the jackpot."+colorama.Fore.RESET)

  elif command.startswith("addmoney"):  
      try:
          with open('add.txt', 'a') as h:
              if USER in ADMINS:
                  item_name = input('Name: ')
                  reason = input("Enter the Amount: ")
                  h.write(f"{item_name},{reason}\n")
              else:
                  print(colorama.Fore.RED+"You're not an Admin."+colorama.Fore.RESET)
      except Exception as e:
          print(f"{colorama.Fore.RED}Error: {e}{colorama.Fore.RESET}")
  elif command.startswith("ban "):  
        try:
            with open('bans.txt', 'a') as h:
                if USER in ADMINS:
                    item_name = input('Name: ')
                    reason = input("Enter the reason for the ban: ")
                    h.write(f"{item_name},{reason}\n")
                else:
                    print(colorama.Fore.RED+"You're not an Admin."+colorama.Fore.RESET)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: {e}{colorama.Fore.RESET}")
  elif command.startswith("sell "):
        parts = command.split(" ")
        item_name = ' '.join(parts[1:-1])
        amount_str = parts[-1]
        if amount_str.startswith("x") and amount_str[1:].isdigit():
            quantity = int(amount_str[1:])
            sell_item(item_name, quantity)
        else:
            sell_item(item_name)
  elif command == "cases":
        show_cases()
  elif command.startswith("Preview ") or command.startswith("preview "):
        case_name = ' '.join(command.split(" ")[1:])
        preview_case(case_name)
  elif command == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')
  else:
        print(colorama.Fore.RED+"Invalid command"+colorama.Fore.RESET)
