import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -----------------------------
# Load Assets
# -----------------------------
ASSET_DIR = Path(__file__).resolve().parent

model = joblib.load(ASSET_DIR / "gradient_boosting_tree_survival.pkl")
encoders = joblib.load(ASSET_DIR / "label_encoders.pkl")
feature_names = joblib.load(ASSET_DIR / "feature_names.pkl")

# -----------------------------
# Human-readable labels for the legacy model
# -----------------------------
# The current saved Tree_Species encoder contains numeric string labels. These dictionaries let the
# Streamlit UI show names while still sending the numeric codes expected by the
# already-trained model.
LEGACY_SPECIES_TO_MODEL_CODE = {
    "Acacia saligna": 0,
    "Azadiracta indica": 1,
    "Carica papaya": 12,
    "Casimiroa edulis": 14,
    "Citrus sinensis": 15,
    "Coffea arabica": 16,
    "Cordia africana": 17,
    "Faidherbia albida": 18,
    "Grevillea robusta": 19,
    "Jacaranda mimosifolia": 20,
    "Malus domestica": 2,
    "Mangifera indica": 3,
    "Melia volkensii": 4,
    "Moringa oleifera": 5,
    "Olea africana": 7,
    "Others": 8,
    "Persea americana": 9,
    "Psidium guajava": 10,
    "Rhamnus prinodes": 11,
    "Vachellia seyal": 13,
    "Not specified / NA": 6,
}

LEGACY_ZONE_TO_MODEL_CODE = {
    "East Harerge": 0,
    "East Shoa": 1,
    "East Tigray": 2,
    "Southeastern": 3,
}

LEGACY_NICHE_TO_MODEL_CODE = {
    "Along_Terraces": 0,
    "Ex_Boundary": 1,
    "Home_Compound": 2,
    "In_Boundary": 3,
    "Not specified / NA": 4,
    "Other": 5,
    "Scattered": 6,
    "Woodlot": 7,
}


def encoder_contains_only_numeric_codes(encoder_key: str) -> bool:
    """Return True when the saved encoder contains labels such as '0', '1', '10'."""
    encoder = encoders.get(encoder_key)
    if encoder is None:
        return True

    classes = [str(value).strip() for value in encoder.classes_]
    return all(value.isdigit() for value in classes)


def get_display_mapping(encoder_key: str, legacy_mapping: dict[str, int]) -> dict[str, int]:
    """Use readable legacy labels for the old model, otherwise use encoder classes directly."""
    if encoder_contains_only_numeric_codes(encoder_key):
        return legacy_mapping

    encoder = encoders[encoder_key]
    return {
        str(label): int(encoder.transform([label])[0])
        for label in encoder.classes_
    }


def yes_no_to_int(value: str) -> int:
    return 1 if value == "Yes" else 0


species_mapping = get_display_mapping("Tree_Species", LEGACY_SPECIES_TO_MODEL_CODE)
zone_mapping = get_display_mapping("Zone", LEGACY_ZONE_TO_MODEL_CODE)
niche_mapping = get_display_mapping("Niche", LEGACY_NICHE_TO_MODEL_CODE)

species_options = [name for name in species_mapping if name != "Not specified / NA"]
species_options.append("Not specified / NA")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Tree Survival Prediction System",
    layout="wide",
)

st.title("Tree Survival Prediction System")

st.markdown(
    """
This system predicts the probability that a planted tree will survive using a
Gradient Boosting Machine Learning Model. The app shows readable category
names to users and uses numeric model codes only internally.

Gradient Boosting is a supervised machine learning algorithm that builds an ensemble of decision trees sequentially to improve predictive performance. Rather than relying on a single decision tree, the algorithm combines multiple weak learners, with each new tree trained to correct the errors made by the previous ones, thereby progressively reducing prediction error and enhancing model accuracy. In this study, Gradient Boosting was used to predict tree survival probability based on variables such as tree species, height, circumference, age, planting zone, management practices, pest infestation, disease occurrence, and environmental conditions. The model was evaluated alongside Logistic Regression, Decision Tree, Random Forest, and K-Nearest Neighbors (KNN), and it demonstrated the best overall performance across the selected evaluation metrics. Its superior predictive ability is attributed to its capacity to capture complex non-linear relationships among biological, management, and environmental factors while reducing bias and variance through iterative error correction, making it well suited for tree survival prediction.
"""


)
# Style and give page some forestry background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://media.istockphoto.com/id/2208884487/photo/green-leaves-background.webp?a=1&b=1&s=612x612&w=0&k=20&c=QZ7pWS6bb09fu4bMayyUliykJhDw_cRFiJJLKqEeHcs=");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Inputs
# -----------------------------
st.header("Tree Information")

