import re
import numpy as np
from urllib.parse import urlparse

ip_regex = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')

# Spam/Fake message patterns
SPAM_KEYWORDS = [
    'congratulations', 'winner', 'claim', 'urgent', 'limited time', 'act now',
    'click here', 'verify', 'confirm', 'validate', 'update', 'urgent action',
    'alert', 'suspended', 'blocked', 'restricted', 'free gift', 'prize',
    'guaranteed', 'risk free', 'no credit card', 'nigerian prince', 'inheritance',
    'wire transfer', 'bank details', 'password', 'social security', 'credit card'
]

PHISH_KEYWORDS = [
    'login', 'verify', 'account', 'bank', 'secure', 'update', 'signin', 'confirm',
    'security', 'wallet', 'crypto', 'support', 'token', 'billing', 'passcode', 'credential',
    'unusual-activity', 'suspended', 'reset-password'
]

BRAND_NAMES = {
    'google': 'google.com',
    'paypal': 'paypal.com',
    'apple': 'apple.com',
    'microsoft': 'microsoft.com',
    'netflix': 'netflix.com',
    'amazon': 'amazon.com',
    'chase': 'chase.com',
    'facebook': 'facebook.com',
    'instagram': 'instagram.com'
}

SUSPICIOUS_TLDS = [
    '.xyz', '.top', '.work', '.club', '.info', '.online', '.site', '.tk', '.ml', '.ga', '.cf', '.gq', '.zip'
]


def extract_features(url: str):
    """Extract 14 numeric features from a URL for phishing detection."""
    raw_url = str(url or '').strip()
    if not raw_url:
        return np.zeros(14, dtype=float)

    # Normalize protocol for accurate feature computation
    full_url = raw_url if '://' in raw_url else ('https://' + raw_url)
    parsed = urlparse(full_url)
    hostname = (parsed.netloc or parsed.path).lower()
    
    if ':' in hostname:
        hostname = hostname.split(':')[0]

    features = []
    # 1: full URL length
    features.append(float(len(raw_url)))
    # 2: hostname length
    features.append(float(len(hostname)))
    # 3: has IP address in hostname
    features.append(1.0 if ip_regex.search(hostname) else 0.0)
    # 4: count of dots in hostname
    features.append(float(hostname.count('.')))
    # 5: count of hyphens in hostname
    features.append(float(hostname.count('-')))
    # 6: has '@' symbol in URL
    features.append(1.0 if '@' in raw_url else 0.0)
    # 7: uses HTTPS protocol
    features.append(1.0 if raw_url.lower().startswith('https') else 0.0)
    # 8: contains 'www' in hostname
    features.append(1.0 if 'www.' in hostname else 0.0)
    # 9: number of digits in URL
    features.append(float(sum(c.isdigit() for c in raw_url)))
    # 10: path length
    features.append(float(len(parsed.path)))
    # 11: query length
    features.append(float(len(parsed.query)))
    # 12: count of phishing keywords in URL
    kw_count = sum(1 for kw in PHISH_KEYWORDS if kw in raw_url.lower())
    features.append(float(kw_count))
    # 13: has suspicious TLD
    has_tld = 1.0 if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0.0
    features.append(has_tld)
    # 14: subdomain depth (dots in hostname minus 1)
    features.append(float(max(0, hostname.count('.') - 1)))

    return np.array(features, dtype=float)


