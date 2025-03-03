import requests

BASE_URL = "http://127.0.0.1:8000/api/"

class DBManager:
    def __init__(self, endpoint):
        self.url = BASE_URL + endpoint + "/"

    def list(self):
        response = requests.get(self.url)
        return response.json() if response.status_code == 200 else response.text

    def retrieve(self, obj_id):
        response = requests.get(f"{self.url}{obj_id}/")
        return response.json() if response.status_code == 200 else response.text

    def create(self, data):
        response = requests.post(self.url, json=data)
        return response.json() if response.status_code in [200, 201] else response.text

    def update(self, obj_id, data):
        response = requests.put(f"{self.url}{obj_id}/", json=data)
        return response.json() if response.status_code in [200, 204] else response.text

    def partly_update(self, obj_id, data):
        response = requests.patch(f"{self.url}{obj_id}/", json=data)
        return response.json() if response.status_code in [200, 204] else response.text

    def destroy(self, obj_id):
        response = requests.delete(f"{self.url}{obj_id}/")
        return "Deleted successfully" if response.status_code == 204 else response.text

# Initialize managers for different endpoints
users_manager = DBManager("users")
subscriptions_manager = DBManager("subscriptions")
transactions_manager = DBManager("transactions")
topups_manager = DBManager("topups")

# Example usage:
if __name__ == "__main__":
    print(users_manager.list())  # Fetch all users
    print(users_manager.create({"name": "John Doe", "email": "john@example.com"}))  # Create a new user
    print(users_manager.retrieve(1))  # Get details of user with ID 1
    print(users_manager.update(1, {"name": "John Updated", "email": "john.updated@example.com"}))  # Full update
    print(users_manager.partly_update(1, {"name": "John Partial"}))  # Partial update
    print(users_manager.destroy(1))  # Delete user with ID 1
