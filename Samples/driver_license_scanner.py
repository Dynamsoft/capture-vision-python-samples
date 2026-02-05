from dynamsoft_capture_vision_bundle import *
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class DriverLicenseResult:

    def __init__(self, item: ParsedResultItem):
        self.license_number = None
        self.version_number = None
        self.vehicle_class = None
        self.last_name = None
        self.given_name = None
        self.gender = None
        self.birth_date = None
        self.issued_date = None
        self.expiration_date = None
        self.full_name = None
        self.code_type = item.get_code_type()
        if self.code_type != "AAMVA_DL_ID" and self.code_type != "AAMVA_DL_ID_WITH_MAG_STRIPE" and self.code_type != "SOUTH_AFRICA_DL":
            return
        if item.get_field_value("licenseNumber") != None and item.get_field_validation_status("licenseNumber") != EnumValidationStatus.VS_FAILED:
            self.license_number = item.get_field_value("licenseNumber")

        if item.get_field_value("AAMVAVersionNumber") != None and item.get_field_validation_status("AAMVAVersionNumber") != EnumValidationStatus.VS_FAILED:
            self.version_number = item.get_field_value("AAMVAVersionNumber")

        if item.get_field_value("vehicleClass") != None and item.get_field_validation_status("vehicleClass") != EnumValidationStatus.VS_FAILED:
            self.vehicle_class = item.get_field_value("vehicleClass")

        if item.get_field_value("lastName") != None and item.get_field_validation_status("lastName") != EnumValidationStatus.VS_FAILED:
            self.last_name = item.get_field_value("lastName")

        if item.get_field_value("surName") != None and item.get_field_validation_status("surName") != EnumValidationStatus.VS_FAILED:
            self.last_name = item.get_field_value("surName")

        if item.get_field_value("givenName") != None and item.get_field_validation_status("givenName") != EnumValidationStatus.VS_FAILED:
            self.given_name = item.get_field_value("givenName")

        if item.get_field_value("fullName") != None and item.get_field_validation_status("fullName") != EnumValidationStatus.VS_FAILED:
            self.full_name = item.get_field_value("fullName")

        if item.get_field_value("sex") != None and item.get_field_validation_status("sex") != EnumValidationStatus.VS_FAILED:
            self.gender = item.get_field_value("sex")

        if item.get_field_value("gender") != None and item.get_field_validation_status("gender") != EnumValidationStatus.VS_FAILED:
            self.gender = item.get_field_value("gender")

        if item.get_field_value("birthDate") != None and item.get_field_validation_status("birthDate") != EnumValidationStatus.VS_FAILED:
            self.birth_date = item.get_field_value("birthDate")

        if item.get_field_value("issuedDate") != None and item.get_field_validation_status("issuedDate") != EnumValidationStatus.VS_FAILED:
            self.issued_date = item.get_field_value("issuedDate")

        if item.get_field_value("expirationDate") != None and item.get_field_validation_status("expirationDate") != EnumValidationStatus.VS_FAILED:
            self.expiration_date = item.get_field_value("expirationDate")

        if self.full_name is None:
            self.full_name = (self.last_name or "") +((' ' + self.given_name) if self.last_name and self.given_name else (self.given_name or ''))

    def to_string(self):
        return (f"Parsed Information:\n"
            f"\tCode Type: {self.code_type or ''}\n"
            f"\tLicense Number: {self.license_number or ''}\n"
            f"\tVehicle Class: {self.vehicle_class or ''}\n"
            f"\tLast Name: {self.last_name or ''}\n"
            f"\tGiven Name: {self.given_name or ''}\n"
            f"\tFull Name: {self.full_name or ''}\n"
            f"\tGender: {self.gender or ''}\n"
            f"\tDate of Birth: {self.birth_date or ''}\n"
            f"\tIssued Date: {self.issued_date or ''}\n"
            f"\tExpiration Date: {self.expiration_date or ''}\n")


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
            dlResult = DriverLicenseResult(item)
            print(dlResult.to_string())

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
