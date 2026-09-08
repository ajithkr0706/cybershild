import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib


def generate_synthetic_image_dataset(n_samples=1000):
    """
    Generate synthetic dataset of image features based on statistical distributions.
    Label 0: Authentic, Label 1: AI-generated.
    """
    np.random.seed(42)
    half_samples = n_samples // 2

    # Feature 0: has_exif (Authentic has EXIF 85% of time, AI has EXIF 5% of time)
    exif_real = np.random.binomial(1, 0.85, half_samples)
    exif_ai = np.random.binomial(1, 0.05, half_samples)

    # Feature 1: has_ai_metadata (Real has 0%, AI has 25%)
    ai_meta_real = np.zeros(half_samples)
    ai_meta_ai = np.random.binomial(1, 0.25, half_samples)

    # Feature 2: file_size_ratio (Real mean 0.15, AI mean 0.25)
    fs_ratio_real = np.clip(np.random.normal(0.15, 0.05, half_samples), 0.01, 1.0)
    fs_ratio_ai = np.clip(np.random.normal(0.25, 0.08, half_samples), 0.01, 1.0)

    # Feature 3: laplacian_variance (Real mean 200, AI mean 80)
    lap_real = np.clip(np.random.normal(200.0, 50.0, half_samples), 10.0, 500.0)
    lap_ai = np.clip(np.random.normal(80.0, 30.0, half_samples), 5.0, 350.0)

    # Feature 4: color_std_dev (Real mean 45, AI mean 65)
    color_std_real = np.clip(np.random.normal(45.0, 10.0, half_samples), 5.0, 100.0)
    color_std_ai = np.clip(np.random.normal(65.0, 15.0, half_samples), 10.0, 120.0)

    # Feature 5: brightness_mean (Real mean 120, AI mean 135)
    bright_mean_real = np.clip(np.random.normal(120.0, 30.0, half_samples), 10.0, 240.0)
    bright_mean_ai = np.clip(np.random.normal(135.0, 35.0, half_samples), 10.0, 240.0)

    # Feature 6: brightness_std_dev (Real mean 60, AI mean 75)
    bright_std_real = np.clip(np.random.normal(60.0, 15.0, half_samples), 10.0, 100.0)
    bright_std_ai = np.clip(np.random.normal(75.0, 20.0, half_samples), 10.0, 120.0)

    # Feature 7: contrast (Real mean 240, AI mean 250)
    contrast_real = np.clip(np.random.normal(240.0, 15.0, half_samples), 100.0, 255.0)
    contrast_ai = np.clip(np.random.normal(250.0, 5.0, half_samples), 150.0, 255.0)

    # Feature 8: unique_colors_ratio (Real mean 0.20, AI mean 0.55)
    colors_ratio_real = np.clip(np.random.normal(0.20, 0.05, half_samples), 0.01, 1.0)
    colors_ratio_ai = np.clip(np.random.normal(0.55, 0.10, half_samples), 0.01, 1.0)

    # Feature 9: noise_estimate (Real mean 12.0, AI mean 4.5)
    noise_real = np.clip(np.random.normal(12.0, 2.5, half_samples), 1.0, 30.0)
    noise_ai = np.clip(np.random.normal(4.5, 1.5, half_samples), 0.1, 20.0)

    # Combine into a single matrix
    X_real = np.column_stack([
        exif_real, ai_meta_real, fs_ratio_real, lap_real, color_std_dev_real if 'color_std_dev_real' in locals() else color_std_real,
        bright_mean_real, bright_std_real, contrast_real, colors_ratio_real, noise_real
    ])
    X_ai = np.column_stack([
        exif_ai, ai_meta_ai, fs_ratio_ai, lap_ai, color_std_ai,
        bright_mean_ai, bright_std_ai, contrast_ai, colors_ratio_ai, noise_ai
    ])

    X = np.vstack([X_real, X_ai])
    y = np.concatenate([np.zeros(half_samples), np.ones(half_samples)])

    # Shuffle dataset
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]

    columns = [
        'has_exif', 'has_ai_metadata', 'file_size_ratio', 'laplacian_variance',
        'color_std_dev', 'brightness_mean', 'brightness_std_dev', 'contrast',
        'unique_colors_ratio', 'noise_estimate'
    ]
    df = pd.DataFrame(X, columns=columns)
    df['label'] = y.astype(int)

    return df


def main():
    root = os.path.dirname(__file__)
    model_dir = os.path.join(root, 'model')
    csv_path = os.path.join(root, 'dataset', 'images.csv')
    
    os.makedirs(model_dir, exist_ok=True)

    print("Generating synthetic image dataset...")
    df = generate_synthetic_image_dataset()
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated and saved to {csv_path}")

    X = df.drop(columns=['label']).values
    y = df['label'].values

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # Train Random Forest
    print("Training RandomForestClassifier for AI Image Detection...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    print("Training complete!")

    # Evaluation
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "=" * 60)
    print("AI IMAGE DETECTION MODEL PERFORMANCE")
    print("=" * 60)
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("=" * 60)

    # Save model
    model_path = os.path.join(model_dir, 'image_model.pkl')
    joblib.dump(clf, model_path)
    print(f"\n[SUCCESS] Image model saved to: {model_path}")

    # Save metadata
    metadata = {
        'accuracy': round(float(acc) * 100, 2),
        'precision': round(float(prec) * 100, 2),
        'recall': round(float(rec) * 100, 2),
        'f1': round(float(f1) * 100, 2),
        'total_samples': len(df),
        'features': 10,
        'model_type': 'Random Forest Classifier (AI Image Detection)'
    }
    metadata_path = os.path.join(model_dir, 'image_model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {metadata_path}")


if __name__ == '__main__':
    main()
