import sys
import os
# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client
from config import Config

app = Flask(__name__, static_folder='../static', static_url_path='')
app.config.from_object(Config)

supabase: Client = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# Personas
@app.route('/api/persons', methods=['GET'])
def get_persons():
    response = supabase.table('persons')\
        .select('*, groups(code, group_name)') \
        .eq('esta_activo', True) \
        .execute()
    persons = []
    for p in response.data:
        persons.append({
            'code': p['code'],
            'names': p['names'],
            'last_names': p['last_names'],
            'email': p['email'],
            'cellphone': p['cellphone'],
            'address': p['address'],
            'observations': p['observations'],
            'photograph': p['photograph'],
            'esta_activo': p['esta_activo'],
            'group_id': p['group_id'],
            'group_name': p['groups']['group_name'] if p.get('groups') else None
        })
    return jsonify(persons)

@app.route('/api/persons', methods=['POST'])
def create_person():
    data = request.json
    # Verificar grupo
    group_check = supabase.table('groups').select('code').eq('code', data['group_id']).execute()
    if not group_check.data:
        return jsonify({'error': 'Grupo no existe'}), 400
    new_person = {
        'names': data['names'],
        'last_names': data['last_names'],
        'email': data['email'],
        'cellphone': data.get('cellphone', ''),
        'address': data.get('address', ''),
        'observations': data.get('observations', ''),
        'photograph': data.get('photograph', ''),
        'esta_activo': data.get('esta_activo', True),
        'group_id': data['group_id']
    }
    result = supabase.table('persons').insert(new_person).execute()
    return jsonify({'code': result.data[0]['code']}), 201

@app.route('/api/persons/<uuid:code>', methods=['GET'])
def get_person(code):
    response = supabase.table('persons').select('*').eq('code', str(code)).execute()
    if not response.data:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(response.data[0])

@app.route('/api/persons/<uuid:code>', methods=['PUT'])
def update_person(code):
    data = request.json
    update_data = {}
    for field in ['names', 'last_names', 'email', 'cellphone', 'address', 'observations', 'photograph', 'esta_activo', 'group_id']:
        if field in data:
            update_data[field] = data[field]
    supabase.table('persons').update(update_data).eq('code', str(code)).execute()
    return jsonify({'message': 'Actualizado'})

@app.route('/api/persons/<uuid:code>', methods=['DELETE'])
def delete_person(code):
    supabase.table('persons').update({'esta_activo': False}).eq('code', str(code)).execute()
    return jsonify({'message': 'Eliminado'})

# Grupos
@app.route('/api/groups', methods=['GET'])
def get_groups():
    response = supabase.table('groups').select('*').eq('esta_activo', True).execute()
    return jsonify(response.data)

@app.route('/api/groups', methods=['POST'])
def create_group():
    data = request.json
    new_group = {
        'group_name': data['group_name'],  # Cambiado de 'group' a 'group_name'
        'esta_activo': data.get('esta_activo', True)
    }
    result = supabase.table('groups').insert(new_group).execute()
    return jsonify({'code': result.data[0]['code']}), 201

@app.route('/api/groups/<uuid:code>', methods=['GET'])
def get_group(code):
    response = supabase.table('groups').select('*').eq('code', str(code)).execute()
    if not response.data:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(response.data[0])

@app.route('/api/groups/<uuid:code>', methods=['PUT'])
def update_group(code):
    data = request.json
    update_data = {}
    if 'group_name' in data:
        update_data['group_name'] = data['group_name']
    if 'esta_activo' in data:
        update_data['esta_activo'] = data['esta_activo']
    supabase.table('groups').update(update_data).eq('code', str(code)).execute()
    return jsonify({'message': 'Actualizado'})

@app.route('/api/groups/<uuid:code>', methods=['DELETE'])
def delete_group(code):
    supabase.table('groups').update({'esta_activo': False}).eq('code', str(code)).execute()
    return jsonify({'message': 'Eliminado'})

if __name__ == '__main__':
    app.run(debug=True)