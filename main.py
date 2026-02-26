inventory = [
    {'name': 'tomato',  'quantity': 10, 'cost_price': 10, 'selling_price': 15},
    {'name': 'brinjal', 'quantity': 20, 'cost_price': 15, 'selling_price': 20},
    {'name': 'onion',   'quantity': 30, 'cost_price': 15, 'selling_price': 10},
]

visited_customers_count = 0
purchased_customers_count = 0
sales_records = []


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print('<<<< Value must be greater than 0, try again >>>>')
                continue
            return value
        except ValueError:
            print('<<<< Invalid input, please enter a valid number >>>>')


def get_item_from_inventory(item_name):
    """Returns the inventory object if found, else None."""
    for item in inventory:
        if item['name'] == item_name:
            return item
    return None


def show_menu(options):
    """Prints a numbered menu and returns user input."""
    for option in options:
        print(option)
    return input('Choose option: ')

def is_inventory_empty():
    return len(inventory) == 0


# ─────────────────────────────────────────────
# SALES RECORDS FUNCTIONS
# ─────────────────────────────────────────────

def update_sales_records(obj, action):
    for record in sales_records:
        if record['item_name'] == obj['item_name']:
            if action == 'increase':
                record['quantity'] = record['quantity'] + obj['quantity']
            if action == 'decrease':
                record['quantity'] = record['quantity'] - obj['quantity']
            break
    else:
        sales_records.append(obj)


def delete_sales_records(obj):
    for i, record in enumerate(sales_records):
        if record['item_name'] == obj['item_name']:
            sales_records.pop(i)
            break


def display_itemized_report():
    if sales_records != []:
        print('#' * 50)
        total_net_profit = 0
        for i, obj in enumerate(sales_records, 1):
            total_sales = obj['quantity'] * obj['sp']
            total_cost = obj['quantity'] * obj['cp']
            profit = total_sales - total_cost
            if profit > 0:
                print(f'{i}.', f"{obj['item_name']:<20}", f"{obj['quantity']} Kgs", 'profit is == Rs', profit)
            elif profit < 0:
                print(f'{i}.', f"{obj['item_name']:<20}", f"{obj['quantity']} Kgs", 'loss is == ', profit)
            else:
                print(obj['item_name'], 'No profit No loss')
            total_net_profit += profit
        if total_net_profit < 0:
            print('**** End up with the total loss of ==', total_net_profit, '*' * 10)
        elif total_net_profit > 0:
            print('**** End up with the total profit of ==', total_net_profit, '*' * 10)
        else:
            print('Overall profit on total items is == No profit No loss')
        print('#' * 50)
    else:
        print('*' * 10, 'No sales records present', '*' * 10)


# ─────────────────────────────────────────────
# INVENTORY / DISPLAY FUNCTIONS
# ─────────────────────────────────────────────

def show_all_details(user='shopkeeper'):
    if is_inventory_empty():
        print('*' * 10, 'No vegetables available in the store', '*' * 10)
        return
    text = 'Cost Price(Rs)' if user == 'shopkeeper' else ''
    print(f"{'Name':<15} {'Quantity(Kgs)':<20} {'Selling Price(Rs)':<20} {text}")
    for item in inventory:
        if user == 'shopkeeper':
            print(f"{item['name']:<18} {item['quantity']:<23} {item['selling_price']:<23} {item['cost_price']}")
        elif user == 'customer':
            print(f"{item['name']:<15} {item['quantity']:<23} {item['selling_price']}")


# ─────────────────────────────────────────────
# SHOPKEEPER FUNCTIONS
# ─────────────────────────────────────────────

def add_item_to_store():
    if is_inventory_empty():
        print('*' * 10, 'No vegetables available in the store', '*' * 10)
        return
    while True:
        item_name = input('Enter item name: ')
        if get_item_from_inventory(item_name):
            print('This item is already present in the store. Add another item.')
            continue
        qty = get_positive_float('Enter quantity (in kgs): ')
        cp = get_positive_float('Enter cost price (in rupees): ')
        sp = get_positive_float('Enter selling price (in rupees): ')
        inventory.append({'name': item_name, 'quantity': qty, 'cost_price': cp, 'selling_price': sp})
        print('>>> Item added successfully. Item name is', item_name)
        ch = input('Do you want to add item again (yes/no): ')
        if ch == 'yes':
            continue
        elif ch == 'no':
            break
        else:
            print('Invalid input')
            continue


def delete_item_from_store():
    if len(inventory)==0:
        print('*'*10,'Inventory is Empty You can delete','*'*10)
        return False
    while True:
        item_name = input('Enter item name to delete: ')
        item = get_item_from_inventory(item_name)
        if item:
            confirm = input('Do you really want to remove the item? (yes/no): ')
            if confirm == 'yes':
                inventory.remove(item)
                print('>>> Item Deleted Successfully....')
                break
        else:
            print('Item you entered is not present. Enter valid item name.')


