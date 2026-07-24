from dynamsoft_capture_vision_bundle import *
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def print_results(result: ParsedResult) -> None:
    tag = result.get_original_image_tag()
    if isinstance(tag, FileImageTag):
        print("File:", tag.get_file_path())
    if result.get_error_code() != EnumErrorCode.EC_OK and result.get_error_code()!= EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
        print("Error:", result.get_error_string())
    else:
        items = result.get_items()
        print("Parsed", len(items), "Driver License(s).")
        for item in items:
            code_type = item.get_code_type()
            print_data = []
            if code_type == "AAMVA_DL_ID":
                # For full field list and details, please refer to the documentation:
                # https://www.dynamsoft.com/code-parser/docs/core/code-types/aamva-dl-id.html?lang=python#aamva_dl_id-fields

                if item.get_field_value("licenseNumber") != None and item.get_field_validation_status("licenseNumber") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("License Number: ", item.get_field_value("licenseNumber")))
                if item.get_field_value("vehicleClass") != None and item.get_field_validation_status("vehicleClass") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Vehicle Class: ", item.get_field_value("vehicleClass")))
                full_name = None
                if item.get_field_value("fullName") != None and item.get_field_validation_status("fullName") != EnumValidationStatus.VS_FAILED:
                    full_name = item.get_field_value("fullName")
                elif item.get_field_value("givenName") != None and item.get_field_validation_status("givenName") != EnumValidationStatus.VS_FAILED:
                    full_name = item.get_field_value("givenName")
                    if item.get_field_value("lastName") != None and item.get_field_validation_status("lastName") != EnumValidationStatus.VS_FAILED:
                        full_name += " " + item.get_field_value("lastName")
                elif item.get_field_value("firstName") != None and item.get_field_validation_status("firstName") != EnumValidationStatus.VS_FAILED:
                    full_name = item.get_field_value("firstName")
                    if item.get_field_value("middleName") != None and item.get_field_validation_status("middleName") != EnumValidationStatus.VS_FAILED:
                        full_name += " " + item.get_field_value("middleName")
                    if item.get_field_value("lastName") != None and item.get_field_validation_status("lastName") != EnumValidationStatus.VS_FAILED:
                        full_name += " " + item.get_field_value("lastName")
                if full_name != None:
                    print_data.append(("Full Name: ", full_name))
                if item.get_field_value("sex") != None and item.get_field_validation_status("sex") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Sex: ", item.get_field_value("sex")))
                if item.get_field_value("expirationDate") != None and item.get_field_validation_status("expirationDate") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Expiration Date: ", item.get_field_value("expirationDate")))
            elif code_type == "AAMVA_DL_ID_WITH_MAG_STRIPE":
                # For full field list and details, please refer to the documentation:
                # https://www.dynamsoft.com/code-parser/docs/core/code-types/aamva-dl-id.html?lang=python#aamva_dl_id_with_mag_stripe-fields

                if item.get_field_value("DLorID_Number") != None and item.get_field_validation_status("DLorID_Number") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("License Number: ", item.get_field_value("DLorID_Number")))
                if item.get_field_value("ISOIIN") != None and item.get_field_validation_status("ISOIIN") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("ISO IIN: ", item.get_field_value("ISOIIN")))
                if item.get_field_value("name") != None and item.get_field_validation_status("name") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Name: ", item.get_field_value("name")))
                if item.get_field_value("sex") != None and item.get_field_validation_status("sex") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Sex: ", item.get_field_value("sex")))
                if item.get_field_value("expirationDate") != None and item.get_field_validation_status("expirationDate") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Expiration Date: ", item.get_field_value("expirationDate")))
            elif code_type == "SOUTH_AFRICA_DL":
                # For full field list and details, please refer to the documentation:
                # https://www.dynamsoft.com/code-parser/docs/core/code-types/za-dl.html?lang=python#fields

                if item.get_field_value("idNumber") != None and item.get_field_validation_status("idNumber") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("ID Number: ", item.get_field_value("idNumber")))
                if item.get_field_value("licenseNumber") != None and item.get_field_validation_status("licenseNumber") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("License Number: ", item.get_field_value("licenseNumber")))
                if item.get_field_value("vehicleLicense") != None and item.get_field_validation_status("vehicleLicense") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Vehicle License: ", item.get_field_value("vehicleLicense")))
                full_name = None
                if item.get_field_value("surname") != None and item.get_field_validation_status("surname") != EnumValidationStatus.VS_FAILED:
                    full_name = item.get_field_value("surname")
                    if item.get_field_value("initials") != None and item.get_field_validation_status("initials") != EnumValidationStatus.VS_FAILED:
                        full_name += " " + item.get_field_value("initials")
                if full_name != None:
                    print_data.append(("Name: ", full_name))
                if item.get_field_value("gender") != None and item.get_field_validation_status("gender") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("Gender: ", item.get_field_value("gender")))
                if item.get_field_value("licenseValidityTo") != None and item.get_field_validation_status("licenseValidityTo") != EnumValidationStatus.VS_FAILED:
                    print_data.append(("License Valid To: ", item.get_field_value("licenseValidityTo")))
            print("Parsed Information:")
            for data in print_data:
                print("\t" + data[0], data[1])
            print()
if __name__ == '__main__':

    print("**********************************************************")
    print("Welcome to Dynamsoft Capture Vision - DriverLicense Sample")
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
            image_path = input(
                ">> Input your image full path:\n"
                ">> 'Enter' for sample image or 'Q'/'q' to quit\n"
            ).strip(' \'"')

            if image_path.lower() == "q":
                sys.exit(0)

            if image_path == "":
                image_path = str(BASE_DIR.parent / "Images" / "driver-license-sample.jpg")

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            result_array = cvr_instance.capture_multi_pages(image_path, "ReadDriversLicense")
            results = result_array.get_results()
            if results is None or len(results) == 0:
                print("No results.")
            else:
                for i, result in enumerate(results):
                    page_number = i + 1
                    tag = result.get_original_image_tag()
                    if isinstance(tag, FileImageTag):
                        page_number = tag.get_page_number() + 1
                    if result.get_error_code() == EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
                        print("Warning:", result.get_error_code(), result.get_error_string())
                    elif result.get_error_code() != EnumErrorCode.EC_OK:
                        print("Error:", result.get_error_code(), result.get_error_string())
                    parsed_result = result.get_parsed_result()

                    if parsed_result is None or len(parsed_result.get_items()) == 0:
                        print("Page-"+str(page_number), "No parsed results.")
                    else:
                        print_results(parsed_result)
                    print()
    input("Press Enter to quit...")
