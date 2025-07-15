import sys
from dynamsoft_capture_vision_bundle import *
import os
import re
from pathlib import Path
from collections import defaultdict

def group_by_first_layer(paths):
    grouped = defaultdict(list)
    for path in paths:
        first_layer = path.split('.')[0]
        grouped[first_layer].append(path)
    return grouped

def is_ai(x):
    return re.fullmatch(r"\d+|(\d+n)", x) is not None

class GS1AIResult:

    def __init__(self, item: ParsedResultItem):
        self.data = []
        names = item.get_all_field_names()
        grouped = group_by_first_layer(names)
        for name, values in grouped.items():
            if is_ai(name):
                ai = None
                data = None
                for value in values:
                    if value.split('.')[-1] == name + 'AI':
                        ai = item.get_field_value(value)
                    elif value.split('.')[-1] == name + 'Data':
                        data = item.get_field_value(value)
                self.data.append([name, ai, data])
    def to_string(self) ->str:
        ret = ""
        ret +="\n".join(f"AI: {name} ({ai}), Value: {data}" for name, ai, data in self.data)
        return ret.strip()

def print_results(result: ParsedResult) -> None:
    tag = result.get_original_image_tag()
    if isinstance(tag, FileImageTag):
        print("File:", tag.get_file_path())
    if result.get_error_code() != EnumErrorCode.EC_OK and result.get_error_code()!= EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
        print("Error:", result.get_error_string())
    else:
        items = result.get_items()
        print("Parsed", len(items), "GS1 AI(s).")
        for item in items:
            dlResult = GS1AIResult(item)
            print(dlResult.to_string())

def current_dir() -> Path:
    return Path(__file__).parent

if __name__ == '__main__':

    print("**********************************************************")
    print("Welcome to Dynamsoft Capture Vision - GS1 AI Sample")
    print("**********************************************************")

    # Initialize license.
    # You can request and extend a trial license from https://www.dynamsoft.com/customer/license/trialLicense?product=dcv&utm_source=samples&package=python
    # The string 'DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9' here is a free public trial license. Note that network connection is required for this license to work.
    error_code, error_message = LicenseManager.init_license("DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9")
    if error_code != EnumErrorCode.EC_OK and error_code != EnumErrorCode.EC_LICENSE_WARNING:
        print("License initialization failed: ErrorCode:", error_code, ", ErrorString:", error_message)
    else:
        cvr_instance = CaptureVisionRouter()
        template_path = str(current_dir()/"../CustomTemplates/ReadGS1AIBarcode.json")
        errorCode, errorMsg = cvr_instance.init_settings_from_file(template_path)
        if errorCode != EnumErrorCode.EC_OK:
            raise Exception("Init template failed: " + errorMsg)
        while (True):
            image_path = input(
                ">> Input your image full path:\n"
                ">> 'Enter' for sample image or 'Q'/'q' to quit\n"
            ).strip('\'"')

            if image_path.lower() == "q":
                sys.exit(0)

            if image_path == "":
                image_path = str(current_dir()/"../images/gs1-ai-sample.png")

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            result_array = cvr_instance.capture_multi_pages(image_path, "ReadGS1AIBarcode")
            results = result_array.get_results()
            if results is None or len(results) == 0:
                print("No results.")
            else:
                for i, result in enumerate(results):
                    if result.get_error_code() == EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
                        print("Warning:", result.get_error_code(), result.get_error_string())
                    elif result.get_error_code() != EnumErrorCode.EC_OK:
                        print("Error:", result.get_error_code(), result.get_error_string())
                    parsed_result = result.get_parsed_result()

                    if parsed_result is None or len(parsed_result.get_items()) == 0:
                        print("Page-"+str(i+1), "No parsed results.")
                    else:
                        print_results(parsed_result)
                    print()
    input("Press Enter to quit...")
