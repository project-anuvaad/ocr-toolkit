from src.utils.post_processing.base import LayoutBase
from src.utils.util import find_pattern_index, sort_regions
import re
import pandas as pd
from src.utils.util import Logger


"""
Layout mapping 

'm' : 'meta',
'h' : 'header' ,
'fm1' : 'facility-meta-1' ,
'fm2' : 'facility-meta-2',
'fm3' : 'facility-meta-3' 
'fd' : 'facility_data', 
'ms'   : 'meterstand',
't'    : 'total'


"""
filter_patterns = ["\x0c", "\f", "\v", "\x0b", None, ""]


m_patterns = {"customerId": r"\d{6}", "invoiceNumber": r"\d{10}"}
fm1_patterns = {"facilityId": r".*(ingsID|ingsid).*", "address": r".*gsadress.*"}
fm2_pattern = r"\d{8}"
fd_col2_pattern = r"^(kWh|st|Stk|SEK/kWh)$"
fm1_end_pattern = ""

fm2_find_pattern = r"(Kontraktsnummer:)\s\d.*"

crop_config = {
    "ms": {"x": 10, "y": 5},
    "fd": {"x": 20, "y": 1},
    "fm3": {"x": 10, "y": 1},
}


class LayoutClass(LayoutBase):
    def __init__(self, crop_config=crop_config):
        super(LayoutClass, self).__init__()
        self.crop_config = crop_config
        self.lang = "Latin"
        self.score = 1
        self.classs = None
        self.skip_class = ["h"]
        self.tabular_class = ["fd", "ms"]
        self.class_mapping = {
            0: "m",
            1: "fm1",
            2: "fm2",
            3: "fm3",
            4: "fd",
            5: "t",
            6: "ms",
            7: "h",
        }

    @Logger(module_name="process_fm1")
    def process_fm1(self, text):

        return FM1(self.score, text).process_layout()

    @Logger(module_name="process_fm2")
    def process_fm2(self, text):
        return FM2(text).process_layout()

    @Logger(module_name="process_fm3")
    def process_fm3(self, text):
        return FM3(text).process_layout()

    @Logger(module_name="process_fd")
    def process_fd(self, text):
        return FD(text).process_layout()

    @Logger(module_name="process_m")
    def process_m(self, text):
        return M(text).process_layout()

    @Logger(module_name="process_t")
    def process_t(self, text):
        return T(text).process_layout()

    @Logger(module_name="process_ms")
    def process_ms(self, text):
        return MS(text).process_layout()


class M:
    def __init__(self, text, m_pattern=m_patterns, filter_patterns=filter_patterns):
        self.text = text
        self.filter_patterns = filter_patterns
        self.m_patterns = m_pattern
        self.app_context = {}

    def process_layout(self):

        self.app_context["lines"] = [
            line for line in self.text.split("\n") if line not in self.filter_patterns
        ]
        # print(self.app_context["lines"], 'linesss')
        customerId = find_pattern_index(
            self.app_context["lines"], self.m_patterns["customerId"], index=False
        )
        invoiceNumber = find_pattern_index(
            self.app_context["lines"], self.m_patterns["invoiceNumber"], index=False
        )
        return {"customerId": customerId, "invoiceNumber": invoiceNumber}


class FM1:
    def __init__(
        self, score, text, fm1_patterns=fm1_patterns, filter_patterns=filter_patterns
    ):
        self.text = text
        self.score = score
        self.filter_patterns = filter_patterns
        self.fm1_patterns = fm1_patterns
        self.app_context = {}

    def process_layout(self):
        self.app_context["lines"] = [
            line for line in self.text.split("\n") if line not in self.filter_patterns
        ]
        if self.score > 0.8:

            # print(self.app_context["lines"])
            facilityId = find_pattern_index(
                self.app_context["lines"], self.fm1_patterns["facilityId"], index=False
            )
            address = find_pattern_index(
                self.app_context["lines"], self.fm1_patterns["address"], index=False
            )
            # print(self.app_context["lines"])
            return {
                "facilityId": facilityId.split(":")[1][1:],
                "address": address.split("adress:")[1][1:],
            }
        else:
            return self.rectify_misclassification()

    def rectify_misclassification(self):
        fm2_value = FM2(self.text).process_layout()
        if "contractId" in fm2_value.keys():
            return {"data": fm2_value, "class": "fm2"}
        else:
            return {}


