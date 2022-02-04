from src.utils.util import Logger
from src.utils.post_processing.base import AggregateBase
import copy


class Aggregate(AggregateBase):
    
    @Logger(module_name="partition_regions", logtime=True)
    def segment_layout_regions(self):

        self.meta = self.layouts[0]
        segments = [[]]
        last_class = "fm"

        for region in self.layouts[1:]:
            cls = region["class"]
            # print(cls)
            if cls not in self.skip_class:
                # print(cls, last_class, self.skip_class)

                if cls in ["fm2", "fm1"] and "fm" not in last_class:
                    segments.append([region])
                else:
                    segments[-1].append(region)
                last_class = cls
        self.layout_segments = segments

    def merge(self, segment):
        segment = self.merge_ms(segment)
        segment = self.meger_fd(segment)
        return segment

    @Logger(module_name="megre_fd")
    def meger_fd(self, segment):
        rectified_segment = []
        index = 0
        while index < len(segment):
            # print(segment[index]["class"])
            if segment[index]["class"] == "fd" and segment[index + 1]["class"] == "fd":
                segment[index]["data"]["invoiceRows"] += segment[index + 1]["data"][
                    "invoiceRows"
                ]
                if segment[index]["data"]["VAT"] == None:
                    segment[index]["data"]["VAT"] = segment[index + 1]["data"]["VAT"]
                rectified_segment.append(segment[index])
                index += 2
            else:
                rectified_segment.append(segment[index])
                index += 1
        return rectified_segment

    @Logger(module_name="merge_ms")
    def merge_ms(self, maped_data):
        try:
            for index, elem in enumerate(maped_data):

                if (
                    maped_data[index].get("class") == "ms"
                    and (maped_data[index]["data"].get("meterNumber") == None)
                    and maped_data[index - 2].get("class") == "ms"
                    and maped_data[index - 2]["data"].get("meterNumber") != None
                ):
                    maped_data[index - 2]["data"].get("datapoints").extend(
                        maped_data[index]["data"].get("datapoints")
                    )
                if maped_data[index].get("class") == "ms" and (
                    maped_data[index]["data"].get("meterNumber") == None
                ):
                    del maped_data[index]
                if maped_data[index].get("class") == "ms":
                    if maped_data[index]["data"]["datapoints"][1] == None:
                        maped_data[index]["data"]["datapoints"] = maped_data[index][
                            "data"
                        ]["datapoints"][2:]

                    else:
                        maped_data[index]["data"]["datapoints"] = maped_data[index][
                            "data"
                        ]["datapoints"][1:]

        except:
            pass
        return maped_data

    @Logger(module_name="transform_to_target", logtime=True)
    def transform(self):
        resopose = {}
        resopose.update(self.meta["data"])

        resopose["invoiceSections"] = []
        for segment in self.layout_segments:
            invoiceSection = {"costData": [], "meterstands": []}
            for layout in segment:
                # print(layout['class'])
                if layout["class"] in ["fm1", "fm2"]:
                    invoiceSection.update(layout["data"])
                if layout["class"] == "fm3":
                    invoiceSection["costData"].append(layout["data"])

                if layout["class"] == "fd":
                    invoiceSection["costData"][-1]["invoiceRows"] = layout["data"][
                        "invoiceRows"
                    ]
                    # invoiceSection["costData"][-1]["VAT"] = layout["data"]["VAT"]
                    if layout["data"]["VAT"] != None:
                        invoiceSection["VAT"] = layout["data"]["VAT"]

                if layout["class"] == "t":
                    if "totalCost" in layout["data"].keys():
                        invoiceSection["totalCost"] = layout["data"]["totalCost"]
                    if "totalCons" in layout["data"].keys():
                        print(invoiceSection, "insssssss", layout)
                        invoiceSection["meterstands"][-1]["totalCons"] = layout["data"][
                            "totalCons"
                        ]

                if layout["class"] == "ms":
                    invoiceSection["meterstands"].append(layout["data"])
            if (
                len(invoiceSection["costData"]) > 0
                or len(invoiceSection["meterstands"]) > 0
            ):

                resopose["invoiceSections"].append(invoiceSection)

        return resopose

    # def agg_total_cons(self,invoiceSection):
    #     if 'meterstands' in invoiceSection.keys():

    #     return None
