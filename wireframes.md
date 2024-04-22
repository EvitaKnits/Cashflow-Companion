# Wireframes

This file contains the full output that is displayed for each user journey. Please note that this was designed with the input being at the end of the line, rather than on a new one but due to deployment requirements set by Code Institute / Heroku, this had to be changed to a new line. 

## Home

Welcome to Cashflow Companion!

Here are your current budgets: 

A-> Food: £37.50 / £400<br>
B-> Utilities: £200 / £450<br>
C-> Transport: £7.50 / £50<br>
D-> Miscellaneous: £102 / £200

What would you like to do? 

1-> Create a new budget <br>
2-> Edit a budget<br>
3-> Delete a budget<br>
4-> Add, edit or delete an expense<br>
5-> Generate a spending report

(To return home at any time, type 'home' into any input field)

Please type the relevant number and hit enter: [______]

## 1. Create a new budget
OK, what is the name of your new budget?<br>
Please type the name and hit enter: [_____]

Great, and how much do you want to allocate to this budget?<br>
Please type the amount and hit enter: [_____]

Successfully added your new ['Fun'] budget and allocated [£200].

Returning home...

## 2. Edit a budget
Which budget would you like to update?<br>
Please type the relevant letter and hit enter: [____]

We're updating the ['Utilities'] budget.

Would you like to change the name or the amount?<br>
Please type 'N' for name or 'A' for amount: [____]

### Name

---

OK, what would you like the new name for the ['Utilities'] budget to be?<br>
Please type the name and hit enter: [_____]

Changing the name of your ['Utilities'] budget to ['Bills']...

Successfully changed.

Returning home...

### Amount

---

OK, how much would you like to allocate to ['Utilities'] now?<br>
Please type the amount and hit enter:[_____]

Allocating [£500] to your ['Utilities'] budget...

Successfully changed.

Returning home...

## 3. Delete a budget
OK, which budget would you like to delete?<br>
Please type the relevant letter and hit enter: [____]

Are you sure you want to delete your ['Transport'] budget?<br>
Type 'Y' for yes or 'N' for no and hit enter: [____]

### Yes

---

Your ['Transport'] budget has been deleted. 

Returning home...

### No

---

No budget has been deleted.

Returning home...

## 4. Add, edit or delete an expense

### Menu -on first visit: 
OK, in which budget would you like to add, edit or delete an expense?<br>
Please type the relevant letter and hit enter: [____]

Budget:['Miscellaneous']<br>
Total Spent: £[102]<br>
Amount Budgeted: £[200]

Recent Expenses:
--->Cat food : £10
--->Hot chocolate: £2
--->Gift for Anna: £80

Which action would you like to take in the ['Miscellaneous'] budget?

A -> Add an expense<br>
B -> Edit an expense<br>
C -> Delete an expense<br>

Please type the relevant letter and hit enter: [____]

### Menu - on subsequent visits in the same session: 

A-> Food: £37.50 / £400<br>
B-> Utilities: £200 / £450<br>
C-> Transport: £7.50 / £50<br>
D-> Miscellaneous: £102 / £200

OK, in which budget would you like to add, edit or delete an expense?<br>
Please type the relevant letter and hit enter: [____]

Budget:['Miscellaneous']<br>
Total Spent: £[102]<br>
Amount Budgeted: £[200]

Recent Expenses:
--->Cat food : £10
--->Hot chocolate: £2
--->Gift for Anna: £80

Which action would you like to take in the ['Miscellaneous'] budget?

A -> Add an expense<br>
B -> Edit an expense<br>
C -> Delete an expense<br>

### Add

---

What is the name of your new expense?<br>
Please type the name and hit enter: [_____]

And how much did ['Gravel'] cost?<br>
Please type the amount and hit enter: [_____]

Adding your new expense: ['Gravel: £50']...

Successfully added.

Calculating the new running total for your ['Miscellaneous'] budget...

Successfully calculated and updated. 

Returning to the budget menu...

### Edit

---
All Expenses: 

1.Gas: £50.00
2.Pens: £150.00
3.Water: £50.00

Which expense would you like to edit?<br>
Please type the relevant number and hit enter: [____]

Would you like to change the name or the amount?<br>
Please type 'N' for name or 'A' for amount: [____]

#### Name

---

OK, what would you like the new name for this expense to be?<br>
Please type the name and hit enter: [_____]

Changing the name of this expense to ['Parasol']...

Successfully changed. 

Returning to the budget menu...

#### Amount

---

OK, how much would you like this expense to be now?<br>
Please type the amount and hit enter: [_____]

Changing the amount of this expense to ['£7.99']...

Successfully changed.

Calculating the new running total for your ['Miscellaneous'] budget...

Successfully calculated and updated.

Returning to the budget menu...

### Delete

---
All Expenses: 

1.Gas: £50.00
2.Pens: £150.00
3.Water: £50.00

Which expense would you like to delete?<br>
Please type the relevant number and hit enter: [____]

Are you sure you want to delete this expense?<br>
Type 'Y' for yes or 'N' for no and hit enter: [____]

#### Yes

---

This expense has been deleted. 

Updated the running total for this budget. 

Returning to the budget menu...

#### No

---

No expense has been deleted.

Returning to the budget menu...

## 5. Generate a spending report
Which report would you like to run?

A-> A report of whether your spending is under/over in all budgets<br>
B-> A report showing the last three expenses from every budget<br>
C-> A report showing every expense in a specific budget

Please type the relevant letter and hit enter: [____]

### Under/over report

---

You are [35%] of the way through the month.

For each budget, this report compares:
- how far through the month you are
- how far through your budgeted amount you are

Then calculates an 'over'/'under'/'spot on' value.

Here are your current calculations: 

Food - £37.50 / £400 - 9.38% spent - UNDER budget<br>
Utilities - £200 / £450 - 44.44% spent - OVER budget<br>
Transport - £7.50 / £50 - 15% spent - UNDER budget<br>
Miscellaneous - £102 / £200 - 51% spent - OVER budget

When you're ready to return home, type 'home' here and hit enter: [____]

### Last three expenses report

---

Here are the latest three expenses from each budget:<br>
Where there are less than three, all expenses are displayed.

Food - £37.50 / £400<br>
--->Ham: £2<br>
--->Cheese: £3.50<br>
--->Fillet steaks: £32

Utilities - £200 / £450<br>
--->Gas: £50<br>
--->Electric: £150

Transport - £7.50 / £50<br>
--->Taxi: £7.50

Miscellaneous - £102 / £200<br>
--->Gift for Anna: £80<br>
--->Umbrella: £7.50<br>
--->Pencil sharpener: £2.50

When you're ready to return home, type 'home' here and hit enter: [____]

### All expenses in a budget report

---

From which budget would you like to see all of the expenses?<br>
Please type the relevant letter and hit enter: [____]

Budget:['Utilities']<br>
Total Spent: [£115.00]<br>
Amount Budgeted: [£200.00]

All Expenses: 

1.Cat Food: £20.00
2.Plant: £2.00

When you're ready to return home, type 'home' here and hit enter: [____]

## Error messaging 

### Incorrect inputs

- This is not a letter. Please check again.
- Only numbers are accepted - this is not a number.
- Your input must be 1-15 characters long. Please try again.
- This is not an available option. Please check again.
- Blank values not accepted.
- Negative values are not accepted. Please enter a positive number.

### Exception Handling

- System busy. Please try again in one minute.
- This budget name is already taken.
- Sorry, something went wrong. Returning you home...