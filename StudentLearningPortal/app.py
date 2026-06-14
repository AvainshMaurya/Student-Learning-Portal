"""
Student Learning Portal - Flask Backend Application
UN SDG 4: Quality Education
This application provides a platform for students to access educational resources,
video tutorials, quizzes, and study materials in one place.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize database
db = SQLAlchemy(app)

# ============ DATABASE MODELS ============

class User(db.Model):
    """User model for student registration and login"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(200), default='default.jpg')
    
    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True, cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='user', lazy=True, cascade='all, delete-orphan')

class StudyMaterial(db.Model):
    """Study Material model for storing educational content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Mathematics, Science, etc.
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)

class Video(db.Model):
    """Video Learning model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)  # YouTube or other video platform URL
    duration = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

class Quiz(db.Model):
    """Quiz model for online assessments"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    total_questions = db.Column(db.Integer, default=0)
    time_limit = db.Column(db.Integer)  # in minutes
    passing_score = db.Column(db.Float, default=60.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('QuizResult', backref='quiz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    """Question model for quiz questions"""
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    explanation = db.Column(db.Text)

class QuizResult(db.Model):
    """Quiz Result model for tracking student performance"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)  # in seconds
    answers = db.Column(db.Text)  # JSON format

class Feedback(db.Model):
    """Feedback model for user feedback and suggestions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Bug, Suggestion, etc.
    status = db.Column(db.String(20), default='Pending')  # Pending, Reviewed, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ============ AUTHENTICATION FUNCTIONS ============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ ROUTES ============

@app.route('/')
def index():
    """Home page - displays SDG 4 information and project introduction"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        # Validation
        if not all([username, email, password, full_name]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, full_name=full_name)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Student Dashboard - displays progress and quick links"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    # Get user statistics
    total_quizzes_taken = QuizResult.query.filter_by(user_id=user_id).count()
    total_quizzes_passed = QuizResult.query.filter_by(user_id=user_id, passed=True).count()
    avg_score = db.session.query(db.func.avg(QuizResult.percentage)).filter_by(user_id=user_id).scalar() or 0
    
    recent_results = QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.completed_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         user=user,
                         total_quizzes_taken=total_quizzes_taken,
                         total_quizzes_passed=total_quizzes_passed,
                         avg_score=round(avg_score, 2),
                         recent_results=recent_results)

@app.route('/study-materials')
def study_materials():
    """Study Materials Section"""
    category = request.args.get('category', 'All')
    search = request.args.get('search', '')
    
    query = StudyMaterial.query
    
    if category != 'All':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(StudyMaterial.title.ilike(f'%{search}%'))
    
    materials = query.all()
    categories = db.session.query(db.distinct(StudyMaterial.category)).all()
    
    return render_template('study_materials.html', materials=materials, categories=categories, current_category=category, search=search)

@app.route('/api/download-material/<int:material_id>')
@login_required
def download_material(material_id):
    """Download study material"""
    material = StudyMaterial.query.get(material_id)
    if not material:
        return jsonify({'success': False, 'message': 'Material not found'}), 404
    
    # Update download count
    material.downloads += 1
    db.session.commit()
    
    # For demo, create a text file
    content = f"{material.title}\n\n{material.content}"
    buffer = io.BytesIO(content.encode())
    
    return send_file(buffer, as_attachment=True, download_name=f"{material.title}.txt")

@app.route('/videos')
def videos():
    """Video Learning Section"""
    subject = request.args.get('subject', 'All')
    search = request.args.get('search', '')
    
    query = Video.query
    
    if subject != 'All':
        query = query.filter_by(subject=subject)
    
    if search:
        query = query.filter(Video.title.ilike(f'%{search}%'))
    
    videos = query.all()
    subjects = db.session.query(db.distinct(Video.subject)).all()
    
    return render_template('videos.html', videos=videos, subjects=subjects, current_subject=subject)

@app.route('/quizzes')
def quizzes():
    """Online Quiz Section"""
    subject = request.args.get('subject', 'All')
    
    query = Quiz.query
    
    if subject != 'All':
        query = query.filter_by(subject=subject)
    
    quizzes = query.all()
    subjects = db.session.query(db.distinct(Quiz.subject)).all()
    
    return render_template('quizzes.html', quizzes=quizzes, subjects=subjects, current_subject=subject)

@app.route('/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Take a quiz"""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for('quizzes'))
    
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/api/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    """Submit quiz answers"""
    user_id = session.get('user_id')
    data = request.get_json()
    
    quiz_id = data.get('quiz_id')
    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'success': False, 'message': 'Quiz not found'}), 404
    
    # Calculate score
    correct_count = 0
    total_questions = len(answers)
    
    for question_id, answer in answers.items():
        question = Question.query.get(question_id)
        if question and question.correct_answer == answer:
            correct_count += 1
    
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    passed = score >= quiz.passing_score
    
    # Save result
    result = QuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        score=correct_count,
        total_marks=total_questions,
        percentage=score,
        passed=passed,
        time_taken=time_taken,
        answers=json.dumps(answers)
    )
    
    db.session.add(result)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'score': correct_count,
        'total': total_questions,
        'percentage': round(score, 2),
        'passed': passed,
        'result_id': result.id
    }), 200

