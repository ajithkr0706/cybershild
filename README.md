# CyberShield AI - Security Detection System

Advanced AI-powered security detection system with dual capabilities for detecting **phishing URLs** and **fake/spam messages** in real-time.

## Features

✨ **Phishing URL Detection** - Analyzes URLs using 11 heuristic features to detect phishing attempts  
✨ **Fake Message Detection** - Detects spam, phishing messages, and scam content in text messages  
🔐 **Secure Web Interface** - Professional SOC dashboard with real-time threat analysis  
📊 **Advanced Analytics** - Track threat metrics and view detection history  
👤 **User Authentication** - Demo login with email/password  

## Quick Start

### 1. Setup Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Train Models

Train the **Phishing URL Detection Model**:
```bash
python train_model.py
```

Train the **Fake Message Detection Model**:
```bash
python train_message_model.py
```

### 3. Run the Application

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser

**Demo Credentials:**
- Email: `yadavmahendhar65@gmail.com`
- Password: `Mahi@123456`

## Features & How They Work

### URL Phishing Detection

Analyzes URLs using 11 features:
- URL length and hostname analysis
- IP address detection in hostname
- HTTPS/SSL verification
- Special character patterns
- Path and query parameter analysis

**Model:** Random Forest Classifier trained on phishing datasets

### Message Fake Detection

Analyzes messages using 11 features:
- Message length and word count
- Exclamation/question mark frequency
- All-caps words ratio
- URL presence in message
- Spam keyword detection
- Special characters and digit ratio
- Urgency word detection (URGENT, ASAP, etc.)

**Spam Keywords Detected:**
- "congratulations", "winner", "claim", "urgent"
- "limited time", "verify", "password"
- "free gift", "prize", "guaranteed", and more

**Model:** Random Forest Classifier optimized for spam/phishing messages

## Project Structure

```
cybercrime-detection/
├── app.py                          # Flask application
├── feature_extraction.py           # Feature extraction for URLs & messages
├── train_model.py                  # URL phishing model trainer
├── train_message_model.py          # Message detection model trainer
├── requirements.txt                # Dependencies
├── dataset/
│   ├── phishing.csv               # Phishing URL dataset
│   └── messages.csv               # Spam/phishing messages dataset (auto-created)
├── model/
│   ├── phishing_model.pkl         # Trained URL detection model
│   ├── message_model.pkl          # Trained message detection model
│   └── *.json                     # Model metadata
├── static/
│   ├── style.css                  # UI styling
│   └── login.css                  # Login page styling
└── templates/
    ├── index.html                 # Dashboard with dual detection
    └── login.html                 # Login page
```

## Usage

### Scan a URL
1. Click on the **URL Scanner** tab
2. Enter a URL (e.g., https://example.com)
3. Click **SCAN** to analyze
4. View the threat assessment with confidence score

### Analyze a Message
1. Click on the **Message Checker** tab
2. Paste or type a message
3. Click **ANALYZE** to check for fake/spam content
4. Review spam detection results with confidence percentage

## Technologies Used

- **Backend:** Flask (Python web framework)
- **ML Model:** scikit-learn Random Forest Classifier
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Data Processing:** pandas, NumPy
- **Model Serialization:** joblib

## Response Examples

### Safe URL Response
```json
{
  "prediction": "0",
  "probability": 0.98,
  "type": "phishing"
}
```

### Phishing URL Response
```json
{
  "prediction": "1",
  "probability": 0.95,
  "type": "phishing"
}
```

### Legitimate Message Response
```json
{
  "prediction": "0",
  "probability": 0.92,
  "type": "fake_message"
}
```

### Fake Message Response
```json
{
  "prediction": "1",
  "probability": 0.88,
  "type": "fake_message"
}
```

## Model Performance

Both models use Random Forest with 100 estimators trained to high accuracy on curated datasets.

**Current Metrics:**
- Accuracy: ~95%+
- Precision: ~95%+
- Recall: ~95%+
- F1 Score: ~95%+

## Security Notes

⚠️ **For Demo/Educational Use Only:**
- Default credentials are hardcoded for demonstration
- Replace with proper authentication in production
- Implement HTTPS/SSL for real deployments
- Use environment variables for sensitive data
- Add proper input validation and sanitization

## Future Enhancements

- [ ] Integration with real-time threat feeds
- [ ] Multi-language support for message analysis
- [ ] Advanced NLP-based deep learning models
- [ ] Database logging for audit trails
- [ ] API endpoint for third-party integrations
- [ ] Mobile app version

## License

Educational Project - Use for learning purposes
