import gspread
from google.oauth2.service_account import Credentials
import string
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("cashflow_companion")
LETTERS = string.ascii_uppercase

# Validation and exception functions:


def length_check(user_input):
    """ Enforces 1-15 character limit on text inputs, stripping whitespace for
    budget and expense names.
    """
    if len(user_input) <= 15 and len(user_input) >= 1:
        return user_input.strip()
    else:
        print("Your input must be 1-15 characters long. Please try again.")
        return False


def access_data(api_call, *args):
    """ Retrieves or updates necessary program data via API calls, handling 429
    exceptions for exceeding API quotas by exiting the program. Also catches
    other exceptions and restarts the program. The number of arguments varies
    depending on the API call type.
    """
    try:
        if api_call == "all_worksheets":
            return (SHEET.worksheets())
        elif api_call == "one_cell":
            worksheet, cell_address = args
            return worksheet.acell(cell_address)
        elif api_call == "get_records":
            worksheet = args[0]
            return worksheet.get_all_records()
        elif api_call == "get_info":
            worksheet, range = args
            return worksheet.get(range)
        elif api_call == "get_values":
            worksheet = args[0]
            return worksheet.get_all_values()
        elif api_call == "get_rows":
            worksheet, row_index = args
            return worksheet.row_values(row_index)
        elif api_call == "cell_update":
            worksheet, row, column, value = args
            worksheet.update_cell(row, column, value)
        elif api_call == "new_worksheet":
            budget_name, budget_amount = args
            SHEET.add_worksheet(title=f"{budget_name}", rows=100, cols=20)
            current_budget_worksheet = access_data("all_worksheets")[-1]
            current_budget_worksheet.format("B:B", {"numberFormat":
                                            {"type": "NUMBER", "pattern":
                                                "#####0.00"}})
            current_budget_worksheet.update([[budget_name, "", ],
                                            ["Running Total", 0, ],
                                            ["Amount Budgeted",
                                            budget_amount]])
            return
        elif api_call == "update_name":
            worksheet, new_name = args
            worksheet.update_title(new_name)
            return 
        elif api_call == "delete_budget":
            worksheet = args[0]
            SHEET.del_worksheet(worksheet)
            return
        elif api_call == "add_expense":
            worksheet, new_row = args
            worksheet.append_row(new_row)
            return
        elif api_call == "delete_expense":
            worksheet, row_index = args
            worksheet.delete_rows(row_index)
            return
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429:
            print("System busy. Please try again in one minute.")
            exit()
        elif e.response.status_code == 400:
            print("This budget name is already taken.")
            print("Returning you home...")
            main()
        else:
            print("Sorry, something went wrong. Returning you home...")
            main()
    except Exception:
        print("Sorry, something went wrong. Returning you home...")
        main()


def valid_budget_choice(budget_choice):
    """Validates user input received from the calling function and returns
    its validity status.
    """
    all_worksheets = access_data("all_worksheets")

    # Checks the validity of the budget choice and returns the result
    while True:
        if budget_choice == "":
            print("Blank values not accepted.")
            return "invalid"
        if budget_choice.upper() not in LETTERS:
            print("\nThis is not a letter. Please check again.")
            return "invalid"
        index_of_choice = LETTERS.index(budget_choice.upper())
        if index_of_choice >= len(all_worksheets):
            print("\nThis is not an available option. Please check again.")
            return "invalid"
        else:
            return "valid"


# Common action functions

def get_budget_details(worksheet):
    """ Retrieves budget details from the given worksheet. """
    value_range = access_data("get_info", worksheet, "A1:B3")
    budget_name = value_range[0][0]
    running_total = value_range[1][1]
    amount_budgeted = value_range[2][1]
    return budget_name, running_total, amount_budgeted


