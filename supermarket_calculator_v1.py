#===================Imports and directories===================
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCHANGE_RATE_FILE = os.path.join(BASE_DIR, "exchange_rate.txt")
HISTORY_FILE = os.path.join(BASE_DIR, "history.txt")
CSV_FILE = os.path.join(BASE_DIR, "history.csv")
import requests
from datetime import datetime

#===================Variables and constants===================
VERSION = '1.0'           
exchange_rate = None 
GRAMS_PER_POUND = 453.592
POUNDS_PER_KG = 2.20462
HUNDRED_GRAMS_PER_POUND = 4.53592
GST_QST= 1.14975

#===================Helpers===================
#helper_1 - float rules for user inpu
def positive_float(message):
    while True:
        text = input(message)

        if text.lower() == 'menu':
            return None

        try:
            value = float(text)

            if value > 0:
                return value

            elif value == 0:
                print('Value must be different from 0')

            else:
                print('Value must be higher than 0')

        except ValueError:
            print('Invalid data. Switch "," to "." ?')

#helper_2 - Print
def print_currency(label, cad, eur):
    print(label, ':', round(cad, 2), 'CAD$ |', round(eur, 2), '€')
    #print(f'{label}: {cad:.2f}, CAD$ | {eur:.2f} €') also works

#helper_3 - exchange rate
def ensure_exchange_rate():
    global exchange_rate

    if exchange_rate is None:
        print('No exchange rate found')
        print('Trying online source...')

        update_exchange_rate_online()

        if exchange_rate is None:
            print('No exchange rate available. Please set it manually.')
            pause()
            exchange_rate = get_exchange_rate()
            if exchange_rate is not None:
                save_exchange_rate()

    return exchange_rate

#helper_4 - pause function
def pause():
    input('\nPress Enter to continue...')

#helper_5 - screen clear untill I learn a better one
def clear_screen():
    print('\n' * 50)

#helper 6 - save history to a file
def save_history(entry):
    with open(HISTORY_FILE, 'a') as file:
        file.write(entry + '\n')

#helper 7 - separate sections in history
def save_separator(text):
    timestamp = get_timestamp()
    save_history("")
    save_history(timestamp)
    save_history(f"{'-' * 10} {text} {'-' * 10}")

#helper 8 - clear history
def clear_history():   
    with open(HISTORY_FILE, 'w') as file:
        pass

#helper 9 - clear exchange rate
def clear_exchange_rate():
    global exchange_rate
    exchange_rate = None
    with open(EXCHANGE_RATE_FILE, 'w') as file:
        pass
#helper 10 - GST_QST tax helper
def add_tax(price):
    return price * GST_QST

#helper 11 - save exchange rate to a file
def save_exchange_rate():
    with open(EXCHANGE_RATE_FILE, 'w') as file:
        file.write(str(exchange_rate))
        print('Exchange rate saved.')

# helper 12 - load exchange rate from a file
def load_exchange_rate():
    global exchange_rate
    try:
        with open(EXCHANGE_RATE_FILE, 'r') as file:
            exchange_rate = float(file.read())
    except (FileNotFoundError, ValueError):
        exchange_rate = None

#helper 13 - exchange rate function
def get_exchange_rate():
    while True:
        rate = input('Exchange rate (CAD$ to EUR) or menu:' )
        if rate.lower() == 'menu':
            return None
        if rate == '':
            print('Invalid exchange rate')
            continue
        try:
            exchange_rate = float(rate)
            if exchange_rate > 0:
                return exchange_rate
            else:
                 print('exchange rate must be greater than 0')
                    
        except ValueError:
                print('Invalid data. Switch "," to "." ?')

#helper 14 - get exchange rate online
def update_exchange_rate_online():
    global exchange_rate
    try: 
        response = requests.get("https://api.frankfurter.app/latest?from=CAD&to=EUR")
        data = response.json()
        exchange_rate = data['rates']['EUR']
        save_exchange_rate()
        print(f"Exchange rate downloaded: 1 CAD$ = {exchange_rate:.4f} €")
    except Exception as error:
        print(f"Could not get exchange rate from online source. Why?: {error}")

#helper 15: view history
def view_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            print('\n=== Calculation History ===')
            print(file.read())

    except FileNotFoundError:
        print('No history found.')

#helper 16: date and time
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#helper 17: save into csv
def save_csv(calculator, result):
    timestamp = get_timestamp()

    with open(CSV_FILE, 'a') as file:
        file.write(f"{timestamp};{calculator};{result}\n")
