from flask import Blueprint, jsonify

api = Blueprint('api', __name__, template_folder="templates")

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': "API is working!"})