
# Streamlit
import streamlit as st

# Data handling
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression

# Evaluation
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

# Streamlit → building the interactive dashboard
# Pandas & NumPy → data manipulation and analysis
# Matplotlib & Seaborn → plotting and visualization
# Scikit-learn → machine learning models and evaluation

st.header("1. Business Understanding")
st.write(" - Perform EDA on the data: Univariate, bivariate and multivariate analysis")
st.write(" - Add the model analysis")
st.write(" -  following the CRISP-DM methodology ")
st.write(" - Undertake exercise on  *streamlit* ")

st.header("2. Data Understanding")

# Load dataset (default or uploaded)
uploaded_file = st.file_uploader("Upload Diabetes Dataset (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("diabetes.csv")  # local file

# ✅ Preview data
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ✅ Shape of dataset
st.subheader("Dataset Shape")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# ✅ Column names
st.subheader("Columns in Dataset")
st.write(df.columns.tolist())


st.write(" -  The dataset contains multiple medical predictor variables such as Glucose, BMI, Age, and Insulin, alongside the target variable Outcome, which indicates whether a person has diabetes.")
st.write(" - The structure confirms a supervised classification problem with labeled data.")


# ✅ Missing Values
st.subheader("Missing Values")

missing_values = df.isnull().sum()
st.write(missing_values)

# ✅ Summary Statistics
st.subheader("Summary Statistics")

st.write(df.describe())

# ✅ Dataset Info (optional but useful)
import io

st.subheader("Dataset Information")

buffer = io.StringIO()
df.info(buf=buffer)

s = buffer.getvalue()
st.text(s)


st.write("Univariate analysis was performed to understand the distribution and characteristics of individual variables in the dataset. This involved visualizing each feature using histograms and density plots to identify patterns such as skewness, spread, and potential outliers. This step helps in understanding the behavior of each variable independently before exploring relationships between variables.")


st.subheader("Univariate Analysis")

# Select column
column = st.selectbox("Select a Feature for Analysis", df.columns)

# Plot histogram
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.histplot(df[column], kde=True, ax=ax)

ax.set_title(f"Distribution of {column}")

st.pyplot(fig)

st.write("Key Insights")
st.write(" - Most variables show skewed distributions rather than normal distribution")
st.write(" - Features like Glucose and BMI exhibit wide variability, indicating strong predictive potential")
st.write(" - Some variables such as Insulin contain extreme values, suggesting possible outliers")
st.write(" - Age distribution indicates more observations among younger individuals")
st.write(" - Non-normal distributions suggest the need for scaling and careful model selection")


st.write("Bivariate analysis was conducted to explore relationships between pairs of variables, particularly between predictor variables and the target variable (Outcome). This involved visualizing patterns using scatter plots and bar charts to identify how features such as Glucose, BMI, and Age influence the likelihood of diabetes. This step helps uncover trends, correlations, and potential predictors of the target variable.")


st.subheader("Bivariate Analysis")

# Select X (feature) and Y (target)
x_col = st.selectbox("Select Feature (X)", df.columns)

y_col = st.selectbox("Select Target (Y)", df.columns, index=len(df.columns)-1)

import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot
fig, ax = plt.subplots()

sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)

ax.set_title(f"{x_col} vs {y_col}")

st.pyplot(fig)


st.subheader("Feature vs Outcome - Insights using boxplots grouped by Outcome:")

feature = st.selectbox("Select Feature", df.columns)

fig, ax = plt.subplots()

sns.boxplot(x=df['Outcome'], y=df[feature], ax=ax)

ax.set_title(f"{feature} vs Outcome")

st.pyplot(fig)


st.write("Key Insights")
st.write(" - Glucose shows a strong positive relationship with diabetes outcome")
st.write(" - Individuals with higher BMI are more likely to have diabetes")
st.write(" - Age demonstrates a moderate positive association with the target variable")
st.write(" - Some features such as Insulin show high variability with weaker predictive patterns")
st.write(" - lear separation in certain variables indicates their usefulness for classification models")



st.subheader("Multivariate Analysis (Correlation Matrix - Correlation Heatmap)")

st.write("Multivariate analysis was performed to examine relationships among multiple variables simultaneously. This was achieved using a correlation heatmap, which highlights the strength and direction of relationships between features. This step helps identify highly correlated variables, understand feature interactions, and determine which predictors have the strongest relationship with the target variable (Outcome).")


import matplotlib.pyplot as plt
import seaborn as sns

# Create correlation matrix
corr = df.corr()

fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)

st.write("Key Insights")
st.write(" - Glucose exhibits the strongest positive correlation with diabetes outcome, confirming it as the most important predictor")
st.write(" - BMI shows a moderate positive relationship, indicating body weight influences diabetes risk")
st.write(" - Age also demonstrates a moderate association with the target variable")
st.write(" - Most other features show weak correlations, suggesting limited predictive power individually")
st.write(" - There is no strong multicollinearity among predictors, meaning features are relatively independent")




st.write("In this stage, the dataset was prepared for modeling by addressing data quality issues, separating features and target variables, and splitting the data into training and testing sets. Standardization was then applied to ensure that all features are on a similar scale, which improves the performance of machine learning algorithms such as Logistic Regression and KNN.")
    
st.subheader("Data Cleaning")

# Replace 0s with NaN for selected columns
cols_with_zero = ['Glucose', 'BloodPressure', 'BMI', 'Insulin']

df[cols_with_zero] = df[cols_with_zero].replace(0, pd.NA)

st.write("Replaced 0 values with NaN")


# Step 1: Fill missing values with mean
df = df.fillna(df.mean())

st.write("Missing values handled using mean imputation")


# Step 2: Separate Features and Target
st.subheader("Feature Selection")

