from src.services.invoice_to_json import invoice_to_json


class Response(object):
    def __init__(self, json_data):
        self.json_data = json_data

    def nonwf_response(self):

        # try:

        output_json_data = invoice_to_json(self.json_data)

        return output_json_data

        # except Exception as e:
        #     print(e)
        #     return None
