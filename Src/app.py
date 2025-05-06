import streamlit as st
from price_predictor import predictor
import time
import base64
from pathlib import Path

# Set the background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            filter: brightness(0.9) ;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom CSS for theme and animations
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Header bar styling */
    .header {
      position: relative;
      width: 100%;
      padding: 1.5rem 2rem;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      text-align: center;
      z-index: 2;
      margin-bottom: 2rem;
      border-radius: 0.5rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .header h1 {
      margin: 0;
      color: #fff;
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      letter-spacing: -0.02em;
    }
    
    /* Text outline/stroke for better legibility */
    .header h1, .result-animation h1 {
      -webkit-text-stroke: 0.5px rgba(0, 0, 0, 0.8);
      text-shadow:
        1px 1px 2px rgba(0,0,0,0.8),
       -1px -1px 2px rgba(0,0,0,0.8);
    }
    
    /* Overlay for better text readability with background */
    .stApp:after {
        content: "";
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        background: linear-gradient(-45deg, rgba(13,13,13,0.7), rgba(26,26,26,0.7), rgba(15,15,15,0.7), rgba(22,22,22,0.7));
        background-size: 400% 400%;
        animation: bgGradient 15s ease infinite;
        z-index: -1;
    }
    
    @keyframes bgGradient {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    /* Container styling - centered card */
    .main-container {
      background-color: rgba(20,20,20,0.9);
      backdrop-filter: blur(15px);
      padding: 2.5rem;
      border-radius: 1.2rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      margin: 0 auto;
      max-width: 800px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.1);
      position: relative;
      z-index: 1;
    }
    
    /* Rest of the existing styles */
    .centered-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    /* Typography */
    h1, h2, h3 {
      font-family: 'Inter', sans-serif;
      color: #6c8eff;
      margin-bottom: 1.2rem;
      letter-spacing: -0.02em;
      font-weight: 600;
    }
    
    p {
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }

    /* Input fields */
    .stTextInput > div > div > input {
      background-color: rgba(38, 38, 38, 0.8);
      color: #e0e0e0;
      border-radius: 0.6rem;
      border: 1px solid #444;
      padding: 0.9rem;
      font-size: 1rem;
      transition: all 0.3s ease;
      width: 100%;
    }
    .stTextInput > div > div > input:focus {
      border-color: #6c8eff;
      box-shadow: 0 0 15px rgba(108, 142, 255, 0.3);
      outline: none;
    }

    /* Buttons with gradient and animated hover */
    .stButton > button {
      background: linear-gradient(45deg, #4568dc, #6c8eff);
      color: #ffffff;
      border: none;
      border-radius: 0.6rem;
      padding: 0.9rem 1.8rem;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s ease;
      font-weight: 500;
      letter-spacing: 0.02em;
      width: 100%;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .stButton > button:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 24px rgba(108,142,255,0.6);
      background: linear-gradient(45deg, #5576e4, #7c99ff);
    }
    .stButton > button:active {
      transform: translateY(0);
    }

    /* Sidebar */
    .css-1d391kg .css-1d391kg {
      background-color: #1f1f1f;
    }
    .css-1d391kg .css-1v3pvw {
      color: #e0e0e0;
    }

    /* Divider */
    hr {
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(108, 142, 255, 0.5), transparent);
      margin: 2rem 0;
    }
    
    /* Form group spacing */
    .form-group {
      margin-bottom: 1.8rem;
    }
    
    /* Result animation */
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .result-animation {
      animation: fadeInUp 0.5s ease-out;
    }
    
    /* Icon styling */
    .icon {
      margin-right: 8px;
      color: #6c8eff;
    }
    
    /* Feature cards */
    .feature-card {
      background-color: rgba(45, 45, 45, 0.7);
      padding: 1.5rem;
      border-radius: 0.8rem;
      margin-bottom: 1rem;
      border-left: 3px solid #6c8eff;
      transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
      transform: translateX(5px);
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Set background image from the local directory
    try:
        # Try different possible paths for the background image
        possible_paths = [
            "background.jpg",
            "Src/background.jpg",
            Path(__file__).parent / "background.jpg",
            "c:/Users/honpa/OneDrive/Desktop/Programming/PlaWorDet-WARP24/Src/background.jpg",
            "c:/Users/honpa/OneDrive/Desktop/Programming/PlaWorDet-WARP24/background.jpg"
        ]
        
        background_found = False
        for path in possible_paths:
            try:
                path_obj = Path(path)
                if path_obj.exists():
                    add_bg_from_local(str(path_obj))
                    background_found = True
                    break
            except:
                continue
        
        if not background_found:
            st.sidebar.warning("Background image not found. Please add background.jpg to your project directory.")
    except Exception as e:
        st.sidebar.warning(f"Error loading background: {e}")
    
    predictor_fn = predictor()
    page = st.sidebar.selectbox("Go to", ["Prediction", "About"])

    # Add the header before the main container
    if page == "Prediction":
        st.markdown('<div class="header"><h1>⚽ Player Price Prediction</h1></div>', unsafe_allow_html=True)
    else:  # About page
        st.markdown('<div class="header"><h1>About PlaWorDet</h1></div>', unsafe_allow_html=True)

    
    
    if page == "Prediction":
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        st.markdown("<p>Enter the player's details below to calculate their estimated market value</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Using columns for layout variety
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<span class="icon">👤</span> Player Name', unsafe_allow_html=True)
            name = st.text_input("", key="player_name", placeholder="e.g., L. Messi")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<span class="icon">⚽</span> Player Position', unsafe_allow_html=True)
            # Position dropdown with shortforms only
            positions = [
                "ST", "CF", "LW", "RW", "CAM", "CM", "CDM", 
                "LM", "RM", "LB", "RB", "CB", "GK"
            ]
            position = st.selectbox("", options=positions, key="position")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<span class="icon">🏆</span> Club Name', unsafe_allow_html=True)
            club = st.text_input("", key="club", placeholder="e.g., FC Barcelona, Manchester United")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Adding some spacing to align with the other column
            st.markdown('<div style="height: 93px;"></div>', unsafe_allow_html=True)
        
        # Centered button
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        calculate_button = st.button("Calculate Price")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if calculate_button:
            # Simulate calculation time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            price = predictor_fn(name, club, position)
            
            # Clear progress bar after completion
            progress_bar.empty()
            
            # Display result with animation
            st.markdown('<div class="result-animation">', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background: linear-gradient(45deg, rgba(70,80,150,0.4), rgba(108, 142, 255, 0.3)); 
                        padding: 1.5rem; border-radius: 0.8rem; text-align: center; margin-top: 1.5rem;">
                <h2>Predicted Price</h2>
                <h1 style="font-size: 2.5rem; color: #ffffff; text-shadow: 0 0 10px rgba(108, 142, 255, 0.7);">
                    €{price:.2f} Million
                </h1>
                <p style="opacity: 0.8;">Based on current market conditions and player statistics</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:  # About page
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        st.markdown("<p>An AI/ML system for estimating football player market values</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Add local images to the about section with path finding logic
        def find_image(image_name):
            possible_image_paths = [
                f"{image_name}",
                f"Src/{image_name}",
                Path(__file__).parent / image_name,
                f"c:/Users/honpa/OneDrive/Desktop/Programming/PlaWorDet-WARP24/Src/{image_name}",
                f"c:/Users/honpa/OneDrive/Desktop/Programming/PlaWorDet-WARP24/{image_name}"
            ]
            
            for path in possible_image_paths:
                try:
                    path_obj = Path(path)
                    if path_obj.exists():
                        return str(path_obj)
                except:
                    continue
            
            return None  # Return None if image not found
        
        # Remove the image columns and icon images
        
        # Using columns for feature display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🧠 Performance Analysis</h3>
                <p>Our multilayer perceptron model analyzes player performance metrics to establish base valuations.</p>
            </div>
            
            <div class="feature-card">
                <h3>🔄 Team Chemistry</h3>
                <p>We calculate player-team fit through similarity scoring algorithms for more accurate estimations.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📊 Positional Fit</h3>
                <p>Positional distance factors assess how well a player matches required position characteristics.</p>
            </div>
            
            <div class="feature-card">
                <h3>💼 Bid Strategy</h3>
                <p>Get smart recommendations for bidding strategies based on market conditions and player value.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # === New: Accuracy Plot ===
        st.markdown("### Model Training & Validation Accuracy", unsafe_allow_html=True)
        
        # Find accuracy plot image
        accuracy_plot_path = find_image("accuracy_plot.png")
        if accuracy_plot_path:
            st.image(accuracy_plot_path, use_column_width=True,
                    caption="**Fig. 1**: Train vs. Validation Accuracy over 100 Epochs")
        else:
            st.warning("Accuracy plot image not found")
            
        st.markdown("""
        - Training accuracy rises from ~57% to ~80%.  
        - Validation accuracy climbs from ~70% to ~77%, indicating good generalization.  
        """, unsafe_allow_html=True)
        
        # === New: Loss Plot ===
        st.markdown("### Model Training & Validation Loss", unsafe_allow_html=True)
        
        # Find loss plot image
        loss_plot_path = find_image("loss_plot.png")
        if loss_plot_path:
            st.image(loss_plot_path, use_column_width=True,
                    caption="**Fig. 2**: Train vs. Validation Loss over 100 Epochs")
        else:
            st.warning("Loss plot image not found")
            
        st.markdown("""
        - Training loss decreases from 1.4 to ~0.6.  
        - Validation loss stabilizes around ~0.75, confirming effective learning.  
        """, unsafe_allow_html=True)
        
        # === New: Pipeline Diagram ===
        st.markdown("### PlaWorDet Valuation Pipeline", unsafe_allow_html=True)
        
        # Find pipeline diagram image
        pipeline_path = find_image("pipeline.png")
        if pipeline_path:
            st.image(pipeline_path, use_column_width=True,
                    caption="**Fig. 3**: End‑to‑end valuation pipeline")
        else:
            st.warning("Pipeline diagram image not found")
            
        st.markdown("""
        1. **User Entry**: Input stats, preferred position, and club name  
        2. **Base Price MLP**: Predicts a raw starting price  
        3. **Position MLP + Tree**: Determines preferred position and distance factor  
        4. **Team Chemistry**: Computes similarity score against existing roster  
        5. **Transforms**: Merges base price & chemistry into club‑specific value  
        6. **Adjustment**: Applies position factor for the final valuation  
        """, unsafe_allow_html=True)
        
        # Closing description
        st.markdown("""
        <div style="margin-top: 2rem; text-align: center;">
            <p style="opacity: 0.7; font-size: 0.9rem;">
                PlaWorDet leverages advanced ML and comprehensive datasets  
                to deliver the most accurate, club‑specific player valuations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
