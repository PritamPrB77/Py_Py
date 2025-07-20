import pandas as pd
from datetime import datetime, timedelta
"""
# Assignment - 1

# TODO - While creating a task, ask user about the deadline

# Start date - Pick automatically from today's date
# Deadline - 7, 10, 10

# # to-DO

# 1. Task-1 | Days left  | Green-color
# 2. Task-2 | Days left  | Red-color
# 3. Task-3 | Days left  | Green-color
# 4. Task-4 | Days left  | Red-color
"""
# ✅ Step 1: Today's date
today = datetime.today().date()

# ✅ Step 2: Task list and deadlines (in days)
tasks = ['Task-1', 'Task-2', 'Task-3', 'Task-4']
deadline_days = [7, 2, 10, 3]  # You can also ask user for input via input() if needed
"""
for i in range(len(tasks)):
    days = int(input(f"Enter deadline in days for {tasks[i]}: "))
    deadline_days.append(days)
"""
# ✅ Step 3: Calculate deadline date and days left
data = []

for task, days in zip(tasks, deadline_days):
    deadline_date = today + timedelta(days=days)
    days_left = (deadline_date - today).days
    color = 'Green' if days_left >= 5 else 'Red'
    data.append([task, deadline_date, days_left, color])

# ✅ Step 4: Create DataFrame
df = pd.DataFrame(data, columns=['Task', 'Deadline', 'Days Left', 'Color'])

print(df)
