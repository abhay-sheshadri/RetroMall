import requests
from CONFIGS import *
import json
from skimage import io
from skimage.transform import rescale, resize, downscale_local_mean
import os
from pyxelate import Pyx, Pal


def get_product_info(search_string, top_k=10):
    """
    title, price, and image for the top_k results from the search_string
    """
    payload = {
        "api_key": API_KEY,
        "url": "https://www.amazon.com/s?k=" + "+".join(search_string.split()),
        "autoparse": "true"
    }
    r = requests.get('http://api.scraperapi.com', params=payload)
    results_json = json.loads(r.content)["results"]
    # Take the top results
    top_results = []
    for result in results_json[:min(top_k, len(results_json))]:             
        top_results.append({
            "title": result["name"],
            "price": result["price_string"],
            "image": apply_pyxelate(io.imread(result["image"]))
        })
    return top_results


def apply_pyxelate(image):
    """
    Applies the popular pyxelate algorithm to the thumbnail image
    """
    factor = int(image.shape[0] / 128)
    pyx = Pyx(factor=factor, palette=7)
    pyx.fit(image)
    return pyx.transform(image)

