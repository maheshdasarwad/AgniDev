import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class FinancialPlanner:
    def __init__(self, language="en"):
        self.language = language
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set. Please set it in your .env file.")
        genai.configure(api_key=api_key)

        # Use the same high-quality multimodal model for text-based financial planning
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-002')

        if self.language == "mr":
            self.financial_prompt = (
                "तुम्ही शेतकऱ्यांसाठी आर्थिक नियोजन आणि बजेटिंगमध्ये तज्ञ आहात. खालील इनपुट्सच्या आधारे: पिकाचे नाव, जमीन क्षेत्रफळ (एकर मध्ये), आणि बजेट (INR मध्ये), "
                "एक विस्तृत आर्थिक नियोजन रणनीती द्या. तुमच्या सल्ल्यात खालील बाबींचा समावेश असावा:\n"
                "1. जमीन तयार करणे, बियाणे, खत, सिंचन, मजुरी आणि कापणी नंतरच्या प्रक्रियेचा अंदाजे खर्च.\n"
                "2. संबंधित पिकासाठी आणि जमीन क्षेत्रफळासाठी उपलब्ध शासकीय योजना, सबसिडी किंवा कर्जाबद्दल शिफारस.\n"
                "3. खर्च वाचवण्याच्या आणि नफा वाढवण्याच्या रणनीती, बाजार विश्लेषण आणि जोखमीचे व्यवस्थापन.\n"
                "4. बजेटच्या मर्यादेनुसार व्यवसाय वाढवण्याचे उपाय.\n"
                "जर एखादा इनपुट अपूर्ण किंवा अस्पष्ट असेल तर स्पष्टीकरण मागा.\n\n"
                "पिकाचे नाव: {crop}\nजमीन क्षेत्रफळ (एकर): {land}\nबजेट (INR): {budget}\n"
            )
        else:
            self.financial_prompt = (
                "You are an expert agricultural financial advisor specialized in planning and budgeting for farmers. "
                "Based on the following inputs: Crop type, Land area (in acres), and Budget (in INR), provide a detailed financial planning strategy. "
                "Your advice should include:\n"
                "1. An estimated cost breakdown for land preparation, seeds, fertilizers, irrigation, labor, and post-harvest processing.\n"
                "2. Recommendations on government schemes, subsidies, or loans available for the specified crop and land size.\n"
                "3. Strategies for cost-saving and maximizing profit, including market analysis and risk mitigation.\n"
                "4. Suggestions for scaling up operations if the budget allows.\n"
                "If any input is missing or unclear, ask for clarification.\n\n"
                "Crop Type: {crop}\nLand Area (acres): {land}\nBudget (INR): {budget}\n"
            )

    def get_financial_plan(self, crop: str, land: float, budget: float) -> (str, str):
        """
        Calls the generative AI model with the provided financial inputs.
        Returns a tuple: (plan_text, error_message).
        """
        if not crop.strip():
            return None, ("Please enter a valid crop name." if self.language=="en" else "कृपया वैध पिकाचे नाव भरा.")
        if land <= 0:
            return None, ("Please enter a valid land area." if self.language=="en" else "कृपया वैध जमीन क्षेत्रफळ भरा.")
        if budget <= 0:
            return None, ("Please enter a valid budget." if self.language=="en" else "कृपया वैध बजेट भरा.")
        
        prompt = self.financial_prompt.format(crop=crop, land=land, budget=budget)
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                return response.text, None
            return None, "No financial plan generated."
        except Exception as e:
            return None, f"Error: {str(e)}"

def display_financial_planning(language="en"):
    """
    Renders the Financial Planning tab. Accepts crop type, land area, and budget, then displays AI-generated plan.
    """
    if language == "mr":
        st.markdown("<h2 style='color: #2E7D32;'>आर्थिक नियोजन सल्ला</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: #2E7D32;'>Financial Planning Advice</h2>", unsafe_allow_html=True)
    
    crop = st.text_input("Enter Crop Type:" if language=="en" else "पिकाचे नाव भरा:")
    land = st.number_input(
        "Enter Land Area (acres):" if language=="en" else "जमीन क्षेत्रफळ (एकर):",
        min_value=0.0, step=0.1, format="%.2f"
    )
    budget = st.number_input(
        "Enter Budget (INR):" if language=="en" else "बजेट (INR):",
        min_value=0.0, step=1000.0, format="%.2f"
    )
    
    if st.button("Get Financial Plan" if language=="en" else "आर्थिक योजना मिळवा"):
        try:
            planner = FinancialPlanner(language)
            with st.spinner("Generating financial plan..." if language=="en" else "आर्थिक योजना तयार केली जात आहे..."):
                plan, error = planner.get_financial_plan(crop, land, budget)
                if error:
                    st.error(error)
                else:
                    st.markdown(
                        f"<div class='chat-response'><strong>{'Plan' if language=='en' else 'योजना'}:</strong> {plan}</div>",
                        unsafe_allow_html=True
                    )
        except Exception as e:
            st.error(f"Initialization Error: {str(e)}")
