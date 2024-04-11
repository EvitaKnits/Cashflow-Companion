import gspread
from google.oauth2.service_account import Credentials
import string
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cashflow_companion')

# Home menu functions
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
    print("(To return home at any time, type 'home' into any input field)\n")
    
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
        create_new_budget()
    elif menu_choice == '2':
        edit_budget()
    elif menu_choice == '3':
        delete_budget()
    elif menu_choice == '4':
        expense_menu_budget_choice()
    elif menu_choice == '5':
        report_menu()
    elif menu_choice.lower() == 'home':
        main()
    else:
        print("\nThis is not an available option. Please check again.")
        new_menu_choice = input("Please type the corresponding number and hit enter: ")
        home_menu_choice(new_menu_choice)

def create_new_budget():
    """
    Allows the user to create a new budget and amount allocated to it and updates the 
    Google sheet with it. Validates that the inputs are provided in the desired format. 
    Returns the user home. 
    """
    list_budgets = SHEET.worksheets()
    number_budgets = len(list_budgets)

    if number_budgets >= 20:
        print("\nThe maximum number of 20 budgets has already been reached.")
        print("To create a new budget, first delete an existing budget")
        print("\nReturning home...\n")
        main()
    else: 
        print("\nOK, what is the name of your new budget?")
        budget_name = input("Please type the name and hit enter: ")
        new_budget = ['Amount budgeted']
        if budget_name.lower() == 'home':
            main()

        print("\nGreat, and how much do you want to allocate to this budget?")
        budget_amount = input("Please type the amount (numbers only) and hit enter: ")
        if budget_amount.lower() == 'home':
            main()
        
        while True: 
            try: 
                float_amount = float(budget_amount)
                if float_amount < 0:
                    print("\nNegative values are not accepted. Please enter a positive number.")
                    budget_amount = input("Please type the amount (numbers only) and hit enter: ")
                    continue
            except:
                if budget_amount.lower() == 'home':
                    main()  
                else:
                    print("\nOnly numbers are accepted - this is not a number.")
                    budget_amount = input("Please type the amount (numbers only) and hit enter: ")
            else: 
                try: 
                    worksheet = SHEET.add_worksheet(title=f"{budget_name}", rows=100, cols=20)
                except gspread.exceptions.APIError:
                    # This catches were the user attempts to use the same name for a budget twice
                    print("This budget name is already taken.")                    
                    create_new_budget()
                else:
                    current_budget_worksheet = SHEET.get_worksheet(-1)
                    current_budget_worksheet.update_cell(1, 1, budget_name)
                    current_budget_worksheet.update_cell(2, 1, 'Running total')
                    current_budget_worksheet.update_cell(2, 2, 0)
                    new_budget.append(format(float_amount, '.2f'))
                    current_budget_worksheet.append_row(new_budget)
                    print(f"\nSuccessfully added your new '{budget_name}' budget and allocated £{budget_amount}.")
                    print("\nReturning home...\n")
                    main()

def edit_budget():
    """
    Asks user which budget they want to edit and whether they want to edit the name or amount. 
    Allows the user to change name or amount to whatever they input as long as it follows 
    formatting rules. Then it returns the user home. 
    """
    print("\nWhich budget would you like to update?")
    budget_choice = input("Please type the corresponding letter and hit enter: ")
    letters = string.ascii_uppercase
    all_worksheets = SHEET.worksheets()

    while True:  
        if budget_choice.lower() == 'home':
                main()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        else:     
            break  
        
    worksheet = SHEET.get_worksheet(index_of_choice) 
    budget_name = worksheet.acell('A1').value
    print(f"\nWe're updating the '{budget_name}' budget.")
    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    while name_or_amount.upper() != 'N' and name_or_amount.upper() != 'A':
        if name_or_amount.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print("Would you like to change the name or the amount?")
            name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    else: 
        if name_or_amount.upper() == 'N':
            while True: 
                print(f"\nOK, what would you like the new name for the '{budget_name}' budget to be?")
                new_name = input("Please type the name and hit enter: ")
                if new_name.lower() == 'home':
                    main()
                else:
                    try: 
                        worksheet.update_title(new_name)
                    except gspread.exceptions.APIError:
                        # This catches were the user attempts to use the same name for a budget twice
                        print("This budget name is already taken.")  
                        continue
                    else:
                        print(f"\nChanging the name of your '{budget_name}' budget to '{new_name}'...")
                        worksheet.update_cell(1, 1, new_name)
                        print("\nSuccessfully changed.")
                        print("\nReturning home...\n")
                        main()
        else: 
            print(f"\nOK, how much would you like to allocate to '{budget_name}' now?")
            new_amount = input("Please type the amount (numbers only) and hit enter: ")
            while True:
                try: 
                    float_amount = float(new_amount)
                    if float_amount < 0:
                        print("\nNegative values are not accepted. Please enter a positive number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter: ")
                        continue
                except:
                    if new_amount.lower() == 'home':
                        main()
                    else:
                        print("\nOnly numbers are accepted - this is not a number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter: ")
                else: 
                    print(f"\nAllocating £{new_amount} to your '{budget_name}' budget...\n")
                    formatted_number = "{:.2f}".format(float_amount)
                    worksheet.update_cell(3, 2, formatted_number)
                    print("Successfully changed.")
                    print("\nReturning home...\n")
                    main()

