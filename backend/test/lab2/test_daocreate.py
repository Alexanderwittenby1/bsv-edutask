import os
from dotenv import dotenv_values
import pymongo
import pytest

from unittest.mock import patch, MagicMock

from backend.src.util.dao import DAO
from backend.src.util.daos import getDao
from src.controllers.usercontroller import UserController
class TestDaoCreate:

    @pytest.fixture
    def mocked_dao(self):
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
        client = pymongo.MongoClient(MONGO_URL)
        test_db = client.test
        with patch.object(DAO, '__init__', return_value=None) as mocked_dao:
            mocked_dao.collection = test_db["user"]
            yield mocked_dao

    pytest.mark.lab2
    def test_valid_data(mocked_dao):
        input_data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@gmail.com",
        }
        res = mocked_dao.create(input_data)
        assert res["firstName"] == input_data["firstName"]
