from util.env import Env

class NumberUtil(object):
    @staticmethod
    def truncate_digits(in_number: float, max_digits: int = Env.precision_digits()) -> float:
        """Restrict maximum decimal digits by removing them"""
        working_num = int(in_number * (10 ** max_digits))
        return working_num / (10 ** max_digits)