def delete_budget():
    """				
    Asks user which budget they want to delete, then asks them if they're sure. If yes, the				
    budget is deleted, if not, a message confirms that nothing has been deleted. Then it returns				
    the user home.				
    """				
	
    print("\nOK, which budget would you like to delete?")
    budget_choice = input("Please type the corresponding letter and hit enter: ")
    letters = string.ascii_uppercase
    all_worksheets = SHEET.worksheets()

    while True: 
        if budget_choice.lower() == 'home':
            main()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue     
        else:
            break   
    
    worksheet = SHEET.get_worksheet(index_of_choice) 
    budget_name = worksheet.acell('A1').value
    print(f"\nAre you sure you want to delete your '{budget_name}' budget?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter: ")
    while confirm_choice.upper() != 'Y' and confirm_choice.upper() != 'N':
        if confirm_choice.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print(f"Are you sure you want to delete your '{budget_name}' budget?")
            confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter: ")
    else: 
        if confirm_choice.upper() == 'Y':
            SHEET.del_worksheet(worksheet)
            print(f"\nYour '{budget_name}' budget has been deleted.")
            print("\nReturning home...\n")
            main()
        else:
            print("\nNo budget has been deleted.")
            print("\nReturning home...\n")
            main()
            
def expense_menu_budget_choice():
    """
    Allows user to select which budget they would like to perform an action in.
    """
    print("\nOK, in which budget would you like to add, edit or delete an expense?")
    budget_choice = input("Please type the corresponding letter and hit enter: ")
    letters = string.ascii_uppercase
    all_worksheets = SHEET.worksheets()

    while True:  
        if budget_choice.lower() == 'home':
                main()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        else:     
            break   
            
    worksheet = SHEET.get_worksheet(index_of_choice) 
    budget_name = worksheet.acell('A1').value
    running_total = worksheet.acell('B2').value
    amount_budgeted = worksheet.acell('B3').value
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount Budgeted: £{amount_budgeted}")

    num = 4
    expenses = []
    while True:
        values_list = worksheet.row_values(num)
        # use the fact that None is falsy to break the while loop when the worksheet has no more expenses in it
        if not values_list:
            break
        current_expense = []
        for row in values_list:
            current_expense.append(row)
        num += 1
        expenses.append(current_expense)

    if not expenses: 
        print("\nNo expenses logged yet.")
    else: 
        print("\nMost Recent Expenses:\n")
        number = 1
        loop_counter = 0
        while True: 
            if loop_counter == 5:
                break
            if not expenses:
                break
            for expense in expenses:
                if loop_counter == 5:
                    break
                print(f"{number}. {expenses[-1][0]}: £{expenses[-1][1]}")
                expenses.pop(-1)
                number += 1
                loop_counter += 1
    expense_menu_action_choice(budget_name, worksheet)