def get_budgets(type, index_of_choice):
    """ Collects budget names, running totals, and allocated amounts from the
    spreadsheet, then prints them in a consistent format.
    """
    # Retrieve all budgets/worksheets from the spreadsheet
    all_worksheets = access_data("all_worksheets")

    # Retrieves a specific budget/worksheet
    if type == "one":
        worksheet = all_worksheets[index_of_choice]
        budget_name, running_total,\
            amount_budgeted = get_budget_details(worksheet)
        return worksheet, budget_name, running_total, amount_budgeted
    elif type == "all":
        if all_worksheets is None:
            print("You've not added any budgets yet.")
            print("Select option 1 from the main menu to add some.")
        else:
            # Loops through budgets, sequentially printing details with letters
            letter = "A"
            for worksheet in all_worksheets:
                budget_name, running_total,\
                    amount_budgeted = get_budget_details(worksheet)
                print(f"{letter}-> {budget_name}: "
                      f"£{running_total} / £{amount_budgeted}")
                # Increments the letters alongside the budget names each time
                index = LETTERS.index(letter)
                letter = LETTERS[index + 1]
    elif type == "last_three_report":
        for worksheet in all_worksheets:
            budget_name, running_total,\
                amount_budgeted = get_budget_details(worksheet)
            print(f"\n{budget_name} - £{running_total} / £{amount_budgeted}")
            print_expenses(3, worksheet)
        return


def print_expenses(number, worksheet):
    """ Prints the requested number of expenses in the required direction,
    depending on the function calling this function. Takes arguments for how
    many expenses to print and from which budget.
    """
    all_expenses = access_data("get_records", worksheet)[2:]
    all_expenses_list = [list(dictionary.values())
                         for dictionary in all_expenses]

    # For no expenses
    if not all_expenses:
        print("\nNo expenses logged yet.")
        return None

    # For a specific number of expenses, printed in reverse order
    elif number > 0:
        loop_counter = 0
        while True:
            if loop_counter == number:
                break
            if not all_expenses_list:
                break
            # Loops until expenses run out or reach 5
            for expense in reversed(all_expenses_list):
                if loop_counter == number:
                    break
                print(f"--->{expense[0]} : £{'{:.2f}'.format(expense[1])}")
                loop_counter += 1
            break
        return 1
    # For all expenses
    else:
        print("\nAll Expenses:\n")
        number = 1
        while True:
            # Loops until expenses run out or reach 5
            if not all_expenses_list:
                break
            for expense in all_expenses_list:
                # Displays all expenses in a numbered list
                print(f"{number}.{expense[0]}: £{'{:.2f}'.format(expense[1])}")
                number += 1
            break
        return


# Home menu functions

def go_home():
    """ At program start, displays a welcome message, current budgets list, and
    available actions for the user.
    """
    # Prints the welcome message, current budget information and menu options
    print("\nWelcome to Cashflow Companion!\n")
    print("Here are your current budgets:\n")
    get_budgets("all", 0)
    print("\nWhat would you like to do?\n")
    print("1-> Create a new budget")
    print("2-> Edit a budget")
    print("3-> Delete a budget")
    print("4-> Add, edit or delete an expense")
    print("5-> Generate a spending report\n")

    # Informs users how they can access this menu anytime
    print("(To return home at any time, type 'home' into any input field)\n")

    # Prompts the user for their menu choice
    menu_choice = input("Please type the relevant number and hit enter:\n")
    return menu_choice


def home_menu_choice(menu_choice):
    """Receives the menu choice from the "go_home" function, then executes the
    corresponding action function. Validates the choice to ensure it
    corresponds to an available action.
    """
    if menu_choice == "1":
        create_new_budget()
    elif menu_choice == "2":
        edit_budget()
    elif menu_choice == "3":
        delete_budget()
    elif menu_choice == "4":
        expense_menu_budget_choice()
    elif menu_choice == "5":
        report_menu()
    elif menu_choice.lower() == "home":
        main()
    else:
        # If the choice is not valid, the user is prompted to choose again
        print("\nThis is not an available option. Please check again.")
        new_menu_choice = input("Please type the relevant number "
                                "and hit enter:\n")
        home_menu_choice(new_menu_choice)


# User journeys: budgets

