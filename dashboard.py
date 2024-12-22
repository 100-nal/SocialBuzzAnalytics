import pandas as pd
import streamlit as st
import plotly.express as px

# Try to load the merged dataset
@st.cache_data
def load_data():
    try:
        # Ensure the file path is correct
        data = pd.read_csv("merged_social_media_data.csv")
        return data
    except FileNotFoundError:
        st.error("The file 'merged_social_media_data.csv' was not found. Ensure it exists in the specified path.")
        return pd.DataFrame()

# Load data
merged_data_cleaned = load_data()

# Streamlit Dashboard Interface
st.title("Social Media Analytics Dashboard")

# Check if data was loaded successfully
if not merged_data_cleaned.empty:

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    options = st.sidebar.selectbox(
        "Choose an analysis:",
        [
            "Overview",
            "Platform Popularity",
            "Social Media Usage by Gender",
            "Spending by Influence Level",
            "Spending Trends by Age",
            "Interactive Scatter Plot",
        ],
    )

    # Analysis: Overview
    if options == "Overview":
        st.header("Dataset Overview")
        st.write("Here is a quick glance at the dataset:")
        st.dataframe(merged_data_cleaned.head())
        st.write(f"Number of Rows: {merged_data_cleaned.shape[0]}")
        st.write(f"Number of Columns: {merged_data_cleaned.shape[1]}")

    # Analysis: Platform Popularity
    elif options == "Platform Popularity":
        st.header("Platform Popularity")
        if "Social Media Platforms" in merged_data_cleaned.columns:
            platforms = merged_data_cleaned["Social Media Platforms"].str.split(", ").explode()
            platform_counts = platforms.value_counts()
            st.bar_chart(platform_counts)
            st.write(platform_counts)
        else:
            st.warning("'Social Media Platforms' column is missing from the dataset.")

    # Analysis: Social Media Usage by Gender
    elif options == "Social Media Usage by Gender":
        st.header("Average Social Media Usage by Gender")
        if "gender" in merged_data_cleaned.columns and "Social Media Usage (Hours/Day)" in merged_data_cleaned.columns:
            usage_by_gender = merged_data_cleaned.groupby("gender")["Social Media Usage (Hours/Day)"].mean()
            st.bar_chart(usage_by_gender)
            st.write(usage_by_gender)
        else:
            st.warning("Required columns for this analysis are missing from the dataset.")

    # Analysis: Spending by Influence Level
    elif options == "Spending by Influence Level":
        st.header("Spending by Influence Level")
        if "Influence Level" in merged_data_cleaned.columns and "Amount Spent (USD)" in merged_data_cleaned.columns:
            influence_vs_spending = merged_data_cleaned.groupby("Influence Level")["Amount Spent (USD)"].mean()
            st.bar_chart(influence_vs_spending)
            st.write(influence_vs_spending)
        else:
            st.warning("Required columns for this analysis are missing from the dataset.")

    # Analysis: Spending Trends by Age
    elif options == "Spending Trends by Age":
        st.header("Spending Trends by Age")
        if "age" in merged_data_cleaned.columns and "Amount Spent (USD)" in merged_data_cleaned.columns:
            spending_by_age = merged_data_cleaned.groupby("age")["Amount Spent (USD)"].mean()
            st.line_chart(spending_by_age)
            st.write(spending_by_age)
        else:
            st.warning("Required columns for this analysis are missing from the dataset.")

    # Analysis: Interactive Scatter Plot
    elif options == "Interactive Scatter Plot":
        st.header("Social Media Usage vs. Spending Behavior")
        required_columns = ["Social Media Usage (Hours/Day)", "Amount Spent (USD)", "Social Media Platforms", "gender", "Influence Level"]
        if all(col in merged_data_cleaned.columns for col in required_columns):
            fig = px.scatter(
                merged_data_cleaned,
                x="Social Media Usage (Hours/Day)",
                y="Amount Spent (USD)",
                color="Social Media Platforms",
                size="Amount Spent (USD)",
                hover_data=["gender", "Influence Level"],
                title="Social Media Usage vs Spending Behavior",
            )
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns for this analysis are missing from the dataset.")

    # Footer
    st.sidebar.info("Social Media Analytics Dashboard | Powered by Streamlit")

else:
    st.error("Failed to load the dataset. Please check the file path and try again.")