def expense_menu_action_choice(budget_name, worksheet):
    """
    Prints the text for the menu of actions they can do in relation to expenses.
    Allows the user to pick from the menu and moves onto the correct function in the program 
    to carry out that action.
    """
    print(f"\nWould you like to add, edit or delete an expense in the '{budget_name}' budget?")
    print("\nA -> Add an expense")
    print("B -> Edit an expense")
    print("C -> Delete an expense")
    menu_choice = input("\nPlease type the corresponding letter and hit enter: ")
    while menu_choice.upper() != 'A' and menu_choice.upper() != 'B' and menu_choice.upper() != 'C':
        if menu_choice.lower() == 'home':
            main()
        else: 
            print("\nThis is not an available option. Please check again.")
            menu_choice = input("Please type the corresponding letter and hit enter: ")
            if menu_choice.lower() == 'home':
                main()
    else:
        if menu_choice.upper() == 'A':
            new_expense(budget_name, worksheet)
        elif menu_choice.upper() == 'B':
            edit_expense(budget_name, worksheet)
        elif menu_choice.upper() == 'C':
            delete_expense(budget_name, worksheet)

def new_expense(budget_name, worksheet):
    """
    Allows the user to add a new expense to their desired budget
    """
    print("\nWhat is the name of your new expense?")
    name = input("Please type the name and hit enter: ")
    if name.lower() == 'home':
        main()
    else: 
        new_row = []
        new_row.append(name)
        print(f"\nAnd how much did '{name}' cost?")
        cost = input("Please type the amount (numbers only) and hit enter: ")
        if cost.lower() == 'home':
            main()
    while True:
        try: 
            float_amount = float(cost)
            if float_amount < 0:
                print("\nNegative values are not accepted. Please enter a positive number.")
                cost = input("Please type the amount (numbers only) and hit enter: ")
                continue
        except:
            print("\nOnly numbers are accepted - this is not a number.")
            cost = input("Please type the amount (numbers only) and hit enter: ")
            if cost.lower() == 'home':
                main()
        else: 
            new_row.append(format(float_amount, '.2f'))
            formatted_number = "{:.2f}".format(float_amount)
            print(f"\nAdding your new expense: '{name}: £{formatted_number}'...")
            worksheet.append_row(new_row)
            print("\nSuccessfully added.")
            print(f"\nCalculating the new running total for your '{budget_name}' budget...")
            running_total = float(worksheet.acell('B2').value)
            running_total += float_amount 
            worksheet.update_cell(2, 2, running_total)
            print("\nSuccessfully calculated and updated.")
            print(f"\nReturning to '{budget_name}' budget.")
            break
    expense_menu_action_choice(budget_name, worksheet)
        
def delete_expense(budget_name, worksheet):
    """
    Allows the user to delete a specific expense from their desired budget. Then it
    returns the user to that budget and the expense action menu
    """
    # use the fact that None is falsy to break the while loop when the worksheet has no more expenses in it
    num = 4
    expenses = []
    while True:
        values_list = worksheet.row_values(num)
        if not values_list or not any(values_list):
            break
        expenses.append(values_list)
        num += 1

    if not expenses: 
        print("\nNo expenses logged yet.")
    else: 
        print("\nAll Expenses:\n")
        number = 1
        while expenses:
                print(f"{number}. {expenses[0][0]}: £{expenses[0][1]}")
                expenses.pop(0)
                number += 1
    print("\nWhich expense would you like to delete?")
    select_expense = input("Please type the corresponding number and hit enter: ")
    number_rows = worksheet.get_all_values()

    while True:  
        if select_expense.lower() == 'home':
            main()
        if select_expense.isnumeric() != True: 
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the corresponding number and hit enter: ")
            continue
        row_index = int(select_expense) + 3 
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the corresponding number and hit enter: ")
            continue
        else:     
            break  

    print(f"\nAre you sure you want to delete this expense?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter: ")
    while confirm_choice.upper() != 'Y' and confirm_choice.upper() != 'N':
        if confirm_choice.lower() == 'home':
            main()
        else: 
            print("\nThis is not an available option. Please check again.")
            print(f"Are you sure you want to delete this expense?")
            confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter: ")
    else:
        if confirm_choice.upper() == 'Y':
            running_total = float(worksheet.acell('B2').value)
            deleted_expense = worksheet.row_values(row_index)
            deleted_expense_amount = deleted_expense[1]
            running_total -= float(deleted_expense_amount)
            worksheet.update_cell(2, 2, running_total)
            worksheet.delete_rows(row_index)
            print(f"\nThis expense has been deleted.")
            print(f"\nCalculating the new running total for your '{budget_name}' budget...")
            print("\nSuccessfully calculated and updated.")
            print(f"\nReturning to '{budget_name}' budget...")
        else:
            print("\nNo expense has been deleted.")
            print(f"\nReturning to '{budget_name}' budget...")
    expense_menu_action_choice(budget_name, worksheet)

