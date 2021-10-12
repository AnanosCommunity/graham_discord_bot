import decimal

ANANOS_DECIMALS = decimal.Decimal(10) ** -2

class AnanosConversions():
    # 1 ANA = 10e28 RAW
    @staticmethod
    def raw_to_ananos(raw_amt: int) -> float:
        decimal_amt = decimal.Decimal(raw_amt) / (10 ** 28)
        decimal_amt = decimal_amt.quantize(ANANOS_DECIMALS, decimal.ROUND_DOWN)
        return float(decimal_amt)

    @staticmethod
    def ananos_to_raw(ban_amt: float) -> int:
        decimal_amt = decimal.Decimal(str(ban_amt))
        decimal_amt = decimal_amt.quantize(ANANOS_DECIMALS, decimal.ROUND_DOWN)
        return int(decimal_amt * (10 ** 28))