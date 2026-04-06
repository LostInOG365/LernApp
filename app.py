# app.py - Komplette Lern-App Backend
import os
import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS

# ========================
# APP SETUP
# ========================

app = Flask(__name__)
CORS(app)

# SQLite Datenbank konfigurieren
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lern_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========================
# DATABASE MODELS
# ========================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.Integer, default=1)  # 1-5
    times_asked = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.id}>'


class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestResult user={self.user_id} q={self.question_id}>'


class UserStats(db.Model):
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_attempted = db.Column(db.Integer, default=0)
    total_correct = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=0.0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserStats user={self.user_id}>'


# ========================
# ADAPTIVE LEARNING ALGORITHM
# ========================

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
        if question.times_asked == 0:
            days_since_asked = 999
        else:
            days_since_asked = min(question.times_asked, 7)
        
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
        """
        
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


# ========================
# TEST ROUTES
# ========================

@app.route('/', methods=['GET'])
def home():
    return {'message': 'Lern-App Backend läuft! 🚀'}


@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok', 'database': 'SQLite'}


# ========================
# API ENDPOINTS - QUESTIONS
# ========================

@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    """Alle Fragen zurückgeben"""
    questions = Question.query.all()
    return {
        'count': len(questions),
        'questions': [
            {
                'id': q.id,
                'text': q.text,
                'difficulty': q.difficulty,
                'times_asked': q.times_asked,
                'times_correct': q.times_correct
            }
            for q in questions
        ]
    }


@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Eine spezifische Frage zurückgeben"""
    question = Question.query.get(question_id)
    
    if not question:
        return {'error': 'Frage nicht gefunden'}, 404
    
    return {
        'id': question.id,
        'text': question.text,
        'difficulty': question.difficulty,
        'correct_answer': question.correct_answer,
        'times_asked': question.times_asked,
        'times_correct': question.times_correct
    }


# ========================
# API ENDPOINTS - TEST RESULTS
# ========================

@app.route('/api/test-results', methods=['POST'])
def submit_test_result():
    """Test-Ergebnis speichern - Backend vergleicht die Antwort!"""
    
    data = request.get_json()
    
    # Validierung
    if not data or 'user_id' not in data or 'question_id' not in data or 'user_answer' not in data:
        return {'error': 'user_id, question_id und user_answer erforderlich'}, 400
    
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    
    # Existieren User und Question?
    user = User.query.get(user_id)
    question = Question.query.get(question_id)
    
    if not user or not question:
        return {'error': 'User oder Frage nicht gefunden'}, 404
    
    # VERGLEICH AUF DEM BACKEND!
    is_correct = user_answer.lower() == question.correct_answer.lower()
    
    # Test Result speichern
    result = TestResult(
        user_id=user_id,
        question_id=question_id,
        is_correct=is_correct
    )
    db.session.add(result)
    
    # Question-Stats updaten
    question.times_asked += 1
    if is_correct:
        question.times_correct += 1
    
    # User-Stats updaten
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    if user_stats:
        user_stats.total_attempted += 1
        if is_correct:
            user_stats.total_correct += 1
        user_stats.success_rate = user_stats.total_correct / user_stats.total_attempted
        user_stats.last_activity = datetime.utcnow()
    
    db.session.commit()
    
    return {
        'message': 'Ergebnis gespeichert!',
        'correct': is_correct,
        'correct_answer': question.correct_answer,  # ← Nur wenn NACH dem Vergleich!
        'success_rate': user_stats.success_rate if user_stats else 0
    }, 201


# ========================
# API ENDPOINTS - RANKING
# ========================

@app.route('/api/ranking', methods=['GET'])
def get_ranking():
    """Ranking aller User nach Erfolgsquote"""
    stats = UserStats.query.order_by(UserStats.success_rate.desc()).all()
    
    ranking = []
    for idx, stat in enumerate(stats, 1):
        user = User.query.get(stat.user_id)
        ranking.append({
            'rank': idx,
            'username': user.username,
            'success_rate': stat.success_rate,
            'total_attempted': stat.total_attempted,
            'total_correct': stat.total_correct
        })
    
    return {'ranking': ranking}


# ========================
# API ENDPOINTS - ADAPTIVE ALGORITHM
# ========================

