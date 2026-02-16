from flask import Blueprint, request, jsonify
from Services.Service_IA import Service_IA

prediction_blueprint = Blueprint('prediction', __name__)

@prediction_blueprint.route('/predict', methods=['POST'])
def predict():

    question = request.json['user_question']
    user_id = request.json['user_id']
    chat_id = request.json['chat_id']
    user_is_connected = request.json['user_is_connected']
    file_content = request.json['file_content']
    have_file = request.json['have_file']
    model = request.json['model_selected']

    try:
        ia = Service_IA()
        predictions = ia.generate_responses(question, user_id, chat_id, user_is_connected, file_content, have_file, model)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    return jsonify(predictions)
