import requests

BASE_URL = "http://127.0.0.1:8000/api"

def register_user(user_id, password, referred_by=0, language='en'):
    url = f"{BASE_URL}/register/"
    data = {"user_id": user_id, "password": password, "referred_by": referred_by, "language": language}
    response = requests.post(url, json=data)
    return response.json()

def get_token(user_id, password):
    url = f"{BASE_URL}/token/"
    data = {"user_id": user_id, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def refresh_token(refresh):
    url = f"{BASE_URL}/token/refresh/"
    data = {"refresh": refresh}
    response = requests.post(url, json=data)
    return response.json()

def list_users():
    url = f"{BASE_URL}/users/"
    response = requests.get(url)
    return response.json()

def get_user(user_id):
    url = f"{BASE_URL}/users/{user_id}/"
    response = requests.get(url)
    return response.json()

def update_user(user_id, balance=0, words=200, language='en', is_active=True):
    url = f"{BASE_URL}/users/{user_id}/"
    data = {"balance": balance, "words": words, "language": language, "is_active": is_active}
    response = requests.put(url, json=data)
    return response.json()

def patch_user(user_id, data):
    url = f"{BASE_URL}/users/{user_id}/"
    response = requests.patch(url, json=data)
    return response.json()

def delete_user(user_id):
    url = f"{BASE_URL}/users/{user_id}/"
    response = requests.delete(url)
    return response.json()

def list_subscriptions():
    url = f"{BASE_URL}/subscriptions/"
    response = requests.get(url)
    return response.json()

def create_subscription(user_id, sub_type='monthly'):
    url = f"{BASE_URL}/subscriptions/"
    data = {"user_id": user_id, "type": sub_type}
    response = requests.post(url, json=data)
    return response.json()

def get_subscription(sub_id):
    url = f"{BASE_URL}/subscriptions/{sub_id}/"
    response = requests.get(url)
    return response.json()

def update_subscription(sub_id, is_active=True):
    url = f"{BASE_URL}/subscriptions/{sub_id}/"
    data = {"is_active": is_active}
    response = requests.put(url, json=data)
    return response.json()

def delete_subscription(sub_id):
    url = f"{BASE_URL}/subscriptions/{sub_id}/"
    response = requests.delete(url)
    return response.json()

def list_topups():
    url = f"{BASE_URL}/topups/"
    response = requests.get(url)
    return response.json()

def create_topup(user_id, amount, status='pending'):
    url = f"{BASE_URL}/topups/"
    data = {"user_id": user_id, "amount": amount, "status": status}
    response = requests.post(url, json=data)
    return response.json()

def get_topup(topup_id):
    url = f"{BASE_URL}/topups/{topup_id}/"
    response = requests.get(url)
    return response.json()

def update_topup(topup_id, status='completed'):
    url = f"{BASE_URL}/topups/{topup_id}/"
    data = {"status": status}
    response = requests.put(url, json=data)
    return response.json()

def delete_topup(topup_id):
    url = f"{BASE_URL}/topups/{topup_id}/"
    response = requests.delete(url)
    return response.json()

def list_transactions():
    url = f"{BASE_URL}/transactions/"
    response = requests.get(url)
    return response.json()

def create_transaction(user_id, trans_type, amount):
    url = f"{BASE_URL}/transactions/"
    data = {"user_id": user_id, "type": trans_type, "amount": amount}
    response = requests.post(url, json=data)
    return response.json()

def get_transaction(trans_id):
    url = f"{BASE_URL}/transactions/{trans_id}/"
    response = requests.get(url)
    return response.json()

def update_transaction(trans_id, amount):
    url = f"{BASE_URL}/transactions/{trans_id}/"
    data = {"amount": amount}
    response = requests.put(url, json=data)
    return response.json()

def delete_transaction(trans_id):
    url = f"{BASE_URL}/transactions/{trans_id}/"
    response = requests.delete(url)
    return response.json()

# response = register_user(123456, "testpassword")
# print("Register User:", response)

# response = get_token(123456, "testpassword")
# print("Get Token:", response)

# fake_refresh_token = "fake_refresh_token"
# response = refresh_token(fake_refresh_token)
# print("Refresh Token:", response)

# response = list_users()
# print("List Users:", response)

response = get_user(123456)
print("Get User:", response)

# response = update_user(123456, balance=100)
# print("Update User:", response)

# response = patch_user(123456, {"balance": 200})
# print("Patch User:", response)

# response = delete_user(123456)
# print("Delete User:", response)