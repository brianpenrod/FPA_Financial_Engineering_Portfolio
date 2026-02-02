import pandas as pd
import numpy as np
import config # Pulling assumptions from the control panel

def calculate_taxes_and_benefits(row):
    """
    Row-wise logic to calculate Fully Loaded Cost.
    Includes:
    1. OASDI Cap logic
    2. Additional Medicare Tax (>200k)
    3. Dynamic Health Benefit lookup
    """
    base = row['Base_Salary']
    
    # 1. BONUS CALC
    # Safe .get() handles roles not in config
    bonus_pct = config.BONUS_TARGETS.get(row['Role'], 0.10) 
    bonus_amt = base * bonus_pct
    
    gross_comp = base + bonus_amt

    # 2. FICA - SOCIAL SECURITY (OASDI)
    # Tax applies only up to the Wage Base
    taxable_oasdi = min(gross_comp, config.OASDI_WAGE_BASE)
    oasdi_tax = taxable_oasdi * config.OASDI_RATE

    # 3. FICA - MEDICARE
    # Standard Rate
    medicare_std = gross_comp * config.MEDICARE_RATE
    # Additional Medicare Tax (High Earner Surtax)
    medicare_add = max(0, (gross_comp - config.ADDITIONAL_MEDICARE_THRESHOLD) * config.ADDITIONAL_MEDICARE_RATE)
    
    total_medicare = medicare_std + medicare_add

    # 4. FUTA (Federal Unemployment)
    futa_tax = config.FUTA_WAGE_BASE * config.FUTA_RATE

    # 5. BENEFITS BURDEN
    # Lookup cost based on plan selection
    health_cost = config.HEALTH_PLAN_COSTS.get(row['Health_Plan_Selection'], 0)
    
    # TOTAL FULLY LOADED COST
    fully_loaded = gross_comp + oasdi_tax + total_medicare + futa_tax + health_cost
    
    return pd.Series([bonus_amt, oasdi_tax, total_medicare, futa_tax, health_cost, fully_loaded])

def main():
    # Load Data
    try:
        df = pd.read_csv('data/current_roster.csv')
    except FileNotFoundError:
        print("❌ Error: Roster not found. Run generate_roster.py first.")
        return

    # Apply Logic
    cols = ['Bonus_Amt', 'Tax_OASDI', 'Tax_Medicare', 'Tax_FUTA', 'Benefits_Cost', 'Fully_Loaded_Cost']
    df[cols] = df.apply(calculate_taxes_and_benefits, axis=1)

    # --- REPORTING ---
    # Calculate Burden Rate (Loaded / Base)
    avg_burden = df['Fully_Loaded_Cost'].sum() / df['Base_Salary'].sum()
    
    print("\n--- 📊 HEADCOUNT COST ANALYSIS ---")
    print(f"Total Base Salary:      ${df['Base_Salary'].sum():,.0f}")
    print(f"Total Benefits Spend:   ${df['Benefits_Cost'].sum():,.0f}")
    print(f"Total Fully Loaded:     ${df['Fully_Loaded_Cost'].sum():,.0f}")
    print(f"Blended Burden Rate:    {avg_burden:.2f}x")
    
    # Export for Power BI
    df.to_csv('data/roster_with_costs.csv', index=False)
    print("\n✅ Calculation Complete. Exported to data/roster_with_costs.csv")

if __name__ == "__main__":
    main()
