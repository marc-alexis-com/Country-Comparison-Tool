from flask import Flask, render_template, request
import requests
import re
import sys
import csv
import os
from datetime import datetime, timedelta

# Chemin vers le fichier CSV local
CSV_FILE = 'countries_data.csv'

app = Flask(__name__)

def fetch_countries_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()
        countries_data = []
        for country in countries:
            name = country.get('name', {}).get('common', 'Unknown')
            population = country.get('population', None)
            area = country.get('area', None)
            countries_data.append({
                'name': name,
                'population': population,
                'area': area
            })
        return countries_data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données des pays : {e}")
        sys.exit(1)

def save_to_csv(countries):
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'population', 'area'])
            writer.writeheader()
            for country in countries:
                writer.writerow({
                    'name': country['name'],
                    'population': country['population'],
                    'area': country['area']
                })
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données dans le CSV : {e}")

def load_from_csv():
    countries = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country = {
                    'name': row['name'],
                    'population': int(float(row['population'])) if row['population'] else None,
                    'area': float(row['area']) if row['area'] else None
                }
                countries.append(country)
            return countries
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Erreur lors du chargement des données depuis le CSV : {e}")
        return []

def is_csv_fresh():
    if not os.path.exists(CSV_FILE):
        return False
    file_time = datetime.fromtimestamp(os.path.getmtime(CSV_FILE))
    if datetime.now() - file_time < timedelta(days=180):  # 6 mois
        return True
    return False

def calculate_percentage(target, actual):
    if target == 0 or target is None or actual is None:
        return None
    difference = abs(target - actual)
    percentage = (1 - (difference / target)) * 100
    return round(percentage, 2)

def find_top_n_closest(countries, target, key, top_n=3):
    if target is None:
        return []
    valid_countries = [country for country in countries if country.get(key) is not None]
    sorted_countries = sorted(valid_countries, key=lambda x: abs(x[key] - target))
    top_countries = sorted_countries[:top_n]
    results = []
    for country in top_countries:
        percentage = calculate_percentage(target, country[key])
        results.append({
            'name': country['name'],
            key: country[key],
            'percentage': percentage
        })
    return results

def format_number(number):
    if number is None:
        return "Not available"
    return f"{number:,}".replace(',', ' ')

def convert_to_number(value_str, unit):
    try:
        number = float(value_str)
        unit = unit.lower()
        if unit == 'thousand':
            return int(number * 1_000)
        elif unit == 'million':
            return int(number * 1_000_000)
        elif unit == 'billion':
            return int(number * 1_000_000_000)
        else:
            return int(number)
    except ValueError:
        return None

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_pop = request.form.get('population')
        pop_unit = request.form.get('pop_unit')
        input_area = request.form.get('area')
        area_unit = request.form.get('area_unit')

        target_pop = convert_to_number(input_pop, pop_unit) if input_pop else None
        target_area = convert_to_number(input_area, area_unit) if input_area else None

        # Chargement des données
        if is_csv_fresh():
            countries = load_from_csv()
            if not countries:
                countries = fetch_countries_data()
                save_to_csv(countries)
        else:
            countries = fetch_countries_data()
            save_to_csv(countries)

        # Comparaisons
        pop_results = find_top_n_closest(countries, target_pop, 'population') if target_pop else []
        area_results = find_top_n_closest(countries, target_area, 'area') if target_area else []

        return render_template('results.html',
                               active_page='home',
                               input_pop=input_pop,
                               input_area=input_area,
                               pop_unit=pop_unit,
                               area_unit=area_unit,
                               target_pop=target_pop,
                               target_area=target_area,
                               pop_results=pop_results,
                               area_results=area_results,
                               format_number=format_number)
    else:
        return render_template('index.html', active_page='home')

# Route for the documentation page
@app.route('/documentation')
def documentation():
    return render_template('documentation.html', active_page='documentation')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

if __name__ == '__main__':
    app.run(debug=False)