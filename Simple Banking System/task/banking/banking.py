# Write your code here
import random
import sys
import os
import sqlite3


def luhn(number):
    checksum = 0
    count = 1
    for digit in number:
        digit = int(digit)
        if count % 2 != 0:
            digit = digit * 2
            if digit > 9:
                digit -= 9
        checksum += digit
        count += 1
    if checksum % 10 == 0:
        return str(0)
    else:
        return str(10 - (checksum % 10))


class BankingSystem:
    def __init__(self):
        self.account = str()


    def greeting(self):
        choice = int(input("""1. Create an account \n2. Log into account\n0. Exit\n"""))
        if choice in [1, 2, 0]:
            if choice == 1:
                self.generate_card()
                self.greeting()
            elif choice == 2:
                self.login()
            elif choice == 0:
                sys.exit()
        else:
            self.greeting()

    def menu(self):
        choice = int(input("1. Balance\n"
                           "2. Add income\n"
                           "3. Do transfer\n"
                           "4. Close account\n"
                           "5. Log out\n"
                           "0. Exit\n"))
        if choice in [1, 2, 3, 4, 5, 0]:
            if choice == 1:
                print(self.show_balance())
                self.menu()
            elif choice == 2:
                self.add_income()
                self.menu()
            elif choice == 3:
                self.do_transfer()
                self.menu()
            elif choice == 4:
                self.close_account()
                self.menu()
            elif choice == 5:
                self.greeting()
            elif choice == 0:
                print("Bye!")
                sys.exit()
        else:
            self.menu()

    def generate_card(self):
        newcard = "400000" + str(random.randint(0, 999999999)).zfill(9)
        newcard += luhn(newcard)
        cur.execute("SELECT number FROM card")
        if newcard not in cur.fetchall():
            newpin = str(random.randint(0, 9999)).zfill(4)
            cur.execute("INSERT INTO card (number, pin) VALUES ({}, {})".format(newcard, newpin))
            conn.commit()
            print("Your card has been created.\nYour card number:\n{}\nYour card PIN:\n{}".format(newcard, newpin))

    def login(self):
        self.account = input("Enter your card number:")
        pin = input("Enter your PIN:")
        try:
            cur.execute("SELECT pin FROM card WHERE number={}".format(self.account))
            if pin in cur.fetchone()[0]:
                print("You have successfully logged in!")
            else:
                print("Wrong card number or PIN!")
        except:
            print("Wrong card number or PIN!")
            self.greeting()
        self.menu()

    def show_balance(self):
        cur.execute("SELECT balance FROM card WHERE number = {}".format(self.account))
        return cur.fetchone()[0]

    def add_income(self):
        income = int(input("Enter income:\n"))
        cur.execute("UPDATE card SET balance = (balance + {}) WHERE number = {}".format(income, self.account))
        conn.commit()
        print("Income was added!")

    def do_transfer(self):
        target = input("Transfer\nEnter card number:\n")
        if target == self.account:
            print("You can't transfer money to the same account!")
            return
        cur.execute("SELECT number FROM card")
        if luhn(target[:-1]) == target[-1]:
            if any(target in numbers for numbers in cur.fetchall()):
                amount = int(input("Enter how much money you want to transfer:\n"))
                cur.execute("SELECT balance FROM card WHERE number = {}".format(self.account))
                if amount < cur.fetchone()[0]:
                    cur.execute("UPDATE card SET balance = (balance + {}) WHERE number = {};".format(amount, target))
                    cur.execute("UPDATE card SET balance = (balance - {}) WHERE number = {};".format(amount, self.account))
                    conn.commit()
                    print("Success!")
                else:
                    print("Not enough money!")
            else:
                print("Such a card does not exist")
        else:
            print("Probably you made mistake in the card number. Please try again!")

    def close_account(self):
        cur.execute("DELETE FROM card WHERE number = {}".format(self.account))
        conn.commit()

    def main(self):
        self.greeting()


if __name__ == "__main__":
    if "card.s3db" not in os.listdir():
        open("card.s3db", "w")
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
        conn.commit()
    except:
        #print("Database already exists")
        pass
    newbankingsystem = BankingSystem()
    newbankingsystem.main()
