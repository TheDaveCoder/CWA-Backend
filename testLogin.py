import requests
import json

# Login URL
login_url = "http://127.0.0.1:5000/login"
# Replace with valid credentials
payload = {
    "email": "madamba@bennett.com",
    "password": "Dummypassword1!"
}
headers = {
    "Content-Type": "application/json"
}

# Make the POST request to login
login_response = requests.post(login_url, data=json.dumps(payload), headers=headers)

# Check if login was successful
if login_response.status_code == 200:
    # Extract the id_token from the login response
    id_token = login_response.json().get("id_token")
    print("Login Successful. JWT:", id_token)

    # Protected URL that requires authentication
    protected_url = "http://127.0.0.1:5000/protected"

    # Now make a GET request to the protected route with the Bearer token
    protected_headers = {
        "Authorization": f"Bearer {id_token}"
    }

    # Send request to the protected route
    protected_response = requests.get(protected_url, headers=protected_headers)

    # Print the response from the protected endpoint
    print(f"Status Code: {protected_response.status_code}")
    print("Response Body:", protected_response.json())

else:
    print(f"Login failed. Status Code: {login_response.status_code}")
    print("Response Body:", login_response.json())
