# algorithm.py
from app import db, Question
from datetime import datetime, timedelta

class AdaptiveLearningAlgorithm:
    """
    Intelligenter Algorithmus für adaptive Lernfragen-Auswahl.
    
    Priorität-Score = (wrong_count * 2.0) + (days_since_asked * 0.5) - (success_rate * 3.0)
    
    - Fragen die oft falsch beantwortet werden: höhere Priorität
    - Lange nicht gestellte Fragen: höhere Priorität
    - Fragen mit hoher Erfolgsquote: niedrigere Priorität
    """
    
    @staticmethod
    def calculate_priority_score(question):
        """Berechnet Prioritäts-Score für eine Frage"""
        
        # Fehler-Count
        wrong_count = question.times_asked - question.times_correct
        
        # Success-Rate
        success_rate = 0.0
        if question.times_asked > 0:
            success_rate = question.times_correct / question.times_asked
        
        # Tage seit letzter Abfrage
        # Falls noch nie gefragt: 999 Tage (höchste Priorität!)
        if question.times_asked == 0:
            days_since_asked = 999
        else:
            # Hier könnte man last_asked timestamp tracken
            # Für jetzt: einfach times_asked als Proxy verwenden
            days_since_asked = min(question.times_asked, 7)  # Max 7 Tage Bonus
        
        # Priority Score Formel
        priority_score = (wrong_count * 2.0) + (days_since_asked * 0.5) - (success_rate * 3.0)
        
        return priority_score
    
    @staticmethod
    def select_next_question(exclude_question_ids=None, difficulty_filter=None):
        """
        Wählt die nächste Frage basierend auf Priorität.
        
        Strategie:
        - 70% höchster Priorität (Fragen die Hilfe brauchen)
        - 30% zufällig (Abwechslung)
        
        Args:
            exclude_question_ids: Liste von question_ids zum Ausschließen
            difficulty_filter: Optional Difficulty-Level (1-5)
        
        Returns:
            Question object oder None
        """
        import random
        
        # Query aufbauen
        query = Question.query
        
        if exclude_question_ids:
            query = query.filter(~Question.id.in_(exclude_question_ids))
        
        if difficulty_filter:
            query = query.filter(Question.difficulty == difficulty_filter)
        
        questions = query.all()
        
        if not questions:
            return None
        
        # Prioritäts-Score für alle Fragen berechnen
        scored_questions = [
            (q, AdaptiveLearningAlgorithm.calculate_priority_score(q))
            for q in questions
        ]
        
        # Sortieren nach Score (höher = wichtiger)
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        
        # 70% wahrscheinlich: Top-Priority Frage
        if random.random() < 0.7:
            # Wähle aus Top 30% der Fragen
            top_third = max(1, len(scored_questions) // 3)
            return random.choice(scored_questions[:top_third])[0]
        else:
            # 30% wahrscheinlich: Zufällige Frage
            return random.choice(questions)
    
    @staticmethod
    def get_question_stats(question_id):
        """Gibt Statistiken einer Frage zurück"""
        question = Question.query.get(question_id)
        
        if not question:
            return None
        
        success_rate = 0.0
        if question.times_asked > 0:
            success_rate = question.times_correct / question.times_asked
        
        return {
            'question_id': question.id,
            'text': question.text,
            'difficulty': question.difficulty,
            'times_asked': question.times_asked,
            'times_correct': question.times_correct,
            'success_rate': round(success_rate, 2),
            'priority_score': round(AdaptiveLearningAlgorithm.calculate_priority_score(question), 2)
        }