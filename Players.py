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