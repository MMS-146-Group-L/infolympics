import random #used for shuffler
from Questions import easy_questions, medium_questions, hard_questions # import from questions.py
from Players import Player

class QuizGame:
    """
    Manages a single run of the quiz:
      - holds a list of Question instances
      - tracks score and current index
      - presents questions and checks answers
    """
    def __init__(self, question_bank):
        """Initializes the quiz game with a copy of the provided question list."""
        self._question_bank = list(question_bank)  # keep a private copy
        self._score = 0
        self._index = 0
        self._correct_count = 0
        self._total_pesos = 0

        self.shuffle_questions()

    def shuffle_questions(self):
        """Randomize question order at the start or on reset."""
        random.shuffle(self._question_bank)

    def display_question(self):
        """
        Return a formatted question string (including choices),
        or None if no more questions.
        """
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

            if question_bank == easy_questions:
                question_value = 80000 + 40000 * (self._correct_count - 1)

            elif question_bank == medium_questions:
                question_value = 120000 + 70000 * (self._correct_count - 1)

            else:
                question_value = 200000 + 80000 * (self._correct_count - 1)


            self._total_pesos += question_value
            print(f"Correct! You earned ₱{question_value:,} for this question.")
            self._index += 1
            return True # correct → continue game
            
        else:
            print(f"Wrong! The correct answer was: {correct_text}")
            return False # wrong → stop game

    def get_score_text(self):
        """Return a formatted score string."""
        total = len(self._question_bank)
        return f"Score: {self._score}/{total} | Winnings: ₱{self._total_pesos:,}"

    def get_final_score_text(self):
        total = len(self._question_bank)
        return f"Final: {self._score}/{total} | Total Winnings: ₱{self._total_pesos:,}"

    def reset_game(self):
        """Reset score and position, and reshuffle questions."""
        self._score = 0
        self._index = 0
        self._correct_count = 0
        self._total_pesos = 0
        self.shuffle_questions()
        print("\nGame has been reset!")
        
    def finished(self):
        """True if we have already asked all questions."""
        return self._index >= len(self._question_bank)


if __name__ == "__main__":
    
    #asking the players to input their names
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    playername = Player(firstname, lastname)

    # Display their names using get_name()
    print("Welcome to InfoLympics - Your Pop Culture Quiz,", playername.get_name(),"!")

    print("Choose your level of difficulty,", playername.get_name(), "!")

     # ask difficulty ONCE per run
    choice = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    if choice == "easy":
        question_bank = easy_questions
    elif choice == "medium":
        question_bank = medium_questions
    elif choice == "hard":
        question_bank = hard_questions
    else:
        print("Invalid choice. Defaulting to easy.")
        question_bank = easy_questions

    while True:
        game = QuizGame(question_bank)

        # Play one full run
        while not game.finished():
            prompt = game.display_question()
            if prompt is None:
                break

            answer = input(f"{prompt}\nYour answer: ")
            correct = game.check_answer(answer)  # now returns True/False

            if not correct:  # wrong answer ends the game
                print("\nGame over! You lost your winnings.")
                break

            print("--------------------")
            print(game.get_score_text())
            print("--------------------")

        print("\nYou've completed the quiz!")
        print(game.get_final_score_text())

        # Ask to play again
        again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        
        if again not in ("yes", "y"):
            print("Thanks for playing!")

            with open("game_status.txt", "w") as f:
                f.write(f"QuestionIndex:{game._index}\n")
                f.write(f"Score:{game._score}\n")
                f.write(f"Winnings:{game._total_pesos}\n")

            with open("highscores.txt", "a") as f:
                f.write(f"{playername.get_name()} - {game._score} correct - ₱{game._total_pesos}\n")

            break

        print("Choose your level of difficulty,", playername.get_name(), "!")

        # ask difficulty ONCE per run
        choice = input("Choose difficulty (easy/medium/hard): ").strip().lower()
        if choice == "easy":
            question_bank = easy_questions
        elif choice == "medium":
            question_bank = medium_questions
        elif choice == "hard":
            question_bank = hard_questions
        else:
            print("Invalid choice. Defaulting to easy.")
            question_bank = easy_questions

        
