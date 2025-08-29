import random #used for shuffler
from Questions import question_bank # import from questions.py

class QuizGame:

    def __init__(self, question_bank):
        '''Initializes the quiz game'''
        self.question_bank = list(question_bank)    # question list
        self.score = 0                              # player score
        self.question_index = 0                     # question number
        self.shuffle_questions()                    # shuffle

    def shuffle_questions(self):
        random.shuffle(self.question_bank)

    def display_question(self):
        if self.question_index < len(self.question_bank):
            #get current question object
            question = self.question_bank[self.question_index]
            
            #display formatting
            prompt = f"\nQ{self.question_index + 1}: {question.question_text}\n"
            for i, answer in enumerate(question.answers):
                prompt += f"  {chr(65 + i)}) {answer}\n"
            return prompt
        return None

    def check_answer(self, user_answer): #Checks the user's answer by letter OR by full text.
        current_question = self.question_bank[self.question_index]
        user_answer = user_answer.strip() #remove spaces, error prevention
        
        player_choice_text = ""

        #check if answer is letter or full word and correct
        if len(user_answer) == 1 and 'A' <= user_answer.upper() <= 'D':
            choice_index = ord(user_answer.upper()) - ord('A') #convert to number using ascii code
            
            if choice_index < len(current_question.answers):
                player_choice_text = current_question.answers[choice_index] #pulls the actual full word
        else:
            player_choice_text = user_answer

        # check answer and add score if correct
        if player_choice_text.lower() == current_question.correct_answer.lower():
            self.score += 1
            print("Correct! ✅")
        else:
            print(f"Wrong! The correct answer was: {current_question.correct_answer}")
        
        self.question_index += 1 #move to the next question

    def get_score(self):
        total = len(self.question_bank)
        return f"Your final score is: {self.score}/{total}" #score/total

    def reset_game(self): #reset
        self.score = 0
        self.question_index = 0
        self.shuffle_questions()
        print("\nGame has been reset!")

#  METHOD

game = QuizGame(question_bank)

print("--- Welcome to the Pop Culture Quiz! ---")

#game
while True:
    current_question_text = game.display_question()

    if current_question_text is None:
        print("\nYou've completed the quiz!")
        break
    #input answer
    answer = input(f"{current_question_text}Your answer: ")
    game.check_answer(answer)

    #score
    print("\n--------------------")
    print(game.get_score())
    print("--------------------")



    #play again
    play_again = input("\nDo you want to play again? (yes/no): ").lower()
    if play_again not in ("yes", "y"):
        print("Thanks for playing! 👋")
        break
    else:
        game.reset_game()