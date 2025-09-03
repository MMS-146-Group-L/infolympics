import random

class Question:
    def __init__(self, question_text, answers, correct_answer):
        self._question_text = question_text        # the given question
        self._answers = answers[:]                 # list of possible answers (copied)
        self._correct_answer = correct_answer      # the correct answer

    # ——— Getters ———
    def get_question_text(self):
        """Return the question text."""
        return self._question_text

    def get_answers(self):
        """Return a list of possible answers."""
        return self._answers[:]

    def get_correct_answer(self):
        """Return the correct answer."""
        return self._correct_answer

    # ——— Core behaviors ———
    def check_answer(self, user_answer):
        """Return True if user_answer matches the correct answer."""
        return user_answer.strip().lower() == self._correct_answer.lower()

    def display_question(self):
        """Print the question and its current answer choices."""
        print(f"Q: {self._question_text}")
        for idx, ans in enumerate(self._answers, start=1):
            print(f"  {idx}. {ans}")

    def shuffle_answers(self):
        """Randomize the order of answer choices."""
        random.shuffle(self._answers)

    def get_feedback(self, user_answer):
        """Return a feedback message based on correctness."""
        if self.check_answer(user_answer):
            return "✅ Correct!"
        return f"❌ Wrong! The correct answer is: {self._correct_answer}"


# 15 Pop Culture Questions 
question_bank = [
    Question("In the series Game of Thrones, who is known as the 'Mother of Dragons'?",
             ["Cersei Lannister", "Daenerys Targaryen", "Sansa Stark", "Arya Stark"],
             "Daenerys Targaryen"),

    Question("Which animated movie features the characters Woody and Buzz Lightyear?",
             ["Finding Nemo", "Toy Story", "Shrek", "The Incredibles"],
             "Toy Story"),

    Question("Who voices Donkey in Shrek?",
             ["Eddie Murphy", "Chris Rock", "Will Smith", "Kevin Hart"],
             "Eddie Murphy"),

    Question("What is the name of the fictional African country in Black Panther?",
             ["Zamunda", "Wakanda", "Genovia", "Latveria"],
             "Wakanda"),

    Question("In the Harry Potter films, who killed Dumbledore?",
             ["Lord Voldemort", "Severus Snape", "Bellatrix Lestrange", "Draco Malfoy"],
             "Severus Snape"),

    Question("Who is known as the 'King of Pop'?",
             ["Elvis Presley", "Michael Jackson", "Prince", "Bruno Mars"],
             "Michael Jackson"),

    Question("Which female artist released the hit song 'Rolling in the Deep'?",
             ["Adele", "Rihanna", "Beyoncé", "Sia"],
             "Adele"),

    Question("What is the stage name of Stefani Joanne Angelina Germanotta?",
             ["Lady Gaga", "Pink", "Dua Lipa", "Halsey"],
             "Lady Gaga"),

    Question("Which band released the song 'Bohemian Rhapsody'?",
             ["The Beatles", "Queen", "Led Zeppelin", "Pink Floyd"],
             "Queen"),

    Question("Which rapper released the album 'Scorpion' in 2018?",
             ["Kanye West", "Drake", "Jay-Z", "Lil Wayne"],
             "Drake"),

    Question("What is the best-selling video game of all time?",
             ["Minecraft", "Tetris", "Grand Theft Auto V", "Fortnite"],
             "Minecraft"),

    Question("In Among Us, what is the role of the player trying to eliminate others secretly?",
             ["Crewmate", "Impostor", "Leader", "Captain"],
             "Impostor"),

    Question("Which video game character is known for collecting rings?",
             ["Mario", "Sonic the Hedgehog", "Crash Bandicoot", "Kirby"],
             "Sonic the Hedgehog"),

    Question("What color is Pac-Man?",
             ["Red", "Yellow", "Blue", "Green"],
             "Yellow"),

    Question("Which popular game features the phrase 'Victory Royale'?",
             ["PUBG", "Call of Duty", "Fortnite", "Overwatch"],
             "Fortnite")
]


# Test 
if __name__ == "__main__":
    q = question_bank[0]

    # Shuffle & display using your new methods
    q.shuffle_answers()
    print("Q:", q.get_question_text())
    print("Choices:", q.get_answers())

    answer = input("Your answer: ")
    print(q.get_feedback(answer))

    # You can also directly use display_question():
    # q.display_question()
    # answer = input("Your answer: ")
    # print(q.get_feedback(answer))