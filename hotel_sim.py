import sys
import json
import argparse

"""A hotel booking simulator, that takes in user input and returns
the  best hotel for their needs. """
class Hotel:
   
    def __init__(self, name):
         
        """creates name attribute to store name as argument.

        Args: 
        name (str): the user's name
        
        Side Effects:
        Creates 'name' attribute.
    
        """
        # call user_prefs from init 
        # decide to call other methods from init or main
        self.name = name
    
    def user_prefs(self):
        user_data = {}
        name = input("Enter your name: ")
        budget = input("Enter the max you are willing to spend: ")
        city = input("Enter your preferred city: ")
        start_date = input("Enter the start date of your visit: ")
        end_date = input("Enter the end date of your visit: ")
        
        user_data['name'] = name
        user_data['age'] = budget
        user_data['city'] = city
        user_data['start_date'] = start_date
        user_data['end_date'] = end_date
        
    def check_location(self, preferred_location, max_distance, hotels_file):
        # i don't get why we need to open the file again here??
        with open(hotels_file, 'r') as file:
            hotels_data = [line.strip().split(',') for line in file]

        # Define the coordinates of the preferred location
        self.preferred_coords = (preferred_location['latitude'], preferred_location['longitude'])

        nearby_hotels = []
        for hotel in hotels_data:
            hotel_coords = (float(hotel[1]), float(hotel[2]))
            # Assuming latitude is in index 1, and longitude in index 2
            distance = (preferred_coords, hotel_coords).miles

            if distance <= max_distance:
                nearby_hotels.append({'name': hotel[0], 'distance': distance})

        return nearby_hotels

    def check_budget(self):
        """Jeni's method
        checks if user's budget is withing range of possible hotel options.
        
        Args:
            user_budget (float): The user's inputted budget amount
            file_dict (dict): Dictionary of all hotels and their details from an external file.
            
        Returns:
            list: A list of hotels that are within the user's specified budget.
        """
        # potential list comprehension lines 66-74
        budget_hotels = []
        
        for hotel_name, details in file_dict.items():
            hotel_price = details.get("price", 0)
            if hotel_price <= user_budget:
                if budget_hotels.append(hotel_name):
                    # idk if part of got lost or if it never got implemented
                    # but come back and fix
                    pass
        
        if budget_hotels:
            print(f"Hotels within budget: {', '.join(budget_hotels)}")
        else:
            print("No hotels within inputted budget price")
            
        return budget_hotels
        

    def check_date(self, file_dict):
        """Kassia's method. Checks if user's preferred date is within range 
        of possible hotel options.
        
        Args:
            file_dict (dict): Dictionary of all hotels and their details from
            an external file.
            
            
        Side Effects:
        Prints list with matching hotel name's and dates.
        """
        # check_time method could be a little too similar to this method
        user_date = input('Enter your preferred date:')
       
        
        chosen_date = [f"{name} {details[1]}" for name, details
                       in file_dict.items() if user_date == details[1]]
        print(chosen_date)
        
        if len(chosen_date) == 0:
             print ('No avaiable dates. Try again.') 
    
    def find_intersection(self, user_dict, file_dict):
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
        for hotel_name, hotel_details in file_dict.items():
            intersection = user_dict.intersection(hotel_details)
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
            hotel_data = json.load(file)
            hotels = []
            for hotel in hotel_data:
                hotel_dict = {
                    'name': hotel['name'],
                    'location': hotel['location'],
                    'rating': hotel['rating'],
                    'price': hotel['price'],
                }
                hotels.append(hotel_dict)
            return hotels
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
        return []
    # don't catch random exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        # why are you returning an empty list???? 
        return []

def main():
    """Finds the the hotel that matches the user preferences based on 
    the user's input using the data from the specificed file.
    """
    
    pass

if __name__ == '__main__':
    main()
