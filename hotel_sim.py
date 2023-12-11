import sys
import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""Hotel Transylvania themed hotel booking simulator. Or otherwise known as our
'Boo-king Program'. This program takes in a JSON file and CSV file to find
the best vacation spot and best vacation activities for the user based on their
preferences.
"""
class Hotel:
    """Class docstring do later
    """
   
    def __init__(self, json_data, csv_data):
        self.hotels_dict = {}

        for hotel_data in json_data["places"]:
            hotel_name = hotel_data["place_name"]
            location = hotel_data["location"]["country"]
            prices = hotel_data["prices"]
            dates = hotel_data["dates"]

            hotel_info = {
                "location": location,
                "prices": prices,
                "date": dates
            }

            self.hotels_dict[hotel_name] = hotel_info

        self.csv_data = csv_data
        self.user_data = {}
        
    
    def user_prefs(self):
        """Samira's method
        Asks the user a series of questions to gain information about user
        preferences
        
        Returns: user_data (dict): Dictionary that has all user responses.
        """
        user_data = {}
        name = input("Enter your name: ")
        guests = input("Enter the number of guests (1-3): ")
        nights_staying = input("Enter how many nights you will be staying (Integer): ")
        budget = input("Enter the max you are willing to spend for the entire trip (Integer, no dollar sign): ")
        location = input("Enter your preferred (ROM, SVK, USA, or OCEAN)): ")
        date = input("Enter the month of your visit (Capitalize first letter): ")
        
        user_data['name'] = name
        user_data['guests'] = int(guests)
        user_data["nights_staying"] = int(nights_staying)
        user_data['budget'] = int(budget)
        user_data['location'] = location
        user_data['date'] = date
        
        return user_data
        
    def check_location(self, preferred_location):
        """Checks the user inputted preferred location and builds a list of
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
                
        if location_matches:
            print(f"Hotels within location: {', '.join(location_matches)}")
        else:
            print("No hotels within the inputted location")
            
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
            price_key = f"{num_guests}_guest{'s' if num_guests > 1 else ''}"
            nightly_price = details['prices'].get(price_key)

            total_cost = nightly_price * num_nights

            if total_cost <= self.user_data['budget']:
                budget_matches.append(hotel_name)
            else:
                print("That budget is too small to book a vacation.")
                
        if budget_matches:
            print(f"Hotels within budget: {', '.join(budget_matches)}")
        else:
            print("No hotels within the inputted budget price")
        return budget_matches
        
    def spend_budget(self, user_data):
        """Kassia's method. Determines how the user can use the money they have 
        leftover after paying the nightly price and displays pie chart of possible 
        options to spend money
        
        Args:
            user_data(dict): dictionary made of all of the user inputs.
            
        Side Effects:
            Shows pie chart of recommended ways to spend leftover money.
        
        
        """
        self.user_data = user_data
        leftover_money = self.user_data['budget'] - (self.user_data['nights_staying'] * self.user_data.get('guests', 1))
        leftover_money = ["Food", "Activities", "Stay", "Shopping", "Spa"]
        percentages = {"Food": 30, "Activities": 20, "Stay": 10, "Shopping": 25, "Spa": 15}
        spending = {activity: leftover_money * (percent/100) for activity, percent in percentages.items()}
        activites = list(spending.keys())
        amounts = list(spending.values())
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
        date_matches = [hotel_name for hotel_name, details in self.hotels_dict.items() if preferred_date in details["date"]]
        
        if date_matches:
            print(f"Hotels within date: {', '.join(date_matches)}")
        else:
            print("No hotels within the inputted date")
            
        return date_matches
             
         
    
    def best_hotel_selector(self, location_matches, budget_matches, date_matches):
        """Using the three lists of matches; location_matches, budget_matches,
        and date_matches from the check_location, check_budget, and check_date
        methods respectively, create one list combining all hotel names. Then 
        using a lambda expression, find the most common occuring hotel name from
        the list and set it as the best_hotel

        Args:
            location_matches (list): _description_
            budget_matches (list): _description_
            date_matches (list): _description_
        """
        all_matches = location_matches + budget_matches + date_matches
        best_hotel = max(set(all_matches), key=all_matches.count)
        return best_hotel 

def read_file(filename):
    """Sathya's function
    Load hotel data from a JSON file and return a list of hotel objects or dictionaries.

    Parameters:
    filename (str): The path to the JSON file containing hotel data.

    Returns:
    list: A list of hotel objects or dictionaries with the hotel data.
    """
    try:
        with open(filename, 'r') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main(json_filepath, csv_filepath):
    """Finds the the hotel that matches the user preferences based on 
    the user's input using the data from the specificed file.
    """
    json_data = read_file(json_filepath)
    csv_data = pd.read_csv(csv_filepath)
    
    my_trip = Hotel(json_data, csv_data)
    user_data = my_trip.user_prefs()

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expect one mandatory argument:
        - filepath: a path to a file with list of hotel objects 
        or dictionaries.
       

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
    main()
