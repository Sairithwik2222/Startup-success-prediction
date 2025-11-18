def get_currency_for_country(country):
    """Get currency code and symbol for a specific country"""
    
    currency_map = {
        "India": {"code": "INR", "symbol": "₹", "name": "Indian Rupee"},
        "United States": {"code": "USD", "symbol": "$", "name": "US Dollar"},
        "United Kingdom": {"code": "GBP", "symbol": "£", "name": "British Pound"},
        "Canada": {"code": "CAD", "symbol": "C$", "name": "Canadian Dollar"},
        "Australia": {"code": "AUD", "symbol": "A$", "name": "Australian Dollar"},
        "China": {"code": "CNY", "symbol": "¥", "name": "Chinese Yuan"},
        "Japan": {"code": "JPY", "symbol": "¥", "name": "Japanese Yen"},
        "Germany": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "France": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Italy": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Spain": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Netherlands": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Belgium": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Austria": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Ireland": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Portugal": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Greece": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Finland": {"code": "EUR", "symbol": "€", "name": "Euro"},
        "Brazil": {"code": "BRL", "symbol": "R$", "name": "Brazilian Real"},
        "Mexico": {"code": "MXN", "symbol": "MX$", "name": "Mexican Peso"},
        "Argentina": {"code": "ARS", "symbol": "AR$", "name": "Argentine Peso"},
        "Colombia": {"code": "COP", "symbol": "COL$", "name": "Colombian Peso"},
        "Chile": {"code": "CLP", "symbol": "CL$", "name": "Chilean Peso"},
        "Peru": {"code": "PEN", "symbol": "S/", "name": "Peruvian Sol"},
        "South Africa": {"code": "ZAR", "symbol": "R", "name": "South African Rand"},
        "Nigeria": {"code": "NGN", "symbol": "₦", "name": "Nigerian Naira"},
        "Kenya": {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
        "Egypt": {"code": "EGP", "symbol": "E£", "name": "Egyptian Pound"},
        "Singapore": {"code": "SGD", "symbol": "S$", "name": "Singapore Dollar"},
        "United Arab Emirates": {"code": "AED", "symbol": "د.إ", "name": "UAE Dirham"},
        "Saudi Arabia": {"code": "SAR", "symbol": "﷼", "name": "Saudi Riyal"},
        "Israel": {"code": "ILS", "symbol": "₪", "name": "Israeli Shekel"},
        "Turkey": {"code": "TRY", "symbol": "₺", "name": "Turkish Lira"},
        "Russia": {"code": "RUB", "symbol": "₽", "name": "Russian Ruble"},
        "Poland": {"code": "PLN", "symbol": "zł", "name": "Polish Zloty"},
        "Czech Republic": {"code": "CZK", "symbol": "Kč", "name": "Czech Koruna"},
        "Hungary": {"code": "HUF", "symbol": "Ft", "name": "Hungarian Forint"},
        "Romania": {"code": "RON", "symbol": "lei", "name": "Romanian Leu"},
        "Sweden": {"code": "SEK", "symbol": "kr", "name": "Swedish Krona"},
        "Norway": {"code": "NOK", "symbol": "kr", "name": "Norwegian Krone"},
        "Denmark": {"code": "DKK", "symbol": "kr", "name": "Danish Krone"},
        "Switzerland": {"code": "CHF", "symbol": "CHF", "name": "Swiss Franc"},
        "South Korea": {"code": "KRW", "symbol": "₩", "name": "South Korean Won"},
        "Indonesia": {"code": "IDR", "symbol": "Rp", "name": "Indonesian Rupiah"},
        "Malaysia": {"code": "MYR", "symbol": "RM", "name": "Malaysian Ringgit"},
        "Thailand": {"code": "THB", "symbol": "฿", "name": "Thai Baht"},
        "Philippines": {"code": "PHP", "symbol": "₱", "name": "Philippine Peso"},
        "Vietnam": {"code": "VND", "symbol": "₫", "name": "Vietnamese Dong"},
        "Pakistan": {"code": "PKR", "symbol": "₨", "name": "Pakistani Rupee"},
        "Bangladesh": {"code": "BDT", "symbol": "৳", "name": "Bangladeshi Taka"},
        "New Zealand": {"code": "NZD", "symbol": "NZ$", "name": "New Zealand Dollar"},
    }
    
    if country in currency_map:
        return currency_map[country]
    else:
        return {"code": "USD", "symbol": "$", "name": "US Dollar"}

def format_currency(amount, currency_info):
    """Format amount with appropriate currency symbol"""
    return f"{currency_info['symbol']}{amount:,.2f}"
