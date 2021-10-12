import os

from util.conversions import AnanosConversions

class Env():
    @staticmethod
    def raw_to_amount(raw_amt: int) -> float:
        converted = AnanosConversions.raw_to_ananos(raw_amt)
        return converted

    @staticmethod
    def amount_to_raw(amount: float) -> int:
        return AnanosConversions.ananos_to_raw(amount)

    @staticmethod
    def currency_name() -> str:
        return 'Ananos'

    @staticmethod
    def currency_symbol() -> str:
        return 'ANA'

    @staticmethod
    def precision_digits() -> int:
        return 2

    @staticmethod
    def donation_address() -> str:
        return 'ana_33mru1r6bbtows86tud6okhbhsymz4t4c9p3dno6wgoqt8hd6tuqxjhg84jt'

    @classmethod
    def truncate_digits(cls, in_number: float, max_digits: int) -> float:
        """Restrict maximum decimal digits by removing them"""
        working_num = int(in_number * (10 ** max_digits))
        return working_num / (10 ** max_digits)

    @classmethod
    def format_float(cls, in_number: float) -> str:
        """Format a float with un-necessary chars removed. E.g: 1.0000 == 1"""
        in_number = cls.truncate_digits(in_number, 2)
        as_str = f"{in_number:.2f}".rstrip('0')
        if as_str[len(as_str) - 1] == '.':
            as_str = as_str.replace('.', '')
        return as_str

    @classmethod
    def commafy(cls, in_num_str) -> str:
        """Add comma to a number strings"""
        if "." not in in_num_str:
            return in_num_str
        e = list(in_num_str.split(".")[0])
        for i in range(len(e))[::-3][1:]:
            e.insert(i+1,",")
        return "".join(e)+"."+in_num_str.split(".")[1]
