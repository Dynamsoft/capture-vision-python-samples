import sys
from dynamsoft_capture_vision_bundle import *
import os

class VINResult:

    def __init__(self, item: ParsedResultItem):
        self.vin_string = None
        self.wmi = None
        self.region = None
        self.vds = None
        self.vis = None
        self.model_year = None
        self.plant_code = None
        self.code_type = item.get_code_type()
        if self.code_type != "VIN":
            return
        if item.get_field_value("vinString") != None:
            self.vin_string = item.get_field_value("vinString")
            if(item.get_field_validation_status("vinString")==EnumValidationStatus.VS_FAILED):
                self.vin_string += ", Validation Failed"

        if item.get_field_value("WMI") != None and item.get_field_validation_status("WMI") != EnumValidationStatus.VS_FAILED:
            self.wmi = item.get_field_value("WMI")

        if item.get_field_value("region") != None and item.get_field_validation_status("region") != EnumValidationStatus.VS_FAILED:
            self.region = item.get_field_value("region")

        if item.get_field_value("VDS") != None and item.get_field_validation_status("VDS") != EnumValidationStatus.VS_FAILED:
            self.vds = item.get_field_value("VDS")

        if item.get_field_value("VIS") != None and item.get_field_validation_status("VIS") != EnumValidationStatus.VS_FAILED:
            self.vis = item.get_field_value("VIS")

        if item.get_field_value("modelYear") != None and item.get_field_validation_status("modelYear") != EnumValidationStatus.VS_FAILED:
            self.model_year = item.get_field_value("modelYear")

        if item.get_field_value("plantCode") != None and item.get_field_validation_status("plantCode") != EnumValidationStatus.VS_FAILED:
            self.plant_code = item.get_field_value("plantCode")

    def to_string(self):
        return (f"VIN String: {self.vin_string}\n"
            f"Parsed Information:\n"
            f"\tWMI: {self.wmi or ''}\n"
            f"\tRegion: {self.region or ''}\n"
            f"\tVDS: {self.vds or ''}\n"
            f"\tVIS: {self.vis or ''}\n"
            f"\tModelYear: {self.model_year or ''}\n"
            f"\tPlantCode: {self.plant_code or ''}\n")

def print_results(result: ParsedResult) -> None:
    tag = result.get_original_image_tag()
    if isinstance(tag, FileImageTag):
        print("File:", tag.get_file_path())
    if result.get_error_code() != EnumErrorCode.EC_OK and result.get_error_code()!= EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
        print("Error:", result.get_error_string())
    else:
        items = result.get_items()
        print("Parsed", len(items), "VIN codes.")
        for item in items:
            vin_result = VINResult(item)
            print(vin_result.to_string())

if __name__ == '__main__':

    print("**********************************************************")
    print("Welcome to Dynamsoft Capture Vision - VIN Sample")
    print("**********************************************************")

    # Initialize license.
    # You can request and extend a trial license from https://www.dynamsoft.com/customer/license/trialLicense?product=dcv&utm_source=samples&package=python
    # The string 'DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9' here is a free public trial license. Note that network connection is required for this license to work.
    error_code, error_message = LicenseManager.init_license("DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9")
    if error_code != EnumErrorCode.EC_OK and error_code != EnumErrorCode.EC_LICENSE_WARNING:
        print("License initialization failed: ErrorCode:", error_code, ", ErrorString:", error_message)
    else:
        cvr_instance = CaptureVisionRouter()
        while (True):
            image_path = input(">> Enter the image path (or 'Q'/'q' to quit):").strip(' \'"')
            if image_path == "":
                print("Invalid path.")
                continue

            if image_path.lower() == "q":
                sys.exit(0)

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            while(True):
                print(">> Step 2: Choose a Mode Number:")
                print("1. Read VIN from Barcode")
                print("2. Read VIN from Text")
                try:
                    mode = int(input())
                    if mode == 1 or mode == 2:
                        template_name = "ReadVINBarcode" if mode == 1 else "ReadVINText"
                        break
                except ValueError:
                    continue

            result_array = cvr_instance.capture_multi_pages(image_path, template_name)
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
