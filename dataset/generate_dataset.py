import os
import random
import pandas as pd

# Set random seed for reproducibility
random.seed(42)

def generate_url_dataset():
    legitimate_domains = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "reddit.com", "github.com",
        "microsoft.com", "apple.com", "netflix.com", "stackoverflow.com", "bing.com",
        "yahoo.com", "whatsapp.com", "zoom.us", "twitch.tv", "adobe.com",
        "dropbox.com", "spotify.com", "ebay.com", "paypal.com", "chase.com",
        "wellsfargo.com", "bankofamerica.com", "stripe.com", "shopify.com", "wordpress.org",
        "medium.com", "nytimes.com", "bbc.com", "cnn.com", "gov.in",
        "usa.gov", "mit.edu", "stanford.edu", "harvard.edu", "openai.com",
        "cloudflare.com", "canva.com", "pinterest.com", "quora.com", "salesforce.com",
        "oracle.com", "cisco.com", "ibm.com", "intel.com", "nvidia.com"
    ]

    legitimate_paths = [
        "", "/", "/search?q=security", "/wiki/Main_Page", "/features", "/docs/api",
        "/about-us", "/contact", "/pricing", "/help/center", "/blog/news-update-2026",
        "/account/settings", "/dashboard", "/profile/user", "/explore", "/download",
        "/terms-of-service", "/privacy-policy", "/support/tickets", "/login"
    ]

    phishing_brands = [
        "paypal", "apple", "google", "microsoft", "netflix", "amazon", "chase",
        "wellsfargo", "bankofamerica", "facebook", "instagram", "meta", "binance",
        "coinbase", "stripe", "dropbox", "docusign", "usps", "fedex", "dhl"
    ]

    phishing_keywords = [
        "login", "verify", "secure", "account-update", "signin-portal", "confirm-identity",
        "security-alert", "billing-update", "suspended-account", "validation-check",
        "auth-token", "password-reset", "unlock-account", "unusual-activity"
    ]

    phishing_tlds = [".xyz", ".top", ".work", ".club", ".info", ".online", ".site", ".tk", ".ml", ".ga", ".cf", ".gq"]

    urls = []
    labels = []

    # 1. Generate Legitimate URLs (~600)
    for domain in legitimate_domains:
        for proto in ["https://", "http://", "https://www.", "http://www."]:
            for path in legitimate_paths[:8]:
                urls.append(f"{proto}{domain}{path}")
                labels.append(0)

    # 2. Generate Phishing URLs (~600)
    # 2a. IP address hostnames
    ips = ["192.168.1.100", "104.28.14.88", "185.220.101.5", "198.51.100.22", "45.142.214.8", "103.224.182.241"]
    for ip in ips:
        for kw in phishing_keywords:
            urls.append(f"http://{ip}/{kw}.php")
            labels.append(1)
            urls.append(f"http://{ip}/secure/{kw}?user=admin&token={random.randint(1000,9999)}")
            labels.append(1)

    # 2b. Brand spoofing & hyphenated phishing domains
    for brand in phishing_brands:
        for kw in phishing_keywords[:6]:
            for tld in phishing_tlds[:6]:
                urls.append(f"http://{brand}-{kw}{tld}/login.php")
                labels.append(1)
                urls.append(f"https://{brand}.com-{kw}-security{tld}/auth")
                labels.append(1)
                urls.append(f"http://{kw}.{brand}.com.user-verify{tld}/signin?ref={random.randint(100,999)}")
                labels.append(1)

    df_urls = pd.DataFrame({'url': urls, 'label': labels})
    df_urls = df_urls.sample(frac=1, random_state=42).reset_index(drop=True)
    return df_urls

def generate_messages_dataset():
    legitimate_messages = [
        "Hi John, hope you are doing well!",
        "Are we still meeting at 3 PM today?",
        "Please find attached the monthly project status report.",
        "Hey! Don't forget about team lunch tomorrow.",
        "The server deployment completed successfully without issues.",
        "Can you review the pull request on GitHub when you have a moment?",
        "Thanks for sending over the invoice. We will process it shortly.",
        "Happy birthday! Hope you have a wonderful day!",
        "Let me know when you are free for a quick sync call.",
        "The flight reservation confirmation code is ABC123XYZ.",
        "Your package from Amazon is out for delivery today.",
        "Reminder: Doctor appointment tomorrow at 10:00 AM.",
        "Here is the recipe for the cake we talked about.",
        "Great presentation today! Everyone loved the slides.",
        "Can you pick up milk and bread on your way home?"
    ]

    spam_messages = [
        "CONGRATULATIONS! You have won a $1,000 Amazon Gift Card! Click here to claim: http://claim-gift.xyz",
        "URGENT: Your bank account has been suspended due to suspicious activity. Verify now at http://bank-verify.top",
        "Final Warning! Your Netflix subscription is expired. Update payment details immediately: http://netflix-update.site",
        "You have (1) unread security alert! Login to secure your account: http://security-portal.work",
        "Claim your $5,000 lottery prize today! No fees required, reply with your full name and bank account number.",
        "ALERT: Paypal account restricted! Verify your identity now to restore access: http://paypal-auth.online",
        "Exclusive offer! 90% discount on Rolex watches and iPhones! Limited time only, click http://buy-cheap-deals.club",
        "Your package cannot be delivered due to incomplete address. Update info now: http://usps-tracking-update.xyz",
        "URGENT ACTION REQUIRED: Someone tried to login from Russia. Change your password immediately: http://account-sec.tk",
        "Congratulations winner! You were randomly selected for a free iPhone 15 Pro. Claim within 5 minutes!",
        "Dear Customer, your credit card has been charged $499.00. If you did not authorize this, call 1-800-FAKE-NUM or click link.",
        "Nigerian Prince inheritance transfer: $10.5 Million available. Send your bank details to claim."
    ]

    messages = []
    labels = []

    for _ in range(40):
        for msg in legitimate_messages:
            messages.append(msg)
            labels.append(0)

    for _ in range(50):
        for msg in spam_messages:
            messages.append(msg)
            labels.append(1)

    df_msgs = pd.DataFrame({'message': messages, 'label': labels})
    df_msgs = df_msgs.sample(frac=1, random_state=42).reset_index(drop=True)
    return df_msgs

if __name__ == '__main__':
    root = os.path.dirname(__file__)
    
    urls_df = generate_url_dataset()
    urls_path = os.path.join(root, 'phishing.csv')
    urls_df.to_csv(urls_path, index=False)
    print(f"Generated {len(urls_df)} URL dataset rows at {urls_path}")

    msgs_df = generate_messages_dataset()
    msgs_path = os.path.join(root, 'messages.csv')
    msgs_df.to_csv(msgs_path, index=False)
    print(f"Generated {len(msgs_df)} message dataset rows at {msgs_path}")
