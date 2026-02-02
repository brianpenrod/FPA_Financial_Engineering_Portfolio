import pandas as pd
import random
from faker import Faker
import config  # Importing our new config file

def generate_roster(num_employees=100):
    """
    Generates a synthetic roster with granularity:
    - Roles (salary bands)
    - Health Plan Selection (Family vs Single drives variance)
    """
    fake = Faker()
    
    # Salary Bands (Base only)
    salary_bands = {
        'Analyst': (75000, 95000),
        'Manager': (120000, 160000),
        'Director': (170000, 210000),
        'VP': (230000, 300000)
    }
    
    data = []
    
    for _ in range(num_employees):
        role = random.choices(
            ['Analyst', 'Manager', 'Director', 'VP'], 
            weights=[0.4, 0.3, 0.2, 0.1]
        )[0]
        
        # Select Health Plan (Weighted: 40% Family, 50% Single, 10% Waived)
        health_plan = random.choices(
            ['Family', 'Single', 'Waived'], 
            weights=[0.40, 0.50, 0.10]
        )[0]

        row = {
            'Employee_ID': fake.unique.random_number(digits=5),
            'Name': fake.name(),
            'Role': role,
            'Department': random.choice(['Sales', 'Product', 'Engineering', 'G&A']),
            'Base_Salary': random.randint(*salary_bands[role]),
            'Health_Plan_Selection': health_plan,
            'Start_Date': fake.date_between(start_date='-2y', end_date='today')
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv('data/current_roster.csv', index=False)
    print(f"✅ Generated {num_employees} employees with Health Plan granularity.")

if __name__ == "__main__":
    # Ensure a 'data' folder exists or change path
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    generate_roster()
