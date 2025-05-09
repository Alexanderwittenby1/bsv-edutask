import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError, DuplicateKeyError
from src.util.dao import DAO
from src.util.validators import getValidator
# Hur du gör för att köra testerna!!!
# Starta docker med docker-compose up
# Skriv docker ps för att se att containern är igång
# Skriv docker exec -it <container_id> bash för att gå in i containern
# Kör testerna med pytest -s -m lab2_create
# Om du vill köra testerna utan docker, se till att du har MongoDB installerat och kör igång den


@pytest.fixture()
def real_dao():
    MONGODB__URI = "mongodb://root:root@edutask-mongodb:27017"
    client = MongoClient(MONGODB__URI)
    db = client.edutask

    # Get the validator for the user collection
    userCollection = db.get_collection("email")
    userValidator = getValidator(userCollection.name)

    # Drop the collection if it exists
    # Like Drop Table in SQL
    if "test_user" in db.list_collection_names():
        db.drop_collection("test_user")

    # Create the collection with the validator
    db.create_collection("test_user", validator=userValidator)

    dao = DAO("test_user")

    dao.collection.delete_many({})

    yield dao

    dao.collection.delete_many({})
    client.close()


class TestCreateUserIntegration:

    @pytest.mark.lab2_create
    def test_create_user(self, real_dao):
        """Test the actual create method of the DAO with a real database."""
        user_data = {
            'email': 'john.doe@example.com',
        }

        result = real_dao.create(user_data)

        assert result["_id"] is not None
        assert result["email"] == user_data["email"]

    @pytest.mark.lab2_create
    def test_create_user_with_invalid_fields(self, real_dao):
        """Test the create method with invalid email field (wrong type)."""
        user_data = {
            'email': False  # Wrong type, should be string
        }

        with pytest.raises(WriteError):
            real_dao.create(user_data)

    @pytest.mark.lab2_create
    def test_create_user_with_missing_fields(self, real_dao):
        """Test the create method with missing required fields."""
        user_data = {

        }
        with pytest.raises(WriteError):
            real_dao.create(user_data)

    @pytest.mark.lab2_create
    def test_create_user_with_duplicate_email(self, real_dao):
        """Test the create method with duplicate email."""
        user_data1 = {
            'email': 'mary@sue.com'
        }
        user_data2 = {
            'email': 'mary@sue.com'
        }

        real_dao.create(user_data1)

        with pytest.raises(DuplicateKeyError):
            real_dao.create(user_data2)

    @pytest.mark.lab2_create
    def test_create_user_with_invalid_email(self, real_dao):
        """Test the create method with duplicate email."""
        user_data1 = {
            'email': 'mary@@@sue.com'
        }

        with pytest.raises(WriteError):
            real_dao.create(user_data1)
