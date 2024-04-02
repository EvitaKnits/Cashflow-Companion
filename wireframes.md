# Wireframes

This file contains the full plans for the text that will be displayed for each user journey:

## Home

Welcome to Cashflow Companion!

Here are your current budgets: 

A -> Food: £37.50 / £400<br>
B -> Utilities: £200 / £450<br>
C -> Transport: £7.50 / £50<br>
D -> Miscellaneous: £102 / £200

What would you like to do? 

1 -> Create a new budget <br>
2 -> Update an existing budget's name or amount<br>
3 -> Delete a budget<br>
4 -> Add, edit or delete an expense<br>
5 -> Generate a spending report

(If you would like to return home at any point, type 'home' into any input field instead of the requested value)

Please type the corresponding number and hit enter: [______]

## 1. Create a new budget
OK, what is the name of your new budget?<br>
Please type the name (alphanumeric characters only) and hit enter. Name: [_____]


Great, and how much do you want to allocate to this new budget? <br>
Please type the amount (numbers only) and hit enter. Amount: [_____]

Successfully added your new ['Fun'] budget and allocated [£200]...

Returning home...

## 2. Update an existing budget's name or amount
Which budget would you like to update?

Please type the corresponding letter and hit enter: [____]

We're updating the ['Utilities'] budget.

Would you like to change the name or the amount? <br>
Please type 'N' for name or 'A' for amount: [____]

### Name

---

OK, what would you like the new name for the ['Utilities'] budget to be?<br>
Please type the name (alphanumeric characters only) and hit enter. Name: [_____]

Changing the name of your ['Utilities'] budget to ['Bills']...

Successfully changed.

Returning home...

### Amount

---

OK, how much would you like to allocate to ['Utilities'] now?<br>
Please type the amount (numbers only) and hit enter. Amount:[_____]

Allocating [£500] to your ['Utilities'] budget...

Successfully allocated.

Returning home...

## 3. Delete a budget
OK, which budget would you like to delete?

Please type the corresponding letter and hit enter: [____]

Are you sure you would like to delete your ['Transport'] budget?<br>
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
OK, in which budget would you like to add, edit or delete an expense?

A -> Food: £37.50 / £400<br>
B -> Utilities: £200 / £450<br>
C -> Transport: £7.50 / £50<br>
D -> Miscellaneous: £102 / £200

Please type the corresponding letter and hit enter: [____]

Budget:['Miscellaneous: £102 / £200']<br>
Expenses: <br>
1. Cat food: £10
2. Hot chocolate: £2
3. Gift for Anna: £80
4. Umbrella: £7.50
5. Pencil sharpener: £2.50

Would you like to add, edit or delete an expense in the ['Miscellaneous'] budget?

A -> Add an expense
B -> Edit an expense
C -> Delete an expense

Please type the corresponding letter and hit enter: [____]

### Add

---

What is the name of your new expense?<br>
Please type the name (alphanumeric characters only) and hit enter. Name: [_____]

And how much did ['Gravel'] cost?<br>
Please type the amount (numbers only) and hit enter: [_____]

Adding your new expense: ['Gravel: £50']

Successfully added.

Returning to ['Miscellaneous'] budget

### Edit

---

Which expense would you like to edit?<br>
Please type the corresponding number and hit enter: [____]

OK, are we changing the name or amount of the ['Umbrella'] expense?<br>
Please type 'N' for name or 'A' for amount: [____]

#### Name

---

What would you like the new name for the ['Umbrella'] expense to be?<br>
Please type the name (alphanumeric characters only) and hit enter. Name: [_____]

Changing the name of your ['Umbrella'] expense to ['Parasol']...

Successfully changed. 

Returning to ['Miscellaneous'] budget...

#### Amount

---

What would you like to change the price of ['Umbrella'] to?<br>
Please type the amount (numbers only) and hit enter: [_____]

Changing the price of ['Umbrella'] to ['£7.99']...

Successfully changed.

Returning to ['Miscellaneous'] budget...

### Delete

---

Which expense would you like to delete?<br>
Please type the corresponding number and hit enter: [____]

Are you sure you would like to delete your ['Pencil sharpener'] expense?<br>
Type 'Y' for yes or 'N' for no and hit enter: [____]

#### Yes

---

Your ['Pencil sharpener'] expense has been deleted. 

Returning to ['Miscellaneous'] budget...

#### No

---

No expense has been deleted.

Returning to ['Miscellaneous'] budget...

## 5. Generate a spending report
Which report would you like to run?

A -> A report of budget categories with whether your spending is under/over<br>
B -> A report showing the last three expenses from each category

Please type the corresponding letter and hit enter: [____]

### Under/over report

---

You are [35%] of the way through the month.<br>
Here is your spend for each category: 

Food - £37.50 / £400 - 9.38% spent - UNDER budget<br>
Utilities - £200 / £450 - 44.44% spent - OVER budget<br>
Transport - £7.50 / £50 - 15% spent - UNDER budget<br>
Miscellaneous - £102 / £200 - 51% spent - OVER budget

When you're ready to return home, type 'Y' and hit enter: [___]

Returning home....

### Last three expenses report

---

Here are the latest three expenses from each category.<br>
(Where there are less than three, all expenses in that category are displayed)

Food - £37.50 / £400<br>
---> Ham: £2<br>
---> Cheese: £3.50<br>
---> Fillet steaks: £32

Utilities - £200 / £450<br>
---> Gas: £50<br>
---> Electric: £150

Transport - £7.50 / £50<br>
---> Taxi: £7.50

Miscellaneous - £102 / £200<br>
---> Gift for Anna: £80
---> Umbrella: £7.50
---> Pencil sharpener: £2.50

When you're ready to return home, type 'Y' and hit enter: [___]

Returning home....

## Error Messaging

### Incorrect input: numerical
Only numbers are accepted - this is not a number.

### Incorrect input: alphanumerical
Only alphanumerical characters are accepted - this included punctuation or special characters.

### Incorrect input: not an option
This is not an available option. Please check again.