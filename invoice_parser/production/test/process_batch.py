import requests
import json
import os


# input_dir = "/data/input/"

input_dir = "/home/dhiraj/ocr/Mestro/data/testing/25/input/"
supplierId = "SkellefteaKraft"


service_url = "http://52.164.191.160:5000/mestro/v0/invoice_to_json/process"


def get_requeset(input_dir, supplierId="", max_count=None):
    req = {"inputs": [], "meta": {}, "config": {"ocr": "FAST"}}
    pdfs = os.listdir(input_dir)
    if max_count != None:
        pdfs = pdfs[:max_count]

    for pdf_name in pdfs:
        pdf_name = pdf_name[:-4] + ".pdf"
        req["inputs"].append({"invoice": pdf_name, "supplierId": supplierId})
    return req


if __name__ == "__main__":

    req = get_requeset(input_dir, supplierId)
    print(req)
    res = requests.post(service_url, json=req, timeout=None)
    data = res.json()
    print(data)