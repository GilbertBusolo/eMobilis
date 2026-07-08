import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load Assets
# -----------------------------

model = joblib.load(
    "gradient_boosting_tree_survival.pkl"
)

encoders = joblib.load(
    "label_encoders.pkl"
)

feature_names = joblib.load(
    "feature_names.pkl"
)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Tree Survival Prediction System",
    layout="wide"
)

st.title("Tree Survival Prediction System")

st.markdown(
"""
This system predicts the probability that a planted tree will survive
using a Gradient Boosting Machine Learning Model.
"""
)

st.header("Tree Information")

col1, col2 = st.columns(2)

with col1:

    tree_species = st.selectbox(
        "Tree Species",
        encoders['Tree_Species'].classes_
    )

    height = st.number_input(
        "Tree Height (cm)",
        min_value=0.0,
        value=50.0
    )

    tree_age_days = st.number_input(
        "Tree Age (Days)",
        min_value=1,
        value=365
    )

with col2:

    circumference = st.number_input(
        "Tree Circumference (cm)",
        min_value=0.0,
        value=5.0
    )

    num_pc_trees = st.number_input(
        "Number of Trees",
        min_value=1,
        value=10
    )

    st.header("Location Information")

col1, col2 = st.columns(2)

with col1:

    zone = st.selectbox(
        "Zone",
        encoders['Zone'].classes_
    )

with col2:

    niche = st.selectbox(
        "Planting Niche",
        encoders['Niche'].classes_
    )


    st.header("Farmer Information")

col1, col2 = st.columns(2)

with col1:

    farmer_age = st.number_input(
        "Farmer Age",
        min_value=18,
        max_value=100,
        value=40
    )

with col2:

    farmer_gender = st.selectbox(
        "Farmer Gender",
        ["Male", "Female"]
    )

st.header("Management Practices")

col1, col2 = st.columns(2)

with col1:

    watering = st.selectbox(
        "Watering Applied?",
        ["No", "Yes"]
    )

    hours_watering = st.number_input(
        "Hours Watering",
        min_value=0.0,
        value=1.0
    )

    pruning = st.selectbox(
        "Pruning Performed?",
        ["No", "Yes"]
    )

with col2:

    mulch = st.selectbox(
        "Mulching Applied?",
        ["No", "Yes"]
    )

    hours_mulching = st.number_input(
        "Hours Mulching",
        min_value=0.0,
        value=1.0
    )

    fencing = st.selectbox(
        "Fencing Available?",
        ["No", "Yes"]
    )

    st.header("Tree Health & Environmental Factors")

col1, col2 = st.columns(2)

with col1:

    fert_trees = st.selectbox(
        "Fertilizer Applied?",
        ["No", "Yes"]
    )

    weed_prob = st.selectbox(
        "Weed Problem?",
        ["No", "Yes"]
    )

with col2:

    pest_prob = st.selectbox(
        "Pest Problem?",
        ["No", "Yes"]
    )

    disease_prob = st.selectbox(
        "Disease Problem?",
        ["No", "Yes"]
    )

#Convert Yes/No to 0/1
watering = 1 if watering == "Yes" else 0
pruning = 1 if pruning == "Yes" else 0
mulch = 1 if mulch == "Yes" else 0
fencing = 1 if fencing == "Yes" else 0

fert_trees = 1 if fert_trees == "Yes" else 0
weed_prob = 1 if weed_prob == "Yes" else 0
pest_prob = 1 if pest_prob == "Yes" else 0
disease_prob = 1 if disease_prob == "Yes" else 0

#Gender Mapping
gender_map = {
    "Male": 0,
    "Female": 1
}

gender_encoded = gender_map[farmer_gender]

#Management Score
management_score = (
    watering +
    pruning +
    mulch +
    fencing
)

#Encoded Categorical Variables
tree_species_encoded = encoders[
    'Tree_Species'
].transform([tree_species])[0]

zone_encoded = encoders[
    'Zone'
].transform([zone])[0]

niche_encoded = encoders[
    'Niche'
].transform([niche])[0]

#Prediction Selection
st.markdown("---")

if st.button("Predict Tree Survival"):

    input_df = pd.DataFrame([{

        'Tree_Species': tree_species_encoded,
        'Zone': zone_encoded,

        'Farmer_Age': farmer_age,
        'Farmer_Gender': gender_encoded,

        'Num_PC_Trees': num_pc_trees,

        'Height': height,
        'Circumference': circumference,

        'Watering': watering,
        'Hours_Watering': hours_watering,

        'Pruning': pruning,

        'Mulch': mulch,
        'Hours_Mulching': hours_mulching,

        'Fencing': fencing,

        'Fert_Trees': fert_trees,

        'Weed_Prob': weed_prob,
        'Pest_Prob': pest_prob,
        'Disease_Prob': disease_prob,

        'Niche': niche_encoded,

        'Tree_Age_Days': tree_age_days,

        'Management_Score': management_score

    }])

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(
        input_df
    )[0][1]

    #Results Dashboard
    st.header("📊 Prediction Results")

    st.metric(
        "Survival Probability",
        f"{probability*100:.1f}%"
    )

    st.metric(
    "Survival Probability",
    f"{probability*100:.2f}%"
    )

    # if prediction == 1:

    #     st.success(
    #         "Tree is likely to survive."
    #     )

    # else:

    #     st.error(
    #         "Tree is unlikely to survive."
    #     )

    #Risk Intepretation
    if probability >= 0.80:

        st.success(
            "High Survival Probability"
        )

    elif probability >= 0.60:

        st.warning(
            "Moderate Survival Probability"
        )

    else:

        st.error(
            "Low Survival Probability"
        )

#Recommendations
# st.subheader("Recommendations")

# if probability < 0.60:

#         st.write(
#             """
#             • Increase watering frequency
#             • Apply mulching
#             • Improve fencing protection
#             • Monitor pests and diseases
#             • Conduct regular inspections
#             """
#         )

# else:

#         st.write(
#             """
#             • Continue existing management practices
#             • Maintain watering schedule
#             • Monitor growth performance
#             • Continue pest surveillance
#             """
#         )

