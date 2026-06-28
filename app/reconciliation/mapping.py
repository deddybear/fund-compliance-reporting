"""
Mapping between internal figure names and the answer key metric names.
"""

FIGURE_MAPPING = {
    "singapore_government_securities":
        "Singapore Government Securities",

    "mas_bills":
        "MAS Bills",

    "investment_grade_corporate_bonds":
        "Investment Grade Corporate Bonds",

    "high_yield_bonds":
        "High Yield Bonds",

    "foreign_currency_bonds":
        "Foreign Currency Bonds (hedged)",

    "structured_credit":
        "Structured Credit (ABS/MBS)",

    "cash_and_cash_equivalents":
        "Cash & Cash Equivalents",

    "Aggregate Non-IG Exposure":
        "Aggregate non-IG exposure",

    "Single Issuer Concentration":
        "Largest single corporate issuer",

    "GRE Concentration":
        "Largest GRE issuer",

    "Liquidity Ratio":
        "Liquid assets ratio",

    "Portfolio Modified Duration":
        "Portfolio modified duration",

    "Portfolio DV01":
        "Portfolio DV01",
}

INTERNAL_TO_DISPLAY: dict[str, str] = {
    # Allocation
    "singapore_government_securities": "Singapore Government Securities",
    "mas_bills": "MAS Bills",
    "investment_grade_corporate_bonds": "Investment Grade Corporate Bonds",
    "high_yield_bonds": "High Yield Bonds",
    "foreign_currency_bonds": "Foreign Currency Bonds (hedged)",
    "structured_credit": "Structured Credit (ABS/MBS)",
    "cash_and_cash_equivalents": "Cash & Cash Equivalents",

    # Aggregate
    "Aggregate Non-IG Exposure": "Aggregate non-IG exposure",

    # Concentration
    "Single Issuer Concentration": "Largest single corporate issuer",
    "GRE Concentration": "Largest GRE issuer",

    # Liquidity
    "Liquidity Ratio": "Liquid assets ratio",

    # Market Risk
    "Portfolio Modified Duration": "Portfolio modified duration",
    "Portfolio DV01": "Portfolio DV01",
}

DISPLAY_TO_INTERNAL = {
    value: key
    for key, value in INTERNAL_TO_DISPLAY.items()
}

def to_display_name(name: str) -> str:
    return INTERNAL_TO_DISPLAY.get(
        name,
        name,
    )