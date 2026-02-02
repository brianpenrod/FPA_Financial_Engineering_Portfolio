"""
config.py
Central repository for Payroll Tax assumptions and Benefits logic.
Separates 'Data' from 'Logic' - a key Financial Engineering principle.
"""

# --- TAX ASSUMPTIONS (2024/2025 Limits) ---
OASDI_RATE = 0.062
OASDI_WAGE_BASE = 168600  # Cap for Social Security

MEDICARE_RATE = 0.0145
ADDITIONAL_MEDICARE_RATE = 0.009
ADDITIONAL_MEDICARE_THRESHOLD = 200000

FUTA_RATE = 0.006
FUTA_WAGE_BASE = 7000  # $42 max per employee

# --- BENEFITS ASSUMPTIONS ---
# Weighted average cost per plan type
HEALTH_PLAN_COSTS = {
    'Family': 24000,
    'Single': 9500,
    'Waived': 0
}

# --- BONUS TARGETS (% of Base) ---
BONUS_TARGETS = {
    'Analyst': 0.10,
    'Manager': 0.15,
    'Director': 0.25,
    'VP': 0.40
}
