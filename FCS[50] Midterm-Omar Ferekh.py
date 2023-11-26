import requests
from bs4 import BeautifulSoup  #intalled with the help of:https://stackoverflow.com/questions/35748239/failed-to-install-package-beautiful-soup-error-message-is-syntaxerror-missing
import json


class Tab:
    def __init__(self, title, url, nestedTabs=None):
        self.title = title
        self.url = url
        self.nestedTabs = nestedTabs if nestedTabs else []

# display function for title and url:
    def displayTabs(self):
        print(f",Contents of the Tab are: {self.title}, and  {self.url}")

# To display the content of the url:
    def scrape_Tabs(self):  # from stack overflow https://stackoverflow.com/questions/68488306/how-do-i-scrape-data-from-urls-in-a-python-scraped-list-of-urls
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Content of {self.title}: {soup.title.text}")

# Json display format
    def Json(self):
        return{
            'title': self.title,
            'url': self.url,
            'nestedTabs': [tab.Json() for tab in self.nestedTabs]
        }


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

    def DisplayAllTabs(self, tabs=None, level=0):
        if tabs is None:
            tabs = self.Tabs

        if not tabs:
            print("There are no tabs in the dictionary.")
        else:
            print("Titles of Tabs are:")
            self.DisplayAllTabsRecursively(tabs, level)

    def DisplayAllTabsRecursively(self, tabs, level): # https://stackoverflow.com/questions/52625673/recursive-method-to-print-the-hierarchical-dictionary
        for tab in tabs:
            print(" " * level + "-" + tab.title)
            self.DisplayAllTabsRecursively(tab.nestedTabs, level + 3)

    def DisplayAllTabsHERIECALLY(self, tabs=None, level=0):
        if tabs is None:
            tabs = self.Tabs
        if not tabs:
            print("There are no tabs in the dictionary")
        else:
            self.DisplayAllTabsRecursively(tabs, level)

    def OpenNestedTabs(self):
        userInput = int(input("Please enter the index of the Tab you wish to add a nested Tab to it: "))
        if 0 <= userInput < len(self.Tabs):
            parentTab = self.Tabs[userInput]
            title = input("Please enter the title for your Nested Tab: ")
            url = input("Please enter the url of your Nested Tab: ")
            newTab = Tab(title, url)
            parentTab.nestedTabs.append(newTab)
        else:
            print("Invalid index of the Parent Tab.")

    def SaveTabs(self):
        filePath = input("Please enter the file path to save Tabs: ").strip('\"') # input("Please enter the file path to save Tabs: ".strip('\"'))   https://stackoverflow.com/questions/76412991/selective-data-saving-to-a-file-in-python
        with open(filePath, 'w') as file:
            tabs_Json = [tab.Json() for tab in self.Tabs]
            json.dump(tabs_Json, file)  # https://www.geeksforgeeks.org/append-to-json-file-using-python/
        print("Tabs successfully added.")

    def ImportTabs(self):
        filePath = input("Please enter the file path to import files from: ").strip('\"')
        with open(filePath, 'r') as file:
            self.Tabs = json.load(file)
        print(f"Tabs data imported from {filePath}")


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
        elif choice == 4:
            System.DisplayAllTabsHERIECALLY()
        elif choice == 5:
            System.OpenNestedTabs()
        # elif choice == 6:
        #     #Sort All tabs
        elif choice == 7:
            System.SaveTabs()
        elif choice == 8:
            System.ImportTabs()
        elif choice == 9:
            print("The program is closing...")
            break
        else:
            print("Invalid Choice. Please Enter a valid choice (1->9)")


main()

