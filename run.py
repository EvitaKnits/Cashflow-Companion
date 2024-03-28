# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
import string

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cashflow_companion')

# Common actions across multiple journeys
def get_budgets():
    """
    Collects the names, running totals and allocated amounts of each budget available 
    in the spreadsheet
    """
    budgets_list = SHEET.worksheets()
    letter = 'A'
    for budget in budgets_list:
        budget_name = budget.acell('A1').value
        running_total = budget.acell('B2').value
        amount_budgeted = budget.acell('B3').value
        print(f'{letter}-> {budget_name}: £{running_total} / £{amount_budgeted}')
        letters = string.ascii_uppercase
        index = letters.index(letter)
        letter = letters[index + 1]


# def enter_name():


# def enter_amount():


# def select_budget():


# def confirm_choice():


# def input_validation():

def go_home():
    """
    Prints the text at the start of the program and presents user
    with the menu of actions they can do in the app
    """
    print("Welcome to Cashflow Companion!\n")
    print("Here are your current budgets:\n")
    get_budgets()
    print()
    print("What would you like to do?\n")
    print("1-> Create a new budget")
    print("2-> Update an existing budget's name or amount")
    print("3-> Delete a budget")
    print("4-> Add, edit or delete an expense")
    print("5-> Generate a spending report\n")
    print("(If you would like to return home at any point, type 'home' into any input field instead of the requested value)\n")
    
    menu_choice = input("Please type the corresponding number and hit enter: ")
    return menu_choice

# User journeys

def home_menu_choice(menu_choice):
    """
    Takes the menu choice from go_home function and calls the appropriate 
    function to take the action the user chose. Validates that the user
    chose an available action. 
    """
    if menu_choice == '1':
        new_budget()
    elif menu_choice == '2':
        edit_budget()
    elif menu_choice == '3':
        delete_budget()
    elif menu_choice == '4':
        expense_menu()
    elif menu_choice == '5':
        report_menu()
    else:
        print("\nThis is not an available option. Please check again.\n")
        new_menu_choice = input("Please type the corresponding number and hit enter: ")
        home_menu_choice(new_menu_choice)

def new_budget():
    """
    Allows the user to create a new budget and amount allocated to it and updates the 
    Google sheet with it. Validates that the inputs are provided in the desired format. 
    Returns the user home. 
    """
    print("\nOK, what is the name of your new budget?")
    print("Please type the name (alphanumeric characters only) and hit enter.")
    budget_name = input("Name: ")
    if budget_name.isalnum():
        worksheet = SHEET.add_worksheet(title=f"{budget_name}", rows=100, cols=20)
        current_budget_worksheet = SHEET.get_worksheet(-1)
        current_budget_worksheet.update_cell(1, 1, budget_name)
        current_budget_worksheet.update_cell(2, 1, 'Running total')
        current_budget_worksheet.update_cell(3, 1, 'Amount budgeted')
        print("\nGreat, and how much do you want to allocate to this budget?")
        print("Please type the amount (numbers only) and hit enter.")
        budget_amount = input("Amount: ")
        while budget_amount.isnumeric() != True:
            print("\nOnly numbers are accepted - this is not a number.\n")
            print("Please type the amount (numbers only) and hit enter.")
            budget_amount = input("Amount: ")
        else: 
            worksheet.update_cell(3, 2, budget_amount)
            worksheet.update_cell(2, 2, 0)
    else:
        print("\nOnly alphanumerical characters are accepted - this included punctuation or special characters.\n")
        new_budget()
    print(f"Successfully added your new '{budget_name}' budget and allocated £{budget_amount}")
    print("Returning home...\n")
    main()

def edit_budget():
    """
    Asks user which budget they want to edit and whether they want to edit the name or amount. 
    Allows the user to change name or amount to whatever they input as long as it follows 
    formatting rules. Then it returns the user home. 
    """
    print("\nWhich budget would you like to update?\n")
    budget_choice = input("Please type the corresponding letter and hit enter: ")
    letters = string.ascii_uppercase
    index_of_choice = letters.index(budget_choice.upper())
    worksheet = SHEET.get_worksheet(index_of_choice)
    #need to add something here for invalid input - if not a letter, then if a letter but not one from the list
    budget_name = worksheet.acell('A1').value
    print(f"\nWe're updating the '{budget_name}' budget.")
    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    while name_or_amount.upper() != 'N' and name_or_amount.upper() != 'A':
        print("\nThis is not an available option. Please check again.")
        print("\nWould you like to change the name or the amount?")
        name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    else: 
        if name_or_amount.upper() == 'N':
            print(f"OK, what would you like the new name for the '{budget_name}' to be?\n")
            print("Please type the name (alphanumeric characters only) and hit enter.\n")
            new_name = input("Name: ")
            while new_name.isalnum() != True:
                print("\nOnly alphanumerical characters are accepted - this included punctuation or special characters.\n")
                print("Please type the name (alphanumeric characters only) and hit enter.\n")
                new_name = input("Name: ")
            else: 
                print(f"Changing the name of your '{budget_name}' budget to '{new_name}'")
                worksheet.update_cell(1, 1, new_name)
                print("Successfully changed.")
                print("\nReturning home...")
                main()
        else: 
            print(f"OK, how much would you like to allocate to '{budget_name}' now?")
            print("Please type the amount (numbers only) and hit enter.\n")
            new_amount = input("Amount: ")
            while new_amount.isnumeric() != True:
                print("\nOnly numbers are accepted - this is not a number.\n")
                print("Please type the amount (numbers only) and hit enter.")
                new_amount = input("Amount: ")
            else: 
                print(f"Allocating £{new_amount} to your '{budget_name}' budget...")
                worksheet.update_cell(3, 2, new_amount)
                print("Successfully changed.")
                print("\nReturning home...")
                main()

# def delete_budget():

# def expense_menu():

# def new_expense():

# def delete_expense():

# def edit_expense():

# def report_menu():

# def under_over_report():

# def last_three_report():

#The main function where we have the layout of the program and run it from

def main():
    """
    Runs all the functions in the program
    """
    menu_choice = go_home()
    home_menu_choice(menu_choice)


main()