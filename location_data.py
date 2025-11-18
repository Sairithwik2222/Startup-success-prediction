import pycountry

def get_all_countries():
    """Get comprehensive list of all countries"""
    countries = []
    for country in pycountry.countries:
        countries.append(country.name)
    return sorted(countries)

def get_states_for_country(country):
    """Get states/regions for a specific country"""
    
    india_states = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Kadapa", "Tirupati"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro"],
        "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif", "Arrah"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon"],
        "Goa": ["Panaji", "Vasco da Gama", "Margao", "Mapusa", "Ponda"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Junagadh"],
        "Haryana": ["Faridabad", "Gurgaon", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal"],
        "Himachal Pradesh": ["Shimla", "Dharamshala", "Solan", "Mandi", "Kullu", "Manali"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh"],
        "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum", "Gulbarga", "Davanagere", "Bellary"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Palakkad", "Alappuzha", "Kannur"],
        "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Ratlam", "Dewas"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Kolhapur"],
        "Manipur": ["Imphal", "Thoubal", "Churachandpur", "Bishnupur"],
        "Meghalaya": ["Shillong", "Tura", "Nongstoin", "Jowai"],
        "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Pathankot"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur", "Alwar", "Bharatpur"],
        "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Tiruppur", "Vellore"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar", "Mahbubnagar"],
        "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Kailashahar"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi", "Meerut", "Prayagraj", "Bareilly"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Rishikesh"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman", "Malda"],
        "Andaman and Nicobar Islands": ["Port Blair", "Diglipur", "Mayabunder"],
        "Chandigarh": ["Chandigarh"],
        "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
        "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi"],
        "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur"],
        "Ladakh": ["Leh", "Kargil"],
        "Lakshadweep": ["Kavaratti", "Agatti", "Amini"],
        "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"]
    }
    
    usa_states = {
        "Alabama": ["Birmingham", "Montgomery", "Mobile", "Huntsville"],
        "Alaska": ["Anchorage", "Fairbanks", "Juneau"],
        "Arizona": ["Phoenix", "Tucson", "Mesa", "Chandler"],
        "Arkansas": ["Little Rock", "Fort Smith", "Fayetteville"],
        "California": ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Sacramento", "Oakland", "Fresno"],
        "Colorado": ["Denver", "Colorado Springs", "Aurora", "Boulder"],
        "Connecticut": ["Hartford", "New Haven", "Stamford", "Bridgeport"],
        "Delaware": ["Wilmington", "Dover", "Newark"],
        "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"],
        "Georgia": ["Atlanta", "Savannah", "Augusta", "Columbus"],
        "Hawaii": ["Honolulu", "Hilo", "Kailua"],
        "Idaho": ["Boise", "Meridian", "Nampa"],
        "Illinois": ["Chicago", "Aurora", "Naperville", "Rockford"],
        "Indiana": ["Indianapolis", "Fort Wayne", "Evansville"],
        "Iowa": ["Des Moines", "Cedar Rapids", "Davenport"],
        "Kansas": ["Wichita", "Overland Park", "Kansas City"],
        "Kentucky": ["Louisville", "Lexington", "Bowling Green"],
        "Louisiana": ["New Orleans", "Baton Rouge", "Shreveport"],
        "Maine": ["Portland", "Lewiston", "Bangor"],
        "Maryland": ["Baltimore", "Frederick", "Rockville"],
        "Massachusetts": ["Boston", "Worcester", "Springfield", "Cambridge"],
        "Michigan": ["Detroit", "Grand Rapids", "Warren", "Ann Arbor"],
        "Minnesota": ["Minneapolis", "Saint Paul", "Rochester"],
        "Mississippi": ["Jackson", "Gulfport", "Southaven"],
        "Missouri": ["Kansas City", "St. Louis", "Springfield"],
        "Montana": ["Billings", "Missoula", "Great Falls"],
        "Nebraska": ["Omaha", "Lincoln", "Bellevue"],
        "Nevada": ["Las Vegas", "Henderson", "Reno"],
        "New Hampshire": ["Manchester", "Nashua", "Concord"],
        "New Jersey": ["Newark", "Jersey City", "Paterson"],
        "New Mexico": ["Albuquerque", "Las Cruces", "Rio Rancho"],
        "New York": ["New York City", "Buffalo", "Rochester", "Albany"],
        "North Carolina": ["Charlotte", "Raleigh", "Greensboro", "Durham"],
        "North Dakota": ["Fargo", "Bismarck", "Grand Forks"],
        "Ohio": ["Columbus", "Cleveland", "Cincinnati", "Toledo"],
        "Oklahoma": ["Oklahoma City", "Tulsa", "Norman"],
        "Oregon": ["Portland", "Eugene", "Salem"],
        "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown"],
        "Rhode Island": ["Providence", "Warwick", "Cranston"],
        "South Carolina": ["Charleston", "Columbia", "Greenville"],
        "South Dakota": ["Sioux Falls", "Rapid City", "Aberdeen"],
        "Tennessee": ["Nashville", "Memphis", "Knoxville", "Chattanooga"],
        "Texas": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
        "Utah": ["Salt Lake City", "Provo", "West Valley City"],
        "Vermont": ["Burlington", "South Burlington", "Rutland"],
        "Virginia": ["Virginia Beach", "Norfolk", "Richmond", "Arlington"],
        "Washington": ["Seattle", "Spokane", "Tacoma", "Bellevue"],
        "West Virginia": ["Charleston", "Huntington", "Morgantown"],
        "Wisconsin": ["Milwaukee", "Madison", "Green Bay"],
        "Wyoming": ["Cheyenne", "Casper", "Laramie"]
    }
    
    uk_regions = {
        "England": ["London", "Manchester", "Birmingham", "Leeds", "Liverpool", "Bristol", "Newcastle", "Sheffield"],
        "Scotland": ["Edinburgh", "Glasgow", "Aberdeen", "Dundee"],
        "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham"],
        "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Newry"]
    }
    
    canada_provinces = {
        "Alberta": ["Calgary", "Edmonton", "Red Deer"],
        "British Columbia": ["Vancouver", "Victoria", "Surrey", "Burnaby"],
        "Manitoba": ["Winnipeg", "Brandon", "Steinbach"],
        "New Brunswick": ["Moncton", "Saint John", "Fredericton"],
        "Newfoundland and Labrador": ["St. John's", "Mount Pearl", "Corner Brook"],
        "Nova Scotia": ["Halifax", "Sydney", "Dartmouth"],
        "Ontario": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London"],
        "Prince Edward Island": ["Charlottetown", "Summerside"],
        "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau"],
        "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert"]
    }
    
    australia_states = {
        "New South Wales": ["Sydney", "Newcastle", "Wollongong"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat"],
        "Queensland": ["Brisbane", "Gold Coast", "Cairns"],
        "South Australia": ["Adelaide", "Mount Gambier"],
        "Western Australia": ["Perth", "Fremantle", "Bunbury"],
        "Tasmania": ["Hobart", "Launceston"],
        "Northern Territory": ["Darwin", "Alice Springs"],
        "Australian Capital Territory": ["Canberra"]
    }
    
    china_provinces = {
        "Beijing": ["Beijing"],
        "Shanghai": ["Shanghai"],
        "Guangdong": ["Guangzhou", "Shenzhen", "Dongguan", "Foshan"],
        "Zhejiang": ["Hangzhou", "Ningbo", "Wenzhou"],
        "Jiangsu": ["Nanjing", "Suzhou", "Wuxi"],
        "Shandong": ["Qingdao", "Jinan", "Yantai"],
        "Sichuan": ["Chengdu", "Mianyang"],
        "Hubei": ["Wuhan", "Yichang"],
        "Fujian": ["Fuzhou", "Xiamen", "Quanzhou"]
    }
    
    germany_states = {
        "Bavaria": ["Munich", "Nuremberg", "Augsburg"],
        "Berlin": ["Berlin"],
        "Baden-Württemberg": ["Stuttgart", "Karlsruhe", "Mannheim"],
        "North Rhine-Westphalia": ["Cologne", "Düsseldorf", "Dortmund", "Essen"],
        "Hesse": ["Frankfurt", "Wiesbaden", "Kassel"],
        "Hamburg": ["Hamburg"],
        "Saxony": ["Dresden", "Leipzig"]
    }
    
    france_regions = {
        "Île-de-France": ["Paris", "Versailles", "Boulogne-Billancourt"],
        "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon"],
        "Auvergne-Rhône-Alpes": ["Lyon", "Grenoble", "Saint-Étienne"],
        "Nouvelle-Aquitaine": ["Bordeaux", "Limoges", "Poitiers"],
        "Occitanie": ["Toulouse", "Montpellier", "Nîmes"],
        "Hauts-de-France": ["Lille", "Amiens", "Roubaix"],
        "Brittany": ["Rennes", "Brest", "Quimper"],
        "Grand Est": ["Strasbourg", "Reims", "Metz"]
    }
    
    country_states_map = {
        "India": india_states,
        "United States": usa_states,
        "United Kingdom": uk_regions,
        "Canada": canada_provinces,
        "Australia": australia_states,
        "China": china_provinces,
        "Germany": germany_states,
        "France": france_regions,
        "Brazil": {
            "São Paulo": ["São Paulo", "Campinas", "Santos"],
            "Rio de Janeiro": ["Rio de Janeiro", "Niterói"],
            "Minas Gerais": ["Belo Horizonte", "Uberlândia"],
            "Bahia": ["Salvador", "Feira de Santana"]
        },
        "Japan": {
            "Tokyo": ["Tokyo"],
            "Osaka": ["Osaka", "Sakai"],
            "Kanagawa": ["Yokohama", "Kawasaki"],
            "Aichi": ["Nagoya", "Toyota"]
        },
        "Mexico": {
            "Mexico City": ["Mexico City"],
            "Jalisco": ["Guadalajara", "Zapopan"],
            "Nuevo León": ["Monterrey", "San Pedro Garza García"]
        },
        "South Africa": {
            "Gauteng": ["Johannesburg", "Pretoria", "Soweto"],
            "Western Cape": ["Cape Town", "Stellenbosch"],
            "KwaZulu-Natal": ["Durban", "Pietermaritzburg"]
        },
        "Italy": {
            "Lazio": ["Rome"],
            "Lombardy": ["Milan", "Bergamo"],
            "Campania": ["Naples", "Salerno"]
        },
        "Spain": {
            "Madrid": ["Madrid"],
            "Catalonia": ["Barcelona", "Tarragona"],
            "Andalusia": ["Seville", "Málaga"]
        },
        "Singapore": {
            "Singapore": ["Central Region", "North Region", "East Region", "West Region"]
        },
        "United Arab Emirates": {
            "Dubai": ["Dubai"],
            "Abu Dhabi": ["Abu Dhabi"],
            "Sharjah": ["Sharjah"]
        },
        "Netherlands": {
            "North Holland": ["Amsterdam", "Haarlem"],
            "South Holland": ["Rotterdam", "The Hague"]
        },
        "Sweden": {
            "Stockholm": ["Stockholm"],
            "Västra Götaland": ["Gothenburg"]
        },
        "Switzerland": {
            "Zurich": ["Zurich"],
            "Geneva": ["Geneva"],
            "Bern": ["Bern"]
        },
        "Belgium": {
            "Brussels": ["Brussels"],
            "Flemish Region": ["Antwerp", "Ghent"],
            "Wallonia": ["Charleroi", "Liège"]
        },
        "Poland": {
            "Masovian": ["Warsaw"],
            "Lesser Poland": ["Kraków"],
            "Greater Poland": ["Poznań"]
        },
        "Turkey": {
            "Istanbul": ["Istanbul"],
            "Ankara": ["Ankara"],
            "Izmir": ["Izmir"]
        },
        "Russia": {
            "Moscow": ["Moscow"],
            "Saint Petersburg": ["Saint Petersburg"],
            "Novosibirsk Oblast": ["Novosibirsk"]
        },
        "South Korea": {
            "Seoul": ["Seoul"],
            "Busan": ["Busan"],
            "Incheon": ["Incheon"]
        },
        "Indonesia": {
            "Jakarta": ["Jakarta"],
            "West Java": ["Bandung", "Bekasi"],
            "East Java": ["Surabaya"]
        },
        "Malaysia": {
            "Kuala Lumpur": ["Kuala Lumpur"],
            "Selangor": ["Petaling Jaya", "Shah Alam"],
            "Penang": ["George Town"]
        },
        "Thailand": {
            "Bangkok": ["Bangkok"],
            "Chiang Mai": ["Chiang Mai"],
            "Phuket": ["Phuket"]
        },
        "Philippines": {
            "Metro Manila": ["Manila", "Quezon City", "Makati"],
            "Cebu": ["Cebu City"],
            "Davao": ["Davao City"]
        },
        "Vietnam": {
            "Hanoi": ["Hanoi"],
            "Ho Chi Minh City": ["Ho Chi Minh City"],
            "Da Nang": ["Da Nang"]
        },
        "Pakistan": {
            "Punjab": ["Lahore", "Faisalabad", "Rawalpindi"],
            "Sindh": ["Karachi", "Hyderabad"],
            "Khyber Pakhtunkhwa": ["Peshawar"]
        },
        "Bangladesh": {
            "Dhaka": ["Dhaka"],
            "Chittagong": ["Chittagong"],
            "Khulna": ["Khulna"]
        },
        "Nigeria": {
            "Lagos": ["Lagos", "Ikeja"],
            "Kano": ["Kano"],
            "Rivers": ["Port Harcourt"]
        },
        "Kenya": {
            "Nairobi": ["Nairobi"],
            "Mombasa": ["Mombasa"],
            "Kisumu": ["Kisumu"]
        },
        "Egypt": {
            "Cairo": ["Cairo"],
            "Alexandria": ["Alexandria"],
            "Giza": ["Giza"]
        },
        "Argentina": {
            "Buenos Aires": ["Buenos Aires"],
            "Córdoba": ["Córdoba"],
            "Santa Fe": ["Rosario"]
        },
        "Colombia": {
            "Bogotá": ["Bogotá"],
            "Antioquia": ["Medellín"],
            "Valle del Cauca": ["Cali"]
        },
        "Chile": {
            "Santiago Metropolitan": ["Santiago"],
            "Valparaíso": ["Valparaíso", "Viña del Mar"]
        },
        "Peru": {
            "Lima": ["Lima"],
            "Arequipa": ["Arequipa"],
            "La Libertad": ["Trujillo"]
        },
        "New Zealand": {
            "Auckland": ["Auckland"],
            "Wellington": ["Wellington"],
            "Canterbury": ["Christchurch"]
        },
        "Israel": {
            "Tel Aviv": ["Tel Aviv"],
            "Jerusalem": ["Jerusalem"],
            "Haifa": ["Haifa"]
        },
        "Saudi Arabia": {
            "Riyadh": ["Riyadh"],
            "Makkah": ["Jeddah", "Mecca"],
            "Eastern": ["Dammam"]
        },
        "Ireland": {
            "Leinster": ["Dublin"],
            "Munster": ["Cork"],
            "Connacht": ["Galway"]
        },
        "Norway": {
            "Oslo": ["Oslo"],
            "Vestland": ["Bergen"],
            "Trøndelag": ["Trondheim"]
        },
        "Denmark": {
            "Capital Region": ["Copenhagen"],
            "Central Denmark": ["Aarhus"]
        },
        "Finland": {
            "Uusimaa": ["Helsinki"],
            "Pirkanmaa": ["Tampere"]
        },
        "Austria": {
            "Vienna": ["Vienna"],
            "Tyrol": ["Innsbruck"],
            "Styria": ["Graz"]
        },
        "Greece": {
            "Attica": ["Athens"],
            "Central Macedonia": ["Thessaloniki"]
        },
        "Portugal": {
            "Lisbon": ["Lisbon"],
            "Porto": ["Porto"]
        },
        "Czech Republic": {
            "Prague": ["Prague"],
            "South Moravian": ["Brno"]
        },
        "Romania": {
            "Bucharest": ["Bucharest"],
            "Cluj": ["Cluj-Napoca"]
        },
        "Hungary": {
            "Budapest": ["Budapest"],
            "Borsod-Abaúj-Zemplén": ["Miskolc"]
        }
    }
    
    if country in country_states_map:
        return country_states_map[country]
    else:
        return {
            "Northern Region": ["Major City North", "City A", "City B"],
            "Southern Region": ["Major City South", "City C", "City D"],
            "Eastern Region": ["Major City East", "City E", "City F"],
            "Western Region": ["Major City West", "City G", "City H"],
            "Central Region": ["Capital City", "City I", "City J"]
        }

def get_cities_for_state(country, state):
    """Get cities for a specific state/region"""
    states = get_states_for_country(country)
    if state in states:
        return states[state]
    return ["City 1", "City 2", "City 3"]

def get_localities_for_city(city):
    """Get localities/areas for a specific city"""
    locality_templates = [
        f"{city} Central",
        f"{city} North",
        f"{city} South",
        f"{city} East",
        f"{city} West",
        f"{city} Downtown",
        f"{city} Suburbs",
        f"{city} Industrial Area",
        f"{city} Tech Park",
        f"{city} Commercial District"
    ]
    return locality_templates
