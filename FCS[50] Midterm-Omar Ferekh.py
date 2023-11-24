def main():

    while True:
        print("Welcome to the Browser")
        print("1. Open Tab")
        print("2. Close Tab")
        print("3. Switch Tab")
        print("4. Display All Tabs")
        print("5. Open Nested Tab")
        print("6. Sort All Tabs")
        print("7. Save Tabs")
        print("8. Import Tabs")
        print("9. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            # Open Tab
        elif choice == 2:
            # close Tab
        elif choice == 3:
            #Switch Tab
        elif choice == 4:
            #Display All Tabs
        elif choice == 5:
            #Open Nested Tab
        elif choice == 6:
            #Sort All tabs
        elif choice == 7:
            #save Tabs
        elif choice == 8:
            #Import Tabs
        elif choice == 9:
            print("The program is closing...")
            break
        else:
            print("Invalid Choice. Please Enter a valid choice (1->9)")


main()

