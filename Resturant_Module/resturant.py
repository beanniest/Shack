
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#class for a single menu item
class MenuItem:
    def __init__(self, name, ingredient_dict, timing_list, sell_price):    #need to load in ingredients dictionary, timing for making, and sell price from excel
        self.name = name
        #dictionary of ingredients and weights
        self.ingredients = ingredient_dict
        #times for cooking, servers, and prep respectively
        self.timing = timing_list
        #selling price of the item
        self.sell_price = sell_price

class Menu:
    def __init__(self, excel_name):   #need to load in wages and ingredient cost from excel using pandas
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

        #average daily costs list ()
        resturant_info_4 = pd.read_excel(excel_name, sheet_name="Sales Stats", skiprows=1, usecols=[1,2,3,4,5,6,7,8])

        #get average of each day
        self.average_list = []
        for day in range(len(resturant_info_4.columns)):
            days_avg_sales = 0
            for day_of_sales in resturant_info_4.loc[:, resturant_info_4.columns[day]]:
                days_avg_sales = days_avg_sales + float(day_of_sales)
            
            days_avg_sales = days_avg_sales/len(resturant_info_4.loc[:, resturant_info_4.columns[day]])
            self.average_list.append(days_avg_sales)


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
    def calculate_menu_profit(self):
        for item in self.menu_items:
            production_cost = 0

            #caclulate cost of ingredients for menu item
            for name,weight in item.ingredients.items():
                production_cost = production_cost + weight*self.ingredient_cost.get(name)

            #calculate cost of making the food for menu item
            for index in range(3):
                production_cost = production_cost + list(item.timing.values())[index]/60 * list(self.wages.values())[index]

            #print statistics for the menu item using matplot lib
            chart_metrics = ["cost", "sell price", "profit"]
            metric_values = [production_cost, item.sell_price, item.sell_price-production_cost]
            colors=["red", "blue", "green"]

            plt.bar(chart_metrics, metric_values, color=colors)
            plt.xlabel('revenue categories')
            plt.ylabel('Monetary Value $CAD')
            plt.title(item.name + ' comprehensive cost analysis')
            plt.show()

    #to display sales trends
    def calculate_sales_trends(self):
        chart_metrics = ["Monday", "Tuesday", "Wednseday", "Thursday", "Friday", "Saturday", "Sunday", "Daily Operational Costs"]
        metric_values = self.average_list
        colors = ["red", "red", "green", "green", "green", "green", "green", "yellow"]
        plt.bar(chart_metrics, metric_values, color=colors)
        plt.xlabel('Days of the week (earned and spent)')
        plt.ylabel('Monetary Average $CAD')
        plt.title("average daily profit and expenditure")
        plt.show()

            
        
def analyze(file_name):

    #create menu in python
    resturant_menu = Menu(file_name)

    #code for testing that the menu and its items have been calculated correctly
    '''
    #see the contents of the menu and its items
    print(resturant_menu.ingredient_cost)
    print(resturant_menu.wages)
    for item in resturant_menu.menu_items:
        print(item.name)
        print(item.ingredients)
        print(item.timing)
        print(item.sell_price)
    '''

    #calculate profit for each item
    resturant_menu.calculate_menu_profit()

    #calculate weekly sales trends
    resturant_menu.calculate_sales_trends()


    

    

   

    
    