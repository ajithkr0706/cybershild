# CyberShield AI - Security Detection System

Advanced AI-powered security detection system with triple-vector capabilities for real-time detection of **Phishing URLs**, **Fake / Spam Messages**, and **AI-Generated / Deepfake Images**.

> 📖 **Full Technical Documentation**: For complete architecture diagrams, API references, feature extraction specifications, and serverless deployment guides, see [PROJECT_DOCUMENTATION.md](file:///c:/Users/AJITH%20KUMAR/Desktop/cybershild-ai-main/PROJECT_DOCUMENTATION.md).

---

## Key Features

✨ **Phishing URL Detection** - Analyzes URLs using 14 heuristic features, brand impersonation checks, and high-risk TLD filters  
✨ **Fake Message Detection** - Detects spam, phishing, financial scams, and coercive urgency patterns in text  
🖼️ **AI Image Inspector** - Analyzes image uploads for synthetic AI markers, camera EXIF anomalies, Laplacian edge frequency, and sensor noise  
🔐 **Dual Authentication** - Supports Email/Password sign-in and Google OAuth 2.0  
🔑 **Password Reset System** - OTP verification via SMTP email delivery  
📊 **SOC Admin Dashboard** - Live threat metrics, confusion matrix, precision/recall tracking, user management (`/admin`)  
🚀 **Serverless Resilient** - Fallback heuristic models ensuring 100% uptime on cloud platforms like Vercel  

---

## Quick Start

### 1. Environment Setup

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

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

Train the **AI Image Detection Model**:
```bash
python train_image_model.py
```

### 3. Run Application

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

**Demo User Credentials:**
- Email: `yadavmahendhar65@gmail.com`
- Password: `Mahi@123456`

**SOC Admin Credentials:**
- Email: `mahiiii@cybershield.com`
- Password: `Mahi@2004`
- Portal URL: `http://127.0.0.1:5000/admin`

---

## Features & Detection Pipeline

### URL Phishing Detection (14 Features)
- Hostname & path length analysis
- Raw IPv4 address hostname detection
- HTTPS/SSL verification & `@` symbol routing check
- Brand impersonation detection engine (Google, PayPal, Apple, Microsoft, Netflix, Amazon, etc.)
- Phishing keyword extraction & high-risk TLD checks (`.xyz`, `.top`, `.online`, `.zip`, etc.)

### Message Fake Detection (11 Features)
- Text length & word count statistics
- Exclamation/Question mark frequency clusters
- ALL-CAPS words ratio & embedded link extraction
- Financial spam vocabulary matching (`claim`, `winner`, `wire transfer`, `prize`, `social security`)
- Coercive urgency words detection (`urgent`, `asap`, `act now`, `limited time`)

### AI Image Detection (10 Features)
- Camera EXIF metadata verification
- AI software signature tags (Midjourney, DALL-E, Stable Diffusion, Firefly)
- Laplacian edge variance focus analysis
- Color channel standard deviation & unique colors palette depth
- Sensor ISO noise variance estimation

---

## Project Structure

```
cybershild-ai-main/
├── app.py                          # Main Flask Application & API endpoints
├── feature_extraction.py           # Feature extraction engine (URL, Message, Image)
├── train_model.py                  # Phishing URL model trainer
├── train_message_model.py          # Message detection model trainer
├── train_image_model.py            # AI image detection model trainer
├── PROJECT_DOCUMENTATION.md        # Comprehensive technical documentation
├── requirements.txt                # Python dependencies
├── vercel.json                     # Vercel serverless deployment config
├── dataset/                        # Auto-generated CSV training datasets
├── model/                          # Serialized .pkl models and metadata JSONs
├── static/                         # CSS stylesheets, JS scripts & uploaded proof screenshots
└── templates/                      # HTML5 Jinja templates (index, login, signup, admin, reset_password)
```

---

## Documentation & API Reference

For detailed endpoint documentation, schema definitions, and security guidelines, read [PROJECT_DOCUMENTATION.md](file:///c:/Users/AJITH%20KUMAR/Desktop/cybershild-ai-main/PROJECT_DOCUMENTATION.md).

---

## License

Educational & Security Research Project. Use responsibly.
rails
- [ ] API endpoint for third-party integrations
- [ ] Mobile app version

## License

Educational Project - Use for learning purposes
