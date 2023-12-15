import sys
import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

"""Hotel Transylvania themed hotel booking simulator. Or otherwise known as our
'Boo-king Program'. This program takes in a JSON file and CSV file to find
the best vacation spot and best vacation activities for the user based on their
preferences.
"""
class Hotel:
    """
    A class to represent a hotel booking simulator, particularly themed around 
    the concept of 'Hotel Transylvania', known as the 'Boo-king Program'.

    This class is designed to interact with hotel data stored in a JSON file,
    CSV file of acitivities, and user preferences to assist in finding the 
    best vacation spot based on user-specified criteria such as location, 
    budget, dates, activities, or a combination of location, budget, and date.

    Attributes:
        hotel_data (dict): A dictionary containing the hotel data loaded from a JSON file.
        hotels_dict (dict): A dictionary where each key is a hotel name and the value 
                            is another dictionary containing the hotel's location, 
                            pricing, and available dates.
        user_data (dict): A dictionary containing user preferences such as the number of 
                          guests, nights staying, budget, preferred location, and date.
        csv_filepath (str): The file path to a CSV file containing activities associated 
                            with different hotels.

    Methods:
        __init__(json_filepath, csv_filepath): Initializes the Hotel class with hotel data 
                                               from the specified JSON and CSV file paths.
        __getitem__(hotel_name): Allows access to specific hotel details using the hotel's 
                                 name as a key.
        check_location(preferred_location): Filters and returns a list of hotels based on 
                                            the user's preferred location.
        check_budget(): Filters and returns a list of hotels within the user's budget based 
                        on the number of guests and nights.
        check_date(preferred_date): Filters and returns a list of hotels available in the 
                                    user's preferred date.
        spend_budget(): Data visualization showing how much the user should spend on vacation.
        best_hotel_selector(location_matches, budget_matches, date_matches): Determines 
                                                                            the best hotel 
                                                                            match based on 
                                                                            the intersection 
                                                                            of location, 
                                                                            budget, and date 
                                                                            preferences.
        check_activity(): Asks the user what activity they like and filters the activities.csv 
                        file according to that acitivity to return a list of hotels that
                        have that specified activity.
        """
   
    def __init__(self, json_filepath, csv_filepath):
        self.hotel_data = read_file_and_store_in_dict(json_filepath)
        self.hotels_dict = {}
        for hotel_element in self.hotel_data["places"]:
            hotel_name = hotel_element["place_name"]
            location = hotel_element["location"]["country"]
            prices = hotel_element["prices"]
            dates = hotel_element["dates"]
            amenities = hotel_element["amenities"]
            rating = hotel_element["rating"]

            hotel_info = {
                "location": location,
                "prices": prices,
                "date": dates,
                "amenities": amenities,
                "rating": rating
                
            }

            self.hotels_dict[hotel_name] = hotel_info
            
        self.user_data = user_prefs()
        self.csv_filepath = csv_filepath
    
    def __getitem__(self, hotel_name):
        """Samira's method
        Allows access to hotel details using the hotel's name.

        Args:
            hotel_name (str): The name of the hotel whose details are to be accessed.

        Returns:
            hotels_dict: A dictionary containing details of the specified hotel, such as location, 
                prices, available dates, amenities, rating.

        Raises:
            KeyError: If the specified hotel name is not found in the hotel data.
        """
        try:
            print(f"Details for {hotel_name}: {self.hotels_dict[hotel_name]}") 
        except KeyError:
            print(f"Hotel '{hotel_name}' not found.")
            raise

    def check_location(self, preferred_location):
        """Samira's method
        Checks the user inputted preferred location and builds a list of
        hotels that are located in that preferred location.

        Args:
            preferred_location (str): Name of preferred country/location
            "ROM", "SVK", "USA", or "OCEAN".

        Returns:
            location_matches (list): Lists of hotels that match the user's 
            preferred country/location preference
        """
        location_matches = []
        for hotel_name, details in self.hotels_dict.items():
            if details["location"] == preferred_location:
                location_matches.append(hotel_name)
                        
        print(f"Hotels within location: {', '.join(location_matches)}")if location_matches else print("No hotels within the inputted location")
        return location_matches

    def check_budget(self):
        """Jeni's method
        Uses data from user_prefs to check how much it costs for inputted number 
        of guests for however many inputted nights. Finds hotels that match 
        inputted budget.

        Returns:
            budget_matches (list): List of all hotels that match the inputted
            budget
        """
        budget_matches = []
        for hotel_name, details in self.hotels_dict.items():
            num_guests = self.user_data['guests']
            num_nights = self.user_data['nights_staying']
            # f string
            price_key = f"{num_guests}_guest{'s' if num_guests > 1 else ''}"
            nightly_price = details['prices'].get(price_key)

            total_cost = nightly_price * num_nights
            self.total_cost = total_cost
            
            if total_cost <= self.user_data['budget']:
                budget_matches.append(hotel_name)
                
        if budget_matches:
            # f string
            print(f"Hotels within budget: {', '.join(budget_matches)}")
        else:
            print("No hotels within the inputted budget price")
        return budget_matches
 
    def spend_budget(self, user_data):
        """Kassia's method. 
        Determines how the user can use the money they have 
        leftover after paying the nightly price and displays pie chart of possible 
        options to spend money
        
        Args:
            user_data(dict): dictionary made of all of the user inputs.
            
        Side Effects:
            Shows pie chart of recommended ways to spend leftover money.    
        """
        self.user_data = user_data
        leftover_money = self.user_data['budget'] - self.total_cost
        #leftover_money = ["Food", "Activities", "Stay", "Shopping", "Spa"]
        percentages = {"Food": 30, "Activities": 20, "Stay": 10, "Shopping": 25, "Spa": 15}
        spending = {activity: leftover_money * (percent/100) for activity, percent in percentages.items()}
        activites = list(spending.keys())
        amounts = list(spending.values())
        # plt data visualization
        plt.pie(amounts, labels = activites, autopct= '%1.1f%%')
        plt.title('Recommended for leftover money')
        plt.show()

    def check_date(self, preferred_date):
        """Kassia's method
        Check's user inputted preferred month of stay and builds a list of
        hotels that are available to stay at during that month.

        Args:
            preferred_date (str): Name of month that user prefers.
            
        Returns:
            date_matches (list): Lists of hotels that match the user's 
            preferred date preference.
        """
        # list comprehension
        date_matches = [hotel_name for hotel_name, details in self.hotels_dict.items() if preferred_date in details["date"]]
        
        if date_matches:
            print(f"Hotels within date: {', '.join(date_matches)}")
        else:
            print("No hotels within the inputted date")
            
        return date_matches
    
    def first_hotel_selector(self, match_list):
        """ Samira's method
        When there is only one list we are checking for; either location, date, 
        or budget. Just grabs the first item in the list as the best hotel.

        Args:
            match_list (list): List of all possible hotel matches
        """
        best_hotel = match_list[0]
        print(f"The best vacation spot for you is {best_hotel}")
        return best_hotel
    
    def best_hotel_selector(self, location_matches, budget_matches, date_matches):
        """Samira's method
        Using the three lists of matches; location_matches, budget_matches,
        and date_matches from the check_location, check_budget, and check_date
        methods respectively, create one list combining all hotel names. Then 
        using a lambda expression, find the most common occuring hotel name from
        the list and set it as the best_hotel

        Args:
            location_matches (list): Lists of hotels that match the user's 
            preferred country/location preference
            budget_matches (list): List of all hotels that match the inputted
            budget
            date_matches (list): Lists of hotels that match the user's 
            preferred date preference.
        """
        all_matches = location_matches + budget_matches + date_matches
        # key function
        best_hotel = max(set(all_matches), key=all_matches.count)
        print(f"The best vacation spot for you is {best_hotel}")
        return best_hotel 
    
    def check_activity(self):
        """Jeni's Method
        Asks the user what activity they like and filters the activities.csv 
        file according to that acitivity to return a list of hotels that
        have that specified activity.

        Returns:
            hotel_names_list: List of hotels that have the specified activity.
        """
        activity_options = ["Archery", "Dolphin Riding", "Ballroom Dancing", "Potion Mixing", "Swimming"]

        print("Choose from the following activities: ")
        for index, activity in enumerate(activity_options, start=1):
            print(f"{index}. {activity}")

        selected_activity_index = sanitize_user_input("integer", input("Enter the number that corresponds with your chosen activity choice: "))
        if selected_activity_index is not None and 1 <= selected_activity_index <= len(activity_options):
            selected_activity = activity_options[selected_activity_index - 1]

        df = pd.read_csv(self.csv_filepath)
        # boolean filtering
        filtered_df = df[df[selected_activity] == 1]
        hotel_names_list = list(filtered_df['Unnamed: 0'])
        print(f"Hotels with selected activity: {hotel_names_list}")
        return hotel_names_list
    
        
