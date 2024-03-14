import pytest
import requests
import json


base_url = "http://127.0.0.1:8000"
api_url = base_url + "/api/"
people_url = api_url + "people/"
note_url = api_url + "notes/"
mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
    }

character_list = [
    {"lname": "Fairy", "fname": "Tooth", "notes": "I brush my teeth after each meal."},
    {"lname": "Ruprecht", "fname": "Knecht", "notes": "I swear, I'll do better this year."},
    {"lname": "Bunny", "fname": "Easter", "notes": "Please keep the current inflation rate in mind!"}
]

def pretty_print_json(input_string):
    json_dict = json.loads(input_string)
    return json.dumps(json_dict, indent=4)


def test_hello_world():
    r = requests.get(base_url)
    assert r.status_code == 200
    assert "Hello, People!" in r.text


def test_get_people():
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200
    items_to_check = ("Tooth", "Fairy", "Knecht", "timestamp")
    for item in items_to_check: 
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


def test_create_person():
    new_person = {
        "fname": "Art",
        "lname": "Vandelay"
    }
    r = requests.post(url=people_url.rstrip("/"), headers=headers, json=new_person)
    assert r.status_code == 201, r.text
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200
    items_to_check = ("Art", "Vandelay")
    for item in items_to_check:
        assert item in r.text, item + " not found in return string: " +pretty_print_json(r.text)


def test_get_single_person():
    myguy = {
        "fname": "Tooth",
        "lname": "Fairy"
    }
    r = requests.get(people_url + myguy["lname"])
    assert r.status_code == 200, r.text
    items_to_check = ("Tooth", "Fairy")
    for item in items_to_check:
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


def test_get_person_x():
    for guy in character_list:
        r = requests.get(people_url + guy["lname"])
        assert r.status_code == 200
        items_to_check = (guy["lname"], guy["fname"], guy["notes"])
        for item in items_to_check:
            assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text) 


def test_update_person():
    myguy = {
        "fname": "Barry",
        "lname": "Bunny"
    }
    r = requests.put(url=people_url + myguy["lname"], headers=headers, json=myguy)
    assert r.status_code == 201, r.text
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200
    items_to_check = ("Barry", "Bunny")
    for item in items_to_check:
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


def test_delete_person():
    to_delete = {
        "fname": "Art",
        "lname": "Vandelay"
    }
    r = requests.delete(url=people_url + to_delete["lname"], headers=headers)
    assert r.status_code == 200, r.reason
    r = requests.get(people_url + to_delete["lname"])
    assert r.status_code == 404
