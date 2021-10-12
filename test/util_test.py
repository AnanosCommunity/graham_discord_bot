import asyncio
import unittest
import os
from util.conversions import AnanosConversions
from util.env import Env
from util.regex import RegexUtil, AmountAmbiguousException, AmountMissingException, AddressAmbiguousException, AddressMissingException
from util.util import Utils
from util.validators import Validators

def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

class TestConversions(unittest.TestCase):
    def test_unit_conversions(self):
        self.assertEqual(AnanosConversions.raw_to_ananos(10100000000000000000000000000), 1.01)
        self.assertEqual(AnanosConversions.ananos_to_raw(1.01), 10100000000000000000000000000)
        self.assertEqual(AnanosConversions.ananos_to_raw(19.06), 190600000000000000000000000000)
        self.assertEqual(AnanosConversions.ananos_to_raw(0.25), 2500000000000000000000000000)
        self.assertEqual(AnanosConversions.ananos_to_raw(50), 500000000000000000000000000000)
        self.assertEqual(AnanosConversions.ananos_to_raw(0.2), 2000000000000000000000000000)
        self.assertEqual(AnanosConversions.ananos_to_raw(19.089999), 190800000000000000000000000000)

class TestEnv(unittest.TestCase):
    def test_truncate_digits(self):
        self.assertEqual(Env.truncate_digits(1.239, max_digits=2), 1.23)
        self.assertEqual(Env.truncate_digits(1.2, max_digits=2), 1.2)
        self.assertEqual(Env.truncate_digits(0.9999999999999, max_digits=6), 0.999999)

    def test_format_float(self):
        self.assertEqual(Env.format_float(9.90000), "9.9")
        self.assertEqual(Env.format_float(9.0), "9")
        self.assertEqual(Env.format_float(9), "9")
        self.assertEqual(Env.format_float(9.9000010), "9.900001")

class TestRegexUtil(unittest.TestCase):
    def test_find_float(self):
        self.assertEqual(RegexUtil.find_float('Hello 1.23 World'), 1.23)
        self.assertEqual(RegexUtil.find_float('Hello 1.23  4.56 World'), 1.23)
        with self.assertRaises(AmountMissingException) as exc:
            RegexUtil.find_float('Hello World')

    def test_find_send_amounts(self):
        self.assertEqual(RegexUtil.find_send_amounts('Hello 1.23 World'), 1.23)
        with self.assertRaises(AmountMissingException):
            RegexUtil.find_send_amounts('Hello World')
        with self.assertRaises(AmountAmbiguousException):
            RegexUtil.find_send_amounts('Hello 1.23 4.56 World')

    def test_find_address(self):
        self.assertEqual(RegexUtil.find_address_match('sdasdasana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48oksesdadasd'), 'ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse')
        with self.assertRaises(AddressAmbiguousException):
            RegexUtil.find_address_match('sdasdana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48oksesdasd ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse sana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse')
        with self.assertRaises(AddressMissingException):
            RegexUtil.find_address_match('sdadsd')

    def test_find_addresses(self):
        # Multiple addresses
        self.assertEqual(RegexUtil.find_address_matches('sdasdasana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48oksesdadasd'), ['ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse'])
        self.assertEqual(RegexUtil.find_address_matches('sdasdana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48oksesdasd ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse sana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse'), ['ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse', 'ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse', 'ana_3jb1fp4diu79wggp7e171jdpxp95auji4moste6gmc55pptwerfjqu48okse'])
        with self.assertRaises(AddressMissingException):
            RegexUtil.find_address_matches('sdadsd')


class TestGenericUtil(unittest.TestCase):
    def setUp(self):
        self.a = 0
        self.b = 0
        self.c = 0

    def test_emoji_strip(self):
        self.assertEqual(Utils.emoji_strip("字漢字Hello😊myfriend\u2709") ,"字漢字Hellomyfriend") 

    @async_test
    async def test_run_task_list(self):
        async def test_task(value: int):
            if value == 1:
                self.a = value
            elif value == 2:
                self.b = value
            elif value == 3:
                self.c = value
        tasks = [
            test_task(1),
            test_task(2),
            test_task(3)
        ]
        await Utils.run_task_list(tasks)
        self.assertEqual(self.a, 1)
        self.assertEqual(self.b, 2)
        self.assertEqual(self.c, 3)

    def test_random_float(self):
        rand1 = Utils.random_float()
        rand2 = Utils.random_float()
        self.assertNotEqual(rand1, rand2)
        self.assertLess(rand1, 100)
        self.assertLess(rand2, 100)
        self.assertGreaterEqual(rand1, 0)
        self.assertGreaterEqual(rand2, 0)

class TestValidators(unittest.TestCase):
    def test_too_many_decimalse(self):
        self.assertTrue(Validators.too_many_decimals(1.234))
        self.assertFalse(Validators.too_many_decimals(1.23))
        self.assertFalse(Validators.too_many_decimals(1.2))

    def test_valid_address(self):
        # Null should always be false
        self.assertFalse(Validators.is_valid_address(None))
        # Valid
        self.assertTrue(Validators.is_valid_address('ana_38enhxt6k5izyrc47tptcdytga7uhftworydqsbm7gsfgecmrjrowou349ae'))
        # Bad checksum
        self.assertFalse(Validators.is_valid_address('ana_38enhxt6k5izyrc47tptcdytga7uhftworydqsbm7gsfgecmrjrowou349ae'))
        # Bad length
        self.assertFalse(Validators.is_valid_address('ana_38enhxt6k5izyrc47tptcdytga7uhftworydqsbm7gsfgecmrjrowou349ae'))
        