class FM2:
    def __init__(self, text, fm2_pattern=fm2_pattern, filter_patterns=filter_patterns):
        self.text = text
        self.filter_patterns = filter_patterns
        self.fm2_pattern = fm2_pattern
        self.app_context = {}

    def process_layout(self):
        self.app_context["lines"] = [
            line for line in self.text.split("\n") if line not in self.filter_patterns
        ]
        # print(self.app_context["lines"], 'linesss')
        contractId = find_pattern_index(
            self.app_context["lines"], self.fm2_pattern, index=False
        )
        try:
            if contractId:
                contractId = contractId[-8:]
            else:
                fm2_value = " ".join(self.app_context["lines"])
                contract = re.search(fm2_find_pattern, fm2_value)
                if contract:
                    contractId = contract.group()
                    contr = re.sub(r"[A-ZÄäÅåÖöa-z:]", "", contractId)
                    contractId = contr.strip()
                else:
                    return {}
        except Exception as e:
            print("Exception in fm2 : ", e)
        return {"contractId": contractId}


class FM3:
    def __init__(self, text, filter_patterns=filter_patterns):
        self.text = text
        self.filter_patterns = filter_patterns
        self.app_context = {}

    def process_layout(self):

        self.app_context["lines"] = [
            line for line in self.text.split("\n") if line not in self.filter_patterns
        ]

        return self.map_cols(self.app_context["lines"])[0]

    def map_cols(self, col_1):
        mapped_cols = []
        for index in range(len(col_1)):

            word_list = col_1[index].split()

            mapped_cols.append(
                {
                    "kind": word_list[0],
                    "period": " ".join(word_list[1:]),
                }
            )
        return mapped_cols


class T:
    def __init__(self, text, filter_patterns=filter_patterns):
        self.text = text
        self.filter_patterns = filter_patterns
        self.app_context = {}

    def process_layout(self):

        self.app_context["lines"] = [
            line for line in self.text.split("\n") if line not in self.filter_patterns
        ]
        # print(self.app_context["lines"])

        return self.map_cols(self.app_context["lines"][0])

    def map_cols(self, text):

        total = "{}".format(" ".join(text.split()[1:]))
        if "SEK" in total:
            return {"totalCost": total}
        elif "kWh" in total:
            return {"totalCons": total.split("kWh")[0] + "kwh"}
        else:
            return None


class FD:
    def __init__(
        self,
        text,
        fd_col2_pattern=fd_col2_pattern,
        filter_patterns=filter_patterns,
        debug=False,
    ):
        self.text_df = pd.DataFrame(text)
        self.fd_col2_pattern = fd_col2_pattern
        self.data = {"invoiceRows": [], "VAT": None}
        self.debug = debug

    def process_layout(self):
        self.text_df = self.text_df[self.text_df["text"] != ""]
        if len(self.text_df) > 0:
            self.text_df = self.text_df.sort_values(by=["top"])
            self.sorted_rows = sort_regions(self.text_df, [], line_id=0)
        else:
            self.sorted_rows = [self.text_df]

        if self.debug:
            [print(" ".join(row["text"].values) + "\n") for row in self.sorted_rows]

        self.partition_columns()

        return self.data

    def partition_columns(self):

        for row in self.sorted_rows:
            if "Moms" in row["text"].values:
                self.data["VAT"] = self.extract_vat(row)
            else:
                self.data["invoiceRows"].append(self.map_fd(row))

    def extract_vat(self, row):
        split_index = find_pattern_index(list(row.text.values), r"%")
        return " ".join(row["text"].values[split_index + 1 :])

    def map_fd(self, row):
        t_list = list(row.text.values)
        rectified_list = []
        index = 0
        # rectifing the cases where a nubmer is borken due to space between digits
        while index < len(t_list):
            if (
                t_list[index].lstrip("-").isnumeric()
                and len(t_list[index].lstrip("-")) < 3
            ):
                rectified_list.append(" ".join(t_list[index : index + 2]))
                index += 2
            else:
                rectified_list.append(t_list[index])
                index += 1
        col2_index = find_pattern_index(
            rectified_list, self.fd_col2_pattern, index=False
        )
        if len(rectified_list) > 1:
            if len(rectified_list) == 2:
                return {}
            if col2_index is None:
                return {
                    "text": " ".join(rectified_list[:-3]),
                    "spec": rectified_list[-3],
                    "value": " ".join(rectified_list[-2:]),
                }
            else:
                if col2_index in ["st", "Stk"]:
                    return {
                        "text": " ".join(rectified_list[:-5]),
                        "spec": " ".join(rectified_list[-5:-2]),
                        "value": " ".join(rectified_list[-2:]),
                    }

                else:
                    return {
                        "text": " ".join(rectified_list[:-6]),
                        "spec": " ".join(rectified_list[-6:-2]),
                        "value": " ".join(rectified_list[-2:]),
                    }


