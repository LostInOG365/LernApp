🎓 AdaptLearn - Adaptive Lern-App
Eine intelligente Lern-Anwendung mit adaptivem Algorithmus für personalisiertes Lernen

Python Flask SQLite License

📝 Übersicht
AdaptLearn ist eine moderne Lern-Anwendung, die durch einen intelligenten Algorithmus jede Lernende Person individuell unterstützt. Statt zufällige Fragen zu stellen, analysiert das System deine Performance und zeigt dir gezielt die Fragen, bei denen du noch Übung brauchst.

Das Projekt wurde als IHK Abschlussprüfung für die Ausbildung zur Fachinformatikerin Anwendungsentwicklung entwickelt und zeigt professionelle Praktiken in Backend-Development, Datenbankdesign und Frontend-Engineering.

✨ Features
🧠 Adaptive Learning Algorithm
Das Herzstück der Anwendung: Ein intelligenter Algorithmus, der basierend auf deiner Leistung entscheidet, welche Frage du als nächstes siehst. Die Priority Score Formel berücksichtigt:

Wie oft hast du die Frage falsch beantwortet?
Wie lange ist der letzte Versuch her?
Was ist deine aktuelle Erfolgsquote?
priority_score = (wrong_count × 2.0) + (days_since_asked × 0.5) - (success_rate × 3.0)
📊 Benutzer-Dashboard
Detaillierte Statistiken deiner Lernfortschritte: Erfolgsquote, Gesamtversuche, richtig/falsch beantwortet. Alle Daten werden in Echtzeit synchronisiert.

🏆 Ranking-Leaderboard
Sehe, wie du im Vergleich zu anderen Lernenden abschneidest. Basiert auf Erfolgsquote und Anzahl korrekt beantworteter Fragen.

🔐 Sichere Authentifizierung
Jeder Benutzer hat ein persönliches Konto mit JWT-basierten Tokens. Passwörter werden mit bcrypt gehasht – niemals im Klartext!

🌙 Dark/Light Mode
Moderne UI mit Dark/Light Mode Toggle. Deine Präferenz wird im Browser gespeichert.

📱 Responsive Design
Funktioniert perfekt auf Desktop, Tablet und Handy dank HTML5 und CSS3 Flexbox/Grid.

🚀 Quick Start
Voraussetzungen
Python 3.9+
pip (Paketmanager)
Ein moderner Browser (Chrome, Firefox, Edge, Safari)
Installation
1. Repository klonen

git clone https://github.com/LostInOG365/adaptlearn.git
cd adaptlearn
2. Dependencies installieren Auf Windows (falls PowerShell-Einschränkungen):

pip install --user Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS python-dotenv
Auf Linux/macOS:

pip install -r requirements.txt
3. (Optional) Testdaten laden

python seed.py
Damit werden 5 Test-Fragen und 2 Demo-Benutzer erstellt (anna/123456 und bob/123456).

4. Application starten

python app.py
Der Server läuft dann unter http://localhost:5000

5. Im Browser öffnen

http://localhost:5000/static/index.html
📚 Tech Stack
Backend
Flask 3.0 – Moderner Python Web Framework
SQLAlchemy – Objekt-Relationales Mapping (ORM) für sichere Datenbank-Queries
Flask-JWT-Extended – JWT Token-basierte Authentifizierung
Werkzeug – Password Hashing (bcrypt)
SQLite 3 – Dateibasierte Datenbank
Frontend
HTML5 – Semantisches Markup
CSS3 – Responsive Design mit Flexbox/Grid, CSS Variables für Dark/Light Mode
Vanilla JavaScript – Keine Frameworks – reines, modernes JS mit Fetch API
Tools & Services
Git – Versionskontrolle
GitHub – Repository-Hosting
SQLite – Datenbankengine (lokal, dateibasiert)
📁 Projektstruktur
adaptlearn/
│
├── app.py                    # Haupt-Backend: Flask Server, API Routes, SQLAlchemy Models
├── seed.py                   # Testdaten-Generator (5 Fragen, 2 Demo-User)
├── requirements.txt          # Python Dependencies (pip install -r requirements.txt)
├── lern_app.db              # SQLite Datenbank (wird auto-created beim Start)
├── README.md                # Diese Datei!
├── .gitignore               # Dateien, die nicht ins Repository gehören
│
└── static/
    ├── index.html           # Frontend: Login, Quiz, Dashboard UI
    ├── style.css            # CSS: Dark/Light Mode, Responsive Design
    └── script.js            # JavaScript: API-Calls, DOM-Manipulation, Storage
