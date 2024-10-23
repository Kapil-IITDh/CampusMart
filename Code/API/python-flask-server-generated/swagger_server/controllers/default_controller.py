import connexion
import six

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
from swagger_server import util


def chat_partners_get():  # noqa: E501
    """Get Chat Partners

     # noqa: E501


    :rtype: List[InlineResponse2003]
    """
    return 'do some magic!'


def contact_post(body):  # noqa: E501
    """Contact Us

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ContactBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def listings_get():  # noqa: E501
    """Get All Listings

     # noqa: E501


    :rtype: List[InlineResponse2001]
    """
    return 'do some magic!'


def listings_listing_id_delete(listing_id):  # noqa: E501
    """Delete Listing

     # noqa: E501

    :param listing_id: 
    :type listing_id: int

    :rtype: None
    """
    return 'do some magic!'


def listings_listing_id_get(listing_id):  # noqa: E501
    """Get Listing Details

     # noqa: E501

    :param listing_id: 
    :type listing_id: int

    :rtype: None
    """
    return 'do some magic!'


def listings_listing_id_put(body, listing_id):  # noqa: E501
    """Edit Listing

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param listing_id: 
    :type listing_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = ListingsListingIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def listings_post(body):  # noqa: E501
    """Create New Listing

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ListingsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_post(body):  # noqa: E501
    """User Login

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = LoginBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def logout_post():  # noqa: E501
    """User Logout

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def messages_user_id_get(user_id):  # noqa: E501
    """Get Messages

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: List[InlineResponse2004]
    """
    return 'do some magic!'


def messages_user_id_post(body, user_id):  # noqa: E501
    """Send Message

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param user_id: 
    :type user_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = MessagesUserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def profile_get():  # noqa: E501
    """Get User Profile

     # noqa: E501


    :rtype: InlineResponse200
    """
    return 'do some magic!'


def profile_put(body):  # noqa: E501
    """Edit User Profile

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ProfileBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def register_post(body):  # noqa: E501
    """User Registration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = RegisterBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def terms_get():  # noqa: E501
    """Terms and Conditions

     # noqa: E501


    :rtype: str
    """
    return 'do some magic!'


def transactions_buy_post(body):  # noqa: E501
    """Buy Item

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = TransactionsBuyBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def transactions_history_get():  # noqa: E501
    """Transaction History

     # noqa: E501


    :rtype: List[InlineResponse2002]
    """
    return 'do some magic!'
