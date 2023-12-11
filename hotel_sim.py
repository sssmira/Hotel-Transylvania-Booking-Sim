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
            matching_hotels (list): Lists of hotels that match the user's 
            preferred country/location preference
        """
        matching_hotels = []
        for hotel_name, details in self.hotels_dict.items():
            if details["location"] == preferred_location:
                matching_hotels.append(hotel_name)
        return matching_hotels

    def check_budget(self, preferred_budget):
        
        total_cost = self.user_data['guests'] * self.user_data['nights_staying']
        user_budget = self.user_data['budget']
    #I think you have to determine the key for the price based on number of guests
    # Like when the user puts the number of guests they have and according to the json format if a user puts 1
    # then you have to append 1_guest and so forth if there's 2 or 3 guests
    # so you can you refer to the exact pricing depending on the number of guests
    # Maybe try something like this?:
        # num_guests = user_data['guests']
        # nights_staying = user_data['nights_staying']
        # user_budget = user_data['budget']
        # budget_hotels = []
        #for hotel_name, details in self.hotels_dict.items():
        # price key based on the number of guests (e.g., 1_guest, 2_guests, etc… refer to our json “prices” parent key)
        # price_key = f"{num_guests}_guest{'s' if num_guests > 1 else ''}"
 # nightly price for the specified number of guests
        # nightly_price = details['prices'].get(price_key)
        # if nightly_price:
        # total cost for the stay
        # total_cost = nightly_price * nights_staying
        # let’s check if the total cost is within the user's budget
        # if total_cost <= user_budget:
        # budget_hotels.append(hotel_name)
        # if budget_hotels:
        # print(f"Hotels within budget: {', '.join(budget_hotels)}")
        # else:
        # print("No hotels within the inputted budget price")
        # return budget_hotels
        budget_hotels = []

        for hotel_name, details in self.hotels_dict.items():
            hotel_price = details.get("prices", {})
            if hotel_price <= user_budget and total_cost <= user_budget:
                budget_hotels.append(hotel_name)
        
        if budget_hotels:
            print(f"Hotels within budget: {', '.join(budget_hotels)}")
        else:
            print("No hotels within the inputted budget price")
            
        return budget_hotels
        
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
            matching_hotels (list): Lists of hotels that match the user's 
            preferred date preference.
        """
        matching_hotels = [hotel_name for hotel_name, details in self.hotels_dict.items() if details["date"] == preferred_date]
        return matching_hotels
             
         
    
    def find_intersection(self, user_data, hotels_dict):
        """Samira's method. Takes a dictionary made from the user's preferences
        dictionary made earlier and a dictionary from the json file. Finds
        the best hotel that matches the user's specified preferences from 
        earlier.
        
        Args:
            user_dict (dict): Dictionary of all the user's answers for each
            question asked earlier, has their preference in hotels.
            file_dict (dict): Dictionary of all hotels and their details from
            an external file.
        
        Returns:
            best_hotel (dict key): Name of the best hotel found from 
            intersection
        """
        best_hotel = None
        num_intersections = 0
        
        # convert dictionary to set
        # get container of keys in the dictionary 
        for hotel_name, hotel_details in hotels_dict.items():
            intersection = user_data.intersection(hotel_details)
            if len(intersection) > num_intersections:
                num_intersections = len(intersection)
                best_hotel = hotel_name
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
