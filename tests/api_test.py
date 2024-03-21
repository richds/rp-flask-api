import pytest
import requests
import json
import sys


platform = sys.platform
print ("this is the platform: "+ platform)

if "darwin" in platform:
    base_url = 'http://127.0.0.1:8000'
else:
    #base_url = 'http://172.17.0.3:8000'
    base_url = 'http://0.0.0.0:8000'

#base_url = "http://127.0.0.1:8000"
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
        "fname": "Great",
        "lname": "Pumpkin"
    }
    r = requests.post(url=people_url.rstrip("/"), headers=headers, json=new_person)
    assert r.status_code == 201, r.text
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200
    items_to_check = (new_person["fname"], new_person["lname"])
    for item in items_to_check:
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


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
        "fname": "Greg",
        "lname": "Bunny"
    }
    r = requests.put(url=people_url + myguy["lname"], headers=headers, json=myguy)
    assert r.status_code == 201, r.text
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200
    items_to_check = ("Greg", "Bunny")
    for item in items_to_check:
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


def test_delete_person():
    to_delete = {
        "fname": "Great",
        "lname": "Pumpkin"
    }
    r = requests.delete(url=people_url + to_delete["lname"], headers=headers)
    assert r.status_code == 200, r.reason
    r = requests.get(people_url + to_delete["lname"])
    assert r.status_code == 404


def test_get_notes():
    r = requests.get(people_url.rstrip("/"))
    assert r.status_code == 200, r.text
    items_to_check = ("No need to hide the eggs this time.",
                        "Really! Only good deeds from now on!",
                        "I brush my teeth after each meal.")
    for item in items_to_check: 
        assert item in r.text, item + " not found in return string: " + pretty_print_json(r.text)


def test_update_note():
    note_id = "4"
    my_url = note_url + note_id
    content = {"content": "this is a new note"}
    r = requests.put(url=my_url, headers=headers, json=content)
    assert r.status_code == 201, r.text
    r = requests.get(my_url)
    assert r.status_code == 200
    y = requests.get(people_url.rstrip("/"))
    assert "this is a new note" in y.text, "expected string not in: \n" + y.text

@pytest.fixture()
def new_note_fix(request):
    new_note = {
        "content": "This guy gets it.",
        "person_id": 3
    }
    r = requests.post(url=note_url.rstrip("/"), headers=headers, json=new_note)
    assert r.status_code == 201, r.text
    print("This is the new note: " + r.text)
    yield json.loads(r.text)


def test_check_new_note(new_note_fix):
    r = requests.get(people_url + "Bunny")
    assert r.status_code == 200, r.text
    assert new_note_fix["content"] in r.text, "String should be in " + r.text


def test_delete_new_note(new_note_fix):
    note_to_delete = new_note_fix["id"]
    r = requests.delete(url=note_url + str(note_to_delete), headers=headers)
    assert r.status_code == 204, r.text
    r = requests.get(note_url +  str(note_to_delete), headers=headers)
    assert r.status_code == 404, r.text

