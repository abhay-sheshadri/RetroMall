from src.utils import *
from src.db_utils import *

import traceback
import sys


brands_and_categories = {
    "sony": [
        "headphones",
        "cameras",
        "speakers"
    ],
    "nike": [
        "pants",
    ],
}


if __name__ == "__main__":

    db = DatabaseHandler("product_list.db")

    for brand in brands_and_categories:
        for category in brands_and_categories[brand]:
            try:
                results = get_product_info(brand + " " + category)
                for i in range(len(results)):
                    db.put(brand, category, results[i]["title"], results[i]["price"], results[i]["image"])
            except Exception as e:
                print("Failed with", brand, category)
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)


    db.close()

