import requests
import random

class JeopardyGame:
    def __init__(self):
        # Initierar spelarens namn, kategori, svårighetsgrad och antal frågor
        self.player_name = ""
        self.category = 9 # Standardkategori (General Knowledge)
        self.difficulty = 'easy' # Standard svårighetsgrad
        self.amount = 10 # Standard antal frågor att spela

    def fetch_questions(self):
        # Funktion för att hämta frågor från OpenTDB API
        url = f'https://opentdb.com/api.php?amount={self.amount}&category={self.category}&difficulty={self.difficulty}&type=multiple'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['results'] # Returnerar en lista med frågor och svar
        else:
            print(f"Failed to fetch questions, status code: {response.status_code}")
            return []  # Returnerar en tom lista om något gick fel vid hämtningen

    def format_question(self, question_data):
        # Formaterar frågan och dess svarsalternativ
        question = question_data['question']
        correct_answer = question_data['correct_answer']
        incorrect_answers = question_data['incorrect_answers']
        options = incorrect_answers + [correct_answer]
        random.shuffle(options) # Blandar svarsalternativen
        return question, options, correct_answer

    def play_game(self, questions):
        # Funktion för att spela spelet med de hämtade frågorna
        score = 0
        for i, q_data in enumerate(questions):
            question, options, correct_answer = self.format_question(q_data)
            print(f"\nQuestion {i+1}: {question}")
            for idx, option in enumerate(options):
                print(f"{idx + 1}. {option}")

            try:
                answer = int(input("Your answer (1/2/3/4): ")) - 1
                if options[answer] == correct_answer:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong! The correct answer was: {correct_answer}")
            except (ValueError, IndexError):
                print(f"Invalid input! The correct answer was: {correct_answer}")

        print(f"\nGame over, {self.player_name}! Your final score is: {score}/{len(questions)}")

    def main_menu(self):
        print("Welcome to the Jeopardy-like Quiz Game!")
        
        while True:
            print("\nMain Menu:")
            print("1. Play")
            print("2. Quit")
            choice = input("Enter your choice (1/2): ")
            
            if choice == '1':
                while True:
                    self.player_name = input("Enter your first name only: ")
                    # Validera namnet
                    if self.player_name.strip() and self.player_name.isalnum(): # Denna kod använder strip() för att ta bort eventuella tomma mellanslag från början och slutet av strängen och isalnum() för att kontrollera om namnet endast innehåller alfanumeriska tecken (bokstäver och siffror)
                        break
                    else:
                        print("Invalid name! Please enter a valid name without any funny business.")
                
                print("\nCategories:")
                print("9: General Knowledge")
                print("18: Science: Computers")
                print("21: Sports")
                print("23: History")
                # För att hämta frågor, måste den ange den önskade kategorin som en parameter, och dessa nummer används för att välja den önskade kategorin. Därför använder koden numren som API förväntar sig, vill göra det simpelt för bara internet delen i betyget.

                try:
                    self.category = int(input("Choose a category (enter the number): "))
                except ValueError:
                    print("Invalid input. Defaulting to General Knowledge.")
                    self.category = 9
                
                print("\nDifficulties: easy, medium, hard")
                self.difficulty = input("Choose a difficulty: ").lower()
                if self.difficulty not in ['easy', 'medium', 'hard']:
                    print("Invalid input. Defaulting to easy.")
                    self.difficulty = 'easy'
                
                try:
                    self.amount = int(input("How many questions do you want to play? "))
                except ValueError:
                    print("Invalid input. Defaulting to 10 questions.")
                    self.amount = 10
                
                questions = self.fetch_questions()
                if questions:
                    # Funktion för att starta själva spelet efter användarens inputs
                    self.play_game(questions)
                else:
                    # I fall om det inte kunde laddas in några frågor
                    print("Could not load questions. Please try again later.")
            
            elif choice == '2':
                # Om spelaren väljer "quit"
                print("Thank you for playing! Goodbye!")
                break
            
            else:
                # Om spelaren inte väljer 1 eller 2
                print("Invalid choice. Please select again.")

if __name__ == "__main__":
    game = JeopardyGame()
    game.main_menu()