def modify_item_in_store():
    while True:
        item_name = input('Enter item name to modify: ')
        item = get_item_from_inventory(item_name)
        if item:
            while True:
                ch = show_menu(['1.Quantity', '2.Cost Price', '3.Selling Price', '4.Exit'])
                if ch == '1':
                    item['quantity'] = get_positive_float('Enter the new quantity: ')
                    break
                elif ch == '2':
                    item['cost_price'] = get_positive_float('Enter the new cost price: ')
                    break
                elif ch == '3':
                    item['selling_price'] = get_positive_float('Enter the new selling price: ')
                    break
                elif ch == '4':
                    print('Exiting the current tab')
                    break
                else:
                    print('Wrong input, enter correct input')
                    continue
        else:
            print('Item you entered is not present in the list.')
            continue
        ch = input('Do you want to modify again (yes/no): ')
        if ch == 'yes':
            continue
        elif ch == 'no':
            break
        else:
            print('<<<<<Invalid Input>>>>>')
            continue


def shopkeeper_menu():
    print('*' * 10, 'Welcome.... You entered into shopkeeper view', '*' * 10)
    while True:
        ch = show_menu(['1.Add item', '2.Delete item', '3.Modify item', '4.See list details', '5.Customer count', '6.Revenue Report(itemized)', '7.Exit'])
        if ch == '1':
            add_item_to_store()
        elif ch == '2':
            delete_item_from_store()
        elif ch == '3':
            modify_item_in_store()
        elif ch == '4':
            show_all_details('shopkeeper')
        elif ch == '5':
            print('Total Customers visited are: ', visited_customers_count)
            print('Total purchased Customers are: ',purchased_customers_count)
        elif ch == '6':
            display_itemized_report()
        elif ch == '7':
            print('Exiting the shopkeeper view')
            break
        else:
            print('<<<<<Enter valid input>>>>>')


# ─────────────────────────────────────────────
# CART FUNCTIONS
# ─────────────────────────────────────────────

def add_to_cart(cart):
    while True:
        customer_input = input('What do you want? : ')
        item = get_item_from_inventory(customer_input)
        if item:
            qty = get_positive_float('How many kgs do you want: ')
            if qty <= item['quantity']:
                item['quantity'] -= qty
                order_obj_cart = {'item_name': customer_input, 'quantity': qty, 'sp': item['selling_price']}
                order_obj_sales = {'item_name': customer_input, 'quantity': qty, 'sp': item['selling_price'], 'cp': item['cost_price']}
                for obj in cart:
                    if obj['item_name'] == customer_input:
                        obj['quantity'] += qty
                        break
                else:
                    cart.append(order_obj_cart)
                update_sales_records(order_obj_sales, 'increase')
            else:
                print('*' * 10, 'Out Of Stock', '*' * 10)
        else:
            print('<<<< The item you entered is not present, enter other vegetable. >>>>')
            continue
        ch = input('Do you want to buy more? (yes/no): ')
        if ch == 'yes':
            continue
        elif ch == 'no':
            break
        else:
            print('<<<Invalid input>>>>')
            continue


def view_cart_details(cart):
    if cart != []:
        print('#' * 20)
        print(f"{'Name':<15} {'Quantity(Kgs)':<20} {'Selling Price(Rs)':<20}")
        for obj in cart:
            print(f"{obj['item_name']:<15} {obj['quantity']:<23} {obj['sp']}")
        print('#' * 20)
    else:
        print('*' * 10, 'Your Cart is Empty, Continue shopping', '*' * 10)


def check_the_item_in_cart(cart, item_name):
    for obj in cart:
        if obj['item_name'] == item_name:
            return True
    return False


def modify_the_quantity(quant, action, item_name, cart):
    item = get_item_from_inventory(item_name)
    order_obj_sales = {'item_name': item_name, 'quantity': quant, 'sp': item['selling_price'], 'cp': item['cost_price']}
    if action == 'decrease':
        for obj in cart:
            if obj['item_name'] == item_name and obj['quantity'] > 0:
                obj['quantity'] -= quant
                item['quantity'] += quant
                break
        update_sales_records(order_obj_sales, 'decrease')
    elif action == 'increase':
        for obj in cart:
            if obj['item_name'] == item_name:
                obj['quantity'] += quant
                item['quantity'] -= quant
                break
        update_sales_records(order_obj_sales, 'increase')
    return cart


def delete_item_from_cart(cart, item_name):
    remove_obj = None
    for i, obj in enumerate(cart):
        if obj['item_name'] == item_name:
            item = get_item_from_inventory(item_name)
            item['quantity'] += obj['quantity']
            remove_obj = obj
            cart.pop(i)
            print('*' * 10, 'Item Deleted Successfully.....', '*' * 10)
            break
    if remove_obj:
        delete_sales_records(remove_obj)
    return cart


