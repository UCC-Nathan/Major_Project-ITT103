# ------------------ BEST BUY POS SYSTEM------------------

products = {
    "Mixed Parts": {"price": 800, "stock": 50, "unit": "lb"},
    "Fish": {"price": 750, "stock": 15, "unit": "lb"},
    "Nuggets": {"price": 600, "stock": 25, "unit": "lb"},
    "Fries": {"price": 300, "stock": 30, "unit": "lb"},
    "Rice": {"price": 80, "stock": 60, "unit": "lb"},
    "Flour": {"price": 125, "stock": 70, "unit": "lb"},
    "Cornmeal": {"price": 70, "stock": 6, "unit": "lb"},
    "Snacks": {"price": 100, "stock": 200, "unit": "pcs"},
    "Sugar": {"price": 200, "stock": 30, "unit": "lb"},
    "Mackerel": {"price": 400, "stock": 20, "unit": "pcs"},
    "Corn Beef": {"price": 550, "stock": 10, "unit": "pcs"},
    "Tuna": {"price": 240, "stock": 5, "unit": "pcs"},
    "Sardine": {"price": 165, "stock": 8, "unit": "pcs"},
    "Coconut Oil": {"price": 160, "stock": 30, "unit": "litre"},
    "Tang": {"price": 70, "stock": 100, "unit": "pcs"},
    "Soap Powder": {"price": 260, "stock": 20, "unit": "pcs"},
    "Bleach": {"price": 120, "stock": 20, "unit": "litre"},
    "Soda": {"price": 200, "stock": 67, "unit": "pcs"},
    "Cup Noodles": {"price": 180, "stock": 67, "unit": "pcs"},
    "Wheat Crackers": {"price": 130, "stock": 2, "unit": "pcs"},
}

TAX_RATE = 0.10
DISCOUNT_RATE = 0.05
DISCOUNT_THRESHOLD = 5000
cart = {}

def line_filler():
    print("-" * 40)

def show_products():
    print("\nAvailable Products:")
    line_filler()
    print(f"{'No.':<4} {'Product':<22} {'Price':>8} {'Stock':>12}")
    line_filler()
    for i, name in enumerate(products, start=1):
        p = products[name]
        stock_warning = f"{p['stock']} {p['unit']}"
        if p['stock'] < 5 and p['stock'] > 0:
            stock_warning += " - LOW STOCK!"
        print(f"{i:<4} {name:<22} ${p['price']:>7.2f} {stock_warning:>12}")
    line_filler()

def cart_viewer():
    if not cart:
        print("\nYour cart is currently empty!\n")
        return

    print("\nCurrent Cart:")
    line_filler()
    print(f"{'Item':<22} {'Qty':>5} {'Unit':>6} {'Total':>10}")
    line_filler()
    subtotal = 0
    for item, d in cart.items():
        total = d["price"] * d["quantity"]
        subtotal += total
        print(f"{item:<22} {d['quantity']:>5} {d['unit']:>6} ${total:>9.2f}")
    line_filler()
    print(f"{'Subtotal':<35} ${subtotal:>9.2f}")
    line_filler()

def subtotal_generator():
    return sum(d["price"] * d["quantity"] for d in cart.values())

def low_stock_checker():
    low_products = [name for name in products if 0 < products[name]["stock"] < 5]
    if low_products:
        print("\nSTOCK RUNNING LOW!")
        for name in low_products:
            print(f"- {name}: {products[name]['stock']} {products[name]['unit']} left!")
        print()

def out_of_stock_checker():
    out_products = [name for name in products if products[name]["stock"] == 0]
    if out_products:
        print("\nOUT OF STOCK ITEMS!")
        for name in out_products:
            print(f"- {name} is SOLD OUT!")
        print()

def add_product():
    show_products()
    names = list(products.keys())
    choice = input("Select product number (0 to cancel): ")
    if not choice.isdigit():
        print("Invalid input.")
        return
    choice = int(choice)
    if choice == 0:
        return
    if choice < 1 or choice > len(names):
        print("Invalid selection.")
        return

    item = names[choice - 1]
    p = products[item]

    try:
        qty = float(input(f"Enter quantity ({p['unit']}): ")) if p["unit"] in ["lb", "litre"] else int(input("Enter quantity: "))
        if qty <= 0:
            print("Quantity must be positive.")
            return
    except:
        print("Invalid quantity.")
        return

    if qty > p["stock"]:
        print(f"Not enough stock. Available: {p['stock']} {p['unit']}")
        return

    cart[item] = cart.get(item, {"price": p["price"], "quantity": 0, "unit": p["unit"]})
    cart[item]["quantity"] += qty
    p["stock"] -= qty
    print(f"Added {qty} {p['unit']} of {item} to cart.")

    if p["stock"] == 0:
        print(f"Out of stock: {item} is now sold out!")
    elif 0 < p["stock"] < 5:
        print(f"Low stock alert: {item} only {p['stock']} {p['unit']} left!")

    low_stock_checker()
    out_of_stock_checker()