def create_new_budget():
    """Enables users to create a new budget, allocate an amount to it, and
    updates the Google Sheet accordingly. Validates input format and returns
    to the main menu after budget creation.
    """
    # Retrieves the list of existing budgets
    number_budgets = len(access_data("all_worksheets"))

    # Limits the number of budgets to 20 maximum
    if number_budgets >= 20:
        print("\nThe maximum number of 20 budgets has already been reached.")
        print("To create a new budget, first delete an existing budget")
        print("\nReturning home...\n")
        main()

    # Prompts the user for the name of the new budget
    while True:
        print("\nOK, what is the name of your new budget?")
        budget_name = input("Please type the name and hit enter:\n")
        if budget_name.lower() == "home":
            main()
        # Ensures the name is 15 characters or fewer
        if length_check(budget_name):
            break

    # Prompts the user for the amount to allocate to the new budget
    while True:
        print("\nGreat, and how much do you want to allocate to this budget?")
        budget_amount = input("Please type the amount and hit enter:\n")
        if budget_amount.lower() == "home":
            main()
        try:
            if float(budget_amount) < 0:
                print("\nNegative values are not accepted.")
                print("Please enter a positive number.")
                continue
        except ValueError:
            print("\nOnly numbers are accepted - this is not a number.")
            continue
        
        # Calls API function to add new budget to spreadsheet
        budget_amount = format(float(budget_amount), ".2f")
        access_data("new_worksheet", budget_name, budget_amount)
       
        # Notifies the user of successful budget creation and allocation
        print(f"\nSuccessfully added your new '{budget_name}' budget and "
              f"allocated £{budget_amount}.")
        print("\nReturning home...\n")
        main()


def edit_budget():
    """ Updates an existing budget by modifying its name or allocated amount.
    Prompts for the budget to edit, the aspect to change, and the new value.
    Validates input and enforces formatting rules for the new name. Returns to
    the main menu after updating the budget.
    """
    # Prompts the user for which budget they want to update
    validity = "invalid"
    print("\nWhich budget would you like to update?")

    # Calls the valid budget choice checker until a valid option is chosen
    while validity == "invalid":
        budget_choice = input("Please type the relevant letter "
                              "and hit enter:\n")
        if budget_choice.lower() == "home":
            main()
        validity = valid_budget_choice(budget_choice)

    all_worksheets = access_data("all_worksheets")
    index_of_choice = LETTERS.index(budget_choice.upper())

    # Retrieves the worksheet corresponding to the selected budget
    worksheet = all_worksheets[index_of_choice]
    budget_name = access_data("one_cell", worksheet, "A1").value
    print(f"\nWe're updating the '{budget_name}' budget.")

    # Asks the user which aspect they want to change
    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for "
                           "amount:\n").upper()
    while name_or_amount not in ("N", "A"):
        if name_or_amount.lower() == "home":
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            name_or_amount = input("Please type 'N' for name or 'A' for "
                                   "amount:\n")

    # Changes the name to user's input as long as it follows formatting rules
    if name_or_amount.upper() == "N":
        while True:
            print(f"\nOK, what would you like the new name for the "
                  f"'{budget_name}' budget to be?")
            new_name = input("Please type the new name and hit enter:\n")
            if length_check(new_name):
                break
        if new_name.lower() == "home":
            main()
        else:
            # Calls API function to change name on worksheet
            new_name_attempt = access_data("update_name", worksheet, new_name)
            # Notifies the user that their change has been successful
            print(f"\nChanging the name of your '{budget_name}' budget "
                    f"to '{new_name}'...")
            access_data("cell_update", worksheet, 1, 1, new_name)
            print("\nSuccessfully changed.\n\nReturning home...\n")
            main()
    else:
        # Changes amount to user's input as long as it follows formatting rules
        print(f"\nOK, how much would you like to allocate to "
              f"'{budget_name}' now?")
        new_amount = input("Please type the amount and hit enter:\n")
        if new_amount.lower() == "home":
            main()
        while True:
            try:
                # Ensures a positive number is chosen for the new amount
                if float(new_amount) < 0:
                    print("\nNegative values are not accepted")
                    print("Please enter a positive number.")
                    new_amount = input("Please type the amount "
                                       "and hit enter:\n")
                    continue
            except Exception:
                if new_amount.lower() == "home":
                    main()
                else:
                    print("\nOnly numbers are accepted - this isn't a number.")
                    new_amount = input("Please type the amount "
                                       "and hit enter:\n")
            else:
                # Notifies the user that their change has been successful
                formatted_number = format(float(new_amount), ".2f")
                print(f"\nAllocating £{formatted_number} to your "
                      f"'{budget_name}' budget...\n")
                access_data("cell_update", worksheet, 3, 2, formatted_number)
                print("Successfully changed.\n\nReturning home...\n")
                main()


