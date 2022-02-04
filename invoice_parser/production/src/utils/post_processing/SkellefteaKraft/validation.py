from src.utils.util import Logger
from src.utils.post_processing.base import ValidateBase


class Validate(ValidateBase):
    @Logger(module_name="validate_keys", logtime=True)
    def check_keys(self, response):

        report = {
            "meta": self.val_k_meta(response),
            "invoiceSections": self.val_k_sections(response),
        }
        return report

    def val_k_meta(self, reponse):
        return self.validate_keys(
            ["customerId", "invoiceNumber", "invoiceSections"], reponse
        )

    def val_k_sections(self, respose):
        report = []
        for section in respose["invoiceSections"]:
            l2 = {"costData": [], "meterstands": []}

            for costdata in section["costData"]:
                l3_fd = []
                for item_fd in costdata["invoiceRows"]:
                    l3_fd.append(self.validate_keys(["text", "spec", "value"], item_fd))

                l2["costData"].append(
                    {
                        "self": self.validate_keys(
                            ["kind", "period", "invoiceRows"], costdata
                        ),
                        "children": l3_fd,
                    }
                )

            for meter in section["meterstands"]:
                l3_ms = []
                for item_ms in meter["datapoints"]:
                    l3_ms.append(self.validate_keys(["date", "value"], item_ms))
                l2["meterstands"].append(
                    {
                        "self": self.validate_keys(
                            ["meterNumber", "datapoints"], meter
                        ),
                        "children": l3_ms,
                    }
                )

            report.append(
                {
                    "self": self.validate_keys(
                        [
                            "facilityId",
                            "address",
                            "contractId",
                            "costData",
                            "meterstands",
                            "VAT",
                            "totalCost",
                        ],
                        section,
                    ),
                    "children": l2,
                }
            )
            return report
