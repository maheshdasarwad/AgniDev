import streamlit as st
from crop_advisor import CropAdvisor
from image_analyzer import ImageAnalyzer
from financial_planning import display_financial_planning
from dotenv import load_dotenv
import os

# Set page configuration
st.set_page_config(
    page_title="Farmer's Assistant",
    page_icon="🍃",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Language Strings for UI texts
LANGUAGE_STRINGS = {
    "en": {
        "welcome": "Welcome, Farmer!",
        "page_header": "Farmer's Crop Planning Assistant",
        "main_header": "Smart Farm Manager",
        "crop_advisor": "Crop Advisor",
        "image_analysis": "Image Analysis",
        "financial_planning": "Financial Planning",
        "enter_crop_name": "Enter Crop Name",
        "get_crop_advice": "Get Crop Advice",
        "analyzing_image": "Analyzing image...",
        "upload_image": "Upload Crop Image",
        "get_financial_plan": "Get Financial Plan",
        "enter_crop_type": "Enter Crop Type",
        "enter_land_area": "Enter Land Area (acres):",
        "enter_budget": "Enter Budget (INR):"
    },
    "mr": {
        "welcome": "शेतकरी, तुमचे स्वागत आहे!",
        "page_header": "शेतकर्‍यासाठी शेती नियोजन सहाय्यक",
        "main_header": "स्मार्ट फार्म मॅनेजर",
        "crop_advisor": "पिक सल्ला",
        "image_analysis": "प्रतिमा विश्लेषण",
        "financial_planning": "आर्थिक नियोजन",
        "enter_crop_name": "पिकाचे नाव भरा",
        "get_crop_advice": "सल्ला मिळवा",
        "analyzing_image": "प्रतिमा विश्लेषण केले जात आहे...",
        "upload_image": "पिकाची प्रतिमा अपलोड करा",
        "get_financial_plan": "आर्थिक योजना मिळवा",
        "enter_crop_type": "पिकाचे नाव",
        "enter_land_area": "जमीन क्षेत्रफळ (एकर):",
        "enter_budget": "बजेट (INR):"
    }
}

# Sidebar language selection with human-readable options
lang_option = st.sidebar.selectbox(
    "भाषा निवडा / Select Language",
    ["मराठी", "English"],
    index=0  # Set Marathi as default
)
language = "en" if lang_option == "English" else "mr"

def inject_header():
    header = f"""
    <header>
        <div class="header-content">
            <div class="logo marathi-text">
                <span>🍃 {LANGUAGE_STRINGS[language]['main_header']}</span>
             <!--   <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" alt="home">  -->
            </div>
        <!--    <div class="user-actions marathi-text">
                <span>{LANGUAGE_STRINGS[language]['welcome']}</span>
            </div>  -->
        </div>
    </header>
    """
    st.markdown(header, unsafe_allow_html=True)

# Update all text containers to use marathi-text class
def display_crop_advisor():
    # ... existing code ...
    st.markdown(
        f"<div class='chat-response marathi-text'><strong>{'सल्ला'}:</strong> {advice}</div>",
        unsafe_allow_html=True
    )
def inject_footer():
    """
    Renders the fixed footer at the bottom of the page.
    """
    footer = """
    <footer>
        <div class="footer-content">
            <div class="footer-left">
                <p>© 2025 Smart Farm Manager. All rights reserved.</p>
            </div>
            <div class="footer-right">
           <!-- <a href="#"><b>About</b></a>
                <a href="#"><b>Contact</b></a>
                <a href="#"><b>Privacy</b></a>  -->
                <span><b>Created by Team AgniDev</b></span>
            </div>
        </div>
    </footer>
    """
    st.markdown(footer, unsafe_allow_html=True)

def display_crop_advisor():
    """
    Renders the Crop Advisor tab. Accepts a crop name and displays AI-generated advice.
    """
    advisor = CropAdvisor(language=language)
    st.subheader(LANGUAGE_STRINGS[language]['crop_advisor'])
    crop_name = st.text_input(
        LANGUAGE_STRINGS[language]['enter_crop_name'],
        help="E.g., Rice, Wheat, Maize etc." if language=="en" else "उदा., तांदूळ, गहू, मका इ."
    )
    if st.button(LANGUAGE_STRINGS[language]['get_crop_advice']):
        with st.spinner("Fetching advice..." if language=="en" else "सल्ला मिळवत आहे..."):
            advice, error = advisor.get_crop_advice(crop_name)
            if error:
                st.error(error)
            else:
                st.markdown(
                    f"<div class='chat-response marathi-text'><strong>{'सल्ला'}:</strong> {advice}</div>",
                    unsafe_allow_html=True
                )

def display_image_analysis():
    """
    Renders the Image Analysis tab. Accepts an image and displays AI-generated crop health analysis.
    """
    st.subheader(LANGUAGE_STRINGS[language]['image_analysis'])
    uploaded_file = st.file_uploader(
        LANGUAGE_STRINGS[language]['upload_image'],
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=False
    )
    if uploaded_file:
        try:
            analyzer = ImageAnalyzer(language=language)
        except Exception as e:
            st.error(f"Initialization Error: {str(e)}")
            return
        with st.spinner(LANGUAGE_STRINGS[language]['analyzing_image']):
            image_data = uploaded_file.getvalue()
            analysis, error = analyzer.analyze_crop_image(image_data)
            st.image(image_data, use_column_width=True)
            if error:
                st.error(f"Analysis Error: {error}")
            elif analysis:
                st.markdown(
                    f"<div class='chat-response'><strong>{'Analysis' if language=='en' else 'विश्लेषण'}:</strong> {analysis}</div>",
                    unsafe_allow_html=True
                )

def main():
    if 'show_lang' not in st.session_state:
        st.session_state.show_lang = False
    if 'language' not in st.session_state:
        st.session_state.language = "mr"  # Default to Marathi

    query_params = st.query_params
    lang_param = query_params.get("lang", "mr")
    
    if lang_param in ["mr", "en"]:
        st.session_state.language = lang_param

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    inject_header()
    st.markdown("<main>", unsafe_allow_html=True)

    tabs = st.tabs([
        LANGUAGE_STRINGS[language]['crop_advisor'],
        LANGUAGE_STRINGS[language]['image_analysis'],
        LANGUAGE_STRINGS[language]['financial_planning']
    ])
    
    with tabs[0]:
        display_crop_advisor()
    
    with tabs[1]:
        display_image_analysis()
    
    with tabs[2]:
        display_financial_planning(language)
    
    
    st.markdown("</main>", unsafe_allow_html=True)
    inject_footer()

if __name__ == "__main__":
    main()
