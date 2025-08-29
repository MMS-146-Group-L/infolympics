class Player:

    def __init__(self, firstname, lastname):
        self.firstname = firstname                           #first name of the player
        self.lastname = lastname                             #last name of the player
        self.player_name = firstname + " " + lastname        #fullname of the player
    
    def get_name(self):
        '''returns the name of the player'''
        return self.player_name
    
    def set_name(self, firstname, lastname):
        '''Updates the player's name'''
        self.firstname = firstname
        self.lastname = lastname
    
#asking the players to input their names
firstname = input("Enter your first name: ")
lastname = input("Enter your last name: ")
playername = Player(firstname, lastname)

# Display their names using get_name()
print("Welcome to infoLympics,", playername.get_name(),"!")

# Ask if they want to update their name
update = input("Would you like to update your name? (yes/no): ").lower()

if update == "yes":
    new_first = input("Type your new first name: ")
    new_last = input("Type your new last name: ")
    playername.set_name(new_first, new_last)
    print("Let's get started,", playername.get_name(), "!")
else:
    print("Alright! Let’s get started,", playername.get_name(), "!")