def modify_cart(cart):
    if cart != []:
        while True:
            item_name = input('Enter item name to modify: ')
            if check_the_item_in_cart(cart, item_name):
                while True:
                    ch = show_menu(['1.Increase quantity', '2.Decrease quantity', '3.Delete item', '4.Exit'])
                    if ch == '1':
                        quant = get_positive_float('Enter quantity: ')
                        item = get_item_from_inventory(item_name)
                        if quant <= item['quantity']:
                            cart = modify_the_quantity(quant, 'increase', item_name, cart)
                            break
                        else:
                            print('*' * 10, 'Out of stock', '*' * 10)
                            continue
                    elif ch == '2':
                        quant = get_positive_float('Enter quantity: ')
                        can_decrease = any(obj['item_name'] == item_name and obj['quantity'] > quant for obj in cart)
                        if can_decrease:
                            cart = modify_the_quantity(quant, 'decrease', item_name, cart)
                            break
                        else:
                            print('*' * 10, 'You dont have that much quantity to decrease', '*' * 10)
                            continue
                    elif ch == '3':
                        cart = delete_item_from_cart(cart, item_name)
                        break
                    elif ch == '4':
                        print('*' * 10, 'Exiting the current tab', '*' * 10)
                        break
                    else:
                        print('<<<<<<Invalid input>>>>>>')
                        continue
                ch = input('Do you want to modify again (yes/no): ')
                if ch == 'yes':
                    continue
                elif ch == 'no':
                    break
                else:
                    print('<<<<Invalid input>>>>')
                    continue
            else:
                print('*' * 10, 'Item not present in the cart.', '*' * 10)
                continue
    else:
        print('*' * 10, 'Your Cart is Empty, Continue shopping', '*' * 10)


def delete_cart(cart):
    for obj in cart:
        item = get_item_from_inventory(obj['item_name'])
        if item:
            item['quantity'] += obj['quantity']
        delete_sales_records(obj)
    return []


def billing(cart):
    total_bill = 0
    if cart != []:
        print('#' * 80)
        print('Your Total Bill')
        print(f"{'Name':<15} {'Quantity(Kgs)':<20} {'Selling Price(Rs)':<20} {'Each Total(Rs)'}")
        for obj in cart:
            if obj['quantity'] > 0:
                each_item_total = obj['quantity'] * obj['sp']
                total_bill += each_item_total
                print(f"{obj['item_name']:<15} {obj['quantity']:<23} {obj['sp']:<20} {each_item_total}")
        print('*' * 80)
        print('Total bill is =', total_bill)
        print('Thanks for shopping in our store.... have a great day...')
        print('*' * 80)
        print('#' * 80)
    else:
        print('*' * 10, 'You did not do the shopping, Continue the Shopping', '*' * 10)
    return total_bill


# ─────────────────────────────────────────────
# CUSTOMER MENU
# ─────────────────────────────────────────────

def customer_menu():
    global visited_customers_count,purchased_customers_count
    cart = []
    print('<<<< Welcome.... You entered into customer view.... Explore our store >>>>')
    visited_customers_count += 1
    while True:
        ch = show_menu(['1.Add to cart', '2.View Cart', '3.Modify Cart', '4.Delete Cart', '5.See Store List', '6.Billing', '7.Checkout', '8.Exit'])
        if ch == '1':
            add_to_cart(cart)
        elif ch == '2':
            view_cart_details(cart)
        elif ch == '3':
            modify_cart(cart)
        elif ch == '4':
            cart = delete_cart(cart)
            print('*' * 10, 'Cart Deleted Successfully.....', '*' * 10)
        elif ch == '5':
            show_all_details('customer')
        elif ch == '6':
            billing(cart)
        elif ch == '7':
            total_amount = billing(cart)
            if total_amount > 0:
                purchased_customers_count+=1
                print('Checking out...')
                print('Your payable amount is', total_amount)
                print('Thanks for shopping with us, Wait for sometime to get your items.')
                print('*' * 80)
                cart = []
                break
            else:
                print('*' * 10, 'You did not do the shopping, continue shopping', '*' * 10)
        elif ch == '8':
            print('*' * 10, 'Exiting the customer view', '*' * 10)
            break
        else:
            print('<<<<<<Invalid input>>>>>>')


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    while True:
        ch = show_menu(['1.Shopkeeper', '2.Customer', '3.Exit'])
        if ch == '1':
            shopkeeper_menu()
        elif ch == '2':
            customer_menu()
        elif ch == '3':
            print('*' * 10, 'Exiting the App', '*' * 10)
            break
        else:
            print('<<<<<<<<<<<<Wrong input. Enter correct input>>>>>>>>>>')
            continue
        ch = input('Do you want to switch between customer and shopkeeper? (yes/no): ')
        if ch == 'yes':
            continue
        elif ch == 'no':
            print('###################################################')
            print('Exited the Store app, Come again, Thank you')
            print('###################################################')
            break
        else:
            print('Invalid Input')
            continue


if __name__ == '__main__':
    main()