def delete_budget():
    """ Prompts user to select budget to delete and asks for confirmation. If
    confirmed, the budget is deleted; otherwise, a message confirms no
    deletion. Returns the user to the main menu afterward.
    """
    # Asks the user which budget they want deleted
    validity = "invalid"
    print("\nOK, which budget would you like to delete?")

    # Calls the valid budget choice checker until a valid option is chosen
    while validity == "invalid":
        budget_choice = input("Please type the relevant letter "
                              "and hit enter:\n")
        if budget_choice.lower() == "home":
            main()
        validity = valid_budget_choice(budget_choice)

    all_worksheets = access_data("all_worksheets")
    index_of_choice = LETTERS.index(budget_choice.upper())

    # Gets the selected budget name and prompts for deletion confirmation
    worksheet = all_worksheets[index_of_choice]
    budget_name = access_data("one_cell", worksheet, "A1").value
    print(f"\nAre you sure you want to delete your '{budget_name}' budget?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and "
                           "hit enter:\n").upper()
    while confirm_choice not in ("Y", "N"):
        if confirm_choice.lower() == "home":
            main()
        else:
            confirm_choice = input("Invalid input. Type 'Y' for yes or 'N' for"
                                   " no and hit enter:\n").upper()

    # Deletes budget if confirmed, or notifies if not, returns to main menu
    if confirm_choice == "Y":
        # Calls API function to delete the worksheet for this budget
        access_data("delete_budget", worksheet)
        print(f"\nYour '{budget_name}' budget has been deleted.\n")
        print("Returning home...\n")
        main()
    else:
        print("\nNo budget has been deleted.\n\nReturning home...\n")
        main()


# User journeys: expenses

def expense_menu_budget_choice():
    """ Enables the user to choose a budget for expense-related actions.
    Displays information about the selected budget and provides recent expenses
    """
    # Asks the user to select a budget
    validity = "invalid"
    print("\nOK, in which budget would you like to add, edit "
          "or delete an expense?")

    # Calls the valid budget choice checker until a valid option is chosen
    while validity == "invalid":
        budget_choice = input("Please type the relevant letter "
                              "and hit enter:\n")
        if budget_choice.lower() == "home":
            main()
        validity = valid_budget_choice(budget_choice)

    index_of_choice = LETTERS.index(budget_choice.upper())

    # Calls function to print budget info, receiving worksheet and name
    worksheet, budget_name, running_total,\
        amount_budgeted = get_budgets("one", index_of_choice)
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount"
          f"Budgeted: £{amount_budgeted}")
    print("\nRecent expenses:")

    # Retrieves recent expenses for the selected budget and prints them, if any
    expenses = print_expenses(3, worksheet)
    if not expenses:
        print("\nYou can only add a new expense.")
        new_expense(budget_name, worksheet)
    else:
        expense_menu_action_choice(budget_name, worksheet)


def expense_menu_action_choice(budget_name, worksheet):
    """ Displays the expense-related action menu, allowing users to select an
    option. Moves to the appropriate function in the program to execute the
    chosen action.
    """
    # Defines the menu options for expense actions
    menu_options = {"A": "Add an expense", "B": "Edit an expense",
                    "C": "Delete an expense"}

    # Prints the menu of available actions
    print(f"\nWould you like to add, edit, or delete an expense in the "
          f"'{budget_name}' budget?")
    for key, value in menu_options.items():
        print(f"{key} -> {value}")

    # Prompts the user to select an action and validates their input
    menu_choice = input("\nPlease type the relevant letter and "
                        "hit enter:\n").upper()
    while menu_choice not in menu_options.keys():
        if menu_choice.lower() == "home":
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            menu_choice = input("Please type the relevant letter and "
                                "hit enter:\n").upper()

    # Directs to the appropriate function for the chosen expense action
    if menu_choice == "A":
        new_expense(budget_name, worksheet)
    elif menu_choice == "B":
        edit_expense(budget_name, worksheet)
    elif menu_choice == "C":
        delete_expense(budget_name, worksheet)