#==============================================Calculators=============================== 
#Calculator 1 - price converter
def price_converter():
    price_cad = positive_float('Price in CAD$ or menu: ')
    if price_cad is None:
        return
    price_eur = price_cad * exchange_rate
    print_currency('Price:', price_cad, price_eur)
    save_separator("Price Converter")
    save_history(f"Price converted: {price_cad} CAD$ | {price_eur:.2f} €")
    save_csv("Price Converter", f"{price_cad} CAD$ | {price_eur:.2f} €")
    pause()

#Calculator 2 - tax applier
def tax_applier():
    price_cad = positive_float('Price in CAD$ or menu: ')
    if price_cad is None:
        return
    price_with_tax_cad = add_tax(price_cad)
    price_with_tax_eur = price_with_tax_cad * exchange_rate
    tax_amount_cad = price_with_tax_cad - price_cad
    tax_amount_eur = tax_amount_cad * exchange_rate

    print_currency('Price without tax:', price_cad, price_cad * exchange_rate)
    print_currency('Tax amount:', tax_amount_cad, tax_amount_eur)
    print_currency('Price with tax:', price_with_tax_cad, price_with_tax_eur)
   
    save_separator("Tax Applier")
    save_history(f"Price without tax: {price_cad} CAD$ | {price_cad * exchange_rate:.2f} €")
    save_history(f"Tax amount: {tax_amount_cad:.2f} CAD$ | {tax_amount_eur:.2f} €")
    save_history(f"Price with tax: {price_with_tax_cad} CAD$ | {price_with_tax_eur:.2f} €")
    save_csv("Tax Applier",f"Before: {price_cad} CAD$ | Tax: {tax_amount_cad:.2f} CAD$ | After: {price_with_tax_cad:.2f} CAD$")

    pause()

#Calculator 2 - discount calculator
def discount_calculator():
    regular_price = positive_float('Regular Price (CAD$) or menu: ')
    if regular_price is None:
        return
        
    sale_price = positive_float('Sale Price(CAD$) or menu: ')
    if sale_price is None:
        return
    discount_percentage = 100 - sale_price * 100 / regular_price
    
    rounded_discount = round (discount_percentage, 2)

    money_saved_cad = regular_price - sale_price
    money_saved_eur = money_saved_cad * exchange_rate
    
    print('Item is', rounded_discount,'% discounted')
    print('Money saved:', money_saved_cad, 'CAD$ |', round(money_saved_eur, 2), '€')
    save_separator("Discount Calculator")
    save_history(f"Item is {rounded_discount}% discounted | Money saved: {money_saved_cad} CAD$ | {money_saved_eur: .2f} €")
    save_csv("Discount Calculator", f"Regular price: {regular_price} CAD$ | Sale price: {sale_price} CAD$ | Discount: {rounded_discount}% | Money saved: {money_saved_cad} CAD$ | {money_saved_eur: .2f} €")
    if rounded_discount > 100: 
        print('Free or error?')
        pause()
    elif rounded_discount < 0:
        print('Negative discount - Losing money or error?')
        pause()
    elif rounded_discount == 0:
        print ('0? They lied to you')
        pause()
    else:
        print('Enjoy your discount!')
        pause()

#Calculator 3 - package price calculator
def packagepricepound():
    while True:
        unit = input('Weight unit (lb or g):').lower()
        if unit == 'menu':
            return
        if unit in ('lb', 'g'):
            break
        
        print('Wrong unit, use lb or g')
        
    if unit == 'lb':
        weight_lb = positive_float('Weight in lb:')
        if weight_lb is None:
            return  
    
    elif unit == 'g':
        weight_g = positive_float('Weight in g:')
        if weight_g is None:
            return
        weight_lb = weight_g / GRAMS_PER_POUND
        

    package_price_cad = positive_float('Price in CAD$:')

    if package_price_cad is None:
        return 
    
            
    price_per_lb_cad = package_price_cad / weight_lb
    price_per_lb_eur = price_per_lb_cad * exchange_rate

    price_per_kg_cad = price_per_lb_cad * POUNDS_PER_KG
    price_per_kg_eur = price_per_kg_cad * exchange_rate
   
    price_per_100g_cad = price_per_kg_cad / 10
    price_per_100g_eur = price_per_kg_eur / 10
    

    print_currency('Price per 100g is:', price_per_100g_cad, price_per_100g_eur)
    print_currency('Price per lb is:', price_per_lb_cad, price_per_lb_eur)
    print_currency('Price per kg is:', price_per_kg_cad, price_per_kg_eur)

    save_separator("Package Price")

    save_history(f"Price per 100g is: {price_per_100g_cad: .2f} CAD$ | {price_per_100g_eur:.2f} €")
    save_history(f"Price per lb is: {price_per_lb_cad: .2f} CAD$ | {price_per_lb_eur:.2f} €")
    save_history(f"Price per kg is: {price_per_kg_cad: .2f} CAD$ | {price_per_kg_eur:.2f} €")
    save_csv("Package Price",f"Input: {package_price_cad:.2f} CAD$ for {weight_lb:.2f} lb | "f"100g: {price_per_100g_cad:.2f} CAD$ ({price_per_100g_eur:.2f} €) | " f"lb: {price_per_lb_cad:.2f} CAD$ ({price_per_lb_eur:.2f} €) | " f"kg: {price_per_kg_cad:.2f} CAD$ ({price_per_kg_eur:.2f} €)")
    pause()
    