target = 'Outcome'

X = df.drop(target, axis=1)
y = df[target]

st.write("Features:", X.columns.tolist())
st.write("Target:", target)

# Step 3: Train-Test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

st.write("Data split into training and testing sets")

# Step 4: Standardization
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

st.write("Data successfully standardized")

st.write("Key Insights")
st.write(" - Certain variables contained invalid zero values, which were treated as missing data")
st.write(" - Missing values were handled using mean imputation, ensuring no data loss")
st.write(" - The dataset was split into training (80%) and testing (20%) setse")
st.write(" - Feature scaling was applied to ensure all variables are on the same scale")
st.write(" - Standardization is especially important for distance-based models like KNN")



st.subheader("Modelling")

st.write(" In this stage, multiple machine learning models were developed to predict diabetes outcomes. The selected models include Logistic Regression, Random Forest, and K-Nearest Neighbors (KNN). Each model was trained on the prepared dataset and evaluated using performance metrics such as accuracy and AUC. This step aims to identify the most effective model for predicting diabetes.")

st.subheader("Model Training")

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN (k=11)": KNeighborsClassifier(n_neighbors=11)
}

# Step 2: Train Models & Make Predictions
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    results[name] = {
        "predictions": y_pred,
        "probabilities": y_prob
    }

st.write("Models trained successfully")


# Step 3: Evaluate Models (Accuracy & AUC)
from sklearn.metrics import accuracy_score, roc_auc_score

performance = {}

for name, result in results.items():
    acc = accuracy_score(y_test, result["predictions"])
    auc = roc_auc_score(y_test, result["probabilities"])
    
    performance[name] = {
        "Accuracy": acc,
        "AUC": auc
    }

st.subheader("Model Performance")
st.write(performance)


st.write("Key Insights")
st.write(" - Logistic Regression achieved the highest accuracy (76.6%), indicating that it made the most correct predictions among the models tested.")
st.write(" - Logistic Regression also recorded the highest AUC (0.824), showing that it has the best ability to distinguish between diabetic and non-diabetic cases.")
st.write(" - Random Forest performed slightly lower than Logistic Regression in both accuracy and AUC, suggesting that while it captures complex patterns, it may not generalize as well on this dataset.")
st.write(" - The KNN model (k = 11) showed the lowest performance, with accuracy and AUC of approximately 72% and 0.79 respectively, indicating that distance-based methods are less effective for this dataset.")
st.write(" - The close performance between Logistic Regression and Random Forest suggests that the dataset may have relatively strong linear relationships, which Logistic Regression captures effectively.")
st.write(" - All models achieved AUC values above 0.79, indicating that they have good classification capability and are significantly better than random guessing.")
st.write(" - Logistic Regression emerges as the best overall model, combining both high accuracy and strong AUC, making it the most reliable choice for predicting diabetes in this dataset.")


st.header("Model Evaluation")

st.write("The ROC (Receiver Operating Characteristic) curve was used to evaluate the classification performance of the models. It illustrates the trade-off between the True Positive Rate (sensitivity) and False Positive Rate across different thresholds. The Area Under the Curve (AUC) provides a single performance metric, where higher values indicate better classification ability. This visualization helps compare models beyond accuracy and confirms which model best separates the classes.")

st.header("4. Model Evaluation (ROC Curve)")

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve

fig, ax = plt.subplots()

for name, result in results.items():
    y_prob = result["probabilities"]
    
    # Compute ROC
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    
    # Get AUC value from earlier performance dict
    auc_value = performance[name]["AUC"]
    
    ax.plot(fpr, tpr, label=f"{name} (AUC = {auc_value:.2f})")

# Baseline (random classifier)
ax.plot([0,1], [0,1], 'k--')

ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curve Comparison")
ax.legend()

st.pyplot(fig)

st.write("Key Insights")
st.write(" - The ROC curves show that Logistic Regression consistently stays closer to the top-left corner, confirming its superior ability to distinguish between diabetic and non-diabetic cases.")
st.write(" - Random Forest performs closely to Logistic Regression but falls slightly below it, indicating good but not optimal classification performance.")
st.write(" - The KNN model has a lower curve compared to the other models, reinforcing its relatively weaker ability to separate the classes.")
st.write(" - All models perform better than the random baseline, as their curves lie above the diagonal line, confirming that they have learned meaningful patterns from the data.")
st.write(" - The ROC analysis supports earlier findings from accuracy and AUC, validating Logistic Regression as the most effective model for this dataset.")



st.write(" Feature importance analysis was conducted using the Random Forest model to identify which variables contribute most to predicting diabetes. This helps in understanding the key factors influencing the outcome and enhances interpretability of the model.")

st.header("5. Feature Importance (Random Forest)")

# Get trained Random Forest model
rf_model = models["Random Forest"]

# Extract importance
importances = rf_model.feature_importances_

# Create DataFrame
import pandas as pd

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Plot
st.bar_chart(importance_df.set_index("Feature"))


st.write("Key Insights")
st.write(" - Glucose emerges as the most important feature, confirming its strong relationship with diabetes outcomes observed during EDA.")
st.write(" - BMI and Age also show significant importance, indicating their influence on diabetes risk")
st.write(" - Features such as BloodPressure and SkinThickness contribute less, suggesting limited predictive power")
st.write(" - The model relies on a small number of dominant predictors, reinforcing earlier correlation findings")
st.write(" - Feature importance aligns strongly with results from both bivariate and multivariate analysis, validating the overall model consistency")


st.write("The study successfully applied the CRISP-DM methodology to analyze and predict diabetes outcomes using a combination of exploratory data analysis and machine learning models. Key insights were derived from the dataset, and model performance was evaluated using accuracy and AUC metrics.")













