import requests

ENDPOINT = "http://127.0.0.1:5000"

#happy path
def test_movies_are_displayed():  #1
    response = requests.get(ENDPOINT + "/movies")
    assert response.status_code == 200

#happy path
def test_users_saved_database(): #2
    payload = {               
        "name": "test",
        "last_name": "test",
        "pasword": "test",
        "email": "test",
        "phone_number": 1       
    }
    response = requests.post(ENDPOINT + "/registration", json=payload)
    assert response.status_code == 200

#happy path
def test_authenticates_user_and_returns_token(): #3
    payload = {
        "email": "rafagalindo@gmail.com",
        "pasword": "32681"       
    }
    response = requests.post(ENDPOINT + "/autentication", json=payload)
    assert response.status_code == 200

#happy path
def test_save_tickets_database(): #4
    payload = {
        "id": 9999,
        "id_movie": "200",
        "id_seat": "101"    
    }
    response = requests.post(ENDPOINT + "/shoping", json=payload)
    assert response.status_code == 200

#happy path
def test_check_tikets_list(): #5
    response = requests.get(ENDPOINT + "/checkTickets")
    assert response.status_code == 200

#happy path
def test_delete_tikets_shoping(): #6

     payload = {
        "id": 9999999,
        "id_movie": "200",
        "id_seat": "991341991"    
    }
     requests.post(ENDPOINT + "/shoping", json=payload)

     response = requests.delete(ENDPOINT + "/cancelTicket/9999999")
     assert response.status_code == 200