def item_removal():
    if not cart:
        print("Your cart is currently empty!")
        return
    items = list(cart.keys())
    for i, item in enumerate(items, 1):
        print(f"{i}. {item} ({cart[item]['quantity']} {cart[item]['unit']})")
    choice = input("Select product to remove (0 to cancel): ")
    if not choice.isdigit():
        print("Invalid input.")
        return
    choice = int(choice)
    if choice == 0:
        return
    if choice < 1 or choice > len(items):
        print("Invalid selection.")
        return

    item = items[choice - 1]
    current_qty = cart[item]["quantity"]
    unit = cart[item]["unit"]

    try:
        qty = float(input(f"Remove how much ({unit}) max {current_qty}: ")) if unit in ["lb", "litre"] else int(input("Enter quantity: "))
    except:
        print("Invalid input.")
        return

    if qty <= 0 or qty > current_qty:
        print("Invalid quantity.")
        return

    cart[item]["quantity"] -= qty
    products[item]["stock"] += qty
    if cart[item]["quantity"] == 0:
        del cart[item]
    print(f"Removed {qty} {unit} of {item} from cart.")

def checkout():
    if not cart:
        print("Your cart is currently empty!")
        return False

    subtotal = subtotal_generator()
    discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_THRESHOLD else 0
    subtotal_after_discount = subtotal - discount
    tax = subtotal_after_discount * TAX_RATE
    total = subtotal_after_discount + tax

    print("\n--- CHECKOUT ---")
    print(f"Subtotal: ${subtotal:.2f}")
    if discount > 0:
        print(f"Discount (5%): -${discount:.2f}")
    print(f"Tax (10%): ${tax:.2f}")
    print(f"Total due: ${total:.2f}")

    while True:
        try:
            payment = float(input("Enter amount received: $"))
            if payment < total:
                print("Insufficient amount.")
                continue
            break
        except:
            print("Invalid input.")

    change = payment - total
    receipt_printer(subtotal, discount, tax, total, payment, change)
    return True

def receipt_printer(subtotal, discount, tax, total, payment, change):
    print("\n" + "="*40)
    print("        BEST BUY RETAIL STORE")
    print("               RECEIPT")
    print("="*40)
    print(f"{'Item':<22} {'Qty':>5} {'Unit':>6} {'Total':>10}")
    print("-"*40)
    for item, d in cart.items():
        total_item = d["quantity"] * d["price"]
        print(f"{item:<22} {d['quantity']:>5} {d['unit']:>6} ${total_item:>9.2f}")
    print("-"*40)
    print(f"{'Subtotal':<35} ${subtotal:>9.2f}")
    if discount > 0:
        print(f"{'Discount (5%)':<35} -${discount:>9.2f}")
    print(f"{'Tax (10%)':<35} ${tax:>9.2f}")
    print("-"*40)
    print(f"{'TOTAL DUE':<35} ${total:>9.2f}")
    print(f"{'Amount Paid':<35} ${payment:>9.2f}")
    print(f"{'Change':<35} ${change:>9.2f}")
    print("="*40)
    print("   Thank you for making it Best Buy!")
    print("="*40 + "\n")

def new_transaction():
    if cart:
        confirm = input("Your cart is not currently empty! Do you still wish to start a new transaction? (yes/no): ").strip().lower()
        if confirm != "yes":
            return
        for item in cart:
            products[item]["stock"] += cart[item]["quantity"]
        cart.clear()
    print("New transaction started.\n")

def main():
    print("="*40)
    print("                 WELCOME")
    print("                   TO")
    print("          BEST BUY RETAIL STORE")
    print("="*40)

    while True:
        print("\n               MENU SCREEN")
        line_filler()
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. Remove Product from Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Start New Transaction")
        print("7. Exit")
        line_filler()

        option = input("Choose an option (1-7): ").strip()
        if option == "1":
            show_products()
        elif option == "2":
            add_product()
        elif option == "3":
            item_removal()
        elif option == "4":
            cart_viewer()
        elif option == "5":
            if checkout():
                cart.clear()
                print("Transaction complete!\n")
        elif option == "6":
            new_transaction()
        elif option == "7":
            if cart:
                confirm = input("Your cart is not currently empty! Do you still wish to Exit? (yes/no): ").strip().lower()
                if confirm != "yes":
                    continue
            print("\nThank you for making it Best Buy! Do Enjoy the rest of your day!\n")
            break
        else:
            print("Invalid option. Please choose 1-7.")

main()