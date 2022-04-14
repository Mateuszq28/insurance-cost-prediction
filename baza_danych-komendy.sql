sqlite3 cost_base.db

--array with all collected data written in easy to read way
CREATE TABLE data_not_formatted (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_zapisu DATE,
    wzrost INTEGER,
    waga FLOAT,
    wiek INTEGER,
    plec VARCHAR(6),
    bmi FLOAT,
    dzieci INTEGER,
    palenie VARCHAR(3),
    region VARCHAR(20),
    koszty_ground_true FLOAT);

--array with all collected data written in one-hot-encoding way
CREATE TABLE data_formatted (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_written DATE,
    height INTEGER,
    b_weight FLOAT,
    age INTEGER,
    is_man BOOLEAN, --one_hot_encoding
    bmi FLOAT,
    children INTEGER,
    is_smoking BOOLEAN, --one_hot_encoding
    is_southwest BOOLEAN, --one_hot_encoding
    is_southeast BOOLEAN, --one_hot_encoding
    is_northwest BOOLEAN, --one_hot_encoding
    is_northeast BOOLEAN, --one_hot_encoding
    expenses_ground_true FLOAT);

--array with only data that is used in classifier
CREATE TABLE data_classifier_input (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    is_man BOOLEAN, --one_hot_encoding
    bmi FLOAT,
    children INTEGER,
    is_smoking BOOLEAN, --one_hot_encoding
    is_southwest BOOLEAN, --one_hot_encoding
    is_southeast BOOLEAN, --one_hot_encoding
    is_northwest BOOLEAN, --one_hot_encoding
    is_northeast BOOLEAN, --one_hot_encoding
    expenses_ground_true FLOAT);


INSERT INTO data_not_formatted (data_zapisu, wzrost, waga, wiek, plec, bmi,
    dzieci, palenie, region, koszty_ground_true)
    VALUES (2022-01-16, 178, 66.5, 23, "male", 20.93,
    0, true, "northeast", null);

INSERT INTO data_formatted (date_written, height, b_weight, age, is_man, bmi,
    children, is_smoking, is_southwest, is_southeast, is_northwest,
    is_northeast, expenses_ground_true)
    VALUES (2022-01-16, 178, 66.5, 23, true, 20.93,
    0, true, false, false, false,
    true, null);

INSERT INTO data_classifier_input (age, is_man, bmi,
    children, is_smoking, is_southwest, is_southeast, is_northwest,
    is_northeast, expenses_ground_true)
    VALUES (23, true, 20.93,
    0, true, false, false, false,
    true, null);

SELECT * FROM data_not_formatted;
SELECT * FROM data_formatted;
SELECT * FROM data_classifier_input;

DELETE FROM data_not_formatted;
DELETE FROM data_formatted;
DELETE FROM data_classifier_input;
