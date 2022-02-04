import flask_restful
from flask.json import jsonify
from flask import request
from src.utils.util import Logger, create_ouput_dirs, logging, save_json
from src.utils.app_context import app_context
import config
from src.utils.request_parse import Invoice
from flask import Flask
import config
import uuid
from src.services.invoice_to_json import invoice_to_json
from src.services.get_status import get_status

import queue

invoiceQueue = queue.Queue()

invoice_app = Flask(__name__)
invoice_api = flask_restful.Api(invoice_app)


@Logger(module_name="initiate_request")
@invoice_api.representation("application/json")
@invoice_app.route(
    config.API_URL_PREFIX + "/v0/invoice_to_json/process", methods=["POST"]
)
def init_request():
    json_data = request.get_json()
    job_id = str(uuid.uuid4())
    json_data["jobId"] = job_id
    invoiceQueue.put(json_data)
    return jsonify({"msg": "invoice_to_json started", "jobId": job_id})


@Logger(module_name="get_status")
@invoice_api.representation("application/json")
@invoice_app.route(config.API_URL_PREFIX + "/v0/invoice_to_json/get_status", methods=["POST"])
def check_status():
    json_data = request.get_json()
    return jsonify(get_status(json_data["jobId"]))


def worker():
    while True:
        process_request()


@Logger(module_name="process_request")
def process_request():
    data = invoiceQueue.get(block=True)
    job_id = data["jobId"]
    inovices = data["inputs"]

    if "config" in data.keys():
        invConfig = data["config"]
    else:
        invConfig = {"ocr": config.OCR_MODE}
    fine, run_time_errors, validation_errors, output_dir = create_ouput_dirs(job_id)
    save_json(output_dir, data, "request")
    for inovice in inovices:
        app_context["log_perfix"] = ""
        invoice_props = Invoice(inovice)
        invoice_props.set_config(invConfig)
        invoice_props.set_job_id(job_id)
        output_json_data = invoice_to_json(invoice_props)
        app_context["log_perfix"] = ""
        if output_json_data["code"] == 200:
            save_json(fine, output_json_data, invoice_props.get_file_name())
        elif output_json_data["code"] == 300:
            save_json(
                validation_errors, output_json_data, invoice_props.get_file_name()
            )
        else:
            save_json(run_time_errors, output_json_data, invoice_props.get_file_name())
        logging("####")
