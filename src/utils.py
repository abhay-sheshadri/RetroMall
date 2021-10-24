import requests
from CONFIGS import *
import json
from skimage import io
from skimage.transform import rescale, resize, downscale_local_mean
from pyxelate import Pyx, Pal
import pygame
import random
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from src.sc_utils import *


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
            "image": apply_pyxelate(io.imread(result["image"])),
            "url": result["url"]
        })
    return top_results


def get_pixeled_face():
    Tk().withdraw()
    filename = askopenfilename()
    image = apply_pyxelate(io.imread(filename))
    image = pygame.surfarray.make_surface(image)
    return pygame.transform.rotate(image, -90)


def apply_pyxelate(image):
    """
    Applies the popular pyxelate algorithm to the thumbnail image
    """
    factor = int(image.shape[0] / 32)
    pyx = Pyx(factor=factor, palette=7)
    pyx.fit(image)
    return pyx.transform(image)


def create_new_coupon():
    company = random.choice(["Yamaha", "Samsung", "Nike"])
    discount = random.randint(10,20)
    # NFT stuff maybe?
    add_coupon_to_contract(discount, company)
    #
    font = pygame.font.SysFont(None, 48)
    img = font.render('Congrats! You won a coupon for {} off of {} products!'.format(str(discount)+"%", company), True, (255,0,0))
    return img


def get_coupons_from_chain():
    font = pygame.font.SysFont(None, 48)

    coupon_surface = pygame.Surface((1000, 300), pygame.SRCALPHA, 32)
    coupons = get_user_coupons(ADDRESS)

    for i in range(len(coupons)):
        coupons[i]
        coupon_surface.blit(font.render("{} off at {}".format(
            str(coupons[i]["discount"])+"%", coupons[i]["brand"])
            , True, (255,255,255, 255)), (0, i*50))
    
    return coupon_surface