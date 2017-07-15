import random as rnd

class Game:

    def __init__(self, pl_name = "Player",
                       ai_name = "Computer",
                       board_size = 6):

        self.pl_name = pl_name
        self.pl_score = 0
        
        self.ai_name = ai_name
        self.ai_score = 0

        self.turn = pl_name
        self.selection = []

        self.board_size = board_size
        self.board_out = []
        self.board_data = []
        self.create_board()

        self.running = True
        self.run() 

    def create_board(self):

        if self.board_size % 2 == 0:
            nums = []
            for i in range(int(self.board_size / 2)):
                nums.append(i + 1)
                nums.append(i + 1)
            
            for i in range(self.board_size):
                self.board_out.append(0)

                r = rnd.randint(0, len(nums) - 1)
                self.board_data.append(nums[r])
                del nums[r]
            
        else:
            raise UnevenCardTotal("Make sure the board size is an even number.")

    def display_scores(self):
        ''' Prints the current scores of the players '''
        print("Current Scores:")
        print("%s: %s" % (self.pl_name, self.pl_score))
        print("%s: %s" % (self.ai_name, self.ai_score))

    def display_board(self):
        ''' Prints the current state of the board '''
        self.display_line(self.board_size * 3)
        
        string = " "
        for i in range(self.board_size):
            if self.board_out[i] != 0:
                string += "%s  " % self.board_data[i]
            else:
                string += "%s  " % self.board_out[i]

        print(string)
        self.display_line(self.board_size * 3)

    def display_line(self, n):
        ''' Prints a line of dashes equal to n '''
        string = ""
        for i in range(n):
            string += "-"

        print(string)

    def display_ending(self):
        ''' Checks who won and outputs the winner '''
        if (self.pl_score > self.ai_score):
            print ("%s wins!" % self.pl_name)
        elif (self.pl_score < self.ai_score):
            print ("%s wins!" % self.ai_name)
        else:
            print ("It's a draw, nobody wins!")
   
    def wait_for_user(self):
        ''' Waits for the user to input something '''
        return input(">>: ")

    def wait_for_seconds(self, seconds):
        ''' Waits for the specified number of milliseconds '''
        pass
    
    def select_card(self, index):
        ''' Select a card on the board '''
        if self.board_out[index] == 0 and len(self.selection) < 2:
            self.board_out[index] = 1
            self.selection.append(index)
            print("Card %s selected." % str(index + 1))
            self.display_board()
        else:
            print("Invalid selection! Try again")

    def compare_selection(self):
        ''' Compares the two selected indexes and checks for a match '''
        a = self.selection[0]
        b = self.selection[1]
        if self.board_data[a] == self.board_data[b]:
            self.board_out[a] = 2
            self.board_out[b] = 2
            self.increase_score()
            print("%s got a match! They get 2 points." % self.turn)
        else:
            print("No match for %s." % self.turn)
            self.switch_turns()

        self.selection = []

    def increase_score(self):
        ''' Increases the score of this turns controller '''
        if (self.turn == self.pl_name):
            self.pl_score += 2
        elif (self.turn == self.ai_name):
            self.ai_score += 2

    def switch_turns(self):
        ''' Allows the other player to take actions instead '''
        if (self.turn == self.pl_name):
            self.turn = self.ai_name
        elif (self.turn == self.ai_name):
            self.turn = self.pl_name

        print("It is now %s's turn" % self.turn)

    def reset_board_out(self):
        ''' Resets the board output '''
        for i in range(len(self.board_out)):
            if self.board_out[i] == 1:
                self.board_out[i] = 0

    def check_for_finish(self):
        ''' Checks if all cards have been claimed '''
        if (all(i == 2 for i in self.board_out)):
            self.running = False



    def pl_input_shell(self):
        ''' Take the input of the player from the Python shell '''
        inp = int(self.wait_for_user())

        inp -= 1
        if inp >= len(self.board_out) or inp < 0:
            print("Invalid selection! Try again")
        else:
            self.select_card(inp)

    def ai_input_random(self):
        ''' Randomly selects an input for the ai'''
        inp = rnd.randint(0, len(self.board_out) - 1)
        self.select_card(inp)

        

    def run(self):
        
        while (self.running):

            print()            
            self.display_board()
            self.display_scores()
            print("\nSelect a card, %s!" % self.turn)

            if (self.turn == self.pl_name):
                self.pl_input_shell()
                
            elif (self.turn == self.ai_name):
                self.ai_input_random()

            if (len(self.selection) == 2):
                self.compare_selection()
                self.check_for_finish()
                self.reset_board_out()

            if self.running == False:
                self.display_board()
                self.display_scores()
                self.display_ending()
                break
                    

class UnevenCardTotal(Exception):
    pass

g = Game(board_size = 8)
