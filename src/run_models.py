import os
import joblib

from data_loader import build_combined_dataset
from decision_tree_model import run_decision_tree
from kmeans_model import run_kmeans


def main():
    print("Building combined health and business decision dataset...")

    os.makedirs("../output", exist_ok=True)
    os.makedirs("../models", exist_ok=True)

    df = build_combined_dataset()

    print("\nCombined Dataset Preview:")
    print(df.head())

    print("\nBusiness Strategy Counts:")
    print(df["BusinessStrategy"].value_counts())

    df, decision_tree_model = run_decision_tree(df)
    df, kmeans_model = run_kmeans(df)

    output_file = os.path.join("output", "business_decision_model_results.csv")
    df.to_csv(output_file, index=False)

    decision_tree_path = os.path.join("models", "decision_tree_model.joblib")
    kmeans_path = os.path.join("models", "kmeans_model.joblib")

    joblib.dump(decision_tree_model, decision_tree_path)
    joblib.dump(kmeans_model, kmeans_path)

    print("\nFinal Business Decision Output Preview:")
    print(df[[
        "State",
        "Obesity",
        "Inactivity",
        "Tobacco",
        "RecommendedBusinessStrategy",
        "PricingRecommendation",
        "UnderwritingRecommendation",
        "MarketSegment",
        "ProductRecommendation"
    ]].head())

    print(f"\nResults saved to {output_file}")
    print(f"Decision Tree model saved to {decision_tree_path}")
    print(f"K-Means model saved to {kmeans_path}")


if __name__ == "__main__":
    main()