def new_expense(budget_name, worksheet):
    """ Allows the user to add a new expense to their desired budget. """
    # Asks for the name of the new expense
    while True:
        print("\nWhat is the name of your new expense?")
        name = input("Please type the name and hit enter:\n")
        if length_check(name):
            break
    if name.lower() == "home":
        main()
    else:
        new_row = []
        new_row.append(name)
        # Asks for the amount of the new expense
        print(f"\nAnd how much did '{name}' cost?")
        cost = input("Please type the amount and hit enter:\n")
        if cost.lower() == "home":
            main()

    # Validates the cost input
    while True:
        try:
            if float(cost) < 0:
                print("\nNegative values are not accepted.")
                print("Please enter a positive number.")
                cost = input("Please type the amount and hit enter:\n")
                continue
        except Exception:
            print("\nOnly numbers are accepted - this is not a number.")
            cost = input("Please type the amount and hit enter:\n")
            if cost.lower() == "home":
                main()
        else:
            # Adds the new expense to the correct budget's worksheet
            new_row.append(format(float(cost), ".2f"))
            print(f"\nAdding your new expense: '{name}: "
                  f"£{'{:.2f}'.format(float(cost))}'...")
            # Calls the API function to add the new expense to the sheet
            access_data("add_expense", worksheet, new_row)
            print("\nSuccessfully added.")
            # Updates the running total for the relevant budget
            print(f"\nCalculating the new running total for your "
                  f"'{budget_name}' budget...")
            running_total = float(access_data("one_cell", worksheet,
                                              "B2").value)
            running_total += float(cost)
            access_data("cell_update", worksheet, 2, 2, running_total)
            print(f"\nSuccessfully calculated and updated.\n")
            print(f"Returning to '{budget_name}' budget.")
            break
    expense_menu_action_choice(budget_name, worksheet)


def edit_expense(budget_name, worksheet):
    """Enables the user to edit a specific expense within their chosen budget,
    then returns to that budget's expense action menu.
    """
    # Retrieves and prints all expenses from the relevant budget worksheet
    expenses = print_expenses(0, worksheet)

    # Prompts user to select an expense to edit.
    print("\nWhich expense would you like to edit?")
    select_expense = input("Please type the relevant number and hit enter:\n")
    number_rows = access_data("get_values", worksheet)

    while True:
        if select_expense.lower() == "home":
            main()
        if select_expense.isnumeric() is False:
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the relevant number "
                                   "and hit enter:\n")
            continue
        row_index = int(select_expense) + 3
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the relevant number "
                                   "and hit enter:\n")
            continue
        else:
            break

    # Prompts user to choose editing expense name or amount
    print("\nWould you like to change the name or the amount?")
    name_or_amount = input("Please type 'N' for name or 'A' for "
                           "amount:\n").upper()
    while name_or_amount not in ("N", "A"):
        if name_or_amount.lower() == "home":
            main()
        else:
            print("\nThis is not an available option. Please check again.")
            name_or_amount = input("Please type 'N' for name or "
                                   "'A' for amount:\n")

    # Asks the user for the new name
    if name_or_amount.upper() == "N":
        while True:
            print("\nOK, what would you like the new name for this "
                  "expense to be?")
            new_name = input("Please type the name and hit enter:\n")
            if length_check(new_name):
                break
        if new_name.lower() == "home":
            main()
        else:
            # Attempts update in the spreadsheet and confirms when successful
            print(f"\nChanging the name of this expense to '{new_name}...'")
            access_data("cell_update", worksheet, row_index, 1, new_name)
            print(f"\nSuccessfully changed.\n")
            print(f"Returning to '{budget_name}' budget...")
    else:
        # Asks the user for the new amount
        print(f"\nOK, how much would you like this expense to be now?")
        new_amount = input("Please type the amount and hit enter:\n")
        while True:
            try:
                if float(new_amount) < 0:
                    print("\nNegative values are not accepted.")
                    print("Please enter a positive number.")
                    new_amount = input("Please type the amount "
                                       "and hit enter:\n")
                    continue
            except Exception:
                if new_amount.lower() == "home":
                    main()
                else:
                    print("\nOnly numbers are accepted - this "
                          "is not a number.")
                    new_amount = input("Please type the amount "
                                       "and hit enter:\n")
            else:
                # Attempts spreadsheet update and confirms success
                formatted_number = "{:.2f}".format(float(new_amount))
                print(f"\nChanging the amount of this expense to "
                      f"£{formatted_number}...\n")
                old_amount_row = access_data("get_rows", worksheet, row_index)
                old_amount = old_amount_row[1]
                access_data("cell_update", worksheet, row_index,
                            2, formatted_number)
                print("Successfully changed.")
                print(f"\nCalculating the new running total for your "
                      f"'{budget_name}' budget...")
                running_total = float(access_data("one_cell", worksheet,
                                                  "B2").value)
                running_total -= float(old_amount)
                running_total += float(new_amount)
                access_data("cell_update", worksheet, 2, 2, running_total)
                print(f"\nSuccessfully calculated and updated.\n")
                print(f"Returning to '{budget_name}' budget...")
                break
    # Returns the user to the expense-related action menu
    expense_menu_action_choice(budget_name, worksheet)


