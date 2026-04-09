from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_cors import CORS
from config import Config
from models import db, Customer, Question, QuestionOption, Response, Result, PERSONALITY_TYPES
from collections import Counter
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Routes
@app.route('/')
def index():
    """Main quiz page"""
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions and their options"""
    questions = Question.query.order_by(Question.order).all()
    
    questions_data = []
    for q in questions:
        options_data = []
        for opt in q.options:
            options_data.append({
                'id': opt.id,
                'text': opt.text
            })
        
        questions_data.append({
            'id': q.id,
            'text': q.text,
            'order': q.order,
            'options': options_data
        })
    
    return jsonify(questions_data)

@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz responses and calculate result"""
    data = request.json
    
    # Validate data
    if not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    if not data.get('responses'):
        return jsonify({'error': 'Respostas são obrigatórias'}), 400
    
    try:
        # Create customer
        customer = Customer(
            name=data['name'],
            email=data.get('email'),
            whatsapp=data.get('whatsapp'),
            birthday=data.get('birthday')
        )
        db.session.add(customer)
        db.session.flush()  # Get customer ID
        
        # Store responses and count personality types
        personality_scores = Counter()
        
        for resp in data['responses']:
            option = QuestionOption.query.get(resp['option_id'])
            if not option:
                continue
            
            response = Response(
                customer_id=customer.id,
                question_id=resp['question_id'],
                option_id=resp['option_id']
            )
            db.session.add(response)
            
            # Count points for each personality type
            personality_scores[option.personality_type] += option.points
        
        # Determine the dominant personality type
        if personality_scores:
            dominant_type = personality_scores.most_common(1)[0][0]
        else:
            dominant_type = "zen"  # Default
        
        # Get personality info
        personality_info = PERSONALITY_TYPES.get(dominant_type, PERSONALITY_TYPES["zen"])
        
        # Store result
        result = Result(
            customer_id=customer.id,
            personality_type=dominant_type,
            description=personality_info['description']
        )
        db.session.add(result)
        
        # Commit all changes
        db.session.commit()
        
        # Return result
        return jsonify({
            'success': True,
            'result': {
                'type': dominant_type,
                'name': personality_info['name'],
                'emoji': personality_info['emoji'],
                'description': personality_info['description'],
                'phrase': personality_info['phrase'],
                'color': personality_info['color']
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': 'Erro ao processar respostas'}), 500

@app.route('/admin')
def admin():
    """Admin dashboard to view responses"""
    return render_template('admin.html')

@app.route('/brinde')
def brinde():
    """Brinde (gift) redemption page"""
    return render_template('brinde.html')

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """Get statistics for admin dashboard"""
    total_responses = Customer.query.count()
    
    # Count personality types
    personality_counts = {}
    for result in Result.query.all():
        ptype = result.personality_type
        personality_counts[ptype] = personality_counts.get(ptype, 0) + 1
    
    # Get recent customers
    recent_customers = []
    customers = Customer.query.order_by(Customer.created_at.desc()).limit(50).all()
    
    for customer in customers:
        result = Result.query.filter_by(customer_id=customer.id).first()
        recent_customers.append({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'whatsapp': customer.whatsapp,
            'birthday': customer.birthday,
            'created_at': customer.created_at.strftime('%d/%m/%Y %H:%M'),
            'personality_type': PERSONALITY_TYPES[result.personality_type]['name'] if result else 'N/A'
        })
    
    return jsonify({
        'total_responses': total_responses,
        'personality_counts': personality_counts,
        'personality_types': PERSONALITY_TYPES,
        'recent_customers': recent_customers
    })

@app.route('/api/admin/export', methods=['GET'])
def export_data():
    """Export all data as JSON"""
    customers = Customer.query.all()
    data = []
    
    for customer in customers:
        result = Result.query.filter_by(customer_id=customer.id).first()
        responses = Response.query.filter_by(customer_id=customer.id).all()
        
        response_details = []
        for resp in responses:
            response_details.append({
                'question': resp.question.text,
                'answer': resp.option.text
            })
        
        data.append({
            'name': customer.name,
            'email': customer.email,
            'whatsapp': customer.whatsapp,
            'birthday': customer.birthday,
            'date': customer.created_at.strftime('%d/%m/%Y %H:%M'),
            'personality_type': PERSONALITY_TYPES[result.personality_type]['name'] if result else 'N/A',
            'responses': response_details
        })
    
    return jsonify(data)


@app.route('/api/admin/export/excel', methods=['GET'])
def export_data_excel():
    """Export all data as Excel (.xlsx)"""
    customers = Customer.query.order_by(Customer.created_at.desc()).all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Respostas'

    headers = [
        'Nome',
        'E-mail',
        'WhatsApp',
        'Aniversario',
        'Data',
        'Tipo de Personalidade',
        'Respostas'
    ]
    worksheet.append(headers)

    for customer in customers:
        result = Result.query.filter_by(customer_id=customer.id).first()
        responses = Response.query.filter_by(customer_id=customer.id).all()

        answers_text = ' | '.join(
            f"{resp.question.text}: {resp.option.text}" for resp in responses
        )

        worksheet.append([
            customer.name,
            customer.email or '',
            customer.whatsapp or '',
            customer.birthday or '',
            customer.created_at.strftime('%d/%m/%Y %H:%M'),
            PERSONALITY_TYPES[result.personality_type]['name'] if result else 'N/A',
            answers_text
        ])

    worksheet.column_dimensions['A'].width = 24
    worksheet.column_dimensions['B'].width = 28
    worksheet.column_dimensions['C'].width = 18
    worksheet.column_dimensions['D'].width = 16
    worksheet.column_dimensions['E'].width = 18
    worksheet.column_dimensions['F'].width = 28
    worksheet.column_dimensions['G'].width = 80

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    filename = f"natforms-export-{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
