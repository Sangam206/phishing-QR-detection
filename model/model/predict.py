import sys
import pickle
import cv2
from pyzbar.pyzbar import decode

# Add the main folder to Python so it can find feature_extraction.py
import sys
from pathlib import Path
main_folder = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, main_folder)

from preprocessing.feature_extraction import extract_features

def check_if_safe(image_file_path):
    print("-----------------------------------")
    print("Checking image:", image_file_path)
    
    # Step 1: Tell Python where the saved model file is
    model_file_path = main_folder + "/output/qr_model.pkl"
    
    # Step 2: Open the saved model file
    try:
        with open(model_file_path, "rb") as file:
            ai_model = pickle.load(file)
    except:
        print("Error: Could not find the model file. Did you run train_model.py first?")
        return

    # Step 3: Open the image
    image = cv2.imread(image_file_path)
    if image is None:
        print("Error: Could not open the image file.")
        return
        
    # Step 4: Look for a QR code in the image
    qr_codes_found = decode(image)
    if len(qr_codes_found) == 0:
        print("Error: No QR code was found in this image.")
        return

    # Step 5: Read the URL text from the QR code
    url_text = qr_codes_found[0].data.decode("utf-8")
    print("Found URL:", url_text)

    # Step 6: Turn the URL into a list of numbers (features)
    url_numbers = extract_features(url_text)
    
    # Step 7: Ask the AI to predict if those numbers mean "Safe" or "Dangerous"
    prediction_list = ai_model.predict([url_numbers])
    answer = prediction_list[0]
    
    # Ask the AI how confident it is
    probability_list = ai_model.predict_proba([url_numbers])
    safe_score = probability_list[0][0] * 100
    danger_score = probability_list[0][1] * 100
    
    print(f"Safety Score: {safe_score:.1f}% Safe, {danger_score:.1f}% Dangerous")

    # Step 8: Print the final result in plain english
    if answer == 1:
        print("FINAL RESULT: DANGEROUS! Do not click this link.")
    else:
        print("FINAL RESULT: SAFE. This link seems okay.")
    print("-----------------------------------")


if __name__ == "__main__":
    # If the user runs "python predict.py test.png", sys.argv will contain "test.png"
    if len(sys.argv) > 1:
        # Get the file name the user typed
        user_image_path = sys.argv[1]
        check_if_safe(user_image_path)
    else:
        # If the user didn't type a file name, tell them how to use it
        print("Please type an image path after the script name.")
        print("Example: python predict.py my_image.png")
