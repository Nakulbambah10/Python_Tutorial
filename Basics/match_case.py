'''
Checking City Location
'''

usa = ["atlanta", "new york", "chicago", "baltimore"]
uk = ["london", "bristol", "cambridge"]
india = ["mumbai", "delhi", "bangalore"]

city = input("Enter city name: ").lower()

match city:
    case city if city in usa:
        print(f"{city} is in USA")
    case city if city in uk:
        print(f"{city} is in UK")
    case city if city in india:
        print(f"{city} is in India")
    case _:
        print(f"I won't be able to tell you which country {city} is in! Sorry!")


'''
Comparing Two Cities
'''
usa = ["atlanta", "new york", "chicago", "baltimore"]
uk = ["london", "bristol", "cambridge"]
india = ["mumbai", "delhi", "bangalore"]

city1 = input("Enter city 1: ").lower()
city2 = input("Enter city 2: ").lower()

match (city1, city2):
    case (city1, city2) if city1 in usa and city2 in usa:
        print("Both cities are in USA")
    case (city1, city2) if city1 in uk and city2 in uk:
        print("Both cities are in UK")
    case (city1, city2) if city1 in india and city2 in india:
        print("Both cities are in India")
    case _:
        print("They don't belong to the same country")

'''
Identifying Cuisine
'''

indian = ["samosa", "kachori", "dal", "naan"]
chinese = ["egg roll", "fried rice", "pot sticker"]
italian = ["pizza", "pasta", "risotto"]

dish = input("Enter a dish name: ").lower()

match dish:
    case dish if dish in indian:
        print(f"{dish} is an Indian cuisine")
    case dish if dish in chinese:
        print(f"{dish} is a Chinese cuisine")
    case dish if dish in italian:
        print(f"{dish} is an Italian cuisine")
    case _:
        print(f"Based on whatever little knowledge I've, I can't tell which cuisine {dish} is")