col1, col2 = st.columns(2)

with col1:
    tree_species = st.selectbox(
        "Tree Species",
        species_options,
        index=species_options.index("Mangifera indica") if "Mangifera indica" in species_options else 0,
    )

    height = st.number_input(
        "Tree Height (cm)",
        min_value=0.1,
        value=40.0,
        step=0.1,
        help="Use the measured tree height. Zero is not accepted because it produces unreliable predictions.",
    )

    tree_age_days = st.number_input(
        "Tree Age (Days)",
        min_value=1,
        value=365,
        step=1,
    )

with col2:
    circumference = st.number_input(
        "Tree Circumference (cm)",
        min_value=0.1,
        value=3.5,
        step=0.1,
        help="Use the measured stem circumference. Zero is not accepted because it produces unreliable predictions.",
    )

    num_pc_trees = st.number_input(
        "Number of Trees",
        min_value=1,
        value=18,
        step=1,
    )

st.header("Location Information")

col1, col2 = st.columns(2)

with col1:
    zone = st.selectbox(
        "Zone",
        list(zone_mapping.keys()),
    )

with col2:
    niche = st.selectbox(
        "Planting Niche",
        list(niche_mapping.keys()),
    )

st.header("Farmer Information")

col1, col2 = st.columns(2)

with col1:
    farmer_age = st.number_input(
        "Farmer Age",
        min_value=18,
        max_value=100,
        value=40,
        step=1,
    )

with col2:
    farmer_gender = st.selectbox(
        "Farmer Gender",
        ["Male", "Female"],
    )

st.header("Management Practices")

col1, col2 = st.columns(2)

with col1:
    watering_label = st.selectbox(
        "Watering Applied?",
        ["No", "Yes"],
    )

    if watering_label == "Yes":
        hours_watering = st.number_input(
            "Hours Watering",
            min_value=0.01,
            value=0.16,
            step=0.01,
        )
    else:
        hours_watering = 0.0
        st.caption("Hours Watering set to 0 because watering is marked as No.")

    pruning_label = st.selectbox(
        "Pruning Performed?",
        ["No", "Yes"],
    )

with col2:
    mulch_label = st.selectbox(
        "Mulching Applied?",
        ["No", "Yes"],
    )

    if mulch_label == "Yes":
        hours_mulching = st.number_input(
            "Hours Mulching",
            min_value=0.01,
            value=0.30,
            step=0.01,
        )
    else:
        hours_mulching = 0.0
        st.caption("Hours Mulching set to 0 because mulching is marked as No.")

    fencing_label = st.selectbox(
        "Fencing Available?",
        ["No", "Yes"],
    )

st.header("Tree Health & Environmental Factors")

col1, col2 = st.columns(2)

with col1:
    fert_trees_label = st.selectbox(
        "Fertilizer Applied?",
        ["No", "Yes"],
    )

    weed_prob_label = st.selectbox(
        "Weed Problem?",
        ["No", "Yes"],
    )

with col2:
    pest_prob_label = st.selectbox(
        "Pest Problem?",
        ["No", "Yes"],
    )

    disease_prob_label = st.selectbox(
        "Disease Problem?",
        ["No", "Yes"],
    )

# -----------------------------
# Encode Inputs
# -----------------------------
watering = yes_no_to_int(watering_label)
pruning = yes_no_to_int(pruning_label)
mulch = yes_no_to_int(mulch_label)
fencing = yes_no_to_int(fencing_label)
fert_trees = yes_no_to_int(fert_trees_label)
weed_prob = yes_no_to_int(weed_prob_label)
pest_prob = yes_no_to_int(pest_prob_label)
disease_prob = yes_no_to_int(disease_prob_label)

gender_map = {
    "Male": 0,
    "Female": 1,
}

gender_encoded = gender_map[farmer_gender]
management_score = watering + pruning + mulch + fencing

tree_species_encoded = species_mapping[tree_species]
zone_encoded = zone_mapping[zone]
niche_encoded = niche_mapping[niche]

