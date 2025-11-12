from flask import Flask, render_template, request, redirect, url_for, flash

API="https://pokeapi.co/api/v2/pokemon/"

import requests

app = Flask (__name__)

app.secret_key = 'TU_CLAVE_SECRETA_AQUI'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_pokemon():
    pokemon_name=request.form.get('pokemon_name','').strip().lower()#En el pokemon_name va a ir el nombre que le pusimos al id por ejmplo id=nombre
    if not pokemon_name:
        flash('Por favor,ingresa un nombre de pokemon','error')
    return redirect(url_for('index'))
try:
    resp = requests.get(f"{API}{pokemon_name}")
    if resp.status_code == 200:
        pokemon_data = resp.json()
        return render_template('pokemon_html',pokemon = pokemon_data)
    else:
        flash(f'Pokémon"{pokemon_name}"no encontrado','error')
        return redirect(url_for('index'))
except requests.exceptions.RequestException as e:
    flash('Error al buscar el Pokemon','error')
    return redirect (url_for('index'))