@app.route('/api/next-question', methods=['GET'])
def get_next_adaptive_question():
    """
    Gibt die nächste adaptiv ausgewählte Frage zurück.
    Der Algorithmus wählt basierend auf:
    - Häufigkeit falscher Antworten
    - Tage seit letzter Abfrage
    - Success-Rate
    """
    
    difficulty = request.args.get('difficulty', type=int)
    
    # Nächste Frage wählen
    question = AdaptiveLearningAlgorithm.select_next_question(
        difficulty_filter=difficulty
    )
    
    if not question:
        return {'error': 'Keine Fragen verfügbar'}, 404
    
    return {
        'id': question.id,
        'text': question.text,
        'difficulty': question.difficulty,
        'times_asked': question.times_asked,
        'times_correct': question.times_correct
    }


@app.route('/api/question-stats/<int:question_id>', methods=['GET'])
def get_question_stats_endpoint(question_id):
    """
    Gibt Statistiken und Prioritäts-Score einer Frage zurück.
    Zeigt an, wie dringend diese Frage benötigt wird!
    """
    stats = AdaptiveLearningAlgorithm.get_question_stats(question_id)
    
    if not stats:
        return {'error': 'Frage nicht gefunden'}, 404
    
    return stats


@app.route('/api/algorithm-debug', methods=['GET'])
def debug_algorithm():
    """
    DEBUG: Zeigt Priority-Score aller Fragen (für die Dokumentation!)
    """
    questions = Question.query.all()
    
    debug_data = []
    for q in questions:
        score = AdaptiveLearningAlgorithm.calculate_priority_score(q)
        success_rate = q.times_correct / q.times_asked if q.times_asked > 0 else 0
        
        debug_data.append({
            'question_id': q.id,
            'text': q.text[:50] + '...' if len(q.text) > 50 else q.text,
            'times_asked': q.times_asked,
            'times_correct': q.times_correct,
            'success_rate': round(success_rate, 2),
            'priority_score': round(score, 2)
        })
    
    # Sortiert nach Priorität
    debug_data.sort(key=lambda x: x['priority_score'], reverse=True)
    
    return {
        'algorithm': 'Adaptive Learning Algorithm',
        'formula': 'priority_score = (wrong_count * 2.0) + (days_since_asked * 0.5) - (success_rate * 3.0)',
        'strategy': '70% highest priority, 30% random',
        'questions_ranked_by_priority': debug_data
    }


# ========================
# START
# ========================
# ========================
# JWT CONFIG
# ========================

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app.config['JWT_SECRET_KEY'] = 'dein-super-geheimer-schluessel-aendere-mich-in-produktion'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)


# ========================
# API ENDPOINTS - AUTH
# ========================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Neuen User registrieren"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return {'error': 'username, email und password erforderlich'}, 400
    
    # Prüfe ob User schon existiert
    if User.query.filter_by(username=data['username']).first():
        return {'error': 'Username existiert bereits'}, 409
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email existiert bereits'}, 409
    
    # Neuen User erstellen
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    # User Stats für neuen User erstellen
    user_stats = UserStats(user_id=user.id)
    db.session.add(user_stats)
    db.session.commit()
    
    # Token generieren
    access_token = create_access_token(identity=user.id)
    
    return {
        'message': 'User erfolgreich registriert!',
        'user_id': user.id,
        'username': user.username,
        'access_token': access_token
    }, 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User einloggen"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return {'error': 'username und password erforderlich'}, 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return {'error': 'Falscher Username oder Password'}, 401
    
    # Token generieren
    access_token = create_access_token(identity=str(user.id))
    
    return {
        'message': 'Login erfolgreich!',
        'user_id': user.id,
        'username': user.username,
        'access_token': access_token
    }, 200


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Zeigt aktuellen User (braucht JWT Token!)"""
    from flask_jwt_extended import decode_token
    
    # Token aus Header holen
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return {'error': 'Kein Token gefunden'}, 401
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
    except Exception as e:
        return {'error': 'Ungültiger Token: ' + str(e)}, 401
    
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User nicht gefunden'}, 404
    
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    
    return {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'stats': {
            'total_attempted': user_stats.total_attempted if user_stats else 0,
            'total_correct': user_stats.total_correct if user_stats else 0,
            'success_rate': round(user_stats.success_rate, 2) if user_stats else 0
        }
    }
@app.route('/api/user-stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    """Gibt Stats eines Users zurück (ohne JWT!)"""
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    
    if not user_stats:
        return {'stats': {'total_attempted': 0, 'total_correct': 0, 'success_rate': 0}}
    
    return {
        'stats': {
            'total_attempted': user_stats.total_attempted,
            'total_correct': user_stats.total_correct,
            'success_rate': round(user_stats.success_rate, 2)
        }
    }
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Datenbank initialisiert!")
    
    app.run(debug=True, port=5000)