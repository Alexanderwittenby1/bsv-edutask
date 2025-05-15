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
    def test_find_user(self):
        """Test the get_user_by_email method with a valid email address.
        """
        user = {'first_name': 'Mary',
                'last_name': 'Sue', 'email': 'mary@sue.com'}

        # Mock the email object
        email = 'mary@sue.com'

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = [user]
        uc = UserController(dao=mockedDAO)
        result = uc.get_user_by_email(email)

        assert result == user

    @pytest.mark.lab2
    def test_find_no_user(self):
        """Test the get_user_by_email method with a valid email address.
        """
        user = None
        emailToFind = 'henry@ford.com'
        mockedDAO = MagicMock()
        mockedDAO.find.return_value = [user]
        uc = UserController(dao=mockedDAO)
        assert uc.get_user_by_email(emailToFind) == None

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

    @pytest.mark.lab2
    def test_operation_failure(self):
        """Test the get_user_by_email method with a database operation failure."""

        # Feels like a weird test, but let's assume we want to test the exception handling
        # If so please explain how to test and database operation failure, isn't a invalid email an operation failure?

        email = 'hej@a123.com'
        mockedDAO = MagicMock()
        mockedDAO.find.side_effect = Exception("Database error")
        uc = UserController(dao=mockedDAO)

        with pytest.raises(Exception, match="Database error"):
            uc.get_user_by_email(email)
