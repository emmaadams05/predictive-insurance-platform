from data_loader import build_combined_dataset
from decision_tree_model import run_decision_tree
from kmeans_model import run_kmeans
import joblib
import os


def main():
    print("Building combined health and business decision dataset...")

    df = build_combined_dataset()

    print("\nCombined Dataset Preview:")
    print(df.head())

    print("\nBusiness Strategy Counts:")
    print(df["BusinessStrategy"].value_counts())

    df, decision_tree_model = run_decision_tree(df)
    df, kmeans_model = run_kmeans(df)

    output_file = "output/business_decision_model_results.csv"
    df.to_csv(output_file, index=False)

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


if __name__ == "__main__":
    main()