@app.route('/quiz-result/<int:result_id>')
@login_required
def quiz_result(result_id):
    """View quiz result"""
    result = QuizResult.query.get(result_id)
    if not result or result.user_id != session.get('user_id'):
        return redirect(url_for('dashboard'))
    
    return render_template('quiz_result.html', result=result)

@app.route('/api/generate-certificate/<int:result_id>')
@login_required
def generate_certificate(result_id):
    """Generate quiz certificate as PDF"""
    result = QuizResult.query.get(result_id)
    if not result or result.user_id != session.get('user_id'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    if not result.passed:
        return jsonify({'success': False, 'message': 'Certificate only available for passed quizzes'}), 400
    
    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add certificate content
    c.setFont("Helvetica-Bold", 28)
    c.drawString(100, height - 100, "Certificate of Achievement")
    
    c.setFont("Helvetica", 14)
    c.drawString(150, height - 150, f"This certifies that")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(130, height - 180, result.user.full_name)
    
    c.setFont("Helvetica", 14)
    c.drawString(100, height - 220, f"has successfully completed the quiz:")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 250, result.quiz.title)
    
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 290, f"Score: {result.percentage}%")
    c.drawString(100, height - 310, f"Date: {result.completed_at.strftime('%Y-%m-%d')}")
    
    c.drawString(100, height - 380, "Student Learning Portal")
    c.drawString(100, height - 410, "UN SDG 4: Quality Education")
    
    c.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"certificate_{result_id}.pdf", mimetype='application/pdf')