def user_prefs():
    """Samira's method
    Asks the user a series of questions to gain information about user
    preferences
    
    Returns: 
        user_data (dict): Dictionary that has all user responses.
    """
    user_data = {}
    name = sanitize_user_input("default", input("Enter your name: "))
    guests = sanitize_user_input("integer", input("Enter the number of guests (1-3): "))
    nights_staying = sanitize_user_input("integer", input("Enter how many nights you will be staying (Integer): "))
    budget = sanitize_user_input("integer", input("Enter the max you are willing to spend for the entire trip (Integer, no dollar sign): "))
    location = sanitize_user_input("location", input("Enter your preferred location (ROM, SVK, USA, or OCEAN): "))
    date = sanitize_user_input("date", input("Enter the month of your visit: "))

    user_data['name'] = name
    user_data['guests'] = guests if guests is not None else 0
    user_data["nights_staying"] = nights_staying if nights_staying is not None else 0
    user_data['budget'] = budget if budget is not None else 0
    user_data['location'] = location
    user_data['date'] = date

    return user_data
        
def sanitize_user_input(input_type, user_input):
    """ Sathya's method
    Helper method to sanitize and validate user input based on the input type.
    It handles different types of inputs such as integer, location, and date.

    Parameters:
    input_type (str): The type of user input to be sanitized. Accepted values are 
                      'integer', 'location', and 'date'.
    user_input (str): The user input string that needs to be sanitized.

    Returns:
    int or str: Sanitized input which is either an integer for 'integer' input type, 
                or a string for 'location' and 'date' input types. If the input is 
                invalid for 'integer' type, it returns None.

    Raises:
    ValueError: If the 'integer' input type is provided and the sanitized input cannot 
                be converted to an integer.
    
    """
    if input_type == "integer":
        # Strip non-numeric characters and convert to integer
        # regular expression
        sanitized_input = re.sub(r'[^\d]', '', user_input)
        try:
            return int(sanitized_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

    elif input_type == "location":
        # Uppercase the input and strip non-alphabetic characters
        return re.sub(r'[^a-zA-Z]', '', user_input).upper()

    elif input_type == "date":
        # Capitalize the input and strip non-alphabetic characters
        return re.sub(r'[^a-zA-Z]', '', user_input).capitalize()

    else:
        # Default case for other inputs like name
        return user_input.strip() 

def read_file_and_store_in_dict(filepath):
    """Sathya's function
    Load hotel data from a JSON file and return a list of hotel objects or dictionaries.

    Parameters:
    filepath (str): The path to the JSON file containing hotel data.

    Returns:
    list: A list of hotel objects or dictionaries with the hotel data.
    """
    try:
        with open(filepath, 'r') as file:
            # json.load()
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print(f"The file {filepath} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filepath}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def in_range(actual_cost, user_budget):
    if (actual_cost < user_budget or actual_cost == user_budget):
        return True
    return False

def main(json_filepath, csv_filepath):
    """Finds the the hotel that matches the user preferences based on 
    the user's input using the data from the specificed file.
    
    Args:
        json_filepath (str): path to json file.
        csv_filepath (str): path to csv file.
    
    Side effects:
        Writes to stdout.
    """
    print('Welcome to the Hotel BOO-king Simulator, find out what vacation is the best for you!')
    print('------------------------------------------------------------------------------------')
    
    my_trip = Hotel(json_filepath, csv_filepath)
    choice = input("""
                   Choose which way to filter the best fitting hotels:
          1.) Filter by Location
          2.) Filter by Budget
          3.) Filter by Date
          4.) Filter by Activity
          5.) Get our perspective on the best hotel for you!
          
          Pick one: 
          """)
    
    if (choice == str(1)):
        location_matches = my_trip.check_location(my_trip.user_data['location'])
        best_hotel = my_trip.first_hotel_selector(location_matches)
        my_trip.__getitem__(best_hotel)
        
    elif (choice == str(2)):
        budget_matches = my_trip.check_budget()
        best_hotel = my_trip.first_hotel_selector(budget_matches)
        my_trip.__getitem__(best_hotel)
        
    elif (choice == str(3)):
        date_matches = my_trip.check_date(my_trip.user_data['date'])
        best_hotel = my_trip.first_hotel_selector(date_matches)
        my_trip.__getitem__(best_hotel)
        
    elif (choice == str(4)):
        activity_matches = my_trip.check_activity()
        best_hotel = my_trip.first_hotel_selector(activity_matches)
        my_trip.__getitem__(best_hotel)
        
    else:
        location_matches = my_trip.check_location(my_trip.user_data['location'])
        budget_matches = my_trip.check_budget()
        date_matches = my_trip.check_date(my_trip.user_data['date'])
        best_hotel = my_trip.best_hotel_selector(location_matches, budget_matches, date_matches)
        my_trip.__getitem__(best_hotel)

def parse_args(arglist):
    """Parse command-line arguments and provide help messages
       
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("json_filepath", help="JSON file with hotel data")
    parser.add_argument("csv_filepath", help="CSV file with hotel activities")
    return parser.parse_args(arglist)
  
if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main(args.json_filepath, args.csv_filepath)