#Calculator: 4 100g to lb/kg
def price_100g_converter():
    
    priceper100g = positive_float('What is the price in CAD$ of 100g or menu:' )
    if priceper100g is None:
        return

    exchanged_price = priceper100g * exchange_rate
    
    price_100g_to_pound_cad = priceper100g * HUNDRED_GRAMS_PER_POUND 
    price_100g_to_pound_eur = price_100g_to_pound_cad * exchange_rate
    
    price_100g_to_kg_cad = priceper100g * 10
    price_100g_to_kg_eur = price_100g_to_kg_cad * exchange_rate

    save_separator('Price per 100g') 

    print_currency('Price per 100g is:', priceper100g, exchanged_price)
    print_currency('Price per pound is:', price_100g_to_pound_cad, price_100g_to_pound_eur)
    print_currency('Price per kg is:', price_100g_to_kg_cad, price_100g_to_kg_eur)
    save_history(f"Price per 100g is: {priceper100g} CAD$ | {exchanged_price:.2f} €")
    save_history(f"Price per pound is: {price_100g_to_pound_cad} CAD$ | {price_100g_to_pound_eur:.2f} €")
    save_history(f"Price per kg is: {price_100g_to_kg_cad} CAD$ | {price_100g_to_kg_eur:.2f} €")
    save_csv("Price per 100g", f"Price per 100g: {priceper100g: .2f} CAD$ | {exchanged_price:.2f} € | Price per pound: {price_100g_to_pound_cad: .2f} CAD$ | {price_100g_to_pound_eur:.2f} € | Price per kg: {price_100g_to_kg_cad} CAD$ | {price_100g_to_kg_eur:.2f} €")
    pause()
    
#Calculator 5: this one calculates the package price from cad/lb to the grams of the product
def price_lb_to_g():

    weight_g = positive_float('What is the weight, in grams, of the item? or menu: ')
    if weight_g is None:
        return

    weight_lb = weight_g /GRAMS_PER_POUND 

    price_per_lb_cad = positive_float('What is the price/lb of the item? or menu: ')

    if price_per_lb_cad is None:
        return

    package_price_cad = weight_lb * price_per_lb_cad
    package_price_eur = package_price_cad * exchange_rate

    print_currency('The price of the item is:', package_price_cad, package_price_eur)
    save_separator("Price lb to g")
    save_history(f"Input: {weight_g:.0f} g at {price_per_lb_cad:.2f} CAD$/lb | " f"The price of the item is: {package_price_cad:.2f} CAD$ | {package_price_eur:.2f} €")
    save_csv("Package Price",f"Input: {weight_g:.0f} g at {price_per_lb_cad:.2f} CAD$/lb | " f" The price of the item is: {package_price_cad:.2f} CAD$ | {package_price_eur:.2f} €")
    pause()

