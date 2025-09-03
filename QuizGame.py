import random #used for shuffler
from Questions import question_bank # import from questions.py

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
        if q.check_answer_text(chosen_text):
            self._score += 1
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {correct_text}")

        self._index += 1  # move to next question

    def get_score_text(self):
        """Return a formatted score string."""
        total = len(self._question_bank)
        return f"Your current score: {self._score}/{total}"

    def get_final_score_text(self):
        total = len(self._question_bank)
        return f"Your final score is: {self._score}/{total}"

    def reset_game(self):
        """Reset score and position, and reshuffle questions."""
        self._score = 0
        self._index = 0
        self.shuffle_questions()
        print("\nGame has been reset!")

    def finished(self):
        """True if we have already asked all questions."""
        return self._index >= len(self._question_bank)


if __name__ == "__main__":
    print("--- Welcome to InfoLympics - Your Pop Culture Quiz! ---")

    while True:
        game = QuizGame(question_bank)

        # Play one full run
        while not game.finished():
            prompt = game.display_question()
            if prompt is None:
                break

            answer = input(f"{prompt}\nYour answer: ")
            game.check_answer(answer)
            print("--------------------")
            print(game.get_score_text())
            print("--------------------")

        print("\nYou've completed the quiz!")
        print(game.get_final_score_text())

        # Ask to play again
        again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break