def delete_expense(budget_name, worksheet):
    """ Deletes a specific expense within a chosen budget, then returns to that
    budget's expense action menu.
    """
    # Retrieves and prints all expenses from the relevant budget worksheet
    expenses = print_expenses(0, worksheet)

    # Asks the user to select an expense to delete
    print("\nWhich expense would you like to delete?")
    select_expense = input("Please type the relevant number and hit enter:\n")
    number_rows = access_data("get_values", worksheet)

    # Validates the user's choice and that it corresponds to a valid expense
    while True:
        if select_expense.lower() == "home":
            main()
        if select_expense.isnumeric() is False:
            print("\nOnly numbers are accepted - this is not a number")
            select_expense = input("Please type the relevant number "
                                   "and hit enter:\n")
            continue
        row_index = int(select_expense) + 3
        if row_index > len(number_rows):
            print("\nThis is not an available option. Please check again.")
            select_expense = input("Please type the relevant number "
                                   "and hit enter:\n")
            continue
        else:
            break

    # Prompts user to confirm deletion and deletes if yes
    print(f"\nAre you sure you want to delete this expense?")
    confirm_choice = input("Type 'Y' for yes or 'N' for no and "
                           "hit enter:\n").upper()
    while confirm_choice not in ("Y", "N"):
        if confirm_choice.lower() == "home":
            main()
        else:
            confirm_choice = input("Invalid input. Type 'Y' for yes or 'N' for"
                                   " no and hit enter:\n").upper()

    if confirm_choice.upper() == "Y":
        running_total = float(access_data("one_cell", worksheet, "B2").value)
        deleted_expense_amount = access_data("get_rows", worksheet,
                                             row_index)[1]
        running_total -= float(deleted_expense_amount)
        # Call API function to update running total before deletion
        access_data("cell_update", worksheet, 2, 2, running_total)
        # Call API function to delete expense row in sheet
        access_data("delete_expense", worksheet, row_index)
        print(f"\nThis expense has been deleted.")
        # Updates the running total for the budget after an expense deletion
        print(f"\nCalculating the new running total for your '{budget_name}' "
              f"budget...")
        print(f"\nSuccessfully calculated and updated.\n\nReturning to "
              f"'{budget_name}' budget...")
    else:
        print(f"\nNo expense has been deleted.\n\nReturning to '{budget_name}'"
              f" budget...")
    # Returns the user to the expense-related action menu
    expense_menu_action_choice(budget_name, worksheet)


# User journeys: reports

def report_menu():
    """ Option 5 from the main menu directs to this report menu function, which
    triggers the appropriate function to generate the chosen report. Validates
    the user's selection to ensure it corresponds to an available action.
    """
    # Display the options for generating the three different types of report
    print("\nWhich report would you like to run?\n")
    print("A-> A report of whether your spending is under/over in all budgets")
    print("B-> A report showing the last three expenses from every budget")
    print("C-> A report showing every expense in a specific budget")
    while True:
        # Prompts user for report choice until valid, then proceeds accordingly
        report_choice = input("\nPlease type the relevant letter and hit "
                              "enter:\n")
        if report_choice.upper() == "A":
            under_over_report()
            break
        elif report_choice.upper() == "B":
            last_three_report()
            break
        elif report_choice.upper() == "C":
            every_expense_report()
            break
        elif report_choice.lower() == "home":
            main()
        else:
            print("\nThis is not an available option. Please check again.")