class MS:
    def __init__(
        self,
        text,
        fm1_end_pattern=fm1_end_pattern,
        filter_patterns=filter_patterns,
        debug=False,
    ):
        self.text_df = pd.DataFrame(text)
        self.data = {"meterNumber": None, "datapoints": []}
        self.debug = debug
        # self.text = text
        self.filter_patterns = filter_patterns
        self.fm1_end_pattern = fm1_end_pattern
        self.app_context = {}

    def process_layout(self):
        self.text_df = self.text_df[self.text_df["text"] != ""]
        if len(self.text_df) > 0:
            self.text_df = self.text_df.sort_values(by=["top"])
            self.sorted_rows = sort_regions(self.text_df, [], line_id=0)
        else:
            self.sorted_rows = [self.text_df]

        if self.debug:
            [print(" ".join(row["text"].values) + "\n") for row in self.sorted_rows]

        self.partition_columns()
        # print(self.data)
        return self.data

    def partition_columns(self):

        for i, row in enumerate(self.sorted_rows):

            meterNumber = row["text"].values

            if len(meterNumber) > 1:
                if "Mätarnummer:" in meterNumber:
                    meter = " ".join(row["text"].values)
                    meterNumber = re.sub(r"[A-ZÄäÅåÖöa-z:]", "", meter)
                    if meterNumber:
                        self.data["meterNumber"] = meterNumber.strip()
                    else:
                        self.data["meterNumber"] = None
            else:
                if len(meterNumber) == 1:

                    self.data["meterNumber"] = meterNumber[0]
                else:
                    self.data["meterNumber"] = None

            self.data["datapoints"].append(self.map_ms(row))

    def map_ms(self, row):
        t_list = list(row.text.values)
        rectified_list = []
        mapped_cols = {}
        date_pattern = r"\d{4}(?P<sep>[-])\d{2}(?P=sep)\d{2}"
        # num_pattern = r"\w.*\s\d{4}(?P<sep>[-])\d{2}(?P=sep)\d{2}\s"
        index = 0
        while index < len(t_list):
            if (
                t_list[index].lstrip("-").isnumeric()
                and len(t_list[index].lstrip("-")) < 2
            ):
                rectified_list.append(" ".join(t_list[index : index + 2]))
                index += 2
            else:
                rectified_list.append(t_list[index])
                index += 1
        num_value = " ".join(rectified_list)
        # num = re.sub(num_pattern, "", num_value)
        datee = re.search(date_pattern, num_value)
        try:
            if len(rectified_list) > 1:
                if datee:
                    col1_date = datee.group()
                else:
                    col1_date = None
                if (",") in (rectified_list[2]):
                    col1 = rectified_list[2]
                    if (
                        ("kWh") in rectified_list
                        and len(rectified_list) == 8
                        or ("kWh") in rectified_list
                        and len(rectified_list) == 7
                    ):
                        kwh = " ".join(rectified_list[3:5])
                    elif ("kWh") in rectified_list and len(rectified_list) > 8:
                        kwh = " ".join(rectified_list[3:6])
                    else:
                        kwh = None

                    mapped_cols = {"date": col1_date, "value": col1, "kwh": kwh}
                    return mapped_cols
                elif len(rectified_list) == 3 or len(rectified_list) == 4:
                    col1 = " ".join(rectified_list[2:])
                    if re.search(r"\d{1}\s(kWh)", rectified_list[-1]):
                        col1 = rectified_list[2]
                        kwh = rectified_list[-1]
                    elif "kWh" in rectified_list:
                        kwh = " ".join(rectified_list[-1])
                    else:
                        kwh = None
                    mapped_cols = {"date": col1_date, "value": col1, "kwh": kwh}
                    return mapped_cols
                elif len(rectified_list) == 5:
                    col1 = rectified_list[2]
                    if re.search(r"\d{1}\s(kWh)", rectified_list[-1]):
                        col1 = " ".join(rectified_list[2:4])
                        kwh = rectified_list[-1]
                    elif "kWh" in rectified_list:
                        kwh = " ".join(rectified_list[3:])
                    else:
                        kwh = None
                    mapped_cols = {"date": col1_date, "value": col1, "kwh": kwh}
                    return mapped_cols
                elif len(rectified_list) >= 5:
                    col1 = " ".join(rectified_list[2:4])
                    if "kWh" in rectified_list:
                        kwh = " ".join(rectified_list[4:])
                    else:
                        kwh = None
                    mapped_cols = {"date": col1_date, "value": col1, "kwh": kwh}
                    return mapped_cols

        except Exception as e:
            print("Error in processing ms :", e)
