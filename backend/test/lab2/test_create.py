import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError, DuplicateKeyError
from src.util.dao import DAO

# Hur du gör för att köra testerna!!!
# Starta docker med docker-compose up
# Skriv docker ps för att se att containern är igång
# Skriv docker exec -it <container_id> bash för att gå in i containern
# Kör testerna med pytest -s -m lab2_create
# Om du vill köra testerna utan docker, se till att du har MongoDB installerat och kör igång den

# En custom validator för att säkerställa att alla användare har ett unikt email och att de har rätt datatyper

# Testade med att hämta validator med getCollection men fungerade inte
new_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
                "description": "First name is required"
            },
            "lastName": {
                "bsonType": "string",
                "description": "Last name is required"
            },
            "email": {
                "bsonType": "string",
                "description": "Email is required and must be string",
                "uniqueItems": True
            },
            "tasks": {
                "bsonType": "array",
                "items": {"bsonType": "objectId"}
            }
        }
    }
}


@pytest.fixture()
def real_dao():
    client = MongoClient("mongodb://root:root@edutask-mongodb:27017")
    db = client.edutask

    # Droppa kollektionen om den finns så vi alltid sätter rätt validator
    if "test_user" in db.list_collection_names():
        db.drop_collection("test_user")

    # Skapa med custom validator
    db.create_collection("test_user", validator=new_validator)
    # Skapa ett unikt index på email-fältet eftersom validatorn inte stödjer unika index
    db.test_user.create_index("email", unique=True)

    dao = DAO("user")
    dao.collection = db["test_user"]
    dao.collection.delete_many({})

    yield dao

    dao.collection.delete_many({})
    client.close()


class TestCreateUserIntegration:

    @pytest.mark.lab2_create
    def test_create_user(self, real_dao):
        """Test the actual create method of the DAO with a real database."""
        user_data = {
            'firstName': 'Mary',
            'lastName': 'Sue',
            'email': 'john.doe@example.com',
        }

        result = real_dao.create(user_data)

        assert result["_id"] is not None
        assert result["firstName"] == user_data["firstName"]
        assert result["lastName"] == user_data["lastName"]
        assert result["email"] == user_data["email"]

    @pytest.mark.lab2_create
    def test_create_user_with_invalid_fields(self, real_dao):
        """Test the create method with invalid email field (wrong type)."""
        user_data = {
            'firstName': 'Mary',
            'lastName': 'Sue',
            'email': False  # Wrong type, should be string
        }

        with pytest.raises(WriteError):
            real_dao.create(user_data)

    @pytest.mark.lab2_create
    def test_create_user_with_missing_fields(self, real_dao):
        """Test the create method with missing required fields."""
        user_data = {
            'firstName': 'Mary',
            # 'lastName' is missing
            'email': 'mary@sue.com'
        }
        with pytest.raises(WriteError):
            real_dao.create(user_data)

    @pytest.mark.lab2_create
    def test_create_user_with_duplicate_email(self, real_dao):
        """Test the create method with duplicate email."""
        user_data1 = {
            'firstName': 'Mary',
            'lastName': 'Sue',
            'email': 'mary@sue.com'
        }
        user_data2 = {
            'firstName': 'Mary',
            'lastName': 'Sue',
            'email': 'mary@sue.com'
        }

        real_dao.create(user_data1)

        with pytest.raises(DuplicateKeyError):
            real_dao.create(user_data2)
