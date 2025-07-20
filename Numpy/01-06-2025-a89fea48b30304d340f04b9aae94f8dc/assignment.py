# https://api.nobelprize.org/v1/prize.json


import json
import numpy as np


with open("prize.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# print(data)
print(type(data))
print(type(data["prizes"]))

years = [prize["year"] for prize in data["prizes"]]

# print(years)

years_array = np.array(years)

unique_years, counts = np.unique(years_array, return_counts=True)

print("\n" + "-" * 32)
print(f"{'Year':<10} | {'Prizes Count':<15}")
for year, count in zip(unique_years, counts):
    print(f"{year:<10} | {count:<15}")
print("-" * 32)
unique_years = np.array(unique_years, dtype='str')
# total_count=np.array(counts,dtype=int)
# print(unique_years)
print(unique_years)
print("\n" + "-" * 32)
print(f"{' Total Year Present':<10} | {np.sum(counts):<15}")
print(f"{' Total Prize Awarded':<10} | {np.sum(counts):<15}")
print("-" * 32)


for year in unique_years:
    prize_count = np.sum(years_array == year)
    laureates_count = sum(len(prize["laureates"]) for prize in data["prizes"] if prize["year"] == year)
    categories = set(prize["category"] for prize in data["prizes"] if prize["year"] == year)
    
    print(f"Year: {year}")
    print(f"Total prizes awarded: {prize_count}")
    print(f"Total laureates honoured: {laureates_count}")
    print(f"Total unique categories: {len(categories)}")
    print("-" * 32)


# fix the logic of prize count per year
#  Total years present : 
#  Total prizes awarded : 
#  Total Laurates Honoured : 
#  Total unique categories : 