def under_over_report():
    """ Generates a report comparing the current month's progress with the
    budgeted amounts for each budget. Calculates an 'over'/'under'/'spot on'
    value for each budget based on the percentage of the month elapsed and the
    percentage of the budget spent.
    """
    # Gets today's date information
    todays_date = datetime.datetime.now()
    day_only = todays_date.strftime("%d")
    which_month = todays_date.strftime("%m")

    # Calculates the percentage of the month elapsed
    if which_month == 4 or which_month == 6 or which_month == 9\
            or which_month == 11:
        month_percentage = (float(day_only) / 30) * 100
        formatted_percentage = round(month_percentage, 2)
    elif which_month == 2:
        month_percentage = (float(day_only) / 28) * 100
        formatted_percentage = round(month_percentage, 2)
    else:
        month_percentage = (float(day_only) / 31) * 100
        formatted_percentage = round(month_percentage, 2)

    # Prints introductory/explanatory information for the report
    print(f"\nYou are {formatted_percentage}% of the way through the month.")
    print("\nFor each budget, this report compares:")
    print("- how far through the month you are")
    print(" - how far through your budgeted amount you are")
    print("\nThen calculates an 'over'/'under'/'spot on' value.")
    print("\nHere are your current calculations:\n")

    # Retrieves budget information and calculates progress for each budget
    all_worksheets = access_data("all_worksheets")
    index_of_choice = 0
    for worksheet in all_worksheets:
        worksheet, budget_name, running_total,\
            amount_budgeted = get_budgets("one", index_of_choice)
        index_of_choice += 1
        percentage_spent = (float(running_total) / float(amount_budgeted))\
            * 100
        formatted_spent = round(percentage_spent, 2)

        """ Determines if the spend is over, under, or spot on by comparing the
        percentage of the month elapsed and the percentage of the budget spent.
        """
        if formatted_spent < formatted_percentage:
            over_under = "UNDER"
        elif formatted_spent == formatted_percentage:
            over_under = "SPOT ON"
        else:
            over_under = "OVER"
        # Prints each budget with its information and status.
        print(f"{budget_name} - £{running_total} / £{amount_budgeted} "
              f"- {formatted_spent}% spent - {over_under} budget")

    # Reminds the user how to return home and provides an input field to do so
    home = input("\nWhen you're ready to return home, type 'home' here "
                 "and hit enter:\n")
    while True:
        if home.lower() == "home":
            main()
        else:
            home = input("This isn't an available option. Please type 'home' "
                         "when you're ready and hit enter:\n")


def last_three_report():
    """ Generates a report displaying the latest three expenses from each
    budget, or all expenses if there are fewer than three. It also provides
    information about each budget's running total and budgeted amount.
    """
    print("\nHere are the latest three expenses from each budget:")
    print("Where there are less than three, all expenses are displayed.")
    get_budgets("last_three_report", 0)

    # Reminds the user how to return home and provides an input field to do so
    home = input("\nWhen you're ready to return home, type 'home' here "
                 "and hit enter:\n")
    while True:
        if home.lower() == "home":
            main()
        else:
            home = input("This isn't an available option. Please type 'home' "
                         "when you're ready and hit enter:\n")


def every_expense_report():
    """ Generates a report showing all expenses from a specific budget chosen
    by the user.
    """
    # Asks the user which budget they want the report to run on.
    validity = "invalid"
    print("\nFrom which budget would you like to see all of the expenses?")

    # Calls the valid budget choice checker until a valid option is chosen
    while validity == "invalid":
        budget_choice = input("Please type the relevant letter "
                              "and hit enter:\n")
        if budget_choice.lower() == "home":
            main()
        validity = valid_budget_choice(budget_choice)

    all_worksheets = access_data("all_worksheets")
    index_of_choice = LETTERS.index(budget_choice.upper())

    # Retrieves information for the chosen budget and prints it.
    worksheet, budget_name, running_total, amount_budgeted\
        = get_budgets("one", index_of_choice)
    print(f"\nBudget: {budget_name}\nTotal Spent: £{running_total}\nAmount "
          f"Budgeted: £{amount_budgeted}")

    # Retrieves and prints all expenses from the relevant budget worksheet.
    expenses = print_expenses(0, worksheet)

    # Reminds the user how to return home and provides an input field to do so
    home = input("\nWhen you're ready to return home, type 'home' here "
                 "and hit enter:\n")
    while True:
        if home.lower() == "home":
            main()
        else:
            home = input("This isn't an available option. Please type 'home' "
                         "when you're ready and hit enter:\n")

# The main function that (re)starts the program


def main():
    """ Runs the starter functions in the program """
    menu_choice = go_home()
    home_menu_choice(menu_choice)


main()