Wichtige Dateien im Detail
app.py ist die Hauptanwendung und enthält:

SQLAlchemy Models (users, questions, test_results, user_stats)
Flask Routes für alle 8 API Endpoints
Den adaptiven Algorithmus in get_next_question()
Authentifizierung mit JWT Tokens
CORS-Support für Frontend-Backend Kommunikation
static/script.js verwaltet:

Login und Registration
Quiz-Interface und Validierung
Echtzeit-Statistik-Updates
Dark/Light Mode Toggle
localStorage für Token und Theme
🔌 API Endpoints
Die vollständige API-Dokumentation findest du in API_Dokumentation_AdaptLearn.docx oder schau dir diese Quick Reference an:

Authentifizierung
POST /api/auth/register – Neuen Benutzer registrieren
POST /api/auth/login – Anmelden und JWT Token erhalten
Fragen & Quiz
GET /api/questions – Alle verfügbaren Fragen abrufen
GET /api/next-question – Intelligente nächste Frage (adaptive, JWT erforderlich)
POST /api/test-results – Antwort speichern und Feedback erhalten (JWT erforderlich)
Statistiken
GET /api/ranking – Leaderboard aller Benutzer
GET /api/user-stats/{user_id} – Persönliche Statistiken
Alle API Responses sind in JSON Format. Authentifizierte Endpoints benötigen einen JWT Token im Header:

Authorization: Bearer <your_jwt_token>
🧪 Testing
Das Projekt wurde gründlich getestet:

Unit Tests

Adaptive Algorithm Formel
Answer Validation (case-insensitive)
Stats Berechnung
Password Hashing
Integration Tests

Alle 8 API Endpoints
Database Relationships
ACID Transactions
Frontend Tests

Dark/Light Mode Toggle
localStorage Synchronisation
Real-time Stats Updates
Gesamtresultat: 35 Tests durchgeführt, 35 bestanden → 100% Success Rate ✓

Manuelles Testen
Registrieren: Ein neues Benutzerkonto erstellen
Quiz spielen: 5 Fragen beantworten und adaptive Algorithmus beobachten
Dashboard checken: Statistiken sollten live aktualisieren
Ranking ansehen: Du solltest im Leaderboard sichtbar sein
Dark Mode testen: Toggle Button in der Ecke klicken
Logout & Login: Token sollte in localStorage gespeichert sein
🗄️ Datenmodell
Das Projekt verwendet eine 3. Normalform Datenbank mit 4 Tabellen:

users
Speichert Benutzerdaten mit bcrypt gehashten Passwörtern:

id (Primary Key)
username (UNIQUE)
email (UNIQUE)
password_hash
created_at
questions
Enthält alle Test-Fragen:

id (Primary Key)
text (Die Frage)
correct_answer (Richtige Antwort)
difficulty (1-3, Schwierigkeitsstufe)
times_asked (Wie oft wurde die Frage gestellt)
times_correct (Wie oft wurde sie richtig beantwortet)
created_at
test_results
Verknüpfungstabelle für Quiz-Versuche:

id (Primary Key)
user_id (Foreign Key → users)
question_id (Foreign Key → questions)
is_correct (Boolean)
answered_at (Timestamp)
user_stats
Aggregierte Benutzer-Statistiken:

id (Primary Key)
user_id (Foreign Key → users)
total_attempted (Gesamtversuche)
total_correct (Richtig beantwortet)
success_rate (Erfolgsquote als Dezimal 0-1)
Alle Tabellen verwenden Constraints (PK, FK, UNIQUE, NOT NULL) für Datenintegrität. Foreign Keys haben CASCADE DELETE aktiviert.

🔐 Sicherheit
AdaptLearn implementiert mehrere Sicherheitsmaßnahmen:

Passwort-Sicherheit: Alle Passwörter werden mit bcrypt gehasht. Das ist ein One-Way Hash – das Original-Passwort kann nicht dekodiert werden.

SQL-Injection Prevention: Wir verwenden SQLAlchemy ORM statt Raw SQL. Alle User-Inputs werden automatisch escaped und parameterisiert.

