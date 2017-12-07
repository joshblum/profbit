import datetime
import time
import unittest

from profbit.coinbase_stats import StatTx
from profbit.coinbase_stats import _merge_stat_txs
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
