class OddConverter:
    __ratio = 100

    @classmethod
    def pos_moneyline_to_odd(cls, moneyline: int):
        ratio = moneyline / cls.__ratio + 1
        return ratio

    @classmethod
    def neg_moneyline_to_odd(cls, moneyline: int):
        ratio = cls.__ratio / moneyline + 1
        return ratio

    def converter(self, moneyline: int):
        if moneyline < 0:
            res = self.neg_moneyline_to_odd(moneyline=abs(moneyline))
        else:
            res = self.pos_moneyline_to_odd(moneyline=moneyline)
        return res


odd_converter = OddConverter()

print(odd_converter.converter(-50))