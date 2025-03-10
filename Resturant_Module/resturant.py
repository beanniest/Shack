
import pandas as pd

#class for a single menu item
class MenuItem:
    def __init__(self, name, ingredient_dict, timing_dict, sell_price):    #need to load in ingredients dictionary, timing for making, and sell price from excel!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.name = name
        #dictionary of ingredients and weights
        self.ingredients = ingredient_dict
        #times for cooking, servers, and prep respectively
        self.timing = timing_dict
        #selling price of the item
        self.sell_price = sell_price

class Menu:
    def __init__(self, excel_name):   #need to load in wages and ingredient cost from excel using pandas!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #create a list of menu items and add all items in the excel
        self.menu_items = []
        self.add_items(excel_name)
    
        #cost of wages for chefs, waiters, and prep chefs respectively from excel document
        self.wages = pd.read_excel(excel_name, sheet_name="Employees").loc[0, 'Waiter Hourly Wage $':'Prep Hourly Wage $'].to_dict()

        #cost of ingredients per gram ny reading second sheet of excel
        self.ingredient_cost={}
        resturant_info_2 = pd.read_excel(excel_name, sheet_name="Ingredients", usecols=[0,3])
        for i in range(len(resturant_info_2.Ingredient)):
            self.ingredient_cost[resturant_info_2.Ingredient[i]] = float(resturant_info_2.GramCost[i])

    #to add all menu items to menu
    def add_items(self, excel_name):
        #add all items from excel to menu
        resturant_info_1 = pd.read_excel(excel_name, sheet_name="Menu")

        #define length where ingredients stop
        ingredients_length = len(resturant_info_1.Items)-4
        total_rows = len(resturant_info_1.Items)

        #for each menu item excel column
        for menu_item in range(1,len(resturant_info_1.columns)):

            #get item name
            item_name= resturant_info_1.columns[menu_item]

            #get items ingredients dict
            item_ingredients={}
            ingredients_key_list = resturant_info_1.Items[0:ingredients_length]
            ingredients_value_list = resturant_info_1.loc[0:ingredients_length-1, resturant_info_1.columns[menu_item]]
            for i in range(ingredients_length):
                item_ingredients[ingredients_key_list[i]] = float(ingredients_value_list[i])
            
            #get the list of timings
            item_timing = {}
            timing_key_list = resturant_info_1.Items[total_rows-4:total_rows-1]
            timing_value_list = resturant_info_1.loc[total_rows-4:total_rows-2, resturant_info_1.columns[menu_item]]
            #indxing offset in the loop mecause panda object keep indexing from where they were grabbed in the list
            for i in [0,1,2]:
                item_timing[timing_key_list[i+total_rows-4]] = float(timing_value_list[i+total_rows-4])
            
            #get the selling price for the item
            item_sell_price = float(resturant_info_1.loc[total_rows-1, resturant_info_1.columns[menu_item]])

            #add the item to the list
            self.menu_items.append(MenuItem(item_name, item_ingredients, item_timing, item_sell_price))


    #to caclulate margins of each menu item
    def calculate_profit(self):
        for item in self.menu_items:
            production_cost = 0

            #caclulate cost of ingredients for menu item
            for name,weight in item.ingredients:
                production_cost = production_cost + weight* self.ingredient_cost.get(name)

            #calculate cost of making the food for menu item!!!!!!!!!!!!!!!!1
            for index in [0,1,2]:
                production_cost = production_cost + self.wages[index].value()*item.timing[index]

            #print statistics for the menu item
            print("=====" + item + "=====\n")
            print("Cost: " + production_cost + " $CAD\n")
            print("sell price: " + item.sell_price + " $CAD\n")
            print("profit: " + item.sell_price-production_cost + " $CAD\n")
        

def analyze(file_name):

    #create menu in python
    resturant_menu = Menu(file_name)

    #see the contents of the menu and its items
    print(resturant_menu.ingredient_cost)
    print(resturant_menu.wages)
    for item in resturant_menu.menu_items:
        print(item.name)
        print(item.ingredients)
        print(item.timing)
        print(item.sell_price)


    

    

   

    
    