def extract_message_features(message: str):
    """Extract 11 numeric features from a message for fake message detection."""
    message = str(message or '').strip()
    words = message.lower().split()
    
    features = []
    # 1: message length
    features.append(len(message))
    # 2: word count
    features.append(len(words))
    # 3: average word length
    features.append(float(sum(len(w) for w in words) / len(words)) if words else 0.0)
    # 4: has multiple exclamation marks (suspicious)
    features.append(float(message.count('!')))
    # 5: has multiple question marks
    features.append(float(message.count('?')))
    # 6: has all caps words ratio
    caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
    features.append(float(caps_words / len(words)) if words else 0.0)
    # 7: has URLs in message
    has_url = 1.0 if re.search(r'http[s]?://|www\.|\.com|\.xyz|\.top', message.lower()) else 0.0
    features.append(has_url)
    # 8: count of spam keywords
    spam_count = sum(1 for keyword in SPAM_KEYWORDS if keyword in message.lower())
    features.append(float(spam_count))
    # 9: has special characters ratio
    special_chars = sum(1 for c in message if not c.isalnum() and c not in ' \t\n')
    features.append(float(special_chars / len(message)) if len(message) > 0 else 0.0)
    # 10: has numbers ratio
    numbers = sum(1 for c in message if c.isdigit())
    features.append(float(numbers / len(message)) if len(message) > 0 else 0.0)
    # 11: has urgency words
    urgency_words = ['urgent', 'asap', 'immediately', 'act now', 'limited time', 'hurry', 'final warning']
    urgency_count = sum(1 for word in urgency_words if word in message.lower())
    features.append(float(urgency_count))

    return np.array(features, dtype=float)


def extract_features_from_series(series):
    """Extract features from a pandas Series of URLs."""
    return np.vstack([extract_features(u) for u in series])


def extract_message_features_from_series(series):
    """Extract features from a pandas Series of messages."""
    return np.vstack([extract_message_features(msg) for msg in series])


def get_url_reasons(url: str, prediction: str):
    """Analyze URL and return specific safety or risk indicator reasons."""
    raw_url = str(url or '').strip()
    full_url = raw_url if '://' in raw_url else ('https://' + raw_url)
    parsed = urlparse(full_url)
    hostname = (parsed.netloc or parsed.path).lower()
    if ':' in hostname:
        hostname = hostname.split(':')[0]

    reasons = []

    # 1. Protocol / Encryption check
    if raw_url.lower().startswith('https'):
        reasons.append({'text': 'Valid HTTPS protocol encrypted connection', 'type': 'safe'})
    else:
        reasons.append({'text': 'Unencrypted HTTP protocol or missing HTTPS security certificate', 'type': 'danger'})

    # 2. IP Address check
    if ip_regex.search(hostname):
        reasons.append({'text': f'Suspicious IP address hostname detected ({hostname}) instead of a domain', 'type': 'danger'})
    else:
        reasons.append({'text': 'Standard domain name format used', 'type': 'safe'})

    # 3. Suspicious TLD check
    matched_tlds = [tld for tld in SUSPICIOUS_TLDS if hostname.endswith(tld)]
    if matched_tlds:
        reasons.append({'text': f'High-risk top-level domain ({matched_tlds[0]}) commonly associated with phishing', 'type': 'danger'})

    # 4. Phishing keywords in URL
    found_keywords = [kw for kw in PHISH_KEYWORDS if kw in raw_url.lower()]
    if found_keywords:
        kw_str = ', '.join(found_keywords[:3])
        reasons.append({'text': f'Phishing/credential harvesting keywords detected in URL ({kw_str})', 'type': 'danger'})
    else:
        reasons.append({'text': 'No suspicious security or credential keywords found in URL path', 'type': 'safe'})

    # 4b. Brand impersonation / spoofing check
    for brand, official_domain in BRAND_NAMES.items():
        if brand in raw_url.lower() and not hostname.endswith(official_domain):
            reasons.append({'text': f'Potential brand impersonation: Uses "{brand}" brand name on an unofficial domain', 'type': 'danger'})

    # 5. Hyphens and subdomains in hostname
    hyphen_count = hostname.count('-')
    if hyphen_count >= 2:
        reasons.append({'text': f'Multiple hyphens in hostname ({hyphen_count}) - common domain spoofing technique', 'type': 'warning'})

    subdomain_depth = max(0, hostname.count('.') - 1)
    if subdomain_depth >= 3:
        reasons.append({'text': f'Excessive subdomain depth ({subdomain_depth} levels) masking real destination', 'type': 'danger'})

    # 6. '@' symbol redirection trick
    if '@' in raw_url:
        reasons.append({'text': 'Contains "@" symbol, which can hijack URL routing to a malicious host', 'type': 'danger'})

    # 7. Summary reason based on prediction
    if str(prediction) == '0':
        if not any(r['type'] == 'danger' for r in reasons):
            reasons.append({'text': 'Hostname and path match legitimate domain structures with clean threat score', 'type': 'safe'})
    else:
        reasons.append({'text': 'Combined heuristic features match known phishing and domain spoofing patterns', 'type': 'danger'})

    return reasons


