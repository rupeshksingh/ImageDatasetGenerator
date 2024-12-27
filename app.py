import streamlit as st
import os
from src.utils.config import Settings
from src.pipeline import ImageDatasetPipeline
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Image Dataset Builder",
    page_icon="🖼️",
    layout="wide"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🖼️ Image Dataset Builder")
    st.markdown("Build custom image datasets from web scraping with AI-powered captioning")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    serp_api_key = st.sidebar.text_input("SERP API Key", type="password")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    
    max_images = st.sidebar.slider(
        "Max Images per Query",
        min_value=1,
        max_value=50,
        value=10
    )
    
    max_concurrent = st.sidebar.slider(
        "Max Concurrent Downloads",
        min_value=1,
        max_value=10,
        value=5
    )
    
    # Main content
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="E.g., Show me different types of renewable energy installations"
    )
    
    if st.button("Build Dataset", disabled=not (serp_api_key and openai_api_key and prompt)):
        with st.spinner("Building dataset..."):
            try:
                settings = Settings(
                    SERP_API_KEY=serp_api_key,
                    OPENAI_API_KEY=openai_api_key,
                    MAX_IMAGES_PER_QUERY=max_images,
                    MAX_CONCURRENT_DOWNLOADS=max_concurrent
                )
                
                pipeline = ImageDatasetPipeline(settings)
                dataset = pipeline.build_dataset(prompt)
                
                # Display results
                st.success(f"Successfully created dataset with {dataset.metadata.total_images} images!")
                
                # Create tabs for different views
                tabs = st.tabs(["Gallery", "Metadata", "Raw Data"])
                
                # Gallery tab
                with tabs[0]:
                    cols = st.columns(3)
                    for idx, img_data in enumerate(dataset.images):
                        col = cols[idx % 3]
                        with col:
                            image = Image.open(img_data.local_path)
                            st.image(image, caption=img_data.caption)
                
                # Metadata tab
                with tabs[1]:
                    st.json(dataset.metadata.model_dump())
                
                # Raw Data tab
                with tabs[2]:
                    df = pd.DataFrame([img.model_dump() for img in dataset.images])
                    st.dataframe(df)
                
            except Exception as e:
                st.error(f"Error building dataset: {str(e)}")

if __name__ == "__main__":
    main()