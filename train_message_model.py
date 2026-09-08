import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
from feature_extraction import extract_message_features_from_series


def main():
    root = os.path.dirname(__file__)
    csv_path = os.path.join(root, 'dataset', 'messages.csv')
    model_dir = os.path.join(root, 'model')
    
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Check if dataset exists
    if not os.path.exists(csv_path):
        print(f"Creating sample messages dataset at {csv_path}...")
        # Create a sample dataset for demonstration
        sample_data = {
            'message': [
                "Hi John, how are you today?",
                "Meeting scheduled for 3 PM tomorrow.",
                "CONGRATULATIONS! You won $1,000,000! Click here to claim!",
                "Important: Your account has been suspended. Verify now!",
                "Let's grab coffee this weekend.",
                "URGENT ACTION REQUIRED! Update your password immediately!!!",
                "The project deadline has been extended to next month.",
                "You are the lucky winner! Claim your prize today!",
                "Looking forward to the presentation.",
                "LIMITED TIME OFFER!!! 50% OFF!!! Don't miss out!!!",
                "Can you send me the report by EOD?",
                "Nigerian Prince wants to transfer $5M to your account!",
                "Team lunch was delicious.",
                "Verify your credit card details now to avoid account closure!",
                "The weather is nice today.",
                "RISK FREE! Guaranteed returns on your investment!",
                "When are you available for a call?",
                "Your bank account has been compromised. Click here urgently!",
                "Just finished the design mockups.",
                "FREE GIFT AVAILABLE!!! Act now or offer expires!!!"
            ],
            'label': [
                0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1
            ]
        }
        df = pd.DataFrame(sample_data)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"Sample dataset created with {len(df)} messages")
    else:
        print(f"Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"Dataset loaded: {len(df)} rows")

    # Try to locate message and label columns
    if 'message' in df.columns:
        messages = df['message'].astype(str)
    else:
        messages = df.iloc[:, 0].astype(str)

    if 'label' in df.columns:
        labels = df['label']
    elif 'class' in df.columns:
        labels = df['class']
    else:
        labels = df.iloc[:, -1]

    print(f"Extracting features from {len(messages)} messages using 11-feature set...")
    X = extract_message_features_from_series(messages)
    print(f"Features shape: {X.shape}")  # Should be (n_samples, 11)
    
    y = labels.values

    # Encode string labels if present
    if y.dtype == object:
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(y)
        print(f"Encoded labels: {np.unique(y)}")

    # Split data
    stratify = y if len(np.unique(y)) > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )

    # Train Random Forest
    print("Training Random Forest classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("\n=== Model Evaluation ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    model_path = os.path.join(model_dir, 'message_model.pkl')
    joblib.dump(clf, model_path)
    print(f"\nModel saved to {model_path}")

    # Save metadata
    metadata = {
        'accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1': float(f1),
        'features': 11,
        'model_type': 'Random Forest (Fake Message Detection)'
    }
    metadata_path = os.path.join(model_dir, 'message_model_metadata.json')
    import json
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {metadata_path}")


if __name__ == '__main__':
    main()