def edit_expense(budget_name, worksheet):
    """
    Allows the user to edit a specific expense from their desired budget. Then it
    returns the user to that budget and the expense action menu
    """
    # use the fact that None is falsy to break the while loop when the worksheet has no more expenses in it
    num = 4
    expenses = []
    while True:
        values_list = worksheet.row_values(num)
        if not values_list or not any(values_list):
            break
        expenses.append(values_list)
        num += 1

    if not expenses: 
        print("\nNo expenses logged yet.")
    else: 
        print("\nAll Expenses:\n")
        number = 1
        while expenses:
                print(f"{number}. {expenses[0][0]}: £{expenses[0][1]}")
                expenses.pop(0)
                number += 1
    print("\nWhich expense would you like to edit?")
    select_expense = input("Please type the corresponding number and hit enter: ")
    number_rows = worksheet.get_all_values()

    while True:  
        if select_expense.lower() == 'home':
            main()
        if select_expense.isnumeric() != True: 
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the corresponding number and hit enter: ")
            continue
        row_index = int(select_expense) + 3 
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the corresponding number and hit enter: ")
            continue
        else:     
            break  

    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    while name_or_amount.upper() != 'N' and name_or_amount.upper() != 'A':
        if name_or_amount.lower() == 'home':
            main()
        else: 
            print("\nThis is not an available option. Please check again.")
            print("Would you like to change the name or the amount?")
            name_or_amount = input("Please type 'N' for name or 'A' for amount: ")
    else: 
        if name_or_amount.upper() == 'N':
            print(f"\nOK, what would you like the new name for this expense to be?")
            new_name = input("Please type the name and hit enter: ")
            if new_name.lower() == 'home':
                main()
            else:
                print(f"\nChanging the name of this expense to '{new_name}...'")
                worksheet.update_cell(row_index, 1, new_name)
                print("\nSuccessfully changed.")
                print(f"\nReturning to '{budget_name}' budget...")
        else: 
            print(f"\nOK, how much would you like this expense to be now?")
            new_amount = input("Please type the amount (numbers only) and hit enter: ")
            while True:
                try: 
                    float_amount = float(new_amount)
                    if float_amount < 0:
                        print("\nNegative values are not accepted. Please enter a positive number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter: ")
                        continue
                except:
                    if new_amount.lower() == 'home':
                        main()
                    else: 
                        print("\nOnly numbers are accepted - this is not a number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter: ")
                else: 
                    formatted_number = "{:.2f}".format(float_amount)
                    print(f"\nChanging the amount of this expense to £{formatted_number}...\n")
                    old_amount_row = worksheet.row_values(row_index)
                    old_amount = old_amount_row[1]
                    worksheet.update_cell(row_index, 2, formatted_number)
                    print("Successfully changed.")
                    print(f"\nCalculating the new running total for your '{budget_name}' budget...")
                    running_total = float(worksheet.acell('B2').value)
                    running_total -= float(old_amount)
                    running_total += float_amount 
                    worksheet.update_cell(2, 2, running_total)
                    print("\nSuccessfully calculated and updated.")
                    print(f"\nReturning to '{budget_name}' budget...")
                    break
    expense_menu_action_choice(budget_name, worksheet)

def report_menu():
    """
    Option 5 from the home menu function comes to this report menu function which calls 
    the appropriate function to produce the report that the user chose. Validates that the user
    chose an available action. 
    """
    print("\nWhich report would you like to run?")
    print("\nA-> A report of all budgets with whether your spending is under/over")
    print("B-> A report showing the last three expenses from every budget")
    print("C-> A report showing every expense in a specific budget")
    while True:
        report_choice = input("\nPlease type the corresponding letter and hit enter: ")
        if report_choice.upper() == 'A':
            under_over_report()
            break
        elif report_choice.upper() == 'B':
            last_three_report()
            break
        elif report_choice.upper() == 'C':
            every_expense_report()
            break
        elif report_choice.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
       
