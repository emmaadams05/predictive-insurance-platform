import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESULTS_CSV_PATH = os.path.join(
    BASE_DIR,
    "output",
    "business_decision_model_results.csv"
)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_engine():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Set it in your terminal before running the app."
        )

    return create_engine(DATABASE_URL, echo=False, future=True)


def load_model_results():
    if not os.path.exists(RESULTS_CSV_PATH):
        raise FileNotFoundError(
            "Could not find output/business_decision_model_results.csv. "
            "Run python run_models.py first."
        )

    df = pd.read_csv(RESULTS_CSV_PATH)
    df["State"] = df["State"].astype(str).str.strip()

    return df


def find_state_recommendation(state_name):
    df = load_model_results()

    match = df[df["State"].str.lower() == state_name.strip().lower()]

    if match.empty:
        return None

    return match.iloc[0].to_dict()


def insert_quote_workflow(customer, recommendation):
    engine = get_database_engine()

    with engine.begin() as conn:
        party_result = conn.execute(
            text("""
                INSERT INTO PARTY (Name, Address, Email, Phone)
                OUTPUT INSERTED.PartyId
                VALUES (:name, :address, :email, :phone)
            """),
            {
                "name": customer["name"],
                "address": customer["address"],
                "email": customer["email"],
                "phone": customer["phone"]
            }
        )

        party_id = party_result.scalar_one()

        conn.execute(
            text("""
                INSERT INTO PROSPECT (PartyId)
                VALUES (:party_id)
            """),
            {"party_id": party_id}
        )

        medium_result = conn.execute(
            text("""
                SELECT MediumId
                FROM INTERACTION_MEDIUM
                WHERE MediumName = 'Web Portal'
            """)
        )

        medium_id = medium_result.scalar_one_or_none()

        conn.execute(
            text("""
                INSERT INTO INTERACTION (PartyId, MediumId, InteractionDate)
                VALUES (:party_id, :medium_id, :interaction_date)
            """),
            {
                "party_id": party_id,
                "medium_id": medium_id,
                "interaction_date": datetime.now()
            }
        )

        conn.execute(
            text("""
                INSERT INTO RISK_ASSESSMENT (
                    PartyId,
                    StateName,
                    ObesityRate,
                    InactivityRate,
                    TobaccoRate,
                    RecommendedBusinessStrategy,
                    PricingRecommendation,
                    UnderwritingRecommendation,
                    MarketSegment,
                    ProductRecommendation,
                    AssessmentDate
                )
                VALUES (
                    :party_id,
                    :state_name,
                    :obesity_rate,
                    :inactivity_rate,
                    :tobacco_rate,
                    :recommended_business_strategy,
                    :pricing_recommendation,
                    :underwriting_recommendation,
                    :market_segment,
                    :product_recommendation,
                    :assessment_date
                )
            """),
            {
                "party_id": party_id,
                "state_name": recommendation["State"],
                "obesity_rate": float(recommendation["Obesity"]),
                "inactivity_rate": float(recommendation["Inactivity"]),
                "tobacco_rate": float(recommendation["Tobacco"]),
                "recommended_business_strategy": recommendation["RecommendedBusinessStrategy"],
                "pricing_recommendation": recommendation["PricingRecommendation"],
                "underwriting_recommendation": recommendation["UnderwritingRecommendation"],
                "market_segment": recommendation["MarketSegment"],
                "product_recommendation": recommendation["ProductRecommendation"],
                "assessment_date": datetime.now()
            }
        )

    return party_id


@app.route("/", methods=["GET"])
def index():
    try:
        df = load_model_results()
        states = sorted(df["State"].dropna().unique().tolist())
        error = None
    except Exception as e:
        states = []
        error = str(e)

    return render_template("index.html", states=states, error=error)


@app.route("/quote", methods=["POST"])
def quote():
    customer = {
        "name": request.form.get("name", "").strip(),
        "address": request.form.get("address", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "state": request.form.get("state", "").strip()
    }

    if not customer["name"] or not customer["email"] or not customer["state"]:
        return render_template(
            "result.html",
            success=False,
            message="Please enter a customer name, email, and state.",
            customer=customer
        )

    recommendation = find_state_recommendation(customer["state"])

    if recommendation is None:
        return render_template(
            "result.html",
            success=False,
            message=f"No recommendation was found for {customer['state']}.",
            customer=customer
        )

    try:
        party_id = insert_quote_workflow(customer, recommendation)

        return render_template(
            "result.html",
            success=True,
            message="Quote risk review completed and saved to the database.",
            customer=customer,
            recommendation=recommendation,
            party_id=party_id
        )

    except SQLAlchemyError as e:
        return render_template(
            "result.html",
            success=False,
            message="The recommendation was generated, but the database insert failed.",
            customer=customer,
            recommendation=recommendation,
            error=str(e)
        )

    except Exception as e:
        return render_template(
            "result.html",
            success=False,
            message="An application error occurred.",
            customer=customer,
            recommendation=recommendation,
            error=str(e)
        )


if __name__ == "__main__":
    app.run(debug=True)