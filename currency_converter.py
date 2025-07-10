currency_rates = {
    'United States (USD)': ('USD', 1.41),
    'European Union (EUR)': ('EUR', 1.31),
    'United Kingdom (GBP)': ('GBP', 1.12),
    'Canada (CAD)': ('CAD', 1.92),
    'Australia (AUD)': ('AUD', 2.12),
    'China (CNY)': ('CNY', 10.20),
    'Japan (JPY)': ('JPY', 216.30),
    'Saudi Arabia (SAR)': ('SAR', 5.29),
    'United Arab Emirates (AED)': ('AED', 5.18),
    'Kuwait (KWD)': ('KWD', 0.43),
    'Qatar (QAR)': ('QAR', 5.13),
    'Egypt (EGP)': ('EGP', 68.70),
    'Turkey (TRY)': ('TRY', 46.90),
    'India (INR)': ('INR', 118.10),
    'Pakistan (PKR)': ('PKR', 395.20),
    'Thailand (THB)': ('THB', 51.40),
    'Switzerland (CHF)': ('CHF', 1.28),
    'Sweden (SEK)': ('SEK', 14.45),
    'Norway (NOK)': ('NOK', 14.28),
    'South Africa (ZAR)': ('ZAR', 26.80)
}


def convert_from_jod(amount, country):
    if country not in currency_rates:
        return None, None
    currency_code, rate = currency_rates[country]
    converted_amount = amount * rate
    return currency_code, converted_amount


def get_currency_options():
    return list(currency_rates.keys())



