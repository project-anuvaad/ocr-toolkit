import os
import json
import glob
import config
from src.utils.request_parse import Invoice


def get_status(job_id):
    status_report = {"status_report": [], "jobId": job_id}
    output_dir = os.path.join(config.BASE_DIR, "output", "service_output", job_id)
    request_file = os.path.join(output_dir, "request.json")
    if os.path.exists(output_dir):
        with open(request_file) as jp:
            data = json.load(jp)
        invoices = data["inputs"]
        for invoice in invoices:
            invoic_props = Invoice(invoice) 
            check_file = glob.glob(
                "{}/*/{}*".format(output_dir, invoic_props.get_file_name())
            )
            if len(check_file) == 0:
                status_report["status_report"].append(
                    {"invoice": invoic_props.get_file_name(), "status": "inProgress"}
                )
            else:
                response_folder = check_file[0].split("/")[-2]
                if response_folder == "fine":
                    status_report["status_report"].append(
                        {"invoice": invoic_props.get_file_name(), "status": "successful","responsePath":check_file[0]}
                    )
                elif response_folder == "run_time_error":
                    status_report["status_report"].append(
                        {
                            "invoice": invoic_props.get_file_name(),
                            "status": "failed",
                            "erroType": "runTimeError",
                            "logsPath":config.LOGS
                        }
                    )
                elif response_folder == "validation_error":
                    status_report["status_report"].append(
                        {
                            "invoice": invoic_props.get_file_name(),
                            "status": "failed",
                            "errorType": "keyValidationError",
                            "responsePath":check_file[0],
                            "logsPath":config.LOGS
                        }
                    )

        return status_report
    return {"status_report": [], "jobId": job_id,'msg': "Either this job does not exist or it has not started yet"}