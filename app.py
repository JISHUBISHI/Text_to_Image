import streamlit as st
from image_generation import generate_image
import os
from PIL import Image
import time
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #e0e0e0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
    }
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.markdown("<h1 style='text-align: center; color: #2196F3;'>🎨 AI Image Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Transform your imagination into reality with AI-powered image generation</p>", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.markdown("<h2 style='color: #2196F3;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    timeout = st.slider("Generation Timeout (seconds)", 30, 120, 60)
    
    st.markdown("---")
    st.markdown("<h3 style='color: #2196F3;'>💡 Tips for Better Results</h3>", unsafe_allow_html=True)
    st.markdown("- Be specific in your descriptions")
    st.markdown("- Include style references (e.g., 'in the style of Van Gogh')")
    st.markdown("- Add quality indicators (e.g., 'high quality', 'detailed', '4k')")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #2196F3;'>ℹ️ About</h3>", unsafe_allow_html=True)
    st.markdown("This app uses Stable Diffusion XL to generate images from text prompts.")
    st.markdown("Made with ❤️ using Streamlit")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area("Enter your image prompt:", 
                         placeholder="A beautiful sunset over mountains, high quality, detailed, 4k",
                         height=100)
    
    if st.button("✨ Generate Image", key="generate"):
        if not prompt:
            st.warning("Please enter a prompt!")
        else:
            with st.spinner("🎨 Creating your masterpiece... This may take a minute."):
                try:
                    # Generate image
                    result = generate_image(prompt, timeout=timeout)
                    
                    if result:
                        # Display the generated image
                        st.image(result, caption="Generated Image", use_column_width=True)
                        
                        # Convert image to bytes for download
                        buffered = BytesIO()
                        result.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        # Download button with custom styling
                        st.markdown(f"""
                            <a href="data:image/png;base64,{img_str}" download="generated_image.png">
                                <button style="
                                    background: linear-gradient(45deg, #4CAF50, #45a049);
                                    color: white;
                                    padding: 12px 24px;
                                    border: none;
                                    border-radius: 10px;
                                    cursor: pointer;
                                    font-weight: bold;
                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                    transition: all 0.3s ease;
                                ">
                                    💾 Download Image
                                </button>
                            </a>
                        """, unsafe_allow_html=True)
                        
                        st.success("Image generated successfully! Click the download button to save it.")
                    else:
                        st.error("Failed to generate image. Please try again with a different prompt.")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

with col2:
    st.markdown("<h3 style='color: #2196F3;'>🎯 Example Prompts</h3>", unsafe_allow_html=True)
    st.markdown("""
    - "A serene mountain landscape at sunset, digital art, 4k"
    - "A futuristic city with flying cars, cyberpunk style, detailed"
    - "A magical forest with glowing mushrooms, fantasy art, high quality"
    - "A cute puppy playing in a field of flowers, photorealistic"
    - "An astronaut exploring an alien planet, sci-fi, cinematic"
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>© 2024 AI Image Generator | Powered by Stable Diffusion XL</p>", unsafe_allow_html=True)
