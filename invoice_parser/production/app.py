import config
import threading
from src.utils.util import Logger
from src.controller.module import invoice_app, worker


@Logger(module_name="start_workers")
def start_wrokers():
    proecss_worker = threading.Thread(
        target=worker, name="invoice-to-json-worker-thread"
    )
    proecss_worker.start()


if __name__ == "__main__":
    start_wrokers()
    print(invoice_app.url_map)
    invoice_app.run(host=config.HOST, port=config.PORT)
