import os
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
from feature_extraction import extract_features_from_series


def main():
    root = os.path.dirname(__file__)
    csv_path = os.path.join(root, 'dataset', 'phishing.csv')
    model_dir = os.path.join(root, 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    # Check if dataset exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Please place phishing.csv in the dataset/ folder.")

    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Dataset loaded: {len(df)} rows")

    # Try to locate URL and label columns
    if 'url' in df.columns:
        urls = df['url'].astype(str)
    else:
        urls = df.iloc[:, 0].astype(str)

    if 'label' in df.columns:
        labels = df['label']
    elif 'class' in df.columns:
        labels = df['class']
    else:
        labels = df.iloc[:, -1]

    print(f"Extracting features from {len(urls)} URLs using 14-feature set...")
    X = extract_features_from_series(urls)
    print(f"Features shape: {X.shape}")  # Should be (n_samples, 14)
    
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
    print(f"Train set: {X_train.shape}, Test set: {X_test.shape}")

    # Train Random Forest classifier
    print("Training RandomForestClassifier (100 estimators)...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    print("Training complete!")

    # Predictions and metrics
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Choose averaging method based on number of classes
    avg = 'binary' if len(np.unique(y)) == 2 else 'weighted'
    try:
        prec = precision_score(y_test, y_pred, average=avg, zero_division=0)
    except Exception:
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    try:
        rec = recall_score(y_test, y_pred, average=avg, zero_division=0)
    except Exception:
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    try:
        f1 = f1_score(y_test, y_pred, average=avg, zero_division=0)
    except Exception:
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    cm = confusion_matrix(y_test, y_pred)

    # Print metrics
    print("\n" + "="*60)
    print("URL PHISHING MODEL PERFORMANCE METRICS")
    print("="*60)
    print(f'Accuracy:  {acc:.4f}')
    print(f'Precision: {prec:.4f}')
    print(f'Recall:    {rec:.4f}')
    print(f'F1 Score:  {f1:.4f}')
    print('\nConfusion Matrix:')
    print(cm)
    print('\nClassification Report:')
    print(classification_report(y_test, y_pred))
    print("="*60)

    # Save model as phishing_model.pkl
    model_path = os.path.join(model_dir, 'phishing_model.pkl')
    joblib.dump(clf, model_path)
    print(f"\n[SUCCESS] Model successfully saved to: {model_path}")

    # Save metadata
    metadata = {
        'accuracy': round(float(acc) * 100, 2),
        'precision': round(float(prec) * 100, 2),
        'recall': round(float(rec) * 100, 2),
        'f1': round(float(f1) * 100, 2),
        'total_samples': len(df),
        'features': 14,
        'model_type': 'Random Forest Classifier (Phishing URL Detection)'
    }
    metadata_path = os.path.join(model_dir, 'phishing_model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {metadata_path}")


if __name__ == '__main__':
    main()