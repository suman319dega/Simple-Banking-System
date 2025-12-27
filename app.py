import json
import os
import random
import datetime

DATA_FILE = "bank.json"

# ---------------- Utility Functions ----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_account_number():
    return str(random.randint(10000000, 99999999))

def current_time():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# ---------------- Core Banking Features ----------------

def create_account(data):
    print("\n--- Create New Account ---")
    name = input("Enter Name: ")
    pin = input("Set 4-digit PIN: ")

    acc_no = generate_account_number()

    data[acc_no] = {
        "name": name,
        "pin": pin,
        "balance": 0,
        "transactions": []
    }

    save_data(data)
    print(f"\n✅ Account Created Successfully!")
    print(f"Your Account Number: {acc_no}")

def login(data):
    acc_no = input("\nEnter Account Number: ")
    pin = input("Enter PIN: ")

    if acc_no in data and data[acc_no]["pin"] == pin:
        print(f"\n✅ Welcome {data[acc_no]['name']}!")
        user_menu(data, acc_no)
    else:
        print("\n❌ Invalid Account Number or PIN")

def check_balance(data, acc_no):
    print(f"\n💰 Current Balance: ₹{data[acc_no]['balance']}")

def deposit(data, acc_no):
    amount = float(input("Enter deposit amount: "))
    data[acc_no]["balance"] += amount
    data[acc_no]["transactions"].append(
        f"{current_time()} | Deposited ₹{amount}"
    )
    save_data(data)
    print("✅ Amount Deposited Successfully")

def withdraw(data, acc_no):
    amount = float(input("Enter withdrawal amount: "))
    if amount > data[acc_no]["balance"]:
        print("❌ Insufficient Balance")
        return

    data[acc_no]["balance"] -= amount
    data[acc_no]["transactions"].append(
        f"{current_time()} | Withdrawn ₹{amount}"
    )
    save_data(data)
    print("✅ Withdrawal Successful")

def transfer(data, acc_no):
    target = input("Enter receiver account number: ")
    amount = float(input("Enter amount to transfer: "))

    if target not in data:
        print("❌ Receiver account not found")
        return

    if amount > data[acc_no]["balance"]:
        print("❌ Insufficient Balance")
        return

    data[acc_no]["balance"] -= amount
    data[target]["balance"] += amount

    data[acc_no]["transactions"].append(
        f"{current_time()} | Transferred ₹{amount} to {target}"
    )
    data[target]["transactions"].append(
        f"{current_time()} | Received ₹{amount} from {acc_no}"
    )

    save_data(data)
    print("✅ Transfer Successful")

def transaction_history(data, acc_no):
    print("\n--- Transaction History ---")
    if not data[acc_no]["transactions"]:
        print("No transactions yet.")
    else:
        for t in data[acc_no]["transactions"]:
            print(t)

# ---------------- Menus ----------------

def user_menu(data, acc_no):
    while True:
        print("""
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Transfer Money
5. Transaction History
6. Logout
""")
        choice = input("Choose an option: ")

        if choice == "1":
            check_balance(data, acc_no)
        elif choice == "2":
            deposit(data, acc_no)
        elif choice == "3":
            withdraw(data, acc_no)
        elif choice == "4":
            transfer(data, acc_no)
        elif choice == "5":
            transaction_history(data, acc_no)
        elif choice == "6":
            print("👋 Logged Out Successfully")
            break
        else:
            print("❌ Invalid Choice")

def main_menu():
    data = load_data()

    while True:
        print("""
======= PYTHON BANKING APP =======

1. Create Account
2. Login
3. Exit
""")
        choice = input("Select an option: ")

        if choice == "1":
            create_account(data)
        elif choice == "2":
            login(data)
        elif choice == "3":
            print("Thank you for using the Banking App 🙏")
            break
        else:
            print("❌ Invalid Choice")

# ---------------- Run App ----------------

if __name__ == "__main__":
    main_menu()
