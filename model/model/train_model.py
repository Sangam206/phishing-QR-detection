import sys
import os
import re
import pickle
import numpy as np
import pandas as pd
from test_images.glob import glob
from urllib.parse import urlparse

import cv2
from pyzbar.pyzbar import decode
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report

# Add the main folder to Python so it can find feature_extraction.py
import sys
from pathlib import Path
main_folder = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, main_folder)

from preprocessing.feature_extraction import extract_features

def read_qr_url(image_path):
    # Open the image file
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    # Try to find a QR code in the image
    qr_data = decode(image)
    if not qr_data:
        return None
        
    # Return the URL text inside the QR code
    return qr_data[0].data.decode("utf-8")

def get_website_name(url):
    # Get just the basic name, like "google.com" from "http://www.google.com/search"
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    
    website_name = url.split("/")[0]
    
    if website_name.startswith("www."):
        website_name = website_name[4:]
        
    return website_name

print("Step 1: Loading all images...")

# Find all the PNG images in our two folders
safe_images = glob(main_folder + "/dataset/notspam/*.png")
spam_images = glob(main_folder + "/dataset/spam/*.png")

url_data_list = []
urls_already_seen = []

# Process safe images
print("Reading SAFE images...")
for path in safe_images:
    url = read_qr_url(path)
    if url is not None:
        if url not in urls_already_seen:
            urls_already_seen.append(url)
            
            # Save the URL, its website name, and '0' for Safe
            url_data_list.append({
                "url": url,
                "website": get_website_name(url),
                "is_dangerous": 0
            })
            
    # Stop if we collected 10,000 safe ones to save time
    if len(url_data_list) >= 10000:
        break

# Process spam images
print("Reading SPAM images...")
for path in spam_images:
    url = read_qr_url(path)
    if url is not None:
        if url not in urls_already_seen:
            urls_already_seen.append(url)
            
            # Save the URL, its website name, and '1' for Dangerous
            url_data_list.append({
                "url": url,
                "website": get_website_name(url),
                "is_dangerous": 1
            })
            
    # Stop if we collected 20,000 total to save time
    if len(url_data_list) >= 20000:
        break

# Convert our list into a Pandas DataFrame table
dataset_table = pd.DataFrame(url_data_list)
print("Total unique URLs loaded:", len(dataset_table))

print("Step 2: Splitting data into Training and Testing...")
# We group by the website name so the AI doesn't just memorize the name
websites = dataset_table['website'].unique()
train_websites, test_websites = train_test_split(websites, test_size=0.2, random_state=42)

# Create training and testing tables
train_table = dataset_table[dataset_table['website'].isin(train_websites)]
test_table = dataset_table[dataset_table['website'].isin(test_websites)]

print("Step 3: Calculating mathematical features for every URL...")
X_train = []
for url in train_table['url']:
    features = extract_features(url)
    X_train.append(features)
    
y_train = train_table['is_dangerous'].tolist()

X_test = []
for url in test_table['url']:
    features = extract_features(url)
    X_test.append(features)
    
y_test = test_table['is_dangerous'].tolist()

print("Step 4: Training the AI model...")
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)
model.fit(X_train, y_train)

print("Step 5: Testing the model to see how smart it is...")
predicted_answers = model.predict(X_test)

print("\n--- Model Scorecard ---")
print(classification_report(y_test, predicted_answers, target_names=["Safe", "Malicious"]))

print("Step 6: Saving the trained AI to a file...")
save_folder = main_folder + "/output"
os.makedirs(save_folder, exist_ok=True)

with open(save_folder + "/qr_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("All done! Model is ready to use.")