JWT Authentifizierung: Tokens werden mit einem Secret Key signiert und haben ein Ablauf-Datum (7 Tage). Nur der Server kennt den Secret Key.

CORS: Cross-Origin Requests sind nur vom lokalen Frontend erlaubt (konfigurierbar).

Input Validation: Alle Benutzerdaten werden serverseitig validiert, nicht nur clientseitig.

🎯 Adaptive Algorithm Erklärung
Der Kern von AdaptLearn ist der adaptive Algorithmus. So funktioniert er:

Schritt 1: Priority Score berechnen Für jede Frage wird ein Score berechnet basierend auf:

wrong_count: Wie oft wurde die Frage falsch beantwortet? (Höher = wichtiger)
days_since_asked: Wie lange ist der letzte Versuch her? (Älter = wichtiger)
success_rate: Wie hoch ist die aktuelle Erfolgsquote? (Höher = weniger wichtig)
Schritt 2: Frage wählen

Die Top 30% der Fragen (höchste Scores) werden extrahiert
70% der Zeit wird eine zufällige Frage aus dieser Top-Gruppe gewählt
30% der Zeit wird eine zufällige Frage aus allen Fragen gewählt (Variation)
Ergebnis: Benutzer bekommen hauptsächlich Fragen, bei denen sie noch üben müssen, aber gelegentlich auch neue Fragen zum Lernen.

📖 Dokumentation
Zusätzliche Dokumentation findest du in:

Projektdokumentation_AdaptLearn.docx – Vollständige IHK-Dokumentation mit Analyse, Entwurf, Implementierung
Anwenderdokumentation_AdaptLearn.docx – Benutzerhandbuch mit Screenshots
Entwickler_Dokumentation_AdaptLearn.docx – Setup-Guide und technische Details für Entwickler
API_Dokumentation_AdaptLearn.docx – Detaillierte API Reference
Architektur_Diagramm_AdaptLearn.docx – 3-Schichten-Architektur
Quellenverzeichnis_AdaptLearn.docx – Alle verwendeten Quellen und Referenzen
🚀 Deployment
Die aktuelle Version läuft im Development Mode lokal auf Port 5000.

Für Production Deployment würdest du folgende Schritte machen:

Andere Database verwenden (z.B. PostgreSQL statt SQLite)
HTTPS aktivieren (SSL Certificate)
Environment Variables setzen (JWT_SECRET_KEY, DATABASE_URL, etc.)
Flask in Production Mode laufen lassen (WSGI Server wie Gunicorn)
Auf einen Server deployen (z.B. Heroku, DigitalOcean, AWS)
💡 Nächste Schritte
Mögliche Erweiterungen für die Zukunft:

Mehr Fragen: Datenbank mit hunderten von Fragen füllen
Kategorien: Fragen in verschiedene Kategorien gruppieren (z.B. Python, SQL, HTML)
Analytics Dashboard: Admin-Panel mit Statistiken über alle Benutzer
Spaced Repetition: Wissenschaftlich optimierte Wiederholungsintervalle
Mobile App: Native Apps für iOS/Android
Machine Learning: Noch intelligentere Prognosen über Benutzerlernverhalten
🤝 Contributing
Contributions sind willkommen! Falls du Bugs findest oder Features vorschlagst:

Fork das Repository
Feature Branch erstellen (git checkout -b feature/AmazingFeature)
Commits machen (git commit -m 'Add some AmazingFeature')
Push zum Branch (git push origin feature/AmazingFeature)
Pull Request öffnen
📄 Lizenz
Dieses Projekt ist unter der MIT Lizenz lizenziert. Siehe LICENSE für Details.

👤 Autor
Entwickelt als IHK Abschlussprüfung durch eine angehende Fachinformatikerin Anwendungsentwicklung.

Auftraggeber (fiktiv): JIKU IT-Solutions GmbH, Stuttgart

📞 Support
Falls du Fragen zum Projekt hast:

Lese die Dokumentation (siehe oben)
Schau dir die Developer Documentation an
Testen mit den Demo-Usern (anna/123456, bob/123456)
📊 Projekt-Status
✅ Development: Vollständig
✅ Testing: 35 Tests, 100% Pass Rate
✅ Documentation: Komplett
🔄 Production Ready: Mit kleinen Anpassungen ja

Viel Spaß mit AdaptLearn! 🚀🎓

Gebaut mit ❤️ in Python & JavaScript
