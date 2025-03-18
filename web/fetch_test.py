import json
person = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "occupation": "Software Developer",
    "location": {
        "city": "San Francisco",
        "state": "California",
        "country": "USA"
    }
}
print(json.dumps(person))
