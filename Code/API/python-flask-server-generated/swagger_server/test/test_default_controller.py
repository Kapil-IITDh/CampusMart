# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.contact_body import ContactBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.listings_body import ListingsBody  # noqa: E501
from swagger_server.models.listings_listing_id_body import ListingsListingIdBody  # noqa: E501
from swagger_server.models.login_body import LoginBody  # noqa: E501
from swagger_server.models.messages_user_id_body import MessagesUserIdBody  # noqa: E501
from swagger_server.models.profile_body import ProfileBody  # noqa: E501
from swagger_server.models.register_body import RegisterBody  # noqa: E501
from swagger_server.models.transactions_buy_body import TransactionsBuyBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_chat_partners_get(self):
        """Test case for chat_partners_get

        Get Chat Partners
        """
        response = self.client.open(
            '/api/v1/chat-partners',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_contact_post(self):
        """Test case for contact_post

        Contact Us
        """
        body = ContactBody()
        response = self.client.open(
            '/api/v1/contact',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listings_get(self):
        """Test case for listings_get

        Get All Listings
        """
        response = self.client.open(
            '/api/v1/listings',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listings_listing_id_delete(self):
        """Test case for listings_listing_id_delete

        Delete Listing
        """
        response = self.client.open(
            '/api/v1/listings/{listing_id}'.format(listing_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listings_listing_id_get(self):
        """Test case for listings_listing_id_get

        Get Listing Details
        """
        response = self.client.open(
            '/api/v1/listings/{listing_id}'.format(listing_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listings_listing_id_put(self):
        """Test case for listings_listing_id_put

        Edit Listing
        """
        body = ListingsListingIdBody()
        response = self.client.open(
            '/api/v1/listings/{listing_id}'.format(listing_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listings_post(self):
        """Test case for listings_post

        Create New Listing
        """
        body = ListingsBody()
        response = self.client.open(
            '/api/v1/listings',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        User Login
        """
        body = LoginBody()
        response = self.client.open(
            '/api/v1/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_post(self):
        """Test case for logout_post

        User Logout
        """
        response = self.client.open(
            '/api/v1/logout',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_messages_user_id_get(self):
        """Test case for messages_user_id_get

        Get Messages
        """
        response = self.client.open(
            '/api/v1/messages/{user_id}'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_messages_user_id_post(self):
        """Test case for messages_user_id_post

        Send Message
        """
        body = MessagesUserIdBody()
        response = self.client.open(
            '/api/v1/messages/{user_id}'.format(user_id=56),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_profile_get(self):
        """Test case for profile_get

        Get User Profile
        """
        response = self.client.open(
            '/api/v1/profile',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_profile_put(self):
        """Test case for profile_put

        Edit User Profile
        """
        body = ProfileBody()
        response = self.client.open(
            '/api/v1/profile',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_post(self):
        """Test case for register_post

        User Registration
        """
        body = RegisterBody()
        response = self.client.open(
            '/api/v1/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terms_get(self):
        """Test case for terms_get

        Terms and Conditions
        """
        response = self.client.open(
            '/api/v1/terms',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_transactions_buy_post(self):
        """Test case for transactions_buy_post

        Buy Item
        """
        body = TransactionsBuyBody()
        response = self.client.open(
            '/api/v1/transactions/buy',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_transactions_history_get(self):
        """Test case for transactions_history_get

        Transaction History
        """
        response = self.client.open(
            '/api/v1/transactions/history',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
