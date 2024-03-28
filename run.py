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

# User journeys

# def new_budget():

# def delete_budget():

# def edit_budget():

# def new_expense():

# def delete_expense():

# def edit_expense():

# def under_over_report():

# def last_three_report():

#The main function where we have the layout of the program and run it from

def main():
    """
    Run all the functions in the program
    """
    go_home()

main()