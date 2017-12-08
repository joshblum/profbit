import datetime
import time
import unittest

from profbit.coinbase_stats import StatTx
from profbit.coinbase_stats import _merge_stat_txs
from profbit.coinbase_stats import _percent
from profbit.coinbase_stats import parse_timestamp


class CoinbaseStatsTestCase(unittest.TestCase):

    def test_merge_stat_txs(self):
        array1 = [
            StatTx(datetime.datetime.now()),
            StatTx(datetime.datetime.now())
        ]
        time.sleep(1)
        array2 = [
            StatTx(datetime.datetime.now()),
            StatTx(datetime.datetime.now())
        ]
        merged = _merge_stat_txs(array1, array2)
        self.assertEqual(len(merged), len(array1) + len(array2))
        self.assertEqual(merged, array1 + array2)

    def test_parse_datetime(self):
        now = datetime.datetime.now()
        now = now.replace(microsecond=0)
        timestamp = now.isoformat()
        self.assertEqual(now, parse_timestamp(timestamp))

    def test_percent(self):
        # Catch divide by 0
        investment = 0
        return_investment = 100
        self.assertEqual(_percent(investment, return_investment), 0)

        # If we withdraw but still make a profit, lol, net gains are
        # positive.
        investment = -5
        return_investment = 100
        self.assertEqual(_percent(investment, return_investment), 2000)

        investment = -5
        return_investment = -100
        self.assertEqual(_percent(investment, return_investment), -2000)
