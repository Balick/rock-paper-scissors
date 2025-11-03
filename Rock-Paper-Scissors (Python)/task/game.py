import random

FILE_RATING = 'rating.txt'
DEFAULT_OPTIONS = ['scissors', 'paper', 'rock']
OTHER_OPTIONS = ["!exit", "!rating"]
GAME_OPTIONS = DEFAULT_OPTIONS + OTHER_OPTIONS
POINTS = {'draw': 50, 'success': 100}

# For each choice, value is what that choice beats
winning_map = {
    'scissors': 'paper',
    'rock': 'scissors',
    'paper': 'rock'
}


def read_validated_input(game_options=None):
    while True:
        user_input = input().strip().lower()
        if user_input not in game_options + OTHER_OPTIONS:
            print("Invalid input")
        else:
            return user_input


def read_username():
    while True:
        user_input = input("Enter your name: ").strip().capitalize()
        if user_input.isalpha():
            return user_input


def get_user():
    username = read_username()

    data = open(FILE_RATING, 'r', encoding='utf-8')
    for line in data:
        name, score = line.split()

        if name.lower() == username.lower():
            data.close()
            return name, score, False

    data.close()
    return username, 0, True


def exit_game():
    print("Bye!")
    exit()


def print_rating(username, new_user=False):
    score = 0
    if not new_user:
        data = open(FILE_RATING, 'r', encoding='utf-8')
        for line in data:
            name = line.split()[0]
            if username == name:
                score = line.split()[1]
                break
        data.close()
    else:
        data = open(FILE_RATING, 'a')
        data.write(f"{username.capitalize()} {score}\n")

    print(f"Your rating: {score}")


def define_rating(username, rating, new_user=False):
    file_data = open(FILE_RATING, 'r+')
    data = file_data.readlines()
    if new_user:
        data.append(f'{username} {rating}\n')
    else:
        for idx, info in enumerate(data):
            name = info.split()[0]
            if username == name:
                new_rating = int(info.split()[1]) + rating
                data[idx] = f'{name} {new_rating}\n'

    file_data.seek(0)
    file_data.writelines(data)
    file_data.close()


def read_user_options():
    input_options = input().strip().lower()

    return input_options


def fill_options(choice, options):
    idx_user_choice = options.index(choice)
    middle_nb = len(options) // 2
    winning_options, losing_options = [], []

    i = 1
    idx = idx_user_choice + 1
    while i <= middle_nb:
        if idx < len(options):
            winning_options.append(options[idx])
        else:
            idx = 0
            continue
        i += 1
        idx += 1

    losing_options = [option for option in options if option not in winning_options]

    if choice in losing_options: losing_options.remove(choice)
    if choice in winning_options: winning_options.remove(choice)

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
            winning_options, losing_options = fill_options(choice, game_options)
            if computer_choice in winning_options:  # computer win
                is_user_winner = False
            elif computer_choice in losing_options:  # user win
                is_user_winner = True
        elif not is_custom_options:
            if winning_map[choice] != computer_choice:  # computer win
                is_user_winner = False
            elif winning_map[choice] == computer_choice:  # user win
                is_user_winner = True

        if choice == computer_choice:  # draw
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