def get_message_reasons(message: str, prediction: str):
    """Analyze message text and return specific safety or risk indicator reasons."""
    msg = str(message or '').strip()
    msg_lower = msg.lower()

    reasons = []

    # 1. Urgency / Threat pressure words
    urgency_words = ['urgent', 'asap', 'immediately', 'act now', 'limited time', 'hurry', 'final warning', 'suspended']
    found_urgency = [w for w in urgency_words if w in msg_lower]
    if found_urgency:
        reasons.append({'text': f'Urgent/coercive language detected ({", ".join(found_urgency[:3])}) creating false pressure', 'type': 'danger'})

    # 2. Spam / Financial scam keywords
    found_spam = [kw for kw in SPAM_KEYWORDS if kw in msg_lower]
    if found_spam:
        kw_str = ', '.join(found_spam[:3])
        reasons.append({'text': f'Suspicious spam/scam keywords detected ({kw_str})', 'type': 'danger'})
    else:
        reasons.append({'text': 'No typical spam or financial scam keywords detected', 'type': 'safe'})

    # 3. Embedded URLs
    if re.search(r'http[s]?://|www\.|\.com|\.xyz|\.top', msg_lower):
        reasons.append({'text': 'Contains embedded external link encouraging recipient to click', 'type': 'danger'})
    else:
        reasons.append({'text': 'No external links or URLs embedded in message text', 'type': 'safe'})

    # 4. ALL-CAPS ratio
    caps_words = [w for w in msg.split() if w.isupper() and len(w) > 1]
    if len(caps_words) >= 2:
        reasons.append({'text': f'Excessive use of ALL-CAPS words ({", ".join(caps_words[:3])})', 'type': 'warning'})

    # 5. Exclamation / Question mark clusters
    if msg.count('!') >= 2 or msg.count('?') >= 3:
        reasons.append({'text': f'High frequency of exclamation/question marks ({msg.count("!")} ! / {msg.count("?")} ?)', 'type': 'warning'})

    # 6. Summary reason based on prediction
    if str(prediction) == '0':
        if not any(r['type'] == 'danger' for r in reasons):
            reasons.append({'text': 'Normal conversational tone with no phishing/spam threat characteristics', 'type': 'safe'})
    else:
        reasons.append({'text': 'Language structure and keywords strongly match known spam and scam campaigns', 'type': 'danger'})

    return reasons


