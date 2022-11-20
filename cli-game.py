import requests
import random
import inquirer

#LOCAL FLASK DATABASE URL

url = "http://127.0.0.1:9000/presidents/"


def main_function():

    #ADD NEW PRESIDENT FUNCTION

    def add_president():
        name = input("New President's name: ")
        party = input("New President's party: ")
        year = input("New President's election year: ")
        while True:
            alive = input("Is your new President still alive? (y or n) ")
            if alive == "y":
                is_alive = True
                break
            elif alive == "n":
                is_alive = False
                break
            else:
                print("Please enter y or n")

        new_president = {
                "name": name,
                "party": party,
                "year_elected": year,
                "is_alive": is_alive,
                "vice_president_id": len(presidents) + 1
                }
        print(new_president)
        res = requests.post(url, json=new_president)
        print(res.json())
        print(f"Status code {res.status_code}")

    #DELETE PRESIDENT FUNCTION

    def delete_president():
        while True:
            president = input('Enter the name of the President that you want to delete. Type none to cancel.')
            if president == 'none':
                break
            else:
                deleted = False
                for i in range(len(presidents)):
                    if president == presidents[i]['name']:
                        res = requests.delete(f"{url}{presidents[i]['id']}")
                        print("President deleted!")
                        deleted = True
                        break
            if deleted == False:
                print("Sorry, that president wasn't found, try again.")
            else:
                break



    #CLI GAME FUNCTION

    def presidents_game():
        pres_list = list(presidents)
        random.shuffle(pres_list)
        correct = 0
        incorrect = 0

        print(f"Welcome to the US presidents trivia game! Do you know your presidents parties?\nIncludes custom presidents that you've added!")
    
        party_options = ['Democratic', 'Republican', 'Democratic-Republican', 'Whig', 'Federalist', 'None']

        i = 0
        while i < len(pres_list):
            guess = inquirer.list_input(f"{pres_list[i]['name']} belonged to which party?",
                    choices=party_options)

            print(f'You entered: {guess}')

            if guess == pres_list[i]['party']:
                print('Correct!')
                correct += 1
                i += 1
            else:
                print('Incorrect... The correct answer was ' + pres_list[i]['party'])
                incorrect += 1
                i += 1

            print(f'You have {correct} correct answers and {incorrect} incorrect answers\n')
        
        while True:
            play_again = input('Would you like to play again? (y or n) ')
            if play_again == 'y':
                presidents_game()
                break
            elif play_again == 'n':
                break


    response = requests.get(url)
    presidents = response.json()
    main_options = ['Play trivia', 'Add a president', 'Update a President', 'Delete a president']
    choice = inquirer.list_input('What would you like to do?',
            choices = main_options)
    match choice:
        case 'Play trivia':
            presidents_game()
        case 'Add a president':
            add_president()
        case 'Delete a president':
            delete_president()
    while True:
        do_else = input("Would you like to do something else? (y or n) ")
        if do_else == 'y':
            main_function()
            break
        elif do_else == 'n':
            break


print('Welcome to the CLI presidents widget!')
print('Here you can play the Presidents trivia game, add a custom president, update a president, or delete a president.')
main_function()
