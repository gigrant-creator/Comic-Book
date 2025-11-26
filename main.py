import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="AI Comic Studio", page_icon="💥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');
    
    .stApp {
        background-color: #202020;
    }
    
    h1 {
        font-family: 'Bangers', cursive;
        color: #FFD700;
        letter-spacing: 2px;
        font-size: 60px;
        text-shadow: 4px 4px #FF0000;
        text-align: center;
    }
    
    h3 {
        color: white;
        text-align: center;
    }

    /* Comic Panel Borders */
    .stImage {
        border: 4px solid white;
        box-shadow: 10px 10px 0px black;
    }
    
    .stButton>button {
        background-color: #FF0000;
        color: white;
        font-family: 'Bangers', cursive;
        font-size: 24px;
        border: 2px solid white;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💥 AI COMIC STUDIO 💥")
st.markdown("### HAFTR STEM SUMMIT 2026")

# --- 2. SIDEBAR SETUP ---
if "HF_TOKEN" in st.secrets:
    api_key = st.secrets["HF_TOKEN"]
else:
    api_key = st.sidebar.text_input("Enter Hugging Face Token", type="password")

st.sidebar.header("🎨 Art Style")
art_style = st.sidebar.selectbox(
    "Choose your vibe:",
    ["Classic Superhero (Marvel/DC)", "Japanese Manga (B&W)", "Pixar 3D", "Dark Noir (Sin City)"]
)

# --- 3. THE PROMPT ENGINE ---
# This adds hidden "magic words" to make the art look good
style_prompts = {
    "Classic Superhero (Marvel/DC)": "comic book style, vibrant colors, bold ink lines, action shot, marvel comics style, detailed, 4k",
    "Japanese Manga (B&W)": "manga style, black and white, japanese comic, speed lines, high contrast, detailed ink",
    "Pixar 3D": "3d render, pixar style, disney animation, cute, round shapes, 8k, unreal engine",
    "Dark Noir (Sin City)": "film noir style, high contrast, black and white with red accents, frank miller style, dramatic lighting"
}

# --- 4. THE STORYBOARD (INPUTS) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Panel 1: The Setup")
    p1_text = st.text_area("What happens first?", placeholder="A giant robot lands in Times Square...")

with col2:
    st.markdown("#### Panel 2: The Action")
    p2_text = st.text_area("What happens next?", placeholder="A hero flies in and punches the robot...")

with col3:
    st.markdown("#### Panel 3: The Climax")
    p3_text = st.text_area("How does it end?", placeholder="The robot explodes into confetti...")

# --- 5. GENERATION LOGIC ---
if st.button("DRAW MY COMIC PAGE! 🚀"):
    if not api_key:
        st.error("Please enter your API Token in the sidebar!")
    else:
        client = InferenceClient(token=api_key)
        
        # We use Stable Diffusion XL (SDXL) - The best open-source image model
        model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        
        panels = [p1_text, p2_text, p3_text]
        columns = [col1, col2, col3]
        
        for i, prompt in enumerate(panels):
            if prompt:
                with columns[i]:
                    with st.spinner(f"Drawing Panel {i+1}..."):
                        try:
                            # Combine user text + secret style text
                            final_prompt = f"{prompt}, {style_prompts[art_style]}"
                            
                            image = client.text_to_image(
                                model_id,
                                final_prompt,
                                negative_prompt="blurry, bad anatomy, extra fingers, text, watermark"
                            )
                            
                            st.image(image, use_column_width=True)
                            st.caption(f"Panel {i+1}")
                            
                        except Exception as e:
                            st.error(f"Error drawing panel {i+1}")
                            # If SDXL fails (it's heavy), try a lighter model automatically
                            st.warning("Trying lighter model...")
