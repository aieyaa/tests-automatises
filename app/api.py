from flask import Blueprint, jsonify, request, current_app
from app.calculator import Calculator
from app.database import Database

api_bp = Blueprint('api', __name__, url_prefix='/api')
calculator = Calculator()
db = None

@api_bp.before_request
def before_request():
    """Initialise la connexion à la base de données avant chaque requête."""
    global db
    if db is None:
        db = Database(current_app.config.get('DATABASE', ':memory:'))
        db.connect()

@api_bp.teardown_request
def teardown_request(exception):
    """Ferme la connexion à la base de données après chaque requête."""
    global db
    if db is not None:
        db.disconnect()

@api_bp.route('/test', methods=['GET'])
def test():
    """Endpoint de test pour vérifier que le blueprint fonctionne."""
    return jsonify({'status': 'API fonctionne correctement'})

# Modification ici - utilisation de string au lieu de float
@api_bp.route('/add/<a>/<b>', methods=['GET'])
def add(a, b):
    """Endpoint pour additionner deux nombres."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.add(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les paramètres doivent être des nombres'}), 400

# Même modification pour les autres opérations
@api_bp.route('/subtract/<a>/<b>', methods=['GET'])
def subtract(a, b):
    """Endpoint pour soustraire b de a."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.subtract(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les paramètres doivent être des nombres'}), 400

@api_bp.route('/multiply/<a>/<b>', methods=['GET'])
def multiply(a, b):
    """Endpoint pour multiplier deux nombres."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.multiply(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les paramètres doivent être des nombres'}), 400

@api_bp.route('/divide/<a>/<b>', methods=['GET'])
def divide(a, b):
    """Endpoint pour diviser a par b."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.divide(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les paramètres doivent être des nombres'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Division par zéro impossible'}), 400

# Le reste du code reste inchangé
@api_bp.route('/user', methods=['POST'])
def add_user():
    """Endpoint pour ajouter un utilisateur."""
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Les champs username et email sont requis'}), 400
    
    success = db.add_user(data['username'], data['email'])
    if success:
        return jsonify({'message': 'Utilisateur ajouté avec succès'}), 201
    else:
        return jsonify({'error': 'Cet utilisateur existe déjà'}), 409

@api_bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    """Endpoint pour récupérer un utilisateur par son nom d'utilisateur."""
    user = db.get_user(username)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

@api_bp.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    """Endpoint pour supprimer un utilisateur."""
    success = db.delete_user(username)
    if success:
        return jsonify({'message': 'Utilisateur supprimé avec succès'})
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

@api_bp.route('/power/<a>/<b>', methods=['GET']) 
def power(a, b):
    """Endpoint pour calculer a^b."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.power(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les parametres doivent etre des nombres'}), 400

@api_bp.route('/sqrt/<a>', methods=['GET']) 
def sqrt(a):
    """Endpoint pour calculer la racine carrée de a."""
    try:
        a_float = float(a)
        result = calculator.sqrt(a_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Le parametre doit etre un nombre positif'}), 400 

@api_bp.route('/modulo/<a>/<b>', methods=['GET']) 
def modulo(a, b):
    """Endpoint pour calculer le reste de la division de a par b."""
    try:
        a_float = float(a)
        b_float = float(b)
        result = calculator.modulo(a_float, b_float)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Les parametres doivent etre des nombres'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Division par zero impossible'}), 400
