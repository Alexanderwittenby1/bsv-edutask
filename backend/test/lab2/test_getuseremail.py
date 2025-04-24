# File: backend/src/util/daos.py
import pytest

from unittest.mock import patch, MagicMock
from unittest.mock import Mock
import sys
from src.util.daos import getDao

from src.controllers.usercontroller import UserController
import unittest.mock as mock


class TestUserController:
    @pytest.mark.lab2
    def test_invalid_email_adress(self):
        """Test the get_user_by_email method with an invalid email address.
        """

        # Mock the email object
        email = 'janedoe.com'
        # Mock the DAO to return a simulated user
        mockedDAO = MagicMock()

        uc = UserController(dao=mockedDAO)
        with pytest.raises(ValueError, match="Error: invalid email address"):
            uc.get_user_by_email(email)

    @pytest.mark.lab2
    def test_valid_email_address(self):
        """Test the get_user_by_email method with a valid email address (non existing user/email).
        """

        # Mock the email object
        email = 'john@doe.com'

        # Mock the DAO to return a simulated user
        mockedDAO = MagicMock()
        uc = UserController(dao=mockedDAO)
        mockedDAO.find.return_value = []

        with pytest.raises(Exception):
            uc.get_user_by_email(email)

    @pytest.mark.lab2
    def test_find_user(self):
        """Test the get_user_by_email method with a valid email address.
        """
        user = {'first_name': 'Mary',
                'last_name': 'Sue', 'email': 'mary@sue.com'}

        # Mock the email object
        email = 'mary@sue.com'

        mockedDAO = MagicMock()
        uc = UserController(dao=mockedDAO)
        mockedDAO.find.return_value = [user]
        result = uc.get_user_by_email(email)

        assert result == user

    @pytest.mark.lab2
    def test_multiple_users(self):
        """Test the get_user_by_email method with a valid email address.
        """
        user1 = {'first_name': 'Mary',
                 'last_name': 'Sue', 'email': 'mary@sue.com'}
        user2 = {'first_name': 'gary',
                 'last_name': 'sue', 'email': 'mary@sue.com'}

        email = 'mary@sue.com'

        mockedDAO = MagicMock()
        uc = UserController(dao=mockedDAO)

        mockedDAO.find.return_value = [user1, user2]

        result = uc.get_user_by_email(email)
        print("Result multiple:", result)

        assert result == user1
