from services.library import Library
from services.menu import *

def main():
    while True:
        show_menu()
        choice = input("Enter your choice:").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            add_member()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_books()
        elif choice == "6":
            show_members()
        elif choice == "0":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please choose from the menu.")

if __name__ == "__main__":
    main()




