from dynamsoft_capture_vision_bundle import *
import sys
import os
from typing import Dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class NeededResultUnit:
    """
    A container class to hold intermediate result units required/needed for `find_portrait_zone`.
    """
    def __init__(self):
        self.deskewed_image_unit = None
        self.localized_text_lines_unit = None
        self.scaled_colour_img_unit = None
        self.detected_quads_unit = None
        self.recognized_text_lines_unit = None

class MyIntermediateResultReceiver(IntermediateResultReceiver):
    """
    Custom receiver to intercept and store intermediate processing results.

    By inheriting from `IntermediateResultReceiver`, we can hook into the processing pipeline
    of the CaptureVisionRouter to retrieve data that isn't part of the final result but
    is useful for advanced post-processing (like portrait extraction).
    """

    def __init__(self, cvr: CaptureVisionRouter):
        super().__init__()
        self.cvr = cvr
        # Dictionary to group intermediate units by their original image hash ID.
        self.unit_groups: Dict[str, NeededResultUnit] = {}

    def on_deskewed_image_received(self, result: "DeskewedImageUnit", info: IntermediateResultExtraInfo) -> None:
        if info.is_section_level_result:
            id = result.get_original_image_hash_id()
            if self.unit_groups.get(id) is None:
                self.unit_groups[id] = NeededResultUnit()
            self.unit_groups[id].deskewed_image_unit = result

    def on_localized_text_lines_received(self, result: "LocalizedTextLinesUnit", info: IntermediateResultExtraInfo) -> None:
        if info.is_section_level_result:
            id = result.get_original_image_hash_id()
            if self.unit_groups.get(id) is None:
                self.unit_groups[id] = NeededResultUnit()
            self.unit_groups[id].localized_text_lines_unit = result
    def on_scaled_colour_image_unit_received(self, result: ScaledColourImageUnit, info: IntermediateResultExtraInfo) -> None:
        id = result.get_original_image_hash_id()
        if self.unit_groups.get(id) is None:
            self.unit_groups[id] = NeededResultUnit()
        self.unit_groups[id].scaled_colour_img_unit = result

    def on_recognized_text_lines_received(self, result: RecognizedTextLinesUnit, info: IntermediateResultExtraInfo) -> None:
        if info.is_section_level_result:
            id = result.get_original_image_hash_id()
            if self.unit_groups.get(id) is None:
                self.unit_groups[id] = NeededResultUnit()
            self.unit_groups[id].recognized_text_lines_unit = result
    def on_detected_quads_received(self, result: DetectedQuadsUnit, info: IntermediateResultExtraInfo) -> None:
        if info.is_section_level_result:
            id = result.get_original_image_hash_id()
            if self.unit_groups.get(id) is None:
                self.unit_groups[id] = NeededResultUnit()
            self.unit_groups[id].detected_quads_unit = result
    def get_portrait_zone(self,hash_id: str) -> Quadrilateral:
        if self.unit_groups.get(hash_id) is None:
            print("get_precise_portrait_zone failed, hash_id not found:", hash_id)
            return None
        id_processor = IdentityProcessor()
        units = self.unit_groups[hash_id]
        ret, portrait_zone = id_processor.find_portrait_zone(
            units.scaled_colour_img_unit,
            units.localized_text_lines_unit,
            units.recognized_text_lines_unit,
            units.detected_quads_unit,
            units.deskewed_image_unit
        )
        if ret != EnumErrorCode.EC_OK:
            print("get_precise_portrait_zone failed, error code:", ret)
        return portrait_zone

class DCPResultProcessor:
    """
    Helper class to parse the generic `ParsedResultItem` into structured MRZ data.
    """
    def __init__(self, item: ParsedResultItem):
        self.doc_type = item.get_code_type()
        self.raw_text = []
        self.doc_id = None
        self.surname = None
        self.given_name = None
        self.nationality = None
        self.issuer = None
        self.gender = None
        self.date_of_birth = None
        self.date_of_expiry = None
        self.is_passport = False
        if self.doc_type == "MRTD_TD3_PASSPORT":
            if item.get_field_value("passportNumber") != None and item.get_field_validation_status("passportNumber") != EnumValidationStatus.VS_FAILED:
                self.doc_id = item.get_field_value("passportNumber")
            elif item.get_field_value("documentNumber") != None and item.get_field_validation_status("documentNumber") != EnumValidationStatus.VS_FAILED:
                self.doc_id = item.get_field_value("documentNumber")
            self.is_passport = True

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

    def get_string_result(self):
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

def save_processed_document_result(result:CapturedResult, page_number:int, image_path:str):
    processed_document_result = result.get_processed_document_result()
    if processed_document_result is None or len(processed_document_result.get_enhanced_image_result_items()) == 0:
        print("Page-"+str(page_number), "No processed document result found.")
        return
    items = processed_document_result.get_enhanced_image_result_items()
    if len(items) > 0:
        out_path = Path(image_path).stem + "_" + str(page_number) + "_document.png"
        image_io = ImageIO()
        image = items[0].get_image_data()
        if image != None:
            errorCode, errorMsg = image_io.save_to_file(image, out_path)
            if errorCode == 0:
                print("Document file: " + out_path)
            else:
                print("Save processed document failed, error:", errorCode, errorMsg)

def save_portrait(
        irr:MyIntermediateResultReceiver,
        hash_id:str,
        original_image:ImageData,
        page_number:int,
        image_path:str
        ) -> None:
    quad = irr.get_portrait_zone(hash_id)
    if quad is None:
        return
    if original_image is None:

        return
    image_processor = ImageProcessor()
    ret, out_image = image_processor.crop_and_deskew_image(original_image, quad)
    if ret != EnumErrorCode.EC_OK:
        print("crop image failed, error code:", ret)
        return
    output_path = Path(image_path).stem + "_"+str(page_number)+"_Portrait.png"
    image_io = ImageIO()
    error_code, error_msg = image_io.save_to_file(out_image, output_path)
    if error_code == 0:
        print("Portrait file: " + output_path)
    else:
        print("Save portrait failed, error:", error_code, error_msg)
def get_original_image(result:CapturedResult)->ImageData:
    for item in result.get_items():
        if isinstance(item, OriginalImageResultItem):
            image = item.get_image_data()
            return image
    return None
def process_result(
        result: CapturedResult,
        irr:MyIntermediateResultReceiver,
        print_index:int,
        image_path:str
        ) -> None:
    page_number = print_index + 1
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
        return

    hash_id = result.get_original_image_hash_id()
    is_passport = False

    if parsed_result.get_error_code() != EnumErrorCode.EC_OK and parsed_result.get_error_code() != EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
        print("Error:", parsed_result.get_error_string())
    else:
        items = parsed_result.get_items()
        print("Parsed", len(items), "MRZ Zones.")
        for item in items:
            mrz_result = DCPResultProcessor(item)
            if not is_passport:
                is_passport = mrz_result.is_passport
            print(mrz_result.get_string_result())
    if is_passport:
        oi = get_original_image(result)
        save_portrait(irr,hash_id,oi, page_number, image_path)
        save_processed_document_result(result,page_number, image_path)

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
        # Create the CaptureVisionRouter instance
        cvr_instance = CaptureVisionRouter()

        # Access the IntermediateResultManager to manage result receivers
        # We need to add a custom receiver to collect data for portrait extraction
        irm = cvr_instance.get_intermediate_result_manager()
        my_intermediate_result_receiver = None

        while (True):
            # Refresh receiver for each session
            if my_intermediate_result_receiver is not None:
                irm.remove_result_receiver(my_intermediate_result_receiver)

            # Setup custom receiver to collect data for portrait extraction
            my_intermediate_result_receiver = MyIntermediateResultReceiver(cvr_instance)
            irm.add_result_receiver(my_intermediate_result_receiver)

            # Get the full path of the image
            image_path = input(
                ">> Input your image full path:\n"
                ">> 'Enter' for sample image or 'Q'/'q' to quit\n"
            ).strip(' \'"')

            if image_path.lower() == "q":
                sys.exit(0)

            if image_path == "":
                image_path = str(BASE_DIR.parent / "Images" / "passport-sample.jpg")

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue

            # Use the "ReadPassportAndId" template preset
            # capture_multi_pages will process the image and return a full result set
            result_array = cvr_instance.capture_multi_pages(image_path, "ReadPassportAndId")

            results = result_array.get_results()
            if results is None or len(results) == 0:
                print("No results.")
            else:
                tag = results[0].get_original_image_tag()
                if isinstance(tag, FileImageTag):
                    print("File:", tag.get_file_path())
                for i, result in enumerate(results):
                    # Process the final results and utilize collected intermediate data
                    process_result(result, my_intermediate_result_receiver, i, image_path)
                    print()
    input("Press Enter to quit...")
