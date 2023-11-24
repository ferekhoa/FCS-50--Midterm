import requests
from bs4 import BeautifulSoup  #intalled with the help of:https://stackoverflow.com/questions/35748239/failed-to-install-package-beautiful-soup-error-message-is-syntaxerror-missing
class Tab:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def displayTabs(self):
        print(f",Contents of the Tab are: {self.title}, and  {self.url}")

    def scrape_Tabs(self):  # from stack overflow https://stackoverflow.com/questions/68488306/how-do-i-scrape-data-from-urls-in-a-python-scraped-list-of-urls
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Content of {self.title}: {soup.title.text}")

class Browser:
    def __init__(self):
        self.Tabs = []

    def OpenTab(self):
        title = input("Please enter the title for your Tab: ")
        url = input("Please enter the url of your Tab: ")
        newTab = Tab(title, url)
        self.Tabs.append(newTab)

    def CloseTab(self):
        userInput = input("Please enter the index of the tab you wish to close or enter to close the last Tab: ")
        if userInput:
            index = int(userInput)
            if 0 <= index < len(self.Tabs):
                self.Tabs.remove(self.Tabs[index])
            else:
                print("Invalid Index.")
        else:
            self.Tabs.pop()

    def SwitchTab(self):
        userInput = input("Please enter the index of the Tab you wish to preview its content or enter to show the content of the last Tab: ")
        if userInput:
            index = int(userInput)
            if 0 <= index < len(self.Tabs):
                self.Tabs[index].scrape_Tabs()
            else:
                print("Invalid Index.")
        else:
            self.Tabs[-1].scrape_Tabs()


def main():

    System = Browser()
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
            System.OpenTab()
        elif choice == 2:
            System.CloseTab()
        elif choice == 3:
            System.SwitchTab()
        # elif choice == 4:
        #     #Display All Tabs
        # elif choice == 5:
        #     #Open Nested Tab
        # elif choice == 6:
        #     #Sort All tabs
        # elif choice == 7:
        #     #save Tabs
        # elif choice == 8:
        #     #Import Tabs
        elif choice == 9:
            print("The program is closing...")
            break
        else:
            print("Invalid Choice. Please Enter a valid choice (1->9)")


main()

