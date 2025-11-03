import random

FILE_RATING = 'rating.txt'
DEFAULT_OPTIONS = ['scissors', 'paper', 'rock']
OTHER_OPTIONS = ["!exit", "!rating"]
GAME_OPTIONS = DEFAULT_OPTIONS + OTHER_OPTIONS
POINTS = {'draw': 50, 'success': 100}

# For each choice, the value is what that choice **beats** (useful for the default mode with 3 choices).
winning_map = {
    'scissors': 'paper',
    'rock': 'scissors',
    'paper': 'rock'
}


def read_validated_input(game_options=None):
    while True:
        user_input = input().strip().lower()
        # Either a game option or a special command (!exit, !rating) is allowed.
        if user_input not in game_options + OTHER_OPTIONS:
            print("Invalid input")
        else:
            return user_input


def read_username():
    while True:
        user_input = input("Enter your name: ").strip().capitalize()
        # isalpha() prohibits spaces and digits — intention: simple name only
        if user_input.isalpha():
            return user_input


def get_user():
    username = read_username()

    data = open(FILE_RATING, 'r', encoding='utf-8')
    for line in data:
        name, score = line.split()

        # case-insensitive comparison to find the user
        if name.lower() == username.lower():
            data.close()
            # returns the name as it appears in the file, the score (still in str), and False = not new
            return name, score, False

    data.close()
    # if not found, return username, score 0, and True = new user
    return username, 0, True


def exit_game():
    print("Bye!")
    exit()  # terminates the script immediately


def print_rating(username, new_user=False):
    score = 0
    if not new_user:
        data = open(FILE_RATING, 'r', encoding='utf-8')
        for line in data:
            name = line.split()[0]
            if username == name:
                # retrieves the score (string); note: not converted to int here
                score = line.split()[1]
                break
        data.close()
    else:
        # if new user, add an initial line to the file
        data = open(FILE_RATING, 'a')
        data.write(f"{username.capitalize()} {score}\n")

    print(f"Your rating: {score}")


def define_rating(username, rating, new_user=False):
    # opens in r+ to read and then rewrite; reads everything in memory
    file_data = open(FILE_RATING, 'r+')
    data = file_data.readlines()
    if new_user:
        data.append(f'{username} {rating}\n')
    else:
        for idx, info in enumerate(data):
            name = info.split()[0]
            if username == name:
                # adds the new score to the existing score (conversion to int)
                new_rating = int(info.split()[1]) + rating
                data[idx] = f'{name} {new_rating}\n'

    # replace the entire file with the new list
    file_data.seek(0)
    file_data.writelines(data)
    file_data.close()


def read_user_options():
    # reads the custom options entered by the user (e.g., "rock, paper, scissors")
    input_options = input().strip().lower()
    return input_options


def fill_options(choice, options):
    # Calculate, in the circular list `options`, which options beat `choice`.
    idx_user_choice = options.index(choice)
    middle_nb = len(options) // 2  # number of options that must beat or be beaten (for circular logic)
    winning_options, losing_options = [], []

    i = 1
    idx = idx_user_choice + 1
    # We collect the next `middle_nb` elements (circular): these are the ones that **beat** the user's choice.
    while i <= middle_nb:
        if idx < len(options):
            winning_options.append(options[idx])
        else:
            idx = 0
            continue
        i += 1
        idx += 1

    # losing_options = toutes les options moins winning_options
    losing_options = [option for option in options if option not in winning_options]

    # we remove the choice itself from the lists (it shouldn't remain there, but we make sure)
    if choice in losing_options: losing_options.remove(choice)
    if choice in winning_options: winning_options.remove(choice)

    # returns (options that beat the choice, options that the choice beats)
    return winning_options, losing_options


def launch_game(game_options=None, new_user=False):
    is_custom_options = True
    is_user_winner = False

    if game_options is None:
        game_options = DEFAULT_OPTIONS
        is_custom_options = False

    while True:
        choice = read_validated_input(game_options)
        computer_choice = random.choice(game_options)

        if choice == "!exit":
            exit_game()
        elif choice == "!rating":
            print_rating(user_name, new_user)
            new_user = False
            continue

        if is_custom_options:
            # For custom lists, we dynamically calculate who beats whom.
            winning_options, losing_options = fill_options(choice, game_options)
            if computer_choice in winning_options:  # the computer wins
                is_user_winner = False
            elif computer_choice in losing_options:  # the user wins
                is_user_winner = True
        elif not is_custom_options:
            # For classic mode (3 elements), the fixed map is used.
            if winning_map[choice] != computer_choice:  # the computer wins
                is_user_winner = False
            elif winning_map[choice] == computer_choice:  # user wins
                is_user_winner = True

        if choice == computer_choice:  # égalité
            define_rating(user_name, POINTS['draw'], new_user)
            print(f"There is a draw ({choice})")
            new_user = False
        elif is_user_winner:
            define_rating(user_name, POINTS['success'], new_user)
            print(f"Well done. The computer chose {computer_choice} and failed")
            new_user = False
        elif not is_user_winner:
            print(f"Sorry, but the computer chose {computer_choice}")


user_name, user_score, is_new = get_user()
print(f"Hello, {user_name}")

user_options = read_user_options()
print("Okay, let's start")

if user_options:
    new_options = user_options.split(',')
    launch_game(new_options, is_new)
else:
    launch_game()