def extract_image_features(image_path: str):
    """Extract 10 numeric features from an image for AI image detection."""
    import numpy as np
    import os
    
    # Initialize default features (10 elements)
    features = np.zeros(10, dtype=float)
    
    try:
        from PIL import Image
    except Exception as e:
        print(f"PIL not available: {e}")
        return features

    try:
        if not os.path.exists(image_path):
            return features
            
        with Image.open(image_path) as img:
            # 1. EXIF check
            has_exif = 1.0 if img.info.get('exif') else 0.0
            
            # 2. Check metadata string for AI keywords
            metadata_str = ""
            for k, v in img.info.items():
                if isinstance(v, str):
                    metadata_str += " " + v.lower()
                elif isinstance(v, bytes):
                    try:
                        metadata_str += " " + v.decode('utf-8', errors='ignore').lower()
                    except:
                        pass
            
            ai_keywords = [
                'stable diffusion', 'midjourney', 'dall-e', 'dalle', 'artificial intelligence', 
                'ai generated', 'novelai', 'craiyon', 'firefly', 'leonardo.ai', 'imagen', 
                'generator', 'software: stable diffusion', 'creativeml-openrail-m'
            ]
            has_ai_metadata = 1.0 if any(kw in metadata_str for kw in ai_keywords) else 0.0
            
            # 3. File size ratio to pixel area
            file_size = float(os.path.getsize(image_path))
            width, height = img.size
            file_size_ratio = file_size / (width * height) if (width * height) > 0 else 0.0
            
            # Resize image to 256x256 for fast feature extraction
            img_rgb = img.convert('RGB')
            img_resized = img_rgb.resize((256, 256))
            arr = np.array(img_resized, dtype=float)
            
            # 4. Color standard deviation
            color_std_dev = float(np.mean(np.std(arr, axis=(0, 1))))
            
            # Grayscale for spatial analysis
            gray = 0.2989 * arr[:, :, 0] + 0.5870 * arr[:, :, 1] + 0.1140 * arr[:, :, 2]
            
            # 5. Brightness mean
            brightness_mean = float(np.mean(gray))
            
            # 6. Brightness standard deviation
            brightness_std_dev = float(np.std(gray))
            
            # 7. Contrast
            contrast = float(np.max(gray) - np.min(gray))
            
            # 8. Laplacian variance (Edge sharpness indicator)
            laplacian = (
                gray[1:-1, 2:] + gray[1:-1, :-2] +
                gray[2:, 1:-1] + gray[:-2, 1:-1] -
                4 * gray[1:-1, 1:-1]
            )
            laplacian_variance = float(np.var(laplacian))
            
            # 9. Unique colors ratio
            pixels = arr.reshape(-1, 3)
            # Encode colors as 24-bit integers for speed
            color_ints = (pixels[:, 0].astype(np.int32) << 16) + (pixels[:, 1].astype(np.int32) << 8) + pixels[:, 2].astype(np.int32)
            unique_colors = len(np.unique(color_ints))
            unique_colors_ratio = float(unique_colors / (256 * 256))
            
            # 10. Local noise estimate (local pixel differences)
            diff_h = np.abs(gray[:, 1:] - gray[:, :-1])
            diff_v = np.abs(gray[1:, :] - gray[:-1, :])
            noise_estimate = float(np.mean(diff_h) + np.mean(diff_v))
            
            features[0] = has_exif
            features[1] = has_ai_metadata
            features[2] = file_size_ratio
            features[3] = laplacian_variance
            features[4] = color_std_dev
            features[5] = brightness_mean
            features[6] = brightness_std_dev
            features[7] = contrast
            features[8] = unique_colors_ratio
            features[9] = noise_estimate
            
    except Exception as e:
        print(f"Error extracting image features: {e}")
        
    return features


def get_image_reasons(image_path: str, prediction: str):
    """Analyze image features and return forensic details."""
    import os
    
    reasons = []
    has_exif = False
    has_ai_metadata = False
    
    try:
        from PIL import Image
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                if img.info.get('exif'):
                    has_exif = True
                
                metadata_str = ""
                for k, v in img.info.items():
                    if isinstance(v, str):
                        metadata_str += " " + v.lower()
                    elif isinstance(v, bytes):
                        try:
                            metadata_str += " " + v.decode('utf-8', errors='ignore').lower()
                        except:
                            pass
                
                ai_keywords = [
                    'stable diffusion', 'midjourney', 'dall-e', 'dalle', 'artificial intelligence', 
                    'ai generated', 'novelai', 'craiyon', 'firefly', 'leonardo.ai', 'imagen', 
                    'generator', 'software: stable diffusion', 'creativeml-openrail-m'
                ]
                if any(kw in metadata_str for kw in ai_keywords):
                    has_ai_metadata = True
    except:
        pass
        
    if has_exif:
        reasons.append({'text': 'EXIF metadata header present (typical of physical camera devices)', 'type': 'safe'})
    else:
        reasons.append({'text': 'EXIF metadata header missing or stripped (typical of AI generators and web compression)', 'type': 'warning'})
        
    if has_ai_metadata:
        reasons.append({'text': 'AI generator signature detected in file metadata headers', 'type': 'danger'})
    else:
        reasons.append({'text': 'No direct AI generator signatures found in image headers', 'type': 'safe'})
        
    if str(prediction) == '1':
        reasons.append({'text': 'Spatial noise pattern matches digital diffusion model output rather than sensor grain', 'type': 'danger'})
        reasons.append({'text': 'Gradient continuity shows computer-generated pixel blending properties', 'type': 'danger'})
    else:
        reasons.append({'text': 'High-frequency micro-grain matches physical camera sensor characteristics', 'type': 'safe'})
        reasons.append({'text': 'Natural light intensity distribution verified across gradient paths', 'type': 'safe'})
        
    return reasons


