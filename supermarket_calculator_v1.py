#helper_1 - float rules for user input
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
        exchange_rate = get_exchange_rate()

    return exchange_rate
#helper_4 - pause function
def pause():
    input('\nPress Enter to continue...')
#helper_5 - screen clear untill I learn a better one
def clear_screen():
    print('\n' * 50)


VERSION = '1.0'           
exchange_rate = None #state
GRAMS_PER_POUND = 453.592
POUNDS_PER_KG = 2.20462
HUNDRED_GRAMS_PER_POUND = 4.53592

#exchange rate
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

#1 discount function 
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
    
    print('Item is', rounded_discount,'% d1iscounted')
    print('Money saved:', money_saved_cad, 'CAD$ |', round(money_saved_eur, 2), '€')
    
    
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
# 2 price per pound
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
    pause()
    

#3 100g to lbkg
def price_100g_converter():
    
    priceper100g = positive_float('What is the price in CAD$ of 100g or menu:' )
    if priceper100g is None:
        return

    exchanged_price = priceper100g * exchange_rate
    
    price_100g_to_pound_cad = priceper100g * HUNDRED_GRAMS_PER_POUND 
    price_100g_to_pound_eur = price_100g_to_pound_cad * exchange_rate
    
    price_100g_to_kg_cad = priceper100g * 10
    price_100g_to_kg_eur = price_100g_to_kg_cad * exchange_rate
        
    print_currency('Price per 100g is:', priceper100g, exchanged_price)
    print_currency('Price per pound is:', price_100g_to_pound_cad, price_100g_to_pound_eur)
    print_currency('Price per kg is:', price_100g_to_kg_cad, price_100g_to_kg_eur)
    pause()
    
#4 this one calculates the package price from cad/lb to the grams of the product
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
    pause()
#5 compare products
def product_comparison():
    print('\nProduct A')
    weight_a = positive_float('Weight in g or menu:' )
    if weight_a is None:
        return
    price_a = positive_float('Price in CAD$ or menu: ')
    if price_a is None:
        return

    print('\nProduct B')
    weight_b = positive_float('Weight in g or menu:' )
    if weight_b is None:
        return
    price_b = positive_float('Price in CAD$ or menu: ')
    if price_b is None:
        return

    price_100g_a = price_a / weight_a * 100
    price_100g_b = price_b / weight_b * 100

    print('\n Results')
    print_currency('Product A (100g)', price_100g_a, price_100g_a * exchange_rate)
    print_currency('Product B (100g)', price_100g_b, price_100g_b * exchange_rate)

    if price_100g_a > price_100g_b:
        print('Product B is the better deal')
    elif price_100g_a < price_100g_b:
        print('Product A is the better deal')
    else:
        print('Value is equal. Both good deals')
    pause()
#menu function
def show_menu():
    print(f'\n====Shopping Calculator v{VERSION}====')
    if exchange_rate is None:
        print('\n==== Current rate: Not set ====')
    else:
        print(f'\n==== Current rate: 1 CAD$ = {exchange_rate} € ====')
    print('1 - Discount Calculator')
    print('2 - Package price -> lb/kg/100g')
    print('3 - Price per 100g to lb and kg converter')
    print('4 - CAD/lb + grams -> package price')
    print('5 - Comparison tool')
    print('6 - Show current exchange rate')
    print('7 - Change exchange rate')
    print('8 - Exit')
    return input('Choose an option: ' )

#loop for menu
while True:
    clear_screen()
    choice = show_menu()

    if choice == '1':
        if ensure_exchange_rate() is None:
            continue
        discount_calculator()
   
            
    elif choice == '2':
         if ensure_exchange_rate() is None:
                continue
         packagepricepound()


    elif choice == '3':
        if ensure_exchange_rate() is None:
            continue
        price_100g_converter()
        
            
    elif choice == '4':
        if ensure_exchange_rate() is None:
            continue
        price_lb_to_g()
        
            
    elif choice == '5':
        if ensure_exchange_rate() is None:
            continue
        product_comparison()
        
            
    elif choice == '6':
        if exchange_rate is None:
            print('No exchange rate defined yet')
        else:
            print('Current exchange rate: ', exchange_rate)
                
    elif choice == '7':
            exchange_rate = get_exchange_rate()
                
    elif choice == '8':
        print('Goodbye!')
        break
    else:
        print('Invalid option')
        
        
        

















































