import requests
from bs4 import BeautifulSoup  #installed with the help of:https://stackoverflow.com/questions/35748239/failed-to-install-package-beautiful-soup-error-message-is-syntaxerror-missing
import json


class Tab:
    def __init__(self, title, url, nestedTabs=None):
        self.title = title
        self.url = url
        self.nestedTabs = nestedTabs if nestedTabs else []

# display function for title and url:
    def displayTabs(self): # O(1) 
        print(f",Contents of the Tab are: {self.title}, and  {self.url}")

# To display the content of the url:
    def scrape_Tabs(self):  # from stack overflow https://stackoverflow.com/questions/68488306/how-do-i-scrape-data-from-urls-in-a-python-scraped-list-of-urls
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Content of {self.title}: {soup.prettify()}") # https://stackoverflow.com/questions/65780442/scraping-tables-from-a-webpage-into-python
        else:
            print("Failed to retrieve content.")

# Json display format
    def Json(self): # O(n) where n is the number of tabs and nested tabs
        return{
            'title': self.title,
            'url': self.url,
            'nestedTabs': [tab.Json() for tab in self.nestedTabs]
        }


class Browser:
    def __init__(self):
        self.Tabs = []

    def OpenTab(self): # O(1)
        title = input("Please enter the title for your Tab: ")
        url = input("Please enter the url of your Tab: ")
        newTab = Tab(title, url)
        self.Tabs.append(newTab)

    def CloseTab(self): # O(n) where n is the length of the tabs list as the worst case scenario.
        userInput = input("Please enter the index of the tab you wish to close or enter to close the last Tab: ")
        if userInput:
            index = int(userInput)
            if 0 <= index < len(self.Tabs):
                closed_tab = self.Tabs.pop(index)
                print(f"The tab with title '{closed_tab.title}' has ben closed")

            else:
                print("Invalid Index.")
        else:
            closed_tab = self.Tabs.pop()
            print(f"The tab with title '{closed_tab.title}' has ben closed")

    def SwitchTab(self): # O(n) where n is the length of the tabs list as the worst case scenario.
        userInput = input("Please enter the index of the Tab you wish to preview its content or enter to show the content of the last Tab: ")
        if userInput:
            index = int(userInput)
            if 0 <= index < len(self.Tabs):
                self.Tabs[index].scrape_Tabs()
            else:
                print("Invalid Index.")
        else:
            self.Tabs[-1].scrape_Tabs()

    def DisplayAllTabs(self, tabs=None, level=0): # O(n) where n is the number of tabs.
        if tabs is None:
            tabs = self.Tabs

        if not tabs:
            print("There are no tabs in the dictionary.")
        else:
            print("Titles of Tabs are:")
            self.DisplayAllTabsRecursively(tabs, level)

    def DisplayAllTabsRecursively(self, tabs, level): # O(n) where n is the number of tabs and nested tabs # https://stackoverflow.com/questions/52625673/recursive-method-to-print-the-hierarchical-dictionary
        for tab in tabs:
            print(" " * level + "-" + tab.title)
            self.DisplayAllTabsRecursively(tab.nestedTabs, level + 2)

    def DisplayAllTabsHERIECALLY(self, tabs=None, level=0): # O(n) where n is the number of tabs and nested tabs.
        if tabs is None:
            tabs = self.Tabs
        if not tabs:
            print("There are no tabs in the dictionary")
        else:
            self.DisplayAllTabsRecursively(tabs, level)

    def OpenNestedTabs(self): # O(1) since we are choosing an index.
        userInput = int(input("Please enter the index of the Tab you wish to add a nested Tab to it: "))
        if 0 <= userInput < len(self.Tabs):
            parentTab = self.Tabs[userInput]
            title = input("Please enter the title for your Nested Tab: ")
            url = input("Please enter the url of your Nested Tab: ")
            newTab = Tab(title, url)
            parentTab.nestedTabs.append(newTab)
        else:
            print("Invalid index of the Parent Tab.")

    def mergeTabs(self, tabs): # O(nlog(n)) where n is the number of tabs and log is because we are dividing the list into 2 every time.
        if len(tabs) <= 1:
            return tabs
        mid = len(tabs)//2
        left = tabs[:mid]
        right = tabs[mid:]
        left = self.mergeTabs(left)
        right = self.mergeTabs(right)
        return self.merge(left, right)

    def merge(self, left, right):
        new_list = []
        ind1 = 0
        ind2 = 0
        while ind1 < len(left) and ind2 < len(right):
            if left[ind1].title < right[ind2].title:
                new_list.append(left[ind1])
                ind1 += 1
            else:
                new_list.append(right[ind2])
                ind2 += 1
        # https://stackoverflow.com/questions/46860219/how-do-i-make-a-merge-sort-built-for-a-single-list-sort-a-list-of-list-inste
        new_list.extend(left[ind1:])
        new_list.extend(right[ind2:])
        return new_list

    def SortTabsRecursively(self, tab): # O(nlog(n)) where n is the number of tabs since it is will use the merge function.
        tab.nestedTabs = self.mergeTabs(tab.nestedTabs)
        for nestedTab in tab.nestedTabs:
            self.SortTabsRecursively(nestedTab)

    def SortTabs(self): # O(nlog(n)) where n is the number of tabs (same as the merge function)
        self.Tabs = self.mergeTabs(self.Tabs)
        for tab in self.Tabs:
            self.SortTabsRecursively(tab)
        print(f"The Tabs are sorted Successfully")
        for tab in self.Tabs:
            print(json.dumps(tab.Json(), indent=2))

    def SaveTabs(self): # O(n) where n is the number of tabs because it will go in every tab and change it to JSON format.
        filePath = input("Please enter the file path to save Tabs: ").strip('\"') # input("Please enter the file path to save Tabs: ".strip('\"'))   https://stackoverflow.com/questions/76412991/selective-data-saving-to-a-file-in-python
        with open(filePath, 'w') as file:
            tabs_Json = [tab.Json() for tab in self.Tabs]
            json.dump(tabs_Json, file)  # https://www.geeksforgeeks.org/append-to-json-file-using-python/
        print("Tabs successfully added.")

    def ImportTabs(self): # O(n) where n is the number of tabs because it will go through all the tabs to import them.
        filePath = input("Please enter the file path to import files from: ").strip('\"')
        try:
            with open(filePath, 'r') as file:
                fileContent = file.read()
                if not fileContent:
                    print(f"The file at path {filePath} is empty.")
                    return
                tabs_data = json.loads(fileContent)
                self.Tabs = [Tab(tab_data['title'], tab_data['url'], [Tab(**nested) for nested in tab_data['nestedTabs']]) for tab_data in tabs_data]
                print(f"Tabs data imported from {filePath}")
                for tab in self.Tabs:
                    print(json.dumps(tab.Json(), indent=2))
        except FileNotFoundError:
            print("File not found.")


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
        elif choice == 6:
            System.SortTabs()
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