@app.route('/progress')
@login_required
def progress():
    """Progress Tracking Dashboard"""
    user_id = session.get('user_id')
    
    # Get all quiz results
    results = QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.completed_at).all()
    
    # Calculate statistics
    total_attempts = len(results)
    total_passed = sum(1 for r in results if r.passed)
    avg_score = sum(r.percentage for r in results) / total_attempts if total_attempts > 0 else 0
    
    return render_template('progress.html', 
                         results=results,
                         total_attempts=total_attempts,
                         total_passed=total_passed,
                         avg_score=round(avg_score, 2))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact/Feedback Form"""
    if request.method == 'POST':
        data = request.get_json()
        
        if 'user_id' in session:
            user_id = session.get('user_id')
        else:
            user_id = None
        
        feedback = Feedback(
            user_id=user_id,
            subject=data.get('subject'),
            message=data.get('message'),
            category=data.get('category')
        )
        
        try:
            db.session.add(feedback)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Thank you for your feedback!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Failed to submit feedback'}), 500
    
    return render_template('contact.html')

@app.route('/api/user-stats')
@login_required
def user_stats():
    """Get user statistics as JSON"""
    user_id = session.get('user_id')
    
    total_quizzes = QuizResult.query.filter_by(user_id=user_id).count()
    total_passed = QuizResult.query.filter_by(user_id=user_id, passed=True).count()
    avg_score = db.session.query(db.func.avg(QuizResult.percentage)).filter_by(user_id=user_id).scalar() or 0
    
    return jsonify({
        'total_quizzes': total_quizzes,
        'total_passed': total_passed,
        'avg_score': round(avg_score, 2)
    })

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# ============ DATABASE INITIALIZATION ============

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if User.query.first() is not None:
            return
        
        # Add sample users
        user1 = User(
            username='student1',
            email='student1@example.com',
            password=generate_password_hash('password123'),
            full_name='John Doe'
        )
        user2 = User(
            username='student2',
            email='student2@example.com',
            password=generate_password_hash('password123'),
            full_name='Jane Smith'
        )
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Add sample study materials
        materials = [
            StudyMaterial(
                title='Mathematics Fundamentals',
                description='Complete guide to mathematics basics',
                category='Mathematics',
                content='This comprehensive guide covers basic mathematics concepts including algebra, geometry, and trigonometry.',
                downloads=45,
                rating=4.5
            ),
            StudyMaterial(
                title='Physics Concepts',
                description='Understanding physics laws and principles',
                category='Science',
                content='Explore fundamental physics concepts, laws of motion, energy, and wave mechanics.',
                downloads=32,
                rating=4.8
            ),
            StudyMaterial(
                title='Chemistry Made Easy',
                description='Simplified chemistry notes',
                category='Science',
                content='Learn organic and inorganic chemistry with easy-to-understand explanations and examples.',
                downloads=28,
                rating=4.3
            ),
            StudyMaterial(
                title='English Literature',
                description='Classic literature analysis',
                category='Literature',
                content='Study classic English literature, authors, and literary devices with detailed analysis.',
                downloads=21,
                rating=4.6
            ),
            StudyMaterial(
                title='History and Civilization',
                description='World history timeline',
                category='History',
                content='Comprehensive overview of world history from ancient times to modern era.',
                downloads=18,
                rating=4.4
            )
        ]
        
        db.session.add_all(materials)
        db.session.commit()
        
        # Add sample videos
        videos = [
            Video(
                title='Introduction to Python',
                description='Learn Python programming basics',
                subject='Programming',
                video_url='https://www.youtube.com/embed/kqtD5dpn9C0',
                duration='10:30',
                views=1250
            ),
            Video(
                title='Web Development with HTML & CSS',
                description='Create responsive websites',
                subject='Web Development',
                video_url='https://www.youtube.com/embed/hu-q2zYwEYs',
                duration='15:45',
                views=856
            ),
            Video(
                title='Data Science Fundamentals',
                description='Introduction to data science',
                subject='Data Science',
                video_url='https://www.youtube.com/embed/ua-CiY1f7Po',
                duration='12:20',
                views=1100
            ),
            Video(
                title='Machine Learning Basics',
                description='Get started with ML',
                subject='AI & ML',
                video_url='https://www.youtube.com/embed/PeMlggyqfqQ',
                duration='14:00',
                views=945
            )
        ]
        
        db.session.add_all(videos)
        db.session.commit()
        
        # Add sample quizzes
        quiz1 = Quiz(
            title='Mathematics Quiz 1',
            description='Test your mathematics skills',
            subject='Mathematics',
            total_questions=5,
            time_limit=15,
            passing_score=60.0
        )
        
        quiz2 = Quiz(
            title='Science Fundamentals',
            description='Basic science concepts',
            subject='Science',
            total_questions=5,
            time_limit=20,
            passing_score=60.0
        )
        
        db.session.add_all([quiz1, quiz2])
        db.session.commit()
        
        # Add questions for quiz 1
        questions1 = [
            Question(
                quiz_id=quiz1.id,
                question_text='What is 15 × 3?',
                option_a='35', option_b='45', option_c='55', option_d='65',
                correct_answer='B',
                explanation='15 × 3 = 45'
            ),
            Question(
                quiz_id=quiz1.id,
                question_text='What is the square root of 144?',
                option_a='10', option_b='11', option_c='12', option_d='13',
                correct_answer='C',
                explanation='12 × 12 = 144'
            ),
            Question(
                quiz_id=quiz1.id,
                question_text='What is 25% of 200?',
                option_a='40', option_b='50', option_c='60', option_d='70',
                correct_answer='B',
                explanation='25% of 200 = (25/100) × 200 = 50'
            ),
            Question(
                quiz_id=quiz1.id,
                question_text='What is the value of π (approximately)?',
                option_a='2.14', option_b='3.14', option_c='4.14', option_d='5.14',
                correct_answer='B',
                explanation='π ≈ 3.14159'
            ),
            Question(
                quiz_id=quiz1.id,
                question_text='What is 7² (7 squared)?',
                option_a='42', option_b='49', option_c='56', option_d='63',
                correct_answer='B',
                explanation='7 × 7 = 49'
            )
        ]
        
        db.session.add_all(questions1)
        
        # Add questions for quiz 2
        questions2 = [
            Question(
                quiz_id=quiz2.id,
                question_text='What is the chemical symbol for gold?',
                option_a='Gd', option_b='Go', option_c='Au', option_d='Ag',
                correct_answer='C',
                explanation='Au is the chemical symbol for gold from Latin "aurum"'
            ),
            Question(
                quiz_id=quiz2.id,
                question_text='What is the speed of light?',
                option_a='150,000 km/s', option_b='200,000 km/s', option_c='300,000 km/s', option_d='350,000 km/s',
                correct_answer='C',
                explanation='The speed of light is approximately 300,000 km/s or 3×10⁸ m/s'
            ),
            Question(
                quiz_id=quiz2.id,
                question_text='What is the SI unit of force?',
                option_a='Joule', option_b='Newton', option_c='Pascal', option_d='Watt',
                correct_answer='B',
                explanation='Newton (N) is the SI unit of force'
            ),
            Question(
                quiz_id=quiz2.id,
                question_text='What is photosynthesis?',
                option_a='Breaking down of food', 
                option_b='Process of making food from sunlight',
                option_c='Respiration in plants',
                option_d='Digestion of nutrients',
                correct_answer='B',
                explanation='Photosynthesis is the process by which plants make their own food using sunlight'
            ),
            Question(
                quiz_id=quiz2.id,
                question_text='How many bones are in the human body?',
                option_a='186', option_b='206', option_c='226', option_d='246',
                correct_answer='B',
                explanation='An adult human has approximately 206 bones'
            )
        ]
        
        db.session.add_all(questions2)
        db.session.commit()
        
        print("Database initialized successfully!")

# ============ RUN APPLICATION ============

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
