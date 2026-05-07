from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report


def run_decision_tree(df):
    features = ["Obesity", "Inactivity", "Tobacco"]

    X = df[features]
    y = df["BusinessStrategy"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y if y.value_counts().min() >= 2 else None
    )

    model = DecisionTreeClassifier(
        max_depth=4,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n==============================")
    print("MODEL 1: Decision Tree")
    print("Business Use: Pricing, underwriting, and risk review")
    print("==============================")

    print("\nAccuracy:")
    print(accuracy_score(y_test, predictions))

    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    print("\nDecision Rules for Business Strategy:")
    print(export_text(model, feature_names=features))

    df["RecommendedBusinessStrategy"] = model.predict(X)

    df["PricingRecommendation"] = df["RecommendedBusinessStrategy"].apply(
        lambda strategy: "Consider rate revision or additional underwriting review"
        if strategy == "Enhanced Risk Review"
        else "Standard pricing approach"
    )

    df["UnderwritingRecommendation"] = df["RecommendedBusinessStrategy"].apply(
        lambda strategy: "Flag for deeper regional risk assessment"
        if strategy == "Enhanced Risk Review"
        else "Proceed with normal underwriting workflow"
    )

    return df, model