# -----------------------------
# Prediction
# -----------------------------
st.markdown("---")

if st.button("Predict Tree Survival"):
    validation_errors = []
    risk_flags = []

    if height <= 0:
        validation_errors.append("Tree height must be greater than 0 cm.")

    if circumference <= 0:
        validation_errors.append("Tree circumference must be greater than 0 cm.")

    if watering == 0 and hours_watering > 0:
        validation_errors.append("Hours watering cannot be greater than 0 when watering is marked as No.")

    if mulch == 0 and hours_mulching > 0:
        validation_errors.append("Hours mulching cannot be greater than 0 when mulching is marked as No.")

    if management_score <= 1:
        risk_flags.append("Very low management support")

    if watering == 0:
        risk_flags.append("No watering")

    if fert_trees == 0:
        risk_flags.append("No fertilizer")

    if weed_prob == 1:
        risk_flags.append("Weed problem present")

    if pest_prob == 1:
        risk_flags.append("Pest problem present")

    if disease_prob == 1:
        risk_flags.append("Disease problem present")

    if tree_age_days >= 180 and height < 20:
        risk_flags.append("Low height for tree age")

    if circumference < 1:
        risk_flags.append("Very low circumference")

    if validation_errors:
        st.error("Please correct the input values before running prediction.")
        for error in validation_errors:
            st.write(f"• {error}")
        st.stop()

    input_df = pd.DataFrame([{
        "Tree_Species": tree_species_encoded,
        "Zone": zone_encoded,
        "Farmer_Age": farmer_age,
        "Farmer_Gender": gender_encoded,
        "Num_PC_Trees": num_pc_trees,
        "Height": height,
        "Circumference": circumference,
        "Watering": watering,
        "Hours_Watering": hours_watering,
        "Pruning": pruning,
        "Mulch": mulch,
        "Hours_Mulching": hours_mulching,
        "Fencing": fencing,
        "Fert_Trees": fert_trees,
        "Weed_Prob": weed_prob,
        "Pest_Prob": pest_prob,
        "Disease_Prob": disease_prob,
        "Niche": niche_encoded,
        "Tree_Age_Days": tree_age_days,
        "Management_Score": management_score,
    }])

    # Keep the exact feature order expected by the saved model.
    input_df = input_df.reindex(columns=feature_names)

    survival_probability = float(model.predict_proba(input_df)[0][1])
    model_prediction = int(model.predict(input_df)[0])
    risk_count = len(risk_flags)

    st.header("📊 Prediction Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model Survival Probability",
            f"{survival_probability * 100:.1f}%",
        )

    with col2:
        st.metric(
            "Model Class",
            "Survive" if model_prediction == 1 else "Not Survive",
        )

    with col3:
        st.metric(
            "Risk Flags",
            risk_count,
        )

    st.subheader("Decision")

    # The model is highly optimistic because most training records survived.
    # This guard prevents clearly risky field conditions from being displayed
    # as a clean success just because the model probability is high.
    if risk_count >= 4:
        st.error(
            "High-risk field conditions detected. Do not mark this case as successful without review/intervention."
        )
    elif survival_probability >= 0.80:
        st.success("High survival probability")
    elif survival_probability >= 0.60:
        st.warning("Moderate survival probability")
    else:
        st.error("Low survival probability")

    if risk_flags:
        st.subheader("Risk Factors Detected")
        for flag in risk_flags:
            st.write(f"• {flag}")

    st.subheader("Recommendations")

    if risk_count >= 4 or survival_probability < 0.60:
        st.write(
            """
• Increase watering where appropriate
• Apply mulching to conserve soil moisture
• Improve fencing/protection
• Monitor and control weeds, pests and diseases
• Reassess the tree before recording it as a successful survival case
"""
        )
    else:
        st.write(
            """
• Continue the current management practices
• Maintain watering and mulching schedules where applicable
• Continue regular pest, disease and weed monitoring
• Reassess growth during follow-up visits
"""
        )

    with st.expander("Show encoded values sent to the model"):
        st.write(
            pd.DataFrame([{
                "Tree Species Displayed": tree_species,
                "Tree_Species Model Code": tree_species_encoded,
                "Zone Displayed": zone,
                "Zone Model Code": zone_encoded,
                "Niche Displayed": niche,
                "Niche Model Code": niche_encoded,
            }])
        )