#Calculator 6: compare products
def product_comparison():
    print('\nProduct A')
    name_a = input('Name of product A (or menu): ')
    if name_a.lower() == 'menu':
        return
    if name_a.strip() == '':
        print('Please enter a product name')
        return  
    weight_a = positive_float('Weight in g or menu:' )
    if weight_a is None:
        return
    price_a = positive_float('Price in CAD$ or menu: ')
    if price_a is None:
        return

    print('\nProduct B')
    name_b = input('Name of product B (or menu): ')
    if name_b.lower() == 'menu':
        return
    if name_b.strip() == '':
        print('Please enter a product name')
        return  
    weight_b = positive_float('Weight in g or menu:' )
    if weight_b is None:
        return
    price_b = positive_float('Price in CAD$ or menu: ')
    if price_b is None:
        return
    
    price_100g_a = price_a / weight_a * 100
    price_100g_b = price_b / weight_b * 100
    difference_cad = abs(price_100g_a - price_100g_b)
    difference_eur = difference_cad * exchange_rate
    percentage_difference = abs(price_100g_a - price_100g_b) / max(price_100g_a, price_100g_b) * 100

    print('\n Results')
    print_currency(f" {name_a} (100g)", price_100g_a, price_100g_a * exchange_rate)
    print_currency(f" {name_b} (100g)", price_100g_b, price_100g_b * exchange_rate)
    print(f"Difference: {difference_cad:.2f} CAD$ | {difference_eur:.2f} € | {percentage_difference:.2f}%")
    save_separator(f"Comparison between {name_a} and {name_b}")

    save_history(f"{name_a} (100g): {price_100g_a} CAD$ | {price_100g_a * exchange_rate:.2f} €")
    save_history(f"{name_b} (100g): {price_100g_b} CAD$ | {price_100g_b * exchange_rate:.2f} €")
    save_history(f"Difference: {difference_cad:.2f} CAD$ | {difference_eur:.2f} € | {percentage_difference:.2f}%")
    save_csv("Product Comparison", f"{name_a} (100g): {price_100g_a} CAD$ | {price_100g_a * exchange_rate:.2f} € | {name_b} (100g): {price_100g_b} CAD$ | {price_100g_b * exchange_rate:.2f} € | Difference: {difference_cad:.2f} CAD$ | {difference_eur:.2f} € | {percentage_difference:.2f}%")

    if price_100g_a > price_100g_b:
        winner = name_b
        print(f" {name_b} is the better deal")
        save_history(f"{name_b} is the better deal")
    elif price_100g_a < price_100g_b:
        winner = name_a
        print(f" {name_a} is the better deal")
        save_history(f"{name_a} is the better deal")
    else:
        winner = "Tie"
        print('Value is equal. Both good deals')
        save_history('Value is equal. Both good deals')

    save_csv("Product Comparison", f"{name_a} (100g): {price_100g_a:.2f} CAD$ | {price_100g_a * exchange_rate:.2f} € | " f"{name_b} (100g): {price_100g_b:.2f} CAD$ | {price_100g_b * exchange_rate:.2f} € | " f"Difference: {difference_cad:.2f} CAD$ | {difference_eur:.2f} € | "f"{percentage_difference:.2f}% | Winner: {winner}")
    pause()
#================Menu and settings================
#Menu function
def show_menu():
    print(f'\n====Shopping Calculator v{VERSION}====')
    if exchange_rate is None:
        print('\n==== Current rate: Not set ====')
    else:
        print(f'\n==== Current rate: 1 CAD$ = {exchange_rate:.4f} € ====')
    print('1 - Price Converter (CAD$ to EUR)')
    print('2 - Tax Applier (GST/QST)')
    print('3 - Discount Calculator')
    print('4 - Package price -> lb/kg/100g')
    print('5 - Price per 100g to lb and kg converter')
    print('6 - CAD/lb to grams -> package price')
    print('7 - Comparison tool')
    print('8 - Settings')
    print('9 - Exit')
    while True:
        choice = input('Choose an option: ')
        if choice in map(str, range(1, 10)):
            return choice
        print('Invalid option, choose a number between 1 and 9')


def settings_menu():
    print('\n====Settings====')
    print('1 - Show current exchange rate')
    print('2 - Update exchange rate')
    print('3 - View history')
    print('4 - Clear history')
    print('5 - Clear exchange rate')
    return input('Choose an option or any key to go back: ')

#===============Load exchange rate at the start of the program===============
load_exchange_rate() 

#loop for menu
while True:
    clear_screen()
    choice = show_menu()

    if choice == '1':
        if ensure_exchange_rate() is None:
            continue
        price_converter()
    
    if choice == '2':
        if ensure_exchange_rate() is None:
            continue
        tax_applier()
      
    elif choice == '3':
         if ensure_exchange_rate() is None:
                continue
         discount_calculator()


    elif choice == '4':
        if ensure_exchange_rate() is None:
            continue
        packagepricepound()
        
            
    elif choice == '5':
        if ensure_exchange_rate() is None:
            continue
        price_100g_converter()
        
            
    elif choice == '6':
        if ensure_exchange_rate() is None:
            continue
        price_lb_to_g()

    elif choice == '7':
        if ensure_exchange_rate() is None:
            continue
        product_comparison()    

    elif choice == '8':
        settings_choice = settings_menu()
        if settings_choice == '1':
            if exchange_rate is None:
                print('No exchange rate defined yet')
            else:
                print('Current exchange rate: ', exchange_rate)
            pause()  
        elif settings_choice == '2':
             update_exchange_rate_online()
             pause()
        elif settings_choice == '3':
            view_history()
            pause()
        elif settings_choice == '4':
            clear_history()
            print('History cleared.')
            pause()
        elif settings_choice == '5':
            clear_exchange_rate()
            print('Exchange rate cleared.')
            pause()
        

    elif choice == '9':
        print('Goodbye!')
        break
    else:
        print('Invalid option')
        











































