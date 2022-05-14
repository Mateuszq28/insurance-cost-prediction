from flask import Flask
from datetime import datetime
from datetime import date
from flask import jsonify
from flask import request
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import io
import base64
import sqlite3
from currency_converter import CurrencyConverter
import joblib
import sklearn

app = Flask(__name__)


def load_model(path):
    #model = tf.keras.models.load_model(path)
    model = load('model.joblib') 
    return model

@app.route('/')
def main():
    return homepage()

@app.route('/cost')
def homepage():
    with open("static/cost.html", encoding="utf-8") as f:
        message_json = f.read()
    return message_json

def addToDataBase_not_formatted(today_date, height, weight, age, sex, bmi, children, smoking, region, expenses):
    try:
        # łączenie z bazą danych
        sqliteConnection = sqlite3.connect('cost_base.db')
        cursor = sqliteConnection.cursor()
        print("Nawiązano połączenie z bazą danych!")
        # dodanie danych do tabeli
        sqlite_insert_query = '''INSERT INTO data_not_formatted (data_zapisu, wzrost, waga, wiek, plec, bmi,
                                 dzieci, palenie, region, koszty_ground_true) VALUES (
                                 {0}, {1}, {2}, {3}, '{4}', {5}, {6}, '{7}', '{8}', {9})'''.format(
                                 today_date, height, weight, age, sex, bmi, children, smoking, region, expenses)
                                         
        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Poprawnie dodano dane do tabeli. Liczba dodanych wierszy: ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Błąd poczas odczytywania danych z tabeli:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Zakończono połączenie z bazą danych!")

def addToDataBase_formatted(today_date, height, weight, age, is_man, bmi, children, is_smoking, is_region_north, is_region_east, expenses):
    try:
        # łączenie z bazą danych
        sqliteConnection = sqlite3.connect('cost_base.db')
        cursor = sqliteConnection.cursor()
        print("Nawiązano połączenie z bazą danych!")
        # dodanie danych do tabeli
        sqlite_insert_query = '''INSERT INTO data_formatted (date_written, height, b_weight, age, is_woman, bmi,
                                 children, is_smoking, is_region_north, is_region_east, expenses_ground_true) VALUES (
                                 {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})'''.format(
                                 today_date, height, weight, age, is_man, bmi, children, is_smoking, is_region_north, is_region_east, expenses)

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Poprawnie dodano dane do tabeli. Liczba dodanych wierszy: ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Błąd poczas odczytywania danych z tabeli:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Zakończono połączenie z bazą danych!")

def addToDataBase_classifier_input(age, is_man, bmi, children, is_smoking, is_region_north, is_region_east, expenses):
    try:
        # łączenie z bazą danych
        sqliteConnection = sqlite3.connect('cost_base.db')
        cursor = sqliteConnection.cursor()
        print("Nawiązano połączenie z bazą danych!")
        # dodanie danych do tabeli
        sqlite_insert_query = '''INSERT INTO data_formatted (age, is_woman, bmi,
                                 children, is_smoking, is_region_north, is_region_east, expenses_ground_true) VALUES (
                                 {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'''.format(
                                 age, is_man, bmi, children, is_smoking, is_region_north, is_region_east, expenses)

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Poprawnie dodano dane do tabeli. Liczba dodanych wierszy: ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Błąd poczas odczytywania danych z tabeli:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Zakończono połączenie z bazą danych!")

@app.route('/calculate', methods=['POST'])
def calculate_cost():
    message = request.get_json(force=True)
    height = int(message['height'])
    weight = float(message['weight'])
    today_date = message['today_date']
    children = int(message['kids'])
    sex = message['sex']
    smoking = message['smoking']
    age = int(message['age'])
    region = message['race']
    expenses = message['expenses']
    if expenses != "":
        expenses = float(expenses)
    else:
        expenses = "null"

    bmi = weight/(height/100)**2

    addToDataBase_not_formatted(today_date, height, weight, age, sex, bmi, children, smoking, region, expenses)

    is_woman = int(sex == "female")
    is_smoking = int(smoking == "yes")
    is_region_north = int(region == "northwest" or region == "northeast")
    is_region_east = int(region == "southeast" or region == "northeast")

    addToDataBase_formatted(today_date, height, weight, age, is_woman, bmi, children, is_smoking, is_region_north, is_region_east, expenses)
    addToDataBase_classifier_input(age, is_woman, bmi, children, is_smoking, is_region_north, is_region_east, expenses)

    input_vector = [age, is_woman, bmi, children, is_smoking, is_region_north, is_region_east]
    sc = joblib.load("scaler")
    model = joblib.load('cost_predictor')
    input_vector_sc = sc.transform([input_vector])
    expenses_d = round(model.predict(input_vector_sc)[0], 2)
    print(expenses_d)
    c = CurrencyConverter()
    dolar_price = c.convert(1, 'USD', 'PLN')
    expenses_pln = round(dolar_price*expenses_d, 2)

    result_message = {
        "expenses_d": str(expenses_d),
        "expenses_pln": str(expenses_pln),
        "dolar_price": str(round(dolar_price, 2))
    }
    print("wysyłanie")
    print(expenses_d)
    print(expenses_pln)
    print(dolar_price)

    response = jsonify(result_message)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()
    
