# seed.py
from app import app, db, User, Question, TestResult, UserStats
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_database():
    """Füllt die Datenbank mit Testdaten"""
    
    with app.app_context():
        # Alles löschen (nur für Testing!)
        db.drop_all()
        db.create_all()
        print("🗑️  Datenbank geleert und neu erstellt!")
        
        # ========================
        # USERS erstellen
        # ========================
        user1 = User(
            username='anna',
            email='anna@example.com',
            password_hash=generate_password_hash('123456')
        )
        user2 = User(
            username='bob',
            email='bob@example.com',
            password_hash=generate_password_hash('123456')
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        print("✅ 2 Users erstellt!")
        
        # ========================
        # QUESTIONS erstellen
        # ========================
        questions = [
            Question(
                text="Was ist ein Algorithmus?",
                correct_answer="Eine Folge von Schritten zur Lösung eines Problems",
                difficulty=1
            ),
            Question(
                text="Was bedeutet CRUD?",
                correct_answer="Create, Read, Update, Delete",
                difficulty=2
            ),
            Question(
                text="Welche Datenstruktur ist LIFO?",
                correct_answer="Stack",
                difficulty=2
            ),
            Question(
                text="Was ist eine API?",
                correct_answer="Application Programming Interface",
                difficulty=1
            ),
            Question(
                text="Wie heißt die Zeitkomplexität von Binary Search?",
                correct_answer="O(log n)",
                difficulty=3
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()
        print("✅ 5 Fragen erstellt!")
        
        # ========================
        # USER STATS erstellen
        # ========================
        stats1 = UserStats(user_id=user1.id, total_attempted=10, total_correct=7, success_rate=0.7)
        stats2 = UserStats(user_id=user2.id, total_attempted=5, total_correct=3, success_rate=0.6)
        db.session.add(stats1)
        db.session.add(stats2)
        db.session.commit()
        print("✅ User-Statistiken erstellt!")
        
        # ========================
        # TEST RESULTS erstellen
        # ========================
        result1 = TestResult(user_id=user1.id, question_id=1, is_correct=True)
        result2 = TestResult(user_id=user1.id, question_id=2, is_correct=False)
        result3 = TestResult(user_id=user2.id, question_id=1, is_correct=True)
        db.session.add_all([result1, result2, result3])
        db.session.commit()
        print("✅ Test-Ergebnisse erstellt!")
        
        print("\n🎉 DATENBANK ERFOLGREICH GEFÜLLT!")
        print("   Users: anna, bob (Passwort: 123456)")
        print("   Questions: 5")
        print("   TestResults: 3")

if __name__ == '__main__':
    seed_database()