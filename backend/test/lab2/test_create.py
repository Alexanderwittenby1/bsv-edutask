import pytest
from pymongo import MongoClient
from src.util.dao import DAO


class TestCreateUserIntegration:

    @pytest.fixture(scope="function")
    def real_dao(self):
        """Fixture to provide a DAO instance connected to a real test database."""
        # Anslut till databasen med autentisering
        # Använd root-användarnamn och lösenord från Docker
        client = MongoClient("mongodb://root:root@edutask-mongodb:27017")
        db = client.edutask
        # Skapa en DAO-instans
        dao = DAO(collection_name="user")
        dao.collection = db["test_user"]
        # Rensa databasen innan varje test
        dao.collection.delete_many({})

        yield dao

        # Rensa databasen efter varje test
        dao.collection.delete_many({})
        client.close()

    @pytest.mark.lab2_create
    def test_create_user(self, real_dao):
        """Test the actual create method of the DAO with a real database."""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        }

        # Anropa den faktiska create-metoden
        result = real_dao.create(user_data)

        # Kontrollera att resultatet matchar den inskickade datan
        assert result["_id"] is not None
        assert result["first_name"] == user_data["first_name"]
        assert result["last_name"] == user_data["last_name"]
        assert result["email"] == user_data["email"]

        # Kontrollera att objektet finns i databasen
        db_result = real_dao.collection.find_one(
            {"email": "john.doe@example.com"})
        assert db_result is not None
        assert db_result["first_name"] == user_data["first_name"]
        assert db_result["last_name"] == user_data["last_name"]
        assert db_result["email"] == user_data["email"]
