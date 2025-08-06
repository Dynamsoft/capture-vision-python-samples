
import sys
from dynamsoft_capture_vision_bundle import *
import os

class MRZResult:
    def __init__(self, item: ParsedResultItem):
        self.doc_type = item.get_code_type()
        self.raw_text=[]
        self.doc_id = None
        self.surname = None
        self.given_name = None
        self.nationality = None
        self.issuer = None
        self.gender = None
        self.date_of_birth = None
        self.date_of_expiry = None
        if self.doc_type == "MRTD_TD3_PASSPORT":
            if item.get_field_value("passportNumber") != None and item.get_field_validation_status("passportNumber") != EnumValidationStatus.VS_FAILED:
                self.doc_id = item.get_field_value("passportNumber")
            elif item.get_field_value("documentNumber") != None and item.get_field_validation_status("documentNumber") != EnumValidationStatus.VS_FAILED:
                self.doc_id = item.get_field_value("documentNumber")

        line = item.get_field_value("line1")
        if line is not None:
            if item.get_field_validation_status("line1") == EnumValidationStatus.VS_FAILED:
                line += ", Validation Failed"
            self.raw_text.append(line)
        line = item.get_field_value("line2")
        if line is not None:
            if item.get_field_validation_status("line2") == EnumValidationStatus.VS_FAILED:
                line += ", Validation Failed"
            self.raw_text.append(line)
        line = item.get_field_value("line3")
        if line is not None:
            if item.get_field_validation_status("line3") == EnumValidationStatus.VS_FAILED:
                line += ", Validation Failed"
            self.raw_text.append(line)

        if item.get_field_value("nationality") != None and item.get_field_validation_status("nationality") != EnumValidationStatus.VS_FAILED:
            self.nationality = item.get_field_value("nationality")
        if item.get_field_value("issuingState") != None and item.get_field_validation_status("issuingState") != EnumValidationStatus.VS_FAILED:
            self.issuer = item.get_field_value("issuingState")
        if item.get_field_value("dateOfBirth") != None and item.get_field_validation_status("dateOfBirth") != EnumValidationStatus.VS_FAILED:
            self.date_of_birth = item.get_field_value("dateOfBirth")
        if item.get_field_value("dateOfExpiry") != None and item.get_field_validation_status("dateOfExpiry") != EnumValidationStatus.VS_FAILED:
            self.date_of_expiry = item.get_field_value("dateOfExpiry")
        if item.get_field_value("sex") != None and item.get_field_validation_status("sex") != EnumValidationStatus.VS_FAILED:
            self.gender = item.get_field_value("sex")
        if item.get_field_value("primaryIdentifier") != None and item.get_field_validation_status("primaryIdentifier") != EnumValidationStatus.VS_FAILED:
            self.surname = item.get_field_value("primaryIdentifier")
        if item.get_field_value("secondaryIdentifier") != None and item.get_field_validation_status("secondaryIdentifier") != EnumValidationStatus.VS_FAILED:
            self.given_name = item.get_field_value("secondaryIdentifier")
    def to_string(self):
        msg = (f"Raw Text:\n")
        for index, line in enumerate(self.raw_text):
            msg += (f"\tLine {index + 1}: {line}\n")
        msg+=(f"Parsed Information:\n"
            f"\tDocumentType: {self.doc_type or ''}\n"
            f"\tDocumentID: {self.doc_id or ''}\n"
            f"\tSurname: {self.surname or ''}\n"
            f"\tGivenName: {self.given_name or ''}\n"
            f"\tNationality: {self.nationality or ''}\n"
            f"\tIssuingCountryorOrganization: {self.issuer or ''}\n"
            f"\tGender: {self.gender or ''}\n"
            f"\tDateofBirth(YYMMDD): {self.date_of_birth or ''}\n"
            f"\tExpirationDate(YYMMDD): {self.date_of_expiry or ''}\n")
        return msg
def print_results(result: ParsedResult) -> None:
    tag = result.get_original_image_tag()
    if isinstance(tag, FileImageTag):
        print("File:", tag.get_file_path())
    if result.get_error_code() != EnumErrorCode.EC_OK and result.get_error_code()!= EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
        print("Error:", result.get_error_string())
    else:
        items = result.get_items()
        print("Parsed", len(items), "MRZ Zones.")
        for item in items:
            mrz_result = MRZResult(item)
            print(mrz_result.to_string())

if __name__ == '__main__':

    print("**********************************************************")
    print("Welcome to Dynamsoft Capture Vision - MRZ Sample")
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
                image_path = "../images/passport-sample.jpg"

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            result_array = cvr_instance.capture_multi_pages(image_path, "ReadPassportAndId")
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