def under_over_report():
    todays_date = datetime.datetime.now()
    day_only = todays_date.strftime("%d")
    which_month = todays_date.strftime("%m")

    if which_month == 4 or which_month == 6 or which_month == 9 or which_month == 11:
        month_percentage = (float(day_only) / 30) * 100
        formatted_percentage = round(month_percentage, 2)
    elif which_month == 2:
        month_percentage = (float(day_only) / 28) * 100
        formatted_percentage = round(month_percentage, 2)
    else:
        month_percentage = (float(day_only) / 31) * 100
        formatted_percentage = round(month_percentage, 2)
    
    print(f"\nYou are {formatted_percentage}% of the way through the month.")
    print("\nThis report compares:")
    print(" - how far through the month you are")
    print(" - how far through your budgeted amount you are")
    print("\nThen calculates an 'over'/'under'/'spot on' value for each budget.")

    print("\nHere are your current calculations:\n")
    worksheets = SHEET.worksheets()
    for worksheet in worksheets: 
        budget_name = worksheet.acell('A1').value
        running_total = worksheet.acell('B2').value
        amount_budgeted = worksheet.acell('B3').value
        percentage_spent = (float(running_total) / float(amount_budgeted)) *100
        formatted_spent = round(percentage_spent, 2)
        if formatted_spent < formatted_percentage:
            over_under = "UNDER"
        elif formatted_spent == formatted_percentage:
            over_under = "SPOT ON"
        else: 
            over_under = "OVER"
        print(f"{budget_name} - £{running_total} / £{amount_budgeted} - {formatted_spent}% spent - {over_under} budget")
    
    home = input("\nWhen you're ready to return home, type 'home' here and hit enter: ")
    while True: 
        if home.lower() == 'home':
            main()
        else: 
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter: ")

def last_three_report():
    print("\nHere are the latest three expenses from each budget:")
    print("Where there are less than three, all expenses in that budget are displayed.")
    worksheets = SHEET.worksheets()
    for worksheet in worksheets: 
        budget_name = worksheet.acell('A1').value
        running_total = worksheet.acell('B2').value
        amount_budgeted = worksheet.acell('B3').value
        print(f"\n{budget_name} - £{running_total} / £{amount_budgeted}")
        
        num = 4
        expenses = []
        while True:
            values_list = worksheet.row_values(num)
            if not values_list:
                break
            current_expense = []
            for row in values_list:
                current_expense.append(row)
            num += 1
            expenses.append(current_expense)
        
        if not expenses: 
            print("No expenses logged yet.")
        else: 
            loop_counter = 0
            while True:
                if loop_counter == 3:
                    break
                if not expenses:
                    break
                for expense in expenses:
                    if loop_counter == 3:
                        break
                    print(f"---> {expenses[-1][0]}: £{expenses[-1][1]}")
                    expenses.pop (-1)
                    loop_counter += 1       

    home = input("\nWhen you're ready to return home, type 'home' here and hit enter: ")
    while True: 
        if home.lower() == 'home':
            main()
        else: 
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter: ")
    

def every_expense_report():
    print("\nFrom which budget would you like to see all of the expenses?")
    budget_choice = input("Please type the corresponding letter and hit enter: ")
    letters = string.ascii_uppercase
    all_worksheets = SHEET.worksheets()
    
    while True:  
        if budget_choice.lower() == 'home':
                main()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter: ")
            continue
        else:     
            break
              
    worksheet = SHEET.get_worksheet(index_of_choice) 
    budget_name = worksheet.acell('A1').value
    running_total = worksheet.acell('B2').value
    amount_budgeted = worksheet.acell('B3').value
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount Budgeted: £{amount_budgeted}")

    # use the fact that None is falsy to break the while loop when the worksheet has no more expenses in it
    num = 4
    expenses = []
    while True:
        values_list = worksheet.row_values(num)
        if not values_list:
            break
        current_expense = []
        for row in values_list:
            current_expense.append(row)
        num += 1
        expenses.append(current_expense)

    if not expenses: 
        print("\nNo expenses logged yet.")
    else: 
        print("\nAll Expenses:\n")
        number = 1
        while expenses:
            print(f"{number}. {expenses[0][0]}: £{expenses[0][1]}")
            expenses.pop(0)
            number += 1
    home = input("\nWhen you're ready to return home, type 'home' here and hit enter: ")
    while True: 
        if home.lower() == 'home':
            main()
        else: 
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter: ")

#The main function where we have the layout of the program and run it from

def main():
    """
    Runs all the functions in the program
    """
    menu_choice = go_home()
    home_menu_choice(menu_choice)

main()