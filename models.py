from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    """Store customer information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to responses
    responses = db.relationship('Response', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Question(db.Model):
    """Store quiz questions"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    
    # Relationship to options
    options = db.relationship('QuestionOption', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}: {self.text[:30]}>'

class QuestionOption(db.Model):
    """Store possible answers for each question"""
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    personality_type = db.Column(db.String(50), nullable=False)  # Which personality type this answer contributes to
    points = db.Column(db.Integer, default=1)  # Weight for scoring
    
    def __repr__(self):
        return f'<Option {self.id} for Q{self.question_id}>'

class Response(db.Model):
    """Store customer responses to the quiz"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('question_option.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    question = db.relationship('Question', backref='responses')
    option = db.relationship('QuestionOption', backref='responses')
    
    def __repr__(self):
        return f'<Response Customer{self.customer_id} Q{self.question_id}>'

class Result(db.Model):
    """Store final quiz results"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    personality_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    customer = db.relationship('Customer', backref='results')
    
    def __repr__(self):
        return f'<Result {self.personality_type} for Customer{self.customer_id}>'

# Personality types and their descriptions
PERSONALITY_TYPES = {
    "zen": {
        "name": "A ZEN QUE RESOLVE",
        "emoji": "✨",
        "description": "você é o eixo no meio do caos\norganiza, acalma e dá direção\n\ntem um poder silencioso:\nfazer tudo voltar pro lugar",
        "phrase": "calma, a gente resolve",
        "color": "#98D8C8"
    },
    "soltinha": {
        "name": "A SOLTINHA DO BOM HUMOR",
        "emoji": "🌈",
        "description": "você transforma o dia de qualquer pessoa\nleve, espontânea e impossível de ignorar\n\ncom você, a vida respira",
        "phrase": "vamos rir disso?",
        "color": "#F7B731"
    },
    "loba": {
        "name": "A LOBA",
        "emoji": "🔥",
        "description": "você não precisa falar alto pra marcar presença\nintensa, profunda e magnética\n\nvive tudo de verdade e transforma",
        "phrase": "ela não fala muito… mas marca tudo",
        "color": "#C44569"
    },
    "vamo": {
        "name": "A DO 'VAMO?'",
        "emoji": "💥",
        "description": "você puxa, decide, movimenta\né energia de ação\n\ncom você, as coisas saem do lugar",
        "phrase": "confia em mim e vem",
        "color": "#FF6B9D"
    },
    "pra_vida_toda": {
        "name": "A PRA VIDA TODA",
        "emoji": "🤍",
        "description": "você é presença constante\nhistória, vínculo, profundidade\n\nquem tem você… tem base",
        "phrase": "eu tô aqui",
        "color": "#9B59B6"
    }
}
