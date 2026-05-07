from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_segment_label(row):
    obesity = row["Obesity"]
    inactivity = row["Inactivity"]
    tobacco = row["Tobacco"]

    highest_factor = max(
        [("Obesity", obesity), ("Inactivity", inactivity), ("Tobacco", tobacco)],
        key=lambda item: item[1]
    )[0]

    if highest_factor == "Obesity":
        return "Obesity-Driven Market Segment"
    elif highest_factor == "Inactivity":
        return "Inactivity-Driven Market Segment"
    else:
        return "Tobacco-Driven Market Segment"


def get_product_recommendation(segment):
    if segment == "Obesity-Driven Market Segment":
        return "Develop wellness-focused products with nutrition and weight management incentives"
    elif segment == "Inactivity-Driven Market Segment":
        return "Offer fitness-based discounts, activity tracking incentives, and preventative care programs"
    else:
        return "Offer smoking cessation incentives and risk-adjusted policy options"


def run_kmeans(df):
    features = ["Obesity", "Inactivity", "Tobacco"]

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    df["MarketCluster"] = model.fit_predict(X_scaled)

    cluster_summary = df.groupby("MarketCluster")[features].mean()

    cluster_labels = {}

    for cluster_id, row in cluster_summary.iterrows():
        segment = get_segment_label(row)
        cluster_labels[cluster_id] = segment

    df["MarketSegment"] = df["MarketCluster"].map(cluster_labels)
    df["ProductRecommendation"] = df["MarketSegment"].apply(get_product_recommendation)

    print("\n==============================")
    print("MODEL 2: K-Means Clustering")
    print("Business Use: Market segmentation and product design")
    print("==============================")

    print("\nCluster Summary:")
    print(cluster_summary)

    print("\nBusiness Segment Interpretation:")

    for cluster_id, row in cluster_summary.iterrows():
        segment = cluster_labels[cluster_id]

        print(f"\nCluster {cluster_id}: {segment}")
        print(row)
        print("Business Recommendation:")
        print(get_product_recommendation(segment))

    return df, model