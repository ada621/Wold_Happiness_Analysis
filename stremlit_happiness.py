import streamlit as st
import pandas as pd
from PIL import Image
import os

# Streamlit sayfa konfigürasyonu
st.set_page_config(
    page_title="World Happiness Analysis",
    page_icon="😊",
    layout="wide"
)

st.title("🌍 World Happiness Analysis Dashboard")
st.markdown("---")

# Sidebar menu
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose Analysis:",
    ["📊 Overview", "🖼️ Results", "📈 Data"]
)

if page == "📊 Overview":
    st.header("Analysis Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2018 vs 2019 Analysis")
        st.write("""
        - **Models**: OLS for 2018, Robust OLS for 2019
        - **Key Finding**: Freedom to make life choices has strongest effect
        - **Data Quality**: Heteroscedasticity detected in 2019
        """)
    
    with col2:
        st.subheader("Variable Importance")
        st.write("""
        1. Freedom to make life choices (1.45/1.37)
        2. Social support (1.12/1.01)  
        3. Healthy life expectancy (1.08/0.82)
        4. GDP per capita (0.78/1.09)
        """)

elif page == "🖼️ Results":
    st.header("Analysis Results")
    
    figures_path = os.path.join("figures")
    
    # Görselleri göster
    images = ["degisken_etkileri_yillar.png", "mutluluk_etiket_dagilimi.png", 
              "tahmin_vs_gercek_2018.png", "tahmin_vs_gercek_2019.png"]
    
    titles = ["📊 Variable Effects", "🏷️ Label Distribution", 
              "📈 2018 Predictions", "📉 2019 Predictions"]
    
    for img_name, title in zip(images, titles):
        st.subheader(title)
        img_path = os.path.join(figures_path, img_name)
        
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
        

elif page == "📈 Data":
    st.header("Data Overview")
    
    # CSV dosyalarını yükle
    
    df_2018 = pd.read_csv("world_happiness_analysis/regresyon_2018.csv")
    df_2019 = pd.read_csv("world_happiness_analysis/regresyon_2019.csv")
        
    col1, col2 = st.columns(2)
    with col1:
            st.subheader("2018 Data")
            st.dataframe(df_2018.head())
        
    with col2:
            st.subheader("2019 Data")
            st.dataframe(df_2019.head())
    
    

# Footer
st.markdown("---")
st.markdown("### 🎓 Analysis by Psychology → Data Science Student")