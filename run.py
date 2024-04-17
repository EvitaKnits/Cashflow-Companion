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

# Validation and exception functions:


def length_check(user_input):
    """
    Enforces a minimum of 1 chraracter and maximum of 15 characters on text
    inputs when called. This is used for budget and expense names.
    """
    if len(user_input) <= 15 and len(user_input) >= 1:
        stripped_input = user_input.strip()
        return stripped_input
    else:
        print("Your input must be between 1 and 15 characters long. Please try again.")
        return False


def get_data(api_call, *args):
    """
    Calls the API to get all the different types of data the program needs for
    those types that are used more than once. Catches 429 exceptions which are
    thrown when your API call quota is exceeded and exits the program. Also
    catches any other exception when calling the API in a generic fashion and
    starts the program again.
    """
    if api_call == "all_worksheets":
        try:
            return (SHEET.worksheets())
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()
    elif api_call == "one_cell":
        try:
            worksheet = args[0]
            cell_address = args[1]
            return worksheet.acell(cell_address)
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()
    elif api_call == 'get_records':
        try:
            worksheet = args[0]
            return worksheet.get_all_records()
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()
    elif api_call == 'get_info':
        try:
            worksheet = args[0]
            range = args[1]
            return worksheet.get(range)
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()
    elif api_call == 'get_values':
        try:
            worksheet = args[0]
            return worksheet.get_all_values()
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()
    elif api_call == 'get_rows':
        try:
            worksheet = args[0]
            row_index = args[1]
            return worksheet.row_values(row_index)
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()


def write_data(api_call, *args):
    """
    Calls the API to write all the different types of data the program needs
    for those types that are used more than once to update in the Google sheet.
    Catches 429 exceptions which are thrown when your API call quota is
    exceeded and exits the program. Also catches any other exception when
    calling the API in a generic fashion and starts the program again.
    """
    if api_call == 'cell_update':
        try:
            worksheet = args[0]
            row = args[1]
            column = args[2]
            value = args[3]
            worksheet.update_cell(row, column, value)
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("System busy. Please try again in one minute.")
                exit()
        except Exception:
            print("Sorry, something went wrong. Returning you home...")
            main()


# Home menu functions

def get_budgets():
    """
    Collects the names, running totals and allocated amounts of each budget
    available in the spreadsheet
    """
    budgets_list = get_data("all_worksheets")
    letter = 'A'
    for budget in budgets_list:
        value_range = budget.get('A1:B3')
        budget_name = value_range[0][0]
        running_total = value_range[1][1]
        amount_budgeted = value_range[2][1]
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

    menu_choice = input("Please type the corresponding number and hit enter:\n")
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
        new_menu_choice = input("Please type the corresponding number and hit enter:\n")
        home_menu_choice(new_menu_choice)


