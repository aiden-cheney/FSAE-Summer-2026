import random

def get_choices():
    player_choice = input("Enter a choice (Rock, Paper, or Siccors)")
    options = ["Rock", "Paper", "Sissors"]
    computer_choice = random.choice(options)

    choices =  {"player": player_choice, "computer": computer_choice}

    return choices

def check_win(player, computer):
    print (f"You chose {player}, Computer chose {computer}.")
    if player == computer:
        return "It's a tie!"
    
    elif player == "Rock": 
        if computer == "Sciccors":
            return "You win!"
        else:
            return "You Lose!"

    elif player == "Sciccors": 
        if computer == "Paper":
            return "You win!"
        else:
            return "You Lose!"

    elif player == "Paper": 
        if computer == "Rock":
            return "You win!"
        else:
            return "You Lose!"  

choices = get_choices()        
result = check_win(choices["player"], choices["computer"])

print (result)
