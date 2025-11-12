from flask import Flask, render_template, request, redirect, url_for, flash

import requests

app = Flask (__name__)

app.secret_key = 'TU_CLAVE_SECRETA_AQUI'

API="https://pokeapi.co/api/v2/pokemon/"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_pokemon():
    
    pokemon_name=request.form.get('pokemon_name','').strip().lower() #En el pokemon_name va a ir el nombre que le pusimos al id por ejmplo id=nombre, lower minuscula, strip quita espacios
    if not pokemon_name:
        flash('Por favor,ingresa un nombre de pokemon','error')
    return redirect(url_for('index'))

try:#atrapa errores y hace que siga la ejecucion del programa
    
    resp = requests.get(f"{API}{pokemon_name}")
    if resp.status_code == 200:
        pokemon_data = resp.json()
        
        pokemon_info ={
            'name' : pokemon_data['name'].title(),
            'id' : pokemon_data['id'],
            'height' : pokemon_data['height']/10,#convierte a metros
            'weight' : pokemon_data['weight']/10,#convierte a kg
            'image' : pokemon_data['sprites']['front_default'],
            'types' : [t['type']['name'].tittle()for t in pokemon_data['types']],
            'abilities' : [a['ability']['name'].title()for a in pokemon_data['abilities']]
        }
        
        return render_template('pokemon_html',pokemon = pokemon_info)
    
    else:
        
        flash(f'Pokémon"{pokemon_name}"no encontrado','error')
        
        return redirect(url_for('index'))
    
except requests.exceptions.RequestException as e:
    
    flash('Error al buscar el Pokemon','error')
    
    return redirect (url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
