import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import scrapping.scrap as scrap


def test_basic():
    scrap.get_product_dataframe()
    assert True


def test_to_parquet():
    scrap.to_parquet("products.txt")
    assert os.path.exists("results.parquet")
