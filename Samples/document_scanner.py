from dynamsoft_capture_vision_bundle import *
import os
import sys
if __name__ == '__main__':
    # Initialize license.
    # You can request and extend a trial license from https://www.dynamsoft.com/customer/license/trialLicense?product=dcv&utm_source=samples&package=python
    # The string 'DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9' here is a free public trial license. Note that network connection is required for this license to work.
    errorCode, errorMsg = LicenseManager.init_license("DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9")
    if errorCode != EnumErrorCode.EC_OK and errorCode != EnumErrorCode.EC_LICENSE_CACHE_USED:
        print("License initialization failed: ErrorCode:", errorCode, ", ErrorString:", errorMsg)
    else:
        cvr = CaptureVisionRouter()
        while (True):
            image_path = input(
                ">> Input your image full path:\n"
                ">> 'Enter' for sample image or 'Q'/'q' to quit\n"
            ).strip('\'"')

            if image_path.lower() == "q":
                sys.exit(0)

            if image_path == "":
                image_path = "../images/document-sample.jpg"

            if not os.path.exists(image_path):
                print("The image path does not exist.")
                continue
            result = cvr.capture(image_path, EnumPresetTemplate.PT_DETECT_AND_NORMALIZE_DOCUMENT)
            if result.get_error_code() != EnumErrorCode.EC_OK:
                print("Error:", result.get_error_code(), result.get_error_string())
            normalized_images_result = result.get_normalized_images_result()
            if normalized_images_result is None or len(normalized_images_result.get_items()) == 0:
                print("No normalized documents.")
            else:
                items = normalized_images_result.get_items()
                print("Normalized", len(items), "documents.")
                for index,item in enumerate(normalized_images_result.get_items()):                   
                    out_path = "normalizedResult_" + str(index) + ".png"
                    image_manager = ImageManager()
                    image = item.get_image_data()
                    if image != None:
                        errorCode, errorMsg = image_manager.save_to_file(image, out_path)
                        if errorCode == 0:
                            print("Document " + str(index) + " file: " + out_path)
    input("Press Enter to quit...")