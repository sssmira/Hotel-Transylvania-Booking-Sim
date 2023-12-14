from hotel_sim import *
h = Hotel("hotels.json", "activities.csv")
h.total_cost = 0
h.spend_budget(h.user_data)
