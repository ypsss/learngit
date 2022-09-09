from common.headler_conf import conf


class Assertion:

    def asserFictIn(self, expected, res):
        if res.get(k) == v:
            pass
        else:
            raise AssertionError("{} not in {}".format(expected, res))


