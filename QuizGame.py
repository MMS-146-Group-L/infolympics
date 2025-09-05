import os
import random #used for shuffler
from Questions import easy_questions, medium_questions, hard_questions
from Players import Player

class QuizGame:
    """
    Manages a single run of the quiz:
    - holds a list of Question instances
    - tracks score and current index
    - presents questions and checks answers
    """
    def __init__(self, question_bank, difficulty):
        self._question_bank = list(question_bank)
        self._difficulty = difficulty
        self._score = 0
        self._index = 0
        self._correct_count = 0
        self._total_pesos = 0
        self._seed = None

    def setup_new_game(self):
        self._seed = random.randint(1, 1000000) #changed shuffler to random seed generator for save state functionality - michael
        self.shuffle_questions()

    def shuffle_questions(self): #uses the generated seed - m
        random.seed(self._seed)
        random.shuffle(self._question_bank)

    def save_state(self, player_name): #save functionality
        with open("game_status.txt", "w", encoding="utf-8") as f:
            f.write(f"Name:{player_name}\n")
            f.write(f"Difficulty:{self._difficulty}\n")
            f.write(f"Seed:{self._seed}\n")
            f.write(f"Index:{self._index}\n")
            f.write(f"Score:{self._score}\n")
            f.write(f"Winnings:{self._total_pesos}\n")
            f.write(f"CorrectCount:{self._correct_count}\n")
    
    def restore_state(self, state): #save functionality pt2
        self._seed = state['Seed']
        self.shuffle_questions()
        self._index = state['Index']
        self._score = state['Score']
        self._total_pesos = state['Winnings']
        self._correct_count = state['CorrectCount']


    def display_question(self):
        if self._index >= len(self._question_bank):
            return None

        q = self._question_bank[self._index]

        # Shuffle choices so position varies
        q.shuffle_answers()

        # Build the prompt
        prompt = []
        prompt.append(f"\nQ{self._index + 1}: {q.get_question_text()}")
        for i, ans in enumerate(q.get_answers()):
            prompt.append(f"  {chr(65 + i)}) {ans}")  # A) B) C) D)
        return "\n".join(prompt)

    def check_answer(self, user_answer):
        """
        Accept either:
          - a single letter A-D (case-insensitive)
          - or the full answer text
        Update score and advance to the next question.
        """
        q = self._question_bank[self._index]
        answers = q.get_answers()

        user_answer = user_answer.strip()

        # Resolve to the actual answer text
        if len(user_answer) == 1 and 'A' <= user_answer.upper() <= 'D':
            idx = ord(user_answer.upper()) - ord('A')
            if idx < len(answers):
                chosen_text = answers[idx]
            else:
                chosen_text = ""
        else:
            chosen_text = user_answer

        # Check correctness by text (case-insensitive)
        correct_text = q.get_correct_answer()
        if q.check_answer(chosen_text):
            self._score += 1
            self._correct_count += 1

            #scoring
            if self._difficulty == 'easy':
                question_value = 80000 + 40000 * (self._correct_count - 1)
            elif self._difficulty == 'medium':
                question_value = 120000 + 70000 * (self._correct_count - 1)
            else: #hard
                question_value = 200000 + 80000 * (self._correct_count - 1)


            self._total_pesos += question_value
            print(f"Correct! You earned ₱{question_value:,} for this question.")
            self._index += 1
            return True #if correct then continue game
            
        else:
            print(f"Wrong! The correct answer was: {correct_text}")
            return False #if wrong then cry xd

    def get_score_text(self):
        total = len(self._question_bank)
        return f"Score: {self._score}/{total} | Winnings: ₱{self._total_pesos:,}"

    def get_final_score_text(self):
        total = len(self._question_bank)
        return f"Final: {self._score}/{total} | Total Winnings: ₱{self._total_pesos:,}"
        
    def finished(self):
        return self._index >= len(self._question_bank)

def load_game_state():
    if not os.path.exists("game_status.txt"):
        return None
    try:
        with open("game_status.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) < 7:
                return None
            state = {}
            for line in lines:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    state[key] = value
            
            #convert numbers from str to int
            state['Index'] = int(state['Index'])
            state['Score'] = int(state['Score'])
            state['Winnings'] = int(state['Winnings'])
            state['Seed'] = int(state['Seed'])
            state['CorrectCount'] = int(state['CorrectCount'])
            return state
    except (ValueError, KeyError, IndexError):
        return None

def play_one_session(game, player):
    # Main game loop for one session
    while not game.finished():
        prompt = game.display_question()
        if prompt is None:
            break

        answer = input(f"{prompt}\nYour answer: ")
        correct = game.check_answer(answer)

        if not correct:
            print("\nGame over!")
            return

        #if correct, save
        game.save_state(player.get_name())
        print("--------------------")
        print(game.get_score_text())
        print("--------------------")

    #end
    if game.finished():
        print("\nCongratulations! You've completed the quiz!")


if __name__ == "__main__":
    
    playername = None
    game = None

    #ask to start a new game or continue
    choice = input("Enter 'new' for a New Game or 'continue' to resume last session: ").strip().lower()
    
    saved_state = load_game_state()

    if choice == 'continue' and saved_state: #resume previous game state
        print("\nResuming your previous session...")
        
        #pull player info
        full_name = saved_state['Name']
        try:
            first, last = full_name.split(' ', 1)
        except ValueError:
            first, last = full_name, ""
        playername = Player(first, last)

        #pull diff
        difficulty = saved_state['Difficulty']
        if difficulty == "easy": question_bank = easy_questions
        elif difficulty == "medium": question_bank = medium_questions
        else: question_bank = hard_questions

        game = QuizGame(question_bank, difficulty)
        game.restore_state(saved_state)

        print(f"Welcome back, {playername.get_name()}!")
        print("--------------------")
        print(game.get_score_text())
        print("--------------------")

    else: #start new game
        if choice == 'continue' and not saved_state:
            print("No saved game found or file is corrupt. Starting a new game.")

        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        playername = Player(firstname, lastname)
        print("\nWelcome to InfoLympics - Your Pop Culture Quiz,", playername.get_name(),"!")

    #main loop
    while True:
        if game is None:
            print("\nChoose your level of difficulty,", playername.get_name(), "!")
            diff_choice = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            if diff_choice == "easy": question_bank = easy_questions
            elif diff_choice == "medium": question_bank = medium_questions
            elif diff_choice == "hard": question_bank = hard_questions
            else:
                print("Invalid choice. Defaulting to easy.")
                diff_choice = "easy"
                question_bank = easy_questions
            game = QuizGame(question_bank, diff_choice)
            game.setup_new_game()

        #play
        play_one_session(game, playername)

        #final score, append high score
        print(game.get_final_score_text())
        if game._total_pesos > 0:
            with open("highscores.txt", "a", encoding="utf-8") as f:
                f.write(f"{playername.get_name()} - {game._score} correct - ₱{game._total_pesos}\n")
        
        #wipe status (does not occur if file is closed prematurely)
        with open("game_status.txt", "w", encoding="utf-8") as f:
            f.write("")

        #play again?
        again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\nThanks for playing!")
            break
        else:
            #reset
            game = None

