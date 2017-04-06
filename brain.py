class Brain:

    def __init__(self, player_name = "Player", ai_name = "Opponent"):

        self.pl_name = player_name
        self.pl_score = 0
        
        self.ai_name = ai_name
        self.ai_score = 0

        self.memory = []

    def display_scores(self):

        print("Current Scores:")
        print("%s:\t%s" % (pl_name, pl_score))
        print("%s:\t%s" % (ai_name, ai_score))

    # AI Turn
        # Check Memory:
            # If match found in memory, Flip (matched cards)
            # Else Flip (unknown card)

        # Select Card (position):
            # Select a card to be flipped
            # Wait
            # Check Memory

        # Wait
            # Wait for user to flip the card

        # Store Memory:
            # If match not found when both cards are flipped,
            #    store card image and card position
            # Else match will be found so user adds one to ai_score

    # PL Turn
        # Wait
            # When card is flipped, Check Card

        # Check Memory
            # If card in memory, ignore
            # Else Store Memory

        # Store Memory
            # Store card image and card position


    # General Functions
    #   Wait()
    #   Check_Card()
    #   Store_Card()
    #   Select_Card()
    #   PL_Turn()
    #   AI_Turn()

            
    def wait(self):
        ''' Waits for the user to do something '''
        inp = Input(">>: ")
    
    def check_card(self, card):
        ''' Compares a card image to those stored in memory '''
        for m in memory:
            compare(card, m)
    
    def store_card(self, card):
        ''' Stores a card image to memory '''
        self.memory.append(card)
    
    def select_card(self):
        ''' Select a card on the board '''
        pass


b = Brain()