def create_new_budget():
    """
    Allows the user to create a new budget and amount allocated to it and updates the
    Google sheet with it. Validates that the inputs are provided in the desired format.
    Returns the user home.
    """
    list_budgets = get_data("all_worksheets")
    number_budgets = len(list_budgets)

    if number_budgets >= 20:
        print("\nThe maximum number of 20 budgets has already been reached.")
        print("To create a new budget, first delete an existing budget")
        print("\nReturning home...\n")
        main()
    else:
        while True:
            print("\nOK, what is the name of your new budget?")
            budget_name = input("Please type the name and hit enter:\n")
            if length_check(budget_name):
                break
        if budget_name.lower() == 'home':
            main()

        print("\nGreat, and how much do you want to allocate to this budget?")
        budget_amount = input("Please type the amount (numbers only) and hit enter:\n")
        if budget_amount.lower() == 'home':
            main()

        while True:
            try:
                float_amount = float(budget_amount)
                if float_amount < 0:
                    print("\nNegative values are not accepted. Please enter a positive number.")
                    budget_amount = input("Please type the amount (numbers only) and hit enter:\n")
                    continue
            except Exception:
                if budget_amount.lower() == 'home':
                    main()
                else:
                    print("\nOnly numbers are accepted - this is not a number.")
                    budget_amount = input("Please type the amount (numbers only) and hit enter:\n")
            else:
                try:
                    worksheet = SHEET.add_worksheet(title=f"{budget_name}", rows=100, cols=20)
                except gspread.exceptions.APIError as e:
                    if e.response.status_code == 429:
                        # This catches where this request pushes over the quota limit
                        print("System busy. Please try again in one minute.")
                        exit()
                    elif e.response.status_code == 400:
                        # This catches where the user attempts to use the same name for a budget twice
                        print("This budget name is already taken.")
                        create_new_budget()
                    else:
                        # This catches all other APIError codes
                        print("Sorry, something went wrong. Returning home...")
                        main()
                except Exception:
                    # This catches all other exceptions
                    print("Sorry, something went wrong. Returning home...")
                    main()
                else:
                    budget_amount = format(float_amount, '.2f')
                    all_worksheets = get_data("all_worksheets")
                    current_budget_worksheet = all_worksheets[-1]
                    try:
                        current_budget_worksheet.update([[budget_name, '', ], ['Running Total', 0, ], ['Amount Budgeted', budget_amount]])
                    except gspread.exceptions.APIError as e:
                        if e.response.status_code == 429:
                            # This catches where this request pushes over the quota limit
                            print("System busy. Please try again in one minute.")
                            exit()
                        else:
                            # This catches all other APIError codes
                            print("Sorry, something went wrong. Returning home...")
                            main()
                    except Exception:
                        # This catches all other exceptions
                        print("Sorry, something went wrong. Returning home...")
                        main()
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
    budget_choice = input("Please type the corresponding letter and hit enter:\n")
    letters = string.ascii_uppercase
    all_worksheets = get_data("all_worksheets")

    while True:
        if budget_choice.lower() == 'home':
            main()
        if budget_choice == '':
            print("Blank values not accepted.")
            edit_budget()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        else:
            break

    all_worksheets = get_data("all_worksheets")
    worksheet = all_worksheets[index_of_choice]
    budget_name = get_data('one_cell', worksheet, 'A1').value
    print(f"\nWe're updating the '{budget_name}' budget.")
    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for amount:\n")
    while name_or_amount.upper() != 'N' and name_or_amount.upper() != 'A':
        if name_or_amount.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print("Would you like to change the name or the amount?")
            name_or_amount = input("Please type 'N' for name or 'A' for amount:\n")
    else:
        if name_or_amount.upper() == 'N':
            while True:
                while True:
                    print(f"\nOK, what would you like the new name for the '{budget_name}' budget to be?")
                    new_name = input("Please type the name and hit enter:\n")
                    if length_check(new_name):
                        break
                if new_name.lower() == 'home':
                    main()
                else:
                    try:
                        worksheet.update_title(new_name)
                    except gspread.exceptions.APIError as e:
                        if e.response.status_code == 429:
                            # This catches where this request pushes over the quota limit
                            print("System busy. Please try again in one minute.")
                            exit()
                        elif e.response.status_code == 400:
                            # This catches where the user attempts to use the same name for a budget twice
                            print("This budget name is already taken.")
                            edit_budget()
                        else:
                            # This catches all other APIError codes
                            print("Sorry, something went wrong. Returning home...")
                            main()
                    except Exception:
                        # This catches all other exceptions
                        print("Sorry, something went wrong. Returning home...")
                        main()
                    else:
                        print(f"\nChanging the name of your '{budget_name}' budget to '{new_name}'...")
                        write_data('cell_update', worksheet, 1, 1, new_name)
                        print("\nSuccessfully changed.")
                        print("\nReturning home...\n")
                        main()
        else:
            print(f"\nOK, how much would you like to allocate to '{budget_name}' now?")
            new_amount = input("Please type the amount (numbers only) and hit enter:\n")
            while True:
                try:
                    float_amount = float(new_amount)
                    if float_amount < 0:
                        print("\nNegative values are not accepted. Please enter a positive number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter:\n")
                        continue
                except Exception:
                    if new_amount.lower() == 'home':
                        main()
                    else:
                        print("\nOnly numbers are accepted - this is not a number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter:\n")
                else:
                    print(f"\nAllocating £{new_amount} to your '{budget_name}' budget...\n")
                    formatted_number = "{:.2f}".format(float_amount)
                    write_data('cell_update', worksheet, 3, 2, formatted_number)
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
    budget_choice = input("Please type the corresponding letter and hit enter:\n")
    letters = string.ascii_uppercase
    all_worksheets = get_data("all_worksheets")

    while True:
        if budget_choice.lower() == 'home':
            main()
        if budget_choice == '':
            print("Blank values not accepted.")
            delete_budget()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        else:
            break

    all_worksheets = get_data("all_worksheets")
    worksheet = all_worksheets[index_of_choice]
    budget_name = get_data('one_cell', worksheet, 'A1').value
    print(f"\nAre you sure you want to delete your '{budget_name}' budget?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter:\n")
    while confirm_choice.upper() != 'Y' and confirm_choice.upper() != 'N':
        if confirm_choice.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print(f"Are you sure you want to delete your '{budget_name}' budget?")
            confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter:\n")
    else:
        if confirm_choice.upper() == 'Y':
            try:
                SHEET.del_worksheet(worksheet)
            except gspread.exceptions.APIError as e:
                if e.response.status_code == 429:
                    print("System busy. Please try again in one minute.")
                    exit()
            except Exception:
                print("Sorry, something went wrong. Returning you home...")
                main()
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
    budget_choice = input("Please type the corresponding letter and hit enter:\n")
    letters = string.ascii_uppercase
    all_worksheets = get_data("all_worksheets")

    while True:
        if budget_choice.lower() == 'home':
            main()
        if budget_choice == '':
            print("Blank values not accepted.")
            expense_menu_budget_choice()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        else:
            break

    all_worksheets = get_data("all_worksheets")
    worksheet = all_worksheets[index_of_choice]
    value_range = get_data('get_info', worksheet, 'A1:B3')
    budget_name = value_range[0][0]
    running_total = value_range[1][1]
    amount_budgeted = value_range[2][1]
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount Budgeted: £{amount_budgeted}")

    all_rows = get_data('get_records', worksheet)
    all_expenses = all_rows[2:]
    all_expenses_list = [list(dictionary.values()) for dictionary in all_expenses]

    if not all_expenses:
        print("\nNo expenses logged yet.")
        print("You can only add a new expense.")
        new_expense(budget_name, worksheet)

    else:
        print("\nMost Recent Expenses:\n")
        number = 1
        loop_counter = 0
        while True:
            # use the fact that None is falsy to break the while loop when the list has no more expenses in it before reaching 5
            if not all_expenses_list:
                break
            for expense in reversed(all_expenses_list):
                if loop_counter == 5:
                    break
                formatted_number = "{:.2f}".format(expense[1])
                print(f"{number}. {expense[0]}: £{formatted_number}")
                number += 1
                loop_counter += 1
            break
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
    menu_choice = input("\nPlease type the corresponding letter and hit enter:\n")
    while menu_choice.upper() != 'A' and menu_choice.upper() != 'B' and menu_choice.upper() != 'C':
        if menu_choice.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            menu_choice = input("Please type the corresponding letter and hit enter:\n")
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
    while True:
        print("\nWhat is the name of your new expense?")
        name = input("Please type the name and hit enter:\n")
        if length_check(name):
            break
    if name.lower() == 'home':
        main()
    else:
        new_row = []
        new_row.append(name)
        print(f"\nAnd how much did '{name}' cost?")
        cost = input("Please type the amount (numbers only) and hit enter:\n")
        if cost.lower() == 'home':
            main()
    while True:
        try:
            float_amount = float(cost)
            if float_amount < 0:
                print("\nNegative values are not accepted. Please enter a positive number.")
                cost = input("Please type the amount (numbers only) and hit enter:\n")
                continue
        except Exception:
            print("\nOnly numbers are accepted - this is not a number.")
            cost = input("Please type the amount (numbers only) and hit enter:\n")
            if cost.lower() == 'home':
                main()
        else:
            new_row.append(format(float_amount, '.2f'))
            formatted_number = "{:.2f}".format(float_amount)
            print(f"\nAdding your new expense: '{name}: £{formatted_number}'...")
            try:
                worksheet.append_row(new_row)
            except gspread.exceptions.APIError as e:
                if e.response.status_code == 429:
                    print("System busy. Please try again in one minute.")
                    exit()
            except Exception:
                print("Sorry, something went wrong. Returning you home...")
                main()
            print("\nSuccessfully added.")
            print(f"\nCalculating the new running total for your '{budget_name}' budget...")
            running_total = float(get_data('one_cell', worksheet, 'B2').value)
            running_total += float_amount
            write_data('cell_update', worksheet, 2, 2, running_total)
            print("\nSuccessfully calculated and updated.")
            print(f"\nReturning to '{budget_name}' budget.")
            break
    expense_menu_action_choice(budget_name, worksheet)


def delete_expense(budget_name, worksheet):
    """
    Allows the user to delete a specific expense from their desired budget. Then it
    returns the user to that budget and the expense action menu
    """
    all_rows = get_data('get_records', worksheet)
    all_expenses = all_rows[2:]
    all_expenses_list = [list(dictionary.values()) for dictionary in all_expenses]

    if not all_expenses:
        print("\nNo expenses logged yet.")
    else:
        print("\nAll Expenses:\n")
        number = 1
        for expense in all_expenses_list:
            formatted_number = "{:.2f}".format(expense[1])
            print(f"{number}. {expense[0]}: £{formatted_number}")
            number += 1

    print("\nWhich expense would you like to delete?")
    select_expense = input("Please type the corresponding number and hit enter:\n")
    number_rows = get_data('get_values', worksheet)

    while True:
        if select_expense.lower() == 'home':
            main()
        if select_expense.isnumeric() is False:
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the corresponding number and hit enter:\n")
            continue
        row_index = int(select_expense) + 3
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the corresponding number and hit enter:\n")
            continue
        else:
            break

    print(f"\nAre you sure you want to delete this expense?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter:\n")
    while confirm_choice.upper() != 'Y' and confirm_choice.upper() != 'N':
        if confirm_choice.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print(f"Are you sure you want to delete this expense?")
            confirm_choice = input("Type 'Y' for yes or 'N' for no and hit enter:\n")
    else:
        if confirm_choice.upper() == 'Y':
            running_total = float(get_data('one_cell', worksheet, 'B2').value)
            deleted_expense = get_data('get_rows', worksheet, row_index)
            deleted_expense_amount = deleted_expense[1]
            running_total -= float(deleted_expense_amount)
            write_data('cell_update', worksheet, 2, 2, running_total)
            try:
                worksheet.delete_rows(row_index)
            except gspread.exceptions.APIError as e:
                if e.response.status_code == 429:
                    print("System busy. Please try again in one minute.")
                    exit()
            except Exception:
                print("Sorry, something went wrong. Returning you home...")
                main()
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

    all_rows = get_data('get_records', worksheet)
    all_expenses = all_rows[2:]
    all_expenses_list = [list(dictionary.values()) for dictionary in all_expenses]

    if not all_expenses:
        print("\nNo expenses logged yet.")
    else:
        print("\nAll Expenses:\n")
        number = 1
        while True:
            # use the fact that None is falsy to break the while loop when the list has no more expenses in it before reaching 5
            if not all_expenses_list:
                break
            for expense in all_expenses_list:
                formatted_number = "{:.2f}".format(expense[1])
                print(f"{number}. {expense[0]}: £{formatted_number}")
                number += 1
            break
    print("\nWhich expense would you like to edit?")
    select_expense = input("Please type the corresponding number and hit enter:\n")
    number_rows = get_data('get_values', worksheet)

    while True:
        if select_expense.lower() == 'home':
            main()
        if select_expense.isnumeric() is False:
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the corresponding number and hit enter:\n")
            continue
        row_index = int(select_expense) + 3
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the corresponding number and hit enter:\n")
            continue
        else:
            break

    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for amount:\n")
    while name_or_amount.upper() != 'N' and name_or_amount.upper() != 'A':
        if name_or_amount.lower() == 'home':
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            print("Would you like to change the name or the amount?")
            name_or_amount = input("Please type 'N' for name or 'A' for amount:\n")
    else:
        if name_or_amount.upper() == 'N':
            while True:
                print(f"\nOK, what would you like the new name for this expense to be?")
                new_name = input("Please type the name and hit enter:\n")
                if length_check(new_name):
                    break
            if new_name.lower() == 'home':
                main()
            else:
                print(f"\nChanging the name of this expense to '{new_name}...'")
                write_data('cell_update', worksheet, row_index, 1, new_name)
                print("\nSuccessfully changed.")
                print(f"\nReturning to '{budget_name}' budget...")
        else:
            print(f"\nOK, how much would you like this expense to be now?")
            new_amount = input("Please type the amount (numbers only) and hit enter:\n")
            while True:
                try:
                    float_amount = float(new_amount)
                    if float_amount < 0:
                        print("\nNegative values are not accepted. Please enter a positive number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter:\n")
                        continue
                except Exception:
                    if new_amount.lower() == 'home':
                        main()
                    else:
                        print("\nOnly numbers are accepted - this is not a number.")
                        new_amount = input("Please type the amount (numbers only) and hit enter:\n")
                else:
                    formatted_number = "{:.2f}".format(float_amount)
                    print(f"\nChanging the amount of this expense to £{formatted_number}...\n")
                    old_amount_row = get_data('get_rows', worksheet, row_index)
                    old_amount = old_amount_row[1]
                    write_data('cell_update', worksheet, row_index, 2, formatted_number)
                    print("Successfully changed.")
                    print(f"\nCalculating the new running total for your '{budget_name}' budget...")
                    running_total = float(get_data('one_cell', worksheet, 'B2').value)
                    running_total -= float(old_amount)
                    running_total += float_amount
                    write_data('cell_update', worksheet, 2, 2, running_total)
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
        report_choice = input("\nPlease type the corresponding letter and hit enter:\n")
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
    worksheets = get_data("all_worksheets")
    for worksheet in worksheets:
        value_range = get_data('get_info', worksheet, 'A1:B3')
        budget_name = value_range[0][0]
        running_total = value_range[1][1]
        amount_budgeted = value_range[2][1]
        percentage_spent = (float(running_total) / float(amount_budgeted)) * 100
        formatted_spent = round(percentage_spent, 2)
        if formatted_spent < formatted_percentage:
            over_under = "UNDER"
        elif formatted_spent == formatted_percentage:
            over_under = "SPOT ON"
        else:
            over_under = "OVER"
        print(f"{budget_name} - £{running_total} / £{amount_budgeted} - {formatted_spent}% spent - {over_under} budget")

    home = input("\nWhen you're ready to return home, type 'home' here and hit enter:\n")
    while True:
        if home.lower() == 'home':
            main()
        else:
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter:\n")


def last_three_report():
    print("\nHere are the latest three expenses from each budget:")
    print("Where there are less than three, all expenses in that budget are displayed.")
    worksheets = get_data("all_worksheets")
    for worksheet in worksheets:
        value_range = get_data('get_info', worksheet, 'A1:B3')
        budget_name = value_range[0][0]
        running_total = value_range[1][1]
        amount_budgeted = value_range[2][1]
        print(f"\n{budget_name} - £{running_total} / £{amount_budgeted}")

        all_rows = get_data('get_records', worksheet)
        all_expenses = all_rows[2:]
        all_expenses_list = [list(dictionary.values()) for dictionary in all_expenses]

        if not all_expenses:
            print("---> No expenses logged yet.")
        else:
            loop_counter = 0
            while True:
                if loop_counter == 3:
                    break
                if not all_expenses_list:
                    break
                # use the fact that None is falsy to break the while loop when the list has no more expenses in it before reaching 5
                for expense in reversed(all_expenses_list):
                    if loop_counter == 3:
                        break
                    formatted_number = "{:.2f}".format(expense[1])
                    print(f"---> {expense[0]}: £{formatted_number}")
                    loop_counter += 1
                break

    home = input("\nWhen you're ready to return home, type 'home' here and hit enter:\n")
    while True:
        if home.lower() == 'home':
            main()
        else:
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter:\n")


def every_expense_report():
    print("\nFrom which budget would you like to see all of the expenses?")
    budget_choice = input("Please type the corresponding letter and hit enter:\n")
    letters = string.ascii_uppercase
    all_worksheets = get_data("all_worksheets")

    while True:
        if budget_choice.lower() == 'home':
            main()
        if budget_choice == '':
            print("Blank values not accepted.")
            every_expense_report()
        if budget_choice.upper() not in letters:
            print("\nThis is not a letter. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        index_of_choice = letters.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            budget_choice = input("Please type the corresponding letter and hit enter:\n")
            continue
        else:
            break

    all_worksheets = get_data("all_worksheets")
    worksheet = all_worksheets[index_of_choice]
    value_range = get_data('get_info', worksheet, 'A1:B3')
    budget_name = value_range[0][0]
    running_total = value_range[1][1]
    amount_budgeted = value_range[2][1]
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount Budgeted: £{amount_budgeted}")

    all_rows = get_data('get_records', worksheet)
    all_expenses = all_rows[2:]
    all_expenses_list = [list(dictionary.values()) for dictionary in all_expenses]

    if not all_expenses:
        print("\nNo expenses logged yet.")
    else:
        print("\nAll Expenses:\n")
        number = 1
        while True:
            # use the fact that None is falsy to break the while loop when the list has no more expenses in it before reaching 5
            if not all_expenses_list:
                break
            for expense in all_expenses_list:
                formatted_number = "{:.2f}".format(expense[1])
                print(f"{number}. {expense[0]}: £{formatted_number}")
                number += 1
            break
    home = input("\nWhen you're ready to return home, type 'home' here and hit enter:\n")
    while True:
        if home.lower() == 'home':
            main()
        else:
            home = input("This isn't an available option. Please type 'home' when you're ready and hit enter:\n")

# The main function where we have the layout of the program and run it from


def main():
    """
    Runs all the functions in the program
    """
    menu_choice = go_home()
    home_menu_choice(menu_choice)


main()
