import json
from base64 import b64decode, b64encode

from django.test import TestCase

from ..communication import decode_base64_to_dict, encode_dict_to_base64


class TestEncoding(TestCase):

    def setUp(self):
        self.user_data = {
            "first_name": "Abraham",
            "last_name": "Yoba",
            "email": "webpack@pack.ck",
            "phone": "+380698569986",
        }

    def test_encode_dict_to_base64(self):
        self.assertEqual(
            encode_dict_to_base64(self.user_data),
            b64encode(bytes(json.dumps(self.user_data), 'utf-8')).decode("utf-8")
        )

    def test_decode_base64_to_dict(self):
        hash = encode_dict_to_base64(self.user_data)
        self.assertEqual(
            decode_base64_to_dict(hash),
            json.loads(b64decode(hash))
        )
