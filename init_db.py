from app import app, db
from models import Question, QuestionOption

def init_database():
    """Initialize the database with sample questions"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if questions already exist
        if Question.query.first():
            print("Database already initialized!")
            return
        
        # Sample questions - These will be replaced with actual questions
        sample_questions = [
            {
                "text": "Quando tudo sai do controle, você:",
                "options": [
                    {"text": "respira fundo e pensa \"ok, vamos organizar isso\"", "type": "zen"},
                    {"text": "manda áudio rindo: \"amiga, você não vai acreditar\"", "type": "soltinha"},
                    {"text": "some um pouco, sente tudo… e depois volta diferente", "type": "loba"},
                    {"text": "resolve na hora, sem muita conversa", "type": "vamo"},
                    {"text": "chama aquela pessoa que sempre te entende", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Seu áudio no WhatsApp geralmente é:",
                "options": [
                    {"text": "calmo e explicativo", "type": "zen"},
                    {"text": "caótico e engraçado", "type": "soltinha"},
                    {"text": "curto, mas profundo", "type": "loba"},
                    {"text": "direto: \"faz isso e pronto\"", "type": "vamo"},
                    {"text": "longo, íntimo e cheio de detalhes", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Num encontro de amigas, você é:",
                "options": [
                    {"text": "a que equilibra tudo", "type": "zen"},
                    {"text": "a que anima até quem não queria ir", "type": "soltinha"},
                    {"text": "a que observa mais do que fala", "type": "loba"},
                    {"text": "a que decide pra onde todo mundo vai", "type": "vamo"},
                    {"text": "a que segura o grupo", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Seu estilo é mais:",
                "options": [
                    {"text": "clássico com personalidade", "type": "zen"},
                    {"text": "leve e divertido", "type": "soltinha"},
                    {"text": "marcante sem esforço", "type": "loba"},
                    {"text": "ousado e prático", "type": "vamo"},
                    {"text": "confortável com significado", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Quando você ama uma peça, é porque:",
                "options": [
                    {"text": "vai usar muito", "type": "zen"},
                    {"text": "ela é linda e te deixa feliz", "type": "soltinha"},
                    {"text": "ela tem presença", "type": "loba"},
                    {"text": "funciona em mil ocasiões", "type": "vamo"},
                    {"text": "tem história", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Seu maior super-poder na vida é:",
                "options": [
                    {"text": "organizar o caos", "type": "zen"},
                    {"text": "melhorar qualquer clima", "type": "soltinha"},
                    {"text": "transformar o que sente", "type": "loba"},
                    {"text": "fazer acontecer", "type": "vamo"},
                    {"text": "cuidar das relações", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "As pessoas sempre te dizem:",
                "options": [
                    {"text": "\"você me acalma\"", "type": "zen"},
                    {"text": "\"amo sua energia\"", "type": "soltinha"},
                    {"text": "\"você é forte de um jeito diferente\"", "type": "loba"},
                    {"text": "\"você resolve tudo\"", "type": "vamo"},
                    {"text": "\"você é essencial na minha vida\"", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Quando você some, é porque:",
                "options": [
                    {"text": "tá se reorganizando", "type": "zen"},
                    {"text": "tá vivendo e esqueceu o celular", "type": "soltinha"},
                    {"text": "tá processando tudo internamente", "type": "loba"},
                    {"text": "tá resolvendo mil coisas", "type": "vamo"},
                    {"text": "tá no seu cantinho seguro", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Seu tipo de compra é:",
                "options": [
                    {"text": "pensada", "type": "zen"},
                    {"text": "emocional (e feliz)", "type": "soltinha"},
                    {"text": "quando faz MUITO sentido", "type": "loba"},
                    {"text": "prática", "type": "vamo"},
                    {"text": "afetiva", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "Uma frase que poderia ser sua:",
                "options": [
                    {"text": "\"calma, a gente resolve\"", "type": "zen"},
                    {"text": "\"vamos rir disso?\"", "type": "soltinha"},
                    {"text": "\"eu sinto tudo… e transformo\"", "type": "loba"},
                    {"text": "\"bora?\"", "type": "vamo"},
                    {"text": "\"tô aqui\"", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "O que mais te encanta numa marca?",
                "options": [
                    {"text": "consistência", "type": "zen"},
                    {"text": "leveza", "type": "soltinha"},
                    {"text": "identidade forte", "type": "loba"},
                    {"text": "funcionalidade", "type": "vamo"},
                    {"text": "propósito", "type": "pra_vida_toda"}
                ]
            },
            {
                "text": "No fundo, você sabe que:",
                "options": [
                    {"text": "segura muita coisa", "type": "zen"},
                    {"text": "ilumina muita gente", "type": "soltinha"},
                    {"text": "sente mais do que mostra", "type": "loba"},
                    {"text": "puxa muita coisa pra frente", "type": "vamo"},
                    {"text": "sustenta muita história", "type": "pra_vida_toda"}
                ]
            }
        ]
        
        # Add questions to database
        for i, q_data in enumerate(sample_questions, 1):
            question = Question(text=q_data["text"], order=i)
            db.session.add(question)
            db.session.flush()  # Get question ID
            
            for opt_data in q_data["options"]:
                option = QuestionOption(
                    question_id=question.id,
                    text=opt_data["text"],
                    personality_type=opt_data["type"],
                    points=1
                )
                db.session.add(option)
        
        db.session.commit()
        print("Database initialized successfully!")
        print(f"Added {len(sample_questions)} questions")

if __name__ == '__main__':
    init_database()
