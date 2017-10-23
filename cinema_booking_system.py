# Cinema Booking System
# Kieran Widdowson (N0676466)
#
# A system for a cinema that allows the user to log in as a customer or a manager.
# They will have different options based on what they choose. A customer can view films showing and reserve tickets.
# A manager has greater privileges and can perform administrative tasks

import sys, time, pickle

def open_file(file_name, mode):
    """ Open a file. """
    try:
        the_file = open(file_name, mode)
    except IOError as e:
        print("Unable to open the file", file_name, "Ending program.\n",e)
        input("\n\nPress the enter key to exit.")
        sys.exit()
    else:
        return the_file

def check_password(user_password):
    """ Checks the password the user has entered. """
    password = "admin"
    if user_password == password:
        print("\nYour password was correct.\n")
        return 1
    else:
        return None
        
def customer_selected():
    """ Runs the program for a customer. """
    choice = None
    while choice != "0":
        
        print(
        """
\t\tWelcome, Customer.

Please enter one of the options below.

0 - Exit
1 - View Films
2 - View Ticket Prices
3 - Reserve Tickets
"""
            )

        choice = input("Choice: ")
        print()

        # exit
        if choice == "0":
            print("Exiting menu...\n")

        # view films
        elif choice == "1":
            try:
                file = open_file("films.dat", "rb")
                films = pickle.load(file)

                print("\nFilms Currently Showing:\n".upper())
                for key in sorted(films.keys()):
                    print(key)
                                  
                file.close()
            except EOFError:
                print("File is empty.")
                        

            input("\nPress the enter key to continue.")

        # view ticket prices
        elif choice == "2":
            file = open_file("prices.dat", "rb")
            prices = pickle.load(file)
            adultPrice = prices["Adult"]
            childPrice = prices["Child"]
            concessionPrice = prices["Concession"]
            print("Current ticket prices are:\n",
                  "\nAdult: £", "%.2f" % adultPrice,
                  "\nChild: £", "%.2f" % childPrice,
                  "\nConcession: £", "%.2f" % concessionPrice)
            file.close()

            input("\nPress the enter key to continue.\n")

        # reserve tickets
        elif choice == "3":
            try:
                file = open_file("showings.dat", "rb")
                showings = pickle.load(file)

                print("\nFilms Currently Showing:\n".upper())
                for key, value in sorted(showings.items()):
                    print(key)
                    print("Screen:  ", "Date:  ", "           Time:  ")
                    for highlist in value:
                        for lowlistitem in highlist:
                            print(lowlistitem, end="         ")
                        print("\n")
                print("\n")
                                     
                file.close()
            except EOFError:
                print("File is empty.")

            input("\nPress the enter key to continue.")
            print("\n")

            print("\n\nFill in the following information for the showing you wish to reserve.")
            filmToReserve = str(input("\nEnter the film title: "))
            dateToReserve = str(input("Enter the showing date, DD/MM/YYYY: "))
            timeToReserve = str(input("Enter the showing time, HH:MM : "))

            showingToReserve = [filmToReserve,dateToReserve,timeToReserve]

            numAdult = int(input("\nHow many adult tickets?: "))
            numChild = int(input("How many child tickets?: "))
            numConcession = int(input("How many concession tickets?: "))

            file = open_file("prices.dat", "rb")
            prices = pickle.load(file)

            adultPrice = prices["Adult"]
            childPrice = prices["Child"]
            concessionPrice = prices["Concession"]

            file.close()

            totalCost = (numAdult*adultPrice)+(numChild*childPrice)+(numConcession*concessionPrice)

            try:
                file = open_file("tickets_sold.dat", "rb")
                tickets_sold = pickle.load(file)
                adult_sold = tickets_sold["AdultSold"]
                child_sold = tickets_sold["ChildSold"]
                concession_sold = tickets_sold["ConcessionSold"]
                total_taken = tickets_sold["TotalTaken"]
                file.close()
            except EOFError:
                tickets_sold = {}
                adult_sold = 0
                child_sold = 0
                concession_sold = 0
                total_taken = 0                
                
            adult_sold += numAdult
            child_sold += numChild
            concession_sold += numConcession
            total_taken += totalCost

            file = open_file("tickets_sold.dat", "wb")
            tickets_sold["AdultSold"] = adult_sold
            tickets_sold["ChildSold"] = child_sold
            tickets_sold["ConcessionSold"] = concession_sold
            tickets_sold["TotalTaken"] = total_taken
            pickle.dump(tickets_sold, file)
            file.close()

            print("\nYour reservation has been received and is as follows:\n",
                  "\nFilm: ", filmToReserve, "on", dateToReserve, "at", timeToReserve,
                  "\nNumber of Adult tickets:", numAdult,
                  "\nNumber of Child tickets:", numChild,
                  "\nNumber of Concession tickets: ", numConcession,
                  "\n\nThe total to pay is: £", "%.2f" % totalCost)

            input("\nPress the enter key to continue.")
            print("\n")
            
        # some unknown choice
        else:
            print("Sorry, but '", choice, "' isn't a valid choice.\n")

def manager_selected():
    """ Runs the program for a manager. """
    choice = None
    while choice != "0":
        
        print(
        """
\t\tWelcome, Manager.

Please enter one of the options below.

0 - Exit
1 - Set Ticket Prices
2 - Add/Remove Film
3 - Add/Remove Screen
4 - Add/Remove Showing
5 - View Tickets Sold & Income
"""
            )

        choice = input("Choice: ")
        print()

        # exit
        if choice == "0":
            print("Exiting menu...")
        # set ticket prices
        elif choice == "1":
            try:
                file = open_file("prices.dat", "rb")
                prices = pickle.load(file)
                print("Current ticket prices are:\n",
                      "\nAdult: £", prices["Adult"],
                      "\nChild: £", prices["Child"],
                      "\nConcession: £", prices["Concession"])
                file.close()
            except EOFError:
                print("File is empty. Set ticket prices for first time.")
                prices = {}
            

            change_prices = input("\nWould you like to change prices? y/n: ")
            
            if change_prices == "y":
                file = open_file("prices.dat", "wb")
                prices["Adult"] = float(input("\nAdult: £"))
                prices["Child"] = float(input("Child: £"))
                prices["Concession"] = float(input("Concession: £"))
                pickle.dump(prices, file)
                file.close()
            elif change_prices == "n":
                print("Okay, exiting...")
            else:
                print(change_prices, "is not recognised. Try again.")

            input("\nPress the enter key to continue.\n")
            
        # add/remove film
        elif choice == "2":
            choice = None
            while choice != "0":
        
                print(
        """
What would you like to do?

0 - Exit
1 - View Films
2 - Add Film
3 - Remove Film
"""
                )

                choice = input("Choice: ")
                print()

                # exit
                if choice == "0":
                    print("Exiting menu...")

                # view films
                elif choice == "1":
                    try:
                        file = open_file("films.dat", "rb")
                        films = pickle.load(file)

                        print("\nFilms Currently Showing:\n".upper())
                        for key in sorted(films.keys()):
                            print(key)
                                  
                        file.close()
                    except EOFError:
                        print("File is empty.")

                    input("\nPress the enter key to continue.")
                    print("\n")
                        
                # add a film
                elif choice == "2":
                    while True:
                        Title = input("\nEnter the film title: ")
                        Description = input("Enter a description: ")
                        Age_rating = input("Enter the age rating: ")
                        Star_rating = input("Enter a star rating: ")
                        Running_time = input("Enter the running time: ")
                        Dimension = input("Is the film 2D or 3D?: ")

                        try:
                            file = open_file("films.dat", "rb")
                            films = pickle.load(file)
                            file.close()
                        except EOFError:
                            films = {}


                        details = (Description,
                                   "\nAge Rating: ", Age_rating,
                                   "Star Rating: ", Star_rating,
                                   "Running Time: ", Running_time,
                                   Dimension, "\n")
                    
                        films[Title] = details
                    
                    
                        file = open_file("films.dat", "wb")
                        pickle.dump(films, file)
                        file.close()

                        keepLooping = input("\nAnother film to add? y/n: ")
                        if keepLooping == "n":
                            break
                    
                # remove a film
                elif choice == "3":
                    while True:
                        try:
                            file = open_file("films.dat", "rb")
                            films = pickle.load(file)

                            print("\nFilms Currently Showing:\n".upper())
                            for key in sorted(films.keys()):
                                print(key)
                                  
                            file.close()
                        except EOFError:
                            print("File is empty. You must add a film first before you can remove it.")

                        filmToDelete = input("\nEnter the film title to delete: ")

                        try:
                            del films[filmToDelete];
                        except KeyError:
                            print("That film doesn't exist.")

                        file = open_file("films.dat", "wb")
                        pickle.dump(films, file)
                        file.close()

                        keepLooping = input("\nAnother film to delete? y/n: ")
                        if keepLooping == "n":
                            break
                    
                # some unknown choice 
                else:
                    print("Sorry, but ", choice, "isn't a valid choice.\n")

        # add/remove screen
        elif choice == "3":
            choice = None
            while choice != "0":
        
                print(
        """
What would you like to do?

0 - Exit
1 - View Screens
2 - Add Screen
3 - Remove Screen
"""
                )

                choice = input("Choice: ")
                print()

                # exit
                if choice == "0":
                    print("Exiting menu...")

                # view screens
                elif choice == "1":
                    try:
                        file = open_file("screens.dat", "rb")
                        screens = pickle.load(file)

                        print("\nThe following screens are in the file:\n")
                        for key, value in sorted(screens.items()):
                            print("Screen", key, "Capacity: ", value)
                                  
                        file.close()
                    except EOFError:
                        print("File is empty.")

                    input("\nPress the enter key to continue.")
                    print("\n")
                        
                # add a screen
                elif choice == "2":
                    while True:
                        ScreenNum = int(input("\nEnter the screen number: "))
                        Capacity = input("Enter the capacity: ")

                        try:
                            file = open_file("screens.dat", "rb")
                            screens = pickle.load(file)
                            file.close()
                        except EOFError:
                            screens = {}
                    
                        screens[ScreenNum] = Capacity
                    
                        file = open_file("screens.dat", "wb")
                        pickle.dump(screens, file)
                        file.close()

                        keepLooping = input("\nAnother screen to add? y/n: ")
                        if keepLooping == "n":
                            break
                    
                # remove a screen
                elif choice == "3":
                    while True:
                        try:
                            file = open_file("screens.dat", "rb")
                            screens = pickle.load(file)

                            print("\nThe following screens are in the file:\n")
                            for key, value in sorted(screens.items()):
                                print("Screen", key, "Capacity: ", value)
                                  
                            file.close()
                        except EOFError:
                            print("File is empty. You must add a screen first before you can remove it.")

                        screenToDelete = int(input("\nEnter the screen number to delete: "))

                        try:
                            del screens[screenToDelete];
                        except KeyError:
                            print("That screen doesn't exist.")
                            

                        file = open_file("screens.dat", "wb")
                        pickle.dump(screens, file)
                        file.close()

                        keepLooping = input("\nAnother screen to delete? y/n: ")
                        if keepLooping == "n":
                            break
                    
                # some unknown choice 
                else:
                    print("Sorry, but ", choice, "isn't a valid choice.\n")

        # add/remove showing
        elif choice == "4":
            choice = None
            while choice != "0":
        
                print(
        """
What would you like to do?

0 - Exit
1 - View Showings
2 - Add Showing
3 - Remove Showing
"""
                )

                choice = input("Choice: ")
                print()

                # exit
                if choice == "0":
                    print("Exiting menu...")

                # view showings
                elif choice == "1":
                    try:
                        file = open_file("showings.dat", "rb")
                        showings = pickle.load(file)

                        print("\nFilms Currently Showing:\n".upper())
                        for key, value in sorted(showings.items()):
                            print(key)
                            print("Screen:  ", "Date:  ", "           Time:  ")
                            for item in value:
                                for lowlist in item:
                                    print(lowlist, end="         ")
                                print("\n")
                        print("\n")
                                     
                        file.close()
                    except EOFError:
                        print("File is empty.")

                    input("\nPress the enter key to continue.")
                    print("\n")
                        
                # add a showing
                elif choice == "2":
                    while True:
                        try:
                            file = open_file("films.dat", "rb")
                            films = pickle.load(file)

                            print("\nFilms Currently Showing:\n".upper())
                            for key in sorted(films.keys()):
                                print(key)
                                  
                            file.close()
                        except EOFError:
                            print("File is empty.")

                        film = str(input("\nEnter the film showing: "))

                        try:
                            file = open_file("screens.dat", "rb")
                            screens = pickle.load(file)

                            print("\nThe following screens are in the file:\n")
                            for key, value in sorted(screens.items()):
                                print("Screen", key, "Capacity: ", value)
                                  
                            file.close()
                        except EOFError:
                            print("File is empty.")

                        screen = str(input("\nEnter the screen: "))

                        date = str(input("\nEnter the showing date, DD/MM/YYYY: "))
                        time = str(input("Enter the showing time, HH:MM : "))

                        try:
                            file = open_file("showings.dat", "rb")
                            showings = pickle.load(file)
                            file.close()
                        except EOFError:
                            showings = {}

                        details = [screen,date,time]
                    
                        showings.setdefault(film,[]).append(details)
                                        
                        file = open_file("showings.dat", "wb")
                        pickle.dump(showings, file)
                        file.close()

                        keepLooping = input("\nAnother showing to add? y/n: ")
                        if keepLooping == "n":
                            break
                      
                # remove a showing
                elif choice == "3":
                    while True:
                        try:
                            file = open_file("showings.dat", "rb")
                            showings = pickle.load(file)

                            print("\nFilms Currently Showing:\n".upper())
                            for key, value in sorted(showings.items()):
                                print(key)
                                print("Screen:  ", "Date:  ", "           Time:  ")
                                for item in value:
                                    for lowlist in item:
                                        print(lowlist, end="         ")
                                    print("\n")
                            print("\n")
                               
                            file.close()
                        except EOFError:
                            print("File is empty. You must add a showing first before you can remove it.")

                        print("\nFill in the following information for the showing you wish to delete.")
                        screenToDelete = str(input("\nEnter the screen: "))
                        dateToDelete = str(input("Enter the showing date, DD/MM/YYYY: "))
                        timeToDelete = str(input("Enter the showing time, HH:MM : "))

                        valueToDelete = [screenToDelete,dateToDelete,timeToDelete]

                        for value in showings.values():
                            try:
                                value.remove(valueToDelete)
                            except ValueError:
                                pass
                            
                        file = open_file("showings.dat", "wb")
                        pickle.dump(showings, file)
                        file.close()

                        keepLooping = input("\nAnother showing to delete? y/n: ")
                        if keepLooping == "n":
                            break

                        print("\n")
                                            
                # some unknown choice 
                else:
                    print("Sorry, but ", choice, "isn't a valid choice.\n")          

        # view tickets sold & income
        elif choice == "5":
            try:
                file = open_file("tickets_sold.dat", "rb")
                tickets_sold = pickle.load(file)
                adult_sold = tickets_sold["AdultSold"]
                child_sold = tickets_sold["ChildSold"]
                concession_sold = tickets_sold["ConcessionSold"]
                total_taken = tickets_sold["TotalTaken"]
                file.close()

                print("Adult tickets sold: ", adult_sold)
                print("Child tickets sold: ", child_sold)
                print("Concession tickets sold: ", concession_sold)
                print("Total Money taken: £", "%.2f" % total_taken)             
            except EOFError:
                print("File is empty. No tickets have been sold so far.")

            input("\nPress the enter key to continue.\n")

        # some unknown choice
        else:
            print("Sorry, but '", choice, "' isn't a valid choice.\n")

def main():
    """ The main program menu """
    choice = None
    while choice != "0":
        
        print(
        """
\t\tCinema Booking System


Who would you like to login as?

Please enter one of the options below.

0 - Exit
1 - Customer
2 - Manager (password required)
"""
            )

        choice = input("Choice: ")
        print()

        # exit
        if choice == "0":
            print("Exiting program...")

        # enter customer menu
        elif choice == "1":
            customer_selected()

        # enter manager menu
        elif choice == "2":
            entered_password = input("Enter your password: ")
            if check_password(entered_password):
                manager_selected()
            else:
                print("\nSorry, the password you entered was incorrect." \
                      "\nExiting to Main Menu...\n\n")

        # some unknown choice
        else:
            print("Sorry, but '", choice, "' isn't a valid choice.\n")

main()
time.sleep(2)
