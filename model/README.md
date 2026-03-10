# QR Code Phishing Detection System

A robust machine learning pipeline for detecting phishing URLs embedded in QR codes.

## 🚀 Performance
- **Honest Accuracy**: **95.0%** (Weighted Average)
- **Leakage Prevention**: Implements **Domain-Level Splitting** to ensure metrics are not inflated by memorizing domains.
- **Verification**: Strictly verified with **5-Fold Cross-Validation**.

## 🛠️ Features Analyzed
A total of **15 advanced features** are extracted from decoded URLs, including:
- **Brand Detection**: Identification of impersonated tech/finance brands (Google, Yahoo, PayPal, etc.).
- **Subdomain Analysis**: Depth and length of subdomains to catch stealthy links.
- **Structural Signals**: Entropy, digit ratios, and directory depth.

## 📁 Project Structure
- `model/train_model.py`: Script to collect data and train the classifier with regularization.
- `model/predict.py`: Flexible script to predict the safety of an individual image.
- `preprocessing/feature_extraction.py`: Advanced URL logic.
- `output/`: Directory where the trained model and performance reports are saved.

## 🚀 Usage

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Training the Model
```bash
python model/train_model.py
```

### 3. Prediction
You can predict any image by simply passing its path:
```bash
python model/predict.py your_image.png
```
Or use the `--path` flag:
```bash
python model/predict.py --path your_image.png
```

## 📊 Evaluation
The model avoids "shortcuts" like HTTPS bias, forcing it to learn genuine structural patterns of phishing URLs. This makes it much more robust in real-world scenarios.
