import os
import re
import json
import requests
import numpy as np

class CyberBotEngine:
    """
    AI Security Assistant Engine ("CyberBot") for CyberShield AI.
    Combines external LLM APIs (Gemini/OpenAI) with a built-in domain security
    knowledge base and real-time integration with CyberShield ML detection models.
    """
    
    SYSTEM_PROMPT = (
        "You are CyberBot, an elite AI Cybersecurity Specialist & Virtual SOC Analyst for CyberShield AI. "
        "Your mission is to help users spot cyber threats, analyze phishing attempts, secure their accounts, "
        "understand security best practices, and defend against malware, social engineering, and identity theft. "
        "Be concise, professional, friendly, and structured in markdown format with clear headings, bullet points, and emojis."
    )

    KNOWLEDGE_BASE = [
        {
            "patterns": [r"\burl\b", r"\blink\b", r"\bphish", r"\bsuspicious link", r"\bwebsite\b", r"\bdomain\b"],
            "title": "🛡️ How to Spot Suspicious URLs & Phishing Links",
            "response": """### How to Spot Phishing & Fake URLs

When analyzing a web link, look out for these common threat indicators:

1. **Mismatched / Typosquatted Domains**: Scammers use lookalike domains (e.g., `paypa1-security.com` instead of `paypal.com`, or `bannkofamerica-update.net`).
2. **Excessive Subdomains & Hyphens**: Legitimate services rarely use long hyphenated chains like `login.update.account-verification.secure-auth.org`.
3. **HTTP instead of HTTPS**: Non-secure connections (lacking the padlock icon) for sensitive logins are a red flag.
4. **Ip Address as Hostname**: URLs like `http://192.168.1.1/login.php` instead of a brand name.
5. **Shortened URLs**: Bit.ly, TinyURL, or obscure link shorteners hiding the true destination.

💡 **Actionable Tip**: Use the **CyberShield URL Scanner** tab to run a real-time ML diagnostic scan on any URL before clicking!"""
        },
        {
            "patterns": [r"\bpassword", r"\bpasscode", r"\bcredential", r"\bauth\b"],
            "title": "🔑 Password Health & Protection Guidelines",
            "response": """### Password Security Best Practices

Strong authentication is your first line of defense against unauthorized access:

1. **Length Matters**: Passwords should be at least **14–16 characters** long.
2. **Unpredictable Complexity**: Mix upper/lowercase letters, numbers, and symbols (`#`, `@`, `!`, `$`).
3. **Never Reuse Passwords**: Unique passwords for every service prevent *credential stuffing attacks*.
4. **Use a Password Manager**: Tools like Bitwarden, 1Password, or KeePass generate and store uncrackable vault passwords safely.
5. **Enable Multi-Factor Authentication (2FA)**: Always pair your password with app-based TOTP (e.g., Google Authenticator).

💡 **Need a Quick Test?**: Avoid using names, birth years, sequential numbers (`123456`), or common dictionary words!"""
        },
        {
            "patterns": [r"\b2fa\b", r"\bmfa\b", r"\btwo-factor", r"\bmulti-factor", r"\bauthenticator\b"],
            "title": "🔐 Multi-Factor Authentication (2FA) Guide",
            "response": """### Multi-Factor Authentication (2FA / MFA) Explained

2FA adds a mandatory second layer of identity verification when logging in:

* **Authenticator Apps (Recommended)**: Apps like Google Authenticator, Authy, or Microsoft Authenticator generate time-based one-time codes (TOTP) locally on your phone.
* **Security Keys (Strongest)**: Hardware tokens like YubiKey provide physical phishing-resistant encryption.
* **SMS 2FA (Better than nothing)**: Text message codes are vulnerable to *SIM swapping*, but still far safer than passwords alone.

⚡ **Recommendation**: Enable 2FA on your email accounts, financial portals, social media, and cloud storage immediately!"""
        },
        {
            "patterns": [r"\bmessage\b", r"\bsms\b", r"\btext\b", r"\bemail\b", r"\bspam\b", r"\bwhatsapp\b", r"\btelegram\b"],
            "title": "💬 Identifying Fake Messages & Smishing Scams",
            "response": """### How to Spot Fake Messages & SMS Scams (Smishing)

Scammers craft high-urgency messages to trick you into acting without thinking:

* **Urgency & Panic**: Claims like *"Your account will be suspended in 2 hours"*, *"Unpaid delivery fee"*, or *"Unauthorized transaction detected"*.
* **Generic Greetings**: Addresses you as *"Dear Customer"* or *"Valued User"* instead of your actual name.
* **Suspicious Sender**: Unknown numbers, irregular email addresses, or unverified sender handles.
* **Requests for Sensitive Info**: Asking for OTP codes, PINs, passwords, or SSN.

💡 **Actionable Tip**: Paste the text into the **CyberShield Message Checker** tab to evaluate message risk score and scam probability!"""
        },
        {
            "patterns": [r"\bmalware\b", r"\bvirus\b", r"\bransomware\b", r"\btrojan\b", r"\bspyware\b", r"\binfect"],
            "title": "🦠 Malware & Virus Prevention & Response",
            "response": """### Malware & Virus Defense Playbook

If you suspect your system or file is infected:

1. **Disconnect from the Network**: Immediately turn off Wi-Fi and unplug Ethernet to block malware from spreading or contacting command servers.
2. **Boot into Safe Mode**: Restart your device in Safe Mode to prevent malicious startup scripts from running.
3. **Run a Full Antivirus Scan**: Use Windows Defender, Malwarebytes, or Bitdefender to quarantine and remove infected files.
4. **Check Task Manager / Process Monitor**: Look for unfamiliar, CPU-heavy background processes.
5. **Keep Software Updated**: Ensure your Operating System, browsers, and applications have the latest security patches installed."""
        },
        {
            "patterns": [r"\bhacked\b", r"\bcompromised\b", r"\bbreach\b", r"\bstolen\b", r"\brecover\b"],
            "title": "🚨 Incident Response: What to do if you get Hacked",
            "response": """### Immediate Action Plan for Account Compromise

Take these critical emergency steps right away:

1. **Change Account Passwords**: Reset your password on the affected account and any other accounts sharing similar credentials.
2. **Revoke Active Sessions**: Go to account security settings and click *"Sign out of all devices"*.
3. **Check Forwarding & Recovery Info**: Ensure the hacker hasn't changed your backup email, phone number, or email forwarding rules.
4. **Notify Financial Institutions**: If payment cards or bank details were exposed, call your bank immediately to freeze cards.
5. **Enable 2FA**: Lock down the account with an authenticator app."""
        },
        {
            "patterns": [r"\bwifi\b", r"\bwi-fi\b", r"\bvpn\b", r"\bnetwork\b", r"\bpublic wifi\b"],
            "title": "📡 Wi-Fi & Network Security Guidelines",
            "response": """### Wi-Fi & Network Safety Tips

Protect your internet connection from eavesdropping and Man-in-the-Middle (MitM) attacks:

* **Avoid Unsecured Public Wi-Fi**: Free airport or coffee shop Wi-Fi networks can be spoofed by rogue devices ("Evil Twin" networks).
* **Use a Trusted VPN**: Virtual Private Networks encrypt all internet traffic between your device and the server.
* **Secure Your Home Router**: Change default admin credentials, update router firmware, and enforce **WPA3 or WPA2-AES** encryption.
* **Disable Auto-Connect**: Turn off *"Auto-connect to open networks"* on your phone and laptop."""
        },
        {
            "patterns": [r"\bdeepfake\b", r"\bai image\b", r"\bfake image\b", r"\bmanipulated\b", r"\bphotoshop\b"],
            "title": "🖼️ AI Image & Deepfake Detection",
            "response": """### Spotting Synthetic & AI-Generated Images

Deepfakes and AI image generators (Midjourney, DALL-E, Stable Diffusion) leave subtle visual artifacts:

1. **Facial & Anatomical Anomalies**: Distorted fingers, mismatched earrings, asymmetric glasses frames, or blurred teeth.
2. **Text Rendering Glitches**: Background signboards or text with garbled, unreadable glyphs.
3. **Lighting & Shadow Inconsistencies**: Direction of light on face doesn't match background shadows.
4. **EXIF Metadata Check**: AI generators often leave synthetic signature tags or lack camera EXIF details (ISO, Shutter speed).

💡 **Actionable Tip**: Upload suspicious images to **CyberShield AI Image Detector** tab to analyze noise patterns and EXIF metadata!"""
        }
    ]

    def __init__(self):
        self.gemini_key = os.environ.get('GEMINI_API_KEY', '')
        self.openai_key = os.environ.get('OPENAI_API_KEY', '')

    def check_url_in_text(self, text):
        """Extract URLs or domain patterns from text."""
        url_pattern = r'https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        matches = re.findall(url_pattern, text)
        for m in matches:
            m_clean = m.strip('.,;()[]{}')
            if len(m_clean) > 3 and '.' in m_clean and not m_clean.endswith('.'):
                if not m_clean.startswith(('http://', 'https://')):
                    m_clean = 'http://' + m_clean
                return m_clean
        return None

    def generate_llm_gemini(self, message, history=None):
        """Call Google Gemini REST API if GEMINI_API_KEY is available."""
        if not self.gemini_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        headers = {'Content-Type': 'application/json'}
        
        contents = []
        if history:
            for item in history[-6:]: # last 3 turns
                role = "user" if item.get("sender") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item.get("text", "")}]})
        
        contents.append({"role": "user", "parts": [{"text": f"{self.SYSTEM_PROMPT}\n\nUser Question: {message}"}]})
        
        payload = {"contents": contents}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            print(f"Gemini API Exception: {e}")
        return None

    def generate_llm_openai(self, message, history=None):
        """Call OpenAI REST API if OPENAI_API_KEY is available."""
        if not self.openai_key:
            return None
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_key}'
        }
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        if history:
            for item in history[-6:]:
                role = "user" if item.get("sender") == "user" else "assistant"
                messages.append({"role": role, "content": item.get("text", "")})
        messages.append({"role": "user", "content": message})

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 600,
            "temperature": 0.7
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"OpenAI API Exception: {e}")
        return None

    def generate_fallback_knowledge(self, message, user_name="User"):
        """Built-in rule-based Security Assistant response when no API key is provided."""
        msg_lower = message.lower().strip()
        
        # Greetings
        if any(g in msg_lower for g in ["hi", "hello", "hey", "greetings", "start", "who are you"]):
            return (
                f"👋 Hello **{user_name}**! I am **CyberBot**, your CyberShield AI Security Assistant.\n\n"
                "I am trained to help you with:\n"
                "• 🔍 **Live Threat & URL Scanning**: Paste any link or message directly here for instant diagnostic feedback.\n"
                "• 🛡️ **Phishing & Scam Identification**: Learn how to spot fake emails, texts, and fake domains.\n"
                "• 🔑 **Password & 2FA Health**: Recommendations for multi-factor authentication and vault security.\n"
                "• 🚨 **Incident Response**: Emergency guidance if your account or device gets compromised.\n\n"
                "How can I assist your cybersecurity defense today?"
            )
        
        # Check patterns in Knowledge Base
        matched_sections = []
        for item in self.KNOWLEDGE_BASE:
            for pattern in item["patterns"]:
                if re.search(pattern, msg_lower):
                    matched_sections.append(item["response"])
                    break
        
        if matched_sections:
            return "\n\n---\n\n".join(matched_sections[:2])
        
        # Default intelligent response
        return (
            f"🤖 **CyberBot SOC Intelligence Response**\n\n"
            f"I analyzed your query regarding: *\"{message[:100]}\"*\n\n"
            "Here are the recommended cybersecurity actions based on your input:\n\n"
            "1. **Verification**: If this involves an unexpected message, link, or attachment, do **not** interact with it until verified.\n"
            "2. **Use CyberShield Scanners**: You can scan suspicious links in the **URL Scanner** tab or test text messages in the **Message Checker** tab.\n"
            "3. **Account Lockdown**: If you suspect a security breach, change your account credentials immediately and enable 2FA.\n\n"
            "💡 *Tip: Ask me specifically about 'phishing', 'passwords', '2FA', 'malware', or paste a link for instant diagnostic scanning!*"
        )

    def process_chat(self, user_message, chat_history=None, user_name="User", ml_url_scanner=None, ml_msg_scanner=None):
        """
        Main entry point for processing chat queries.
        Supports live URL scanning, generative LLM fallback, and rule knowledge fallback.
        """
        if not user_message or not user_message.strip():
            return {
                "success": False,
                "error": "Empty message received."
            }

        text = user_message.strip()
        live_scan_data = None
        url_found = self.check_url_in_text(text)

        # Live ML URL Scan Integration inside Chat!
        if url_found and ml_url_scanner:
            try:
                pred, prob, reasons = ml_url_scanner(url_found)
                is_threat = (str(pred) == '1')
                status_emoji = "🚨 DANGER: PHISHING DETECTED!" if is_threat else "✅ SAFE: NO THREATS DETECTED"
                badge_class = "danger" if is_threat else "safe"
                
                live_scan_data = {
                    "type": "url_scan",
                    "url": url_found,
                    "prediction": str(pred),
                    "probability": prob,
                    "is_threat": is_threat,
                    "reasons": reasons
                }
                
                scan_intro = (
                    f"### 🔍 Live CyberShield ML Scan Results for `{url_found}`\n\n"
                    f"**Verdict**: **{status_emoji}**\n"
                    f"**AI Confidence Level**: `{prob * 100:.1f}%`\n\n"
                )
                
                if reasons:
                    scan_intro += "**Security Observations**:\n"
                    for r in reasons[:4]:
                        icon = "⚠️" if r.get('type') == 'danger' else "✔️"
                        scan_intro += f"* {icon} {r.get('text', '')}\n"
                    scan_intro += "\n"
                
                if is_threat:
                    scan_intro += "⛔ **Recommendation**: **DO NOT** click this link or enter personal login credentials. It exhibits strong phishing indicators!"
                else:
                    scan_intro += "🛡️ **Recommendation**: This link appears clean based on structural feature extraction. Still maintain general caution."
                
                return {
                    "success": True,
                    "response": scan_intro,
                    "live_scan": live_scan_data
                }
            except Exception as e:
                print(f"Error in live chat URL scan: {e}")

        # Try LLM APIs if key present
        response_text = self.generate_llm_gemini(text, chat_history)
        if not response_text:
            response_text = self.generate_llm_openai(text, chat_history)
        
        # Fallback to built-in knowledge base
        if not response_text:
            response_text = self.generate_fallback_knowledge(text, user_name)

        return {
            "success": True,
            "response": response_text,
            "live_scan": live_scan_data
        }
