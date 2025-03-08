
#class for a single menu item
class MenuItem:
    def __init__(self, excel_name):    #need to load in ingredients dictionary, timing for making, and sell price from excel!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #dictionary of ingredients and weights
        self.ingredients = {}
        #times for cooking, servers, and prep respectively
        self.timing = []
        #selling price of the item
        self.sell_price = 0

class Menu:
    def __init__(self, excel_name):   #need to load in wages and ingredient cost from excel using pandas!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #empty list of menu items
        self.menu_items = []
        #cost of wages for chefs, waiters, and prep chefs respectively
        self.wages = []
        #cost of ingredients per gram
        self.ingredient_cost={}

    #to add a new item to the menu
    def add_item(self,new_item):
        #add an item to the menu items
        self.menu_items.append(new_item)

    #to caclulate margins of each menu item
    def calculate_profit(self):
        for item in self.menu_items:
            production_cost = 0

            #caclulate cost of ingredients for menu item
            for name,weight in item.ingredients:
                production_cost = production_cost + weight* self.ingredient_cost.get(name)

            #calculate cost of making the food for menu item
            for index in [0,1,2]:
                production_cost = production_cost + self.wages[index]*item.timing[index]

            #print statistics for the menu item
            print("=====" + item + "=====\n")
            print("Cost: " + production_cost + " $CAD\n")
            print("sell price: " + item.sell_price + " $CAD\n")
            print("profit: " + item.sell_price-production_cost + " $CAD\n")
        

def analyze(file_name):
    the_menu = Menu(file_name)
    