from dynamsoft_capture_vision_bundle import *
import os
import sys
if __name__ == '__main__':
    # Initialize license.
    # You can request and extend a trial license from https://www.dynamsoft.com/customer/license/trialLicense?product=dcv&utm_source=samples&package=python
    # The string 'DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9' here is a free public trial license. Note that network connection is required for this license to work.
    errorCode, errorMsg = LicenseManager.init_license("DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9")
    if errorCode != EnumErrorCode.EC_OK and errorCode != EnumErrorCode.EC_LICENSE_WARNING:
        print("License initialization failed: ErrorCode:", errorCode, ", ErrorString:", errorMsg)
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
                image_path = "../images/document-sample.jpg"

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            result_array = cvr_instance.capture_multi_pages(image_path, EnumPresetTemplate.PT_DETECT_AND_NORMALIZE_DOCUMENT)
            results = result_array.get_results()
            if results is None or len(results) == 0:
                print("No document found.")
            else:
                for i, result in enumerate(results):
                    if result.get_error_code() == EnumErrorCode.EC_UNSUPPORTED_JSON_KEY_WARNING:
                        print("Warning:", result.get_error_code(), result.get_error_string())
                    elif result.get_error_code() != EnumErrorCode.EC_OK:
                        print("Error:", result.get_error_code(), result.get_error_string())
                    processed_document_result = result.get_processed_document_result()
                    if processed_document_result is None or len(processed_document_result.get_deskewed_image_result_items()) == 0:
                        print("Page-"+str(i+1), "No document found.")
                    else:
                        items = processed_document_result.get_deskewed_image_result_items()
                        print("Page-"+str(i+1), "Deskewed", len(items), "documents.")
                        for index,item in enumerate(items):
                            out_path = "Page_"+str(i+1)+"_deskewedResult_" + str(index) + ".png"
                            image_io = ImageIO()
                            image = item.get_image_data()
                            if image != None:
                                errorCode, errorMsg = image_io.save_to_file(image, out_path)
                                if errorCode == 0:
                                    print("Document " + str(index) + " file: " + out_path)
                            print()
    input("Press Enter to quit...")