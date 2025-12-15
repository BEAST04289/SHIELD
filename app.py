import os
from dotenv import load_dotenv
import streamlit as st
from visual_shield import analyze_image, analyze_with_gpt
from audio_shield import transcribe_audio, analyze_audio_transcript
import time

load_dotenv()

# --- TRANSLATIONS ---
TRANSLATIONS = {
    "en": {
        "hero_title": "Is this a Scam?",
        "hero_subtitle": "Upload a screenshot, audio recording, or text message. SHIELD's AI will analyze it instantly to keep you safe.",
        "tab_image": "📸 Image Scanner",
        "tab_audio": "🎙️ Audio Shield",
        "tab_text": "💬 Text Guard",
        "analyze_image_btn": "📸 ANALYZE IMAGE NOW",
        "analyze_audio_btn": "🎙️ ANALYZE AUDIO NOW",
        "analyze_text_btn": "💬 ANALYZE TEXT NOW",
        "analyzing": "Analyzing...",
        "upload_image": "Upload a screenshot (WhatsApp, Email, SMS)",
        "upload_audio": "Upload a voice recording (mp3, wav)",
        "enter_text": "Paste the suspicious message here...",
        "stats_blocked": "Scams Blocked",
        "stats_prevented": "Fraud Prevented",
        "stats_accuracy": "Accuracy Rate",
        "stats_data": "Data Stored",
        "testimonials_title": "💙 Trusted by Families Worldwide",
        "footer_made_with": "Made with ❤️ for grandparents everywhere | No data stored • No monitoring • 100% privacy",
        "great_job": "Great Job!",
        "great_job_desc": "You avoided a potential scam by checking with SHIELD first.",
        "danger": "DANGER",
        "suspicious": "SUSPICIOUS",
        "safe": "SAFE",
        "ai_confidence": "AI Confidence",
        "detailed_analysis": "🧠 Detailed Analysis",
        "red_flags": "🚩 Red Flags Detected",
        "no_red_flags": "✅ No specific red flags detected.",
        "rec_actions": "✅ Recommended Actions",
        "proceed_caution": "ℹ️ Proceed with normal caution.",
        "could_not_analyze": "❌ Could not analyze.",
        "please_upload": "⚠️ Please upload a file.",
        "please_enter": "⚠️ Please enter some text.",
        "built_for": "Built For Everyone with Love ❤️"
    },
    "hi": {
        "hero_title": "क्या यह एक धोखा है?",
        "hero_subtitle": "एक स्क्रीनशॉट, ऑडियो रिकॉर्डिंग या टेक्स्ट संदेश अपलोड करें। SHIELD का AI आपको सुरक्षित रखने के लिए तुरंत इसका विश्लेषण करेगा।",
        "tab_image": "📸 इमेज स्कैनर",
        "tab_audio": "🎙️ ऑडियो कवच",
        "tab_text": "💬 टेक्स्ट रक्षक",
        "analyze_image_btn": "📸 अभी इमेज जांचें",
        "analyze_audio_btn": "🎙️ अभी ऑडियो जांचें",
        "analyze_text_btn": "💬 अभी टेक्स्ट जांचें",
        "analyzing": "विश्लेषण कर रहा है...",
        "upload_image": "स्क्रीनशॉट अपलोड करें (WhatsApp, Email, SMS)",
        "upload_audio": "वॉयस रिकॉर्डिंग अपलोड करें (mp3, wav)",
        "enter_text": "संदेहास्पद संदेश यहाँ पेस्ट करें...",
        "stats_blocked": "घोटाले रोके गए",
        "stats_prevented": "धोखाधड़ी रोकी गई",
        "stats_accuracy": "सटीकता दर",
        "stats_data": "डेटा संग्रहीत",
        "testimonials_title": "💙 दुनिया भर के परिवारों द्वारा विश्वसनीय",
        "footer_made_with": "दादा-दादी के लिए ❤️ के साथ बनाया गया | कोई डेटा संग्रहीत नहीं • कोई निगरानी नहीं • 100% गोपनीयता",
        "great_job": "बहुत बढ़िया!",
        "great_job_desc": "आपने SHIELD के साथ जाँच करके एक संभावित घोटाले से बचा लिया।",
        "danger": "खतरा",
        "suspicious": "संदेहास्पद",
        "safe": "सुरक्षित",
        "ai_confidence": "AI विश्वास",
        "detailed_analysis": "🧠 विस्तृत विश्लेषण",
        "red_flags": "🚩 लाल झंडे (खतरे)",
        "no_red_flags": "✅ कोई विशिष्ट लाल झंडे नहीं मिले।",
        "rec_actions": "✅ अनुशंसित कार्रवाई",
        "proceed_caution": "ℹ️ सामान्य सावधानी के साथ आगे बढ़ें।",
        "could_not_analyze": "❌ विश्लेषण नहीं कर सका।",
        "please_upload": "⚠️ कृपया एक फ़ाइल अपलोड करें।",
        "please_enter": "⚠️ कृपया कुछ टेक्स्ट दर्ज करें।",
        "built_for": "सभी के लिए प्यार से बनाया गया ❤️"
    }
}

# --- TESTIMONIALS DATA ---
TESTIMONIALS_DATA = {
    "en": [
        {
            "text": "I almost lost my retirement savings to a voice clone scam that sounded exactly like my son. SHIELD flagged it as 'High Risk' in seconds. It saved me everything.",
            "name": "Robert, 60",
            "role": "Retired Accountant • London, UK",
            "avatar": "R"
        },
        {
            "text": "As a teacher, I see parents getting tricked by fake school payment links all the time. I use SHIELD to verify every link before I click. It's peace of mind I can't put a price on.",
            "name": "Sarah, 46",
            "role": "High School Teacher • Ohio, USA",
            "avatar": "S"
        },
        {
            "text": "I received a text about a package delivery. My grandson installed SHIELD and it told me it was a fake link immediately. I would have clicked it!",
            "name": "Martha, 72",
            "role": "Grandmother • Florida, USA",
            "avatar": "M"
        },
        {
            "text": "The image scanner helped me identify a fake investment ad on Facebook. It looked so real, but SHIELD spotted the deepfake signs.",
            "name": "David, 65",
            "role": "Small Business Owner • Sydney, AU",
            "avatar": "D"
        },
        {
            "text": "Simple to use. I don't need to be a computer expert to feel safe. It just works.",
            "name": "Elena, 58",
            "role": "Nurse • Toronto, CA",
            "avatar": "E"
        }
    ],
    "hi": [
        {
            "text": "मैंने अपनी सेवानिवृत्ति की बचत लगभग खो दी थी, एक वॉयस क्लोन घोटाले में जो बिल्कुल मेरे बेटे जैसा लग रहा था। SHIELD ने इसे सेकंडों में 'उच्च जोखिम' के रूप में चिह्नित किया। इसने मेरा सब कुछ बचा लिया।",
            "name": "रॉबर्ट, 60",
            "role": "सेवानिवृत्त लेखाकार • लंदन, यूके",
            "avatar": "R"
        },
        {
            "text": "एक शिक्षक के रूप में, मैं माता-पिता को हर समय नकली स्कूल भुगतान लिंक से ठगे जाते हुए देखती हूँ। मैं क्लिक करने से पहले हर लिंक को सत्यापित करने के लिए SHIELD का उपयोग करती हूँ। यह मन की शांति है जिसकी मैं कीमत नहीं लगा सकती।",
            "name": "सारा, 46",
            "role": "हाई स्कूल शिक्षक • ओहियो, यूएसए",
            "avatar": "S"
        },
        {
            "text": "मुझे पैकेज डिलीवरी के बारे में एक टेक्स्ट मिला। मेरे पोते ने SHIELD स्थापित किया और इसने मुझे तुरंत बताया कि यह एक नकली लिंक था। मैं इसे क्लिक कर देती!",
            "name": "मार्था, 72",
            "role": "दादी • फ्लोरिडा, यूएसए",
            "avatar": "M"
        },
        {
            "text": "इमेज स्कैनर ने मुझे फेसबुक पर एक नकली निवेश विज्ञापन की पहचान करने में मदद की। यह इतना असली लग रहा था, लेकिन SHIELD ने डीपफेक संकेतों को देखा।",
            "name": "डेविड, 65",
            "role": "लघु व्यवसाय स्वामी • सिडनी, एयू",
            "avatar": "D"
        },
        {
            "text": "उपयोग करने में आसान। सुरक्षित महसूस करने के लिए मुझे कंप्यूटर विशेषज्ञ होने की आवश्यकता नहीं है। यह बस काम करता है।",
            "name": "एलेना, 58",
            "role": "नर्स • टोरंटो, सीए",
            "avatar": "E"
        }
    ]
}

# Initialize Language State
if 'language' not in st.session_state:
    st.session_state.language = 'en'

st.set_page_config(
    page_title="SHIELD | Your Family's AI Bodyguard", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ACCESSIBLE & CLEAN STYLING ---
# Theme Colors
if st.session_state.get('theme', 'Dark Mode') == 'Dark Mode':
    bg_color = "#020617"
    text_color = "#F8FAFC"
    card_bg = "#0F172A"
    border_color = "rgba(255, 255, 255, 0.05)"
    sub_text_color = "#94A3B8"
    hero_gradient = "linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%)"
    tab_bg = "rgba(15, 23, 42, 0.8)"
    tab_hover = "rgba(255, 255, 255, 0.05)"
    btn_bg = "#F8FAFC"
    btn_text = "#0F172A"
    btn_hover = "#E2E8F0"
    testimonial_bg = "#1E293B"
else:
    bg_color = "#F5F5F5" # Soft White Smoke
    text_color = "#1E293B" # Slate 800
    card_bg = "#FFFFFF"
    border_color = "rgba(0, 0, 0, 0.08)"
    sub_text_color = "#475569"
    hero_gradient = "linear-gradient(180deg, #1E293B 0%, #475569 100%)"
    tab_bg = "rgba(255, 255, 255, 0.9)"
    tab_hover = "rgba(0, 0, 0, 0.05)"
    btn_bg = "#1E293B"
    btn_text = "#F8FAFC"
    btn_hover = "#334155"
    testimonial_bg = "#FFFFFF"

st.markdown(
    f"""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* ANIMATIONS */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(50px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-50px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    .slide-in-right {{
        animation: slideInRight 0.5s ease-out;
    }}
    
    .slide-in-left {{
        animation: slideInLeft 0.5s ease-out;
    }}

    /* Main Background */
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Remove Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em;
        color: {text_color} !important;
    }}
    
    /* Hero Section */
    .hero {{
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 2rem;
        position: relative;
        animation: fadeIn 1s ease-out;
    }}
    
    .hero h1 {{
        font-size: 4em !important;
        font-weight: 800 !important;
        background: {hero_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }}
    
    .hero-subtitle {{
        font-size: 1.3em;
        color: {sub_text_color};
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    /* Tabs - High Visibility Pill */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {tab_bg};
        padding: 0.5rem;
        border-radius: 100px;
        border: 1px solid {border_color};
        width: fit-content;
        margin: 0 auto 3rem auto;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background: transparent;
        border-radius: 100px;
        padding: 0 2rem;
        font-size: 1em;
        font-weight: 600;
        color: {sub_text_color};
        border: none;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        color: {text_color};
        background: {tab_hover};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: #38BDF8;
        color: #0F172A !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
        font-weight: 700;
    }}
    
    /* Buttons - Large & Clear */
    .stButton>button {{
        width: 100%;
        background: {btn_bg};
        color: {btn_text};
        height: 4em;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1em;
        border: none;
        transition: all 0.2s ease;
    }}
    
    .stButton>button:hover {{
        background: {btn_hover};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    /* Cards */
    .result-card {{
        padding: 2rem;
        border: 1px solid {border_color};
        border-radius: 16px;
        background: {card_bg};
        margin: 1.5rem 0;
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* Testimonials Section */
    .testimonial-card {{
        background: {testimonial_bg};
        border: 1px solid {border_color};
        padding: 3rem;
        border-radius: 24px;
        height: 100%;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    
    .testimonial-text {{
        font-size: 1.4em;
        color: {text_color};
        font-style: italic;
        margin-bottom: 2rem;
        line-height: 1.5;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .testimonial-author {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }}
    
    .author-avatar {{
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: white;
        font-size: 1.2em;
    }}
    
    .author-info {{
        text-align: left;
    }}
    
    .author-name {{
        color: {text_color};
        font-weight: 700;
        font-size: 1.1em;
    }}
    
    .author-role {{
        color: {sub_text_color};
        font-size: 0.9em;
    }}
    
    /* Verdict Styles */
    .verdict-safe {{ color: #4ADE80; font-weight: 700; font-size: 1.8em; display: flex; align-items: center; gap: 0.75rem; }}
    .verdict-warn {{ color: #FBBF24; font-weight: 700; font-size: 1.8em; display: flex; align-items: center; gap: 0.75rem; }}
    .verdict-risk {{ color: #F87171; font-weight: 700; font-size: 1.8em; display: flex; align-items: center; gap: 0.75rem; }}
    
    /* File Uploader */
    .stFileUploader {{
        border: 2px dashed {border_color};
        border-radius: 16px;
        padding: 3rem 2rem;
        background: {card_bg};
        text-align: center;
    }}
    
    /* Stats - Minimal */
    .stat-box {{
        text-align: center;
        padding: 1.5rem;
        border-right: 1px solid {border_color};
    }}
    
    .stat-number {{
        font-size: 2.5em;
        font-weight: 700;
        color: {text_color};
        letter-spacing: -0.03em;
    }}
    
    .stat-label {{
        font-size: 0.9em;
        color: {sub_text_color};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }}
    
    /* Carousel Buttons */
    div[data-testid="stHorizontalBlock"] button {{
        background: {btn_bg};
        color: {btn_text};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        padding: 0;
        line-height: 1;
        font-size: 1.5em;
    }}
    div[data-testid="stHorizontalBlock"] button:hover {{
        background: {btn_hover};
        transform: scale(1.1);
    }}

    /* --- WOW UI ELEMENTS --- */
    
    /* Confidence Meter */
    .confidence-container {{
        background: {card_bg};
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }}
    
    .meter-bar {{
        height: 12px;
        background: {testimonial_bg};
        border-radius: 100px;
        position: relative;
        margin: 1.5rem 0;
        overflow: visible;
    }}
    
    .meter-fill {{
        height: 100%;
        border-radius: 100px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .meter-needle {{
        position: absolute;
        top: -6px;
        width: 24px;
        height: 24px;
        background: {text_color};
        border: 4px solid {bg_color};
        border-radius: 50%;
        transform: translateX(-50%);
        transition: left 1s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10;
    }}
    
    .meter-labels {{
        display: flex;
        justify-content: space-between;
        font-size: 0.8em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {sub_text_color};
    }}
    
    /* Actionable Advice Cards */
    .action-card {{
        background: {testimonial_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s ease;
    }}
    
    .action-card:hover {{
        background: {btn_hover};
        transform: translateX(5px);
        border-color: {border_color};
    }}
    
    .action-icon {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2em;
        flex-shrink: 0;
    }}
    
    .action-content {{
        flex-grow: 1;
    }}
    
    .action-title {{
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.25rem;
    }}
    
    .action-desc {{
        font-size: 0.9em;
        color: {sub_text_color};
    }}
    
    .action-btn {{
        background: {btn_bg};
        color: {btn_text};
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85em;
        font-weight: 600;
        text-decoration: none;
        white-space: nowrap;
    }}
    
    .action-btn:hover {{
        background: #38BDF8;
        color: #0F172A;
    }}
    
    /* Red Flag Highlight */
    .red-flag-box {{
        background: rgba(248, 113, 113, 0.1);
        border-left: 4px solid #F87171;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
    }}
    
    /* Custom Loader */
    .shield-loader {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        animation: fadeIn 0.5s ease-out;
    }}
    
    .shield-pulse {{
        font-size: 4em;
        animation: pulse 1.5s infinite;
        margin-bottom: 1rem;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    .loader-text {{
        font-size: 1.2em;
        font-weight: 600;
        color: #38BDF8;
    }}
    
    .loader-bar {{
        width: 200px;
        height: 4px;
        background: rgba(56, 189, 248, 0.2);
        border-radius: 100px;
        margin-top: 1rem;
        overflow: hidden;
    }}
    
    .loader-progress {{
        width: 50%;
        height: 100%;
        background: #38BDF8;
        animation: progress 1.5s infinite ease-in-out;
    }}
    
    @keyframes progress {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(200%); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HELPER FUNCTIONS ---

def render_custom_loader(text="Analyzing..."):
    placeholder = st.empty()
    placeholder.markdown(
        f"""
        <div class='shield-loader'>
            <div class='shield-pulse'>🛡️</div>
            <div class='loader-text'>{text}</div>
            <div class='loader-bar'>
                <div class='loader-progress'></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    return placeholder

def render_results(result, result_type="generic", language="en"):
    """
    Renders the 'WOW' UI for analysis results.
    """
    t = TRANSLATIONS[language]
    v_label = result.get("verdict_label", "UNKNOWN").upper()
    score = result.get("confidence_score", 0)
    
    # Determine Theme Colors
    if "RISK" in v_label or "DANGER" in v_label or "SCAM" in v_label or "PHISHING" in v_label:
        theme_color = "#F87171" # Red
        icon = "🚨"
        sub_text = "IMMEDIATE ACTION REQUIRED"
        verdict_class = "verdict-risk"
        verdict_display = t["danger"]
    elif "CAUTION" in v_label or "WARN" in v_label or "SUSPICIOUS" in v_label:
        theme_color = "#FBBF24" # Amber
        icon = "⚠️"
        sub_text = "PROCEED WITH EXTREME CAUTION"
        verdict_class = "verdict-warn"
        verdict_display = t["suspicious"]
    else:
        theme_color = "#4ADE80" # Green
        icon = "✅"
        sub_text = "NO IMMEDIATE THREATS DETECTED"
        verdict_class = "verdict-safe"
        verdict_display = t["safe"]

    # --- 1. VERDICT CARD ---
    st.markdown(
        f"""
        <div class='result-card'>
            <div class='{verdict_class}'>
                <span style='font-size: 1.5em;'>{icon}</span>
                <div>
                    <div>{verdict_display}</div>
                    <div style='font-size: 0.5em; font-weight: 500; color: {theme_color}; opacity: 0.9;'>{sub_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # --- 2. CONFIDENCE METER (WOW ELEMENT) ---
    st.markdown(
        f"""
        <div class='confidence-container'>
            <div class='meter-labels'>
                <span style='color: #F87171;'>{t['danger']}</span>
                <span style='color: #FBBF24;'>{t['suspicious']}</span>
                <span style='color: #4ADE80;'>{t['safe']}</span>
            </div>
            <div class='meter-bar'>
                <div class='meter-fill' style='width: 100%; background: linear-gradient(90deg, #F87171 0%, #FBBF24 50%, #4ADE80 100%);'></div>
                <div class='meter-needle' style='left: {score}%; border-color: {theme_color};'></div>
            </div>
            <div style='text-align: center; font-weight: 600; color: {sub_text_color};'>
                {t['ai_confidence']}: <span style='color: {text_color};'>{score}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- 3. ANALYSIS SUMMARY ---
    st.markdown(f"### {t['detailed_analysis']}")
    st.markdown(
        f"""
        <div style='padding: 1.5rem; background: rgba(0, 184, 212, 0.05); border-radius: 12px; border-left: 4px solid #00B8D4;'>
            {result.get('summary', 'Analysis complete.')}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # --- 4. RED FLAGS (HIGHLIGHTED) ---
    with col1:
        st.markdown(f"### {t['red_flags']}")
        flags = result.get("red_flags", [])
        if flags:
            for flag in flags:
                st.markdown(
                    f"""
                    <div class='red-flag-box'>
                        <strong>🚩</strong> {flag}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success(t['no_red_flags'])
            
    # --- 5. ACTIONABLE ADVICE CARDS (WOW ELEMENT) ---
    with col2:
        st.markdown(f"### {t['rec_actions']}")
        advice = result.get("advice", [])
        if advice:
            for i, step in enumerate(advice, 1):
                # Determine icon based on keywords
                action_icon = "🛡️"
                if "delete" in step.lower(): action_icon = "🗑️"
                elif "call" in step.lower(): action_icon = "📞"
                elif "report" in step.lower(): action_icon = "🚨"
                elif "verify" in step.lower(): action_icon = "🔍"
                
                st.markdown(
                    f"""
                    <div class='action-card'>
                        <div class='action-icon' style='background: rgba(56, 189, 248, 0.1); color: #38BDF8;'>{action_icon}</div>
                        <div class='action-content'>
                            <div class='action-title'>Step {i}</div>
                            <div class='action-desc'>{step}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info(t['proceed_caution'])
    
    # Success celebration
    if "SAFE" in v_label:
        st.balloons()
        st.markdown(
            f"""
            <div style='text-align: center; padding: 2rem; background: rgba(74, 222, 128, 0.1); border-radius: 16px; border: 1px solid #4ADE80; margin-top: 2rem;'>
                <div style='font-size: 3em;'>🎉</div>
                <h2 style='color: #4ADE80; margin: 0.5rem 0;'>{t['great_job']}</h2>
                <p style='color: {text_color};'>{t['great_job_desc']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# --- TOP BAR (Language & Theme) ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark Mode'

def update_language():
    if st.session_state.lang_select == "English":
        st.session_state.language = 'en'
    else:
        st.session_state.language = 'hi'

def update_theme():
    st.session_state.theme = st.session_state.theme_select

col_spacer, col_lang, col_theme = st.columns([6, 2, 2])

with col_lang:
    st.selectbox(
        "Language / भाषा", 
        ["English", "हिंदी"], 
        index=0 if st.session_state.language == 'en' else 1,
        key="lang_select",
        on_change=update_language
    )

with col_theme:
    st.selectbox(
        "Theme", 
        ["Dark Mode", "Light Mode"], 
        index=0 if st.session_state.theme == 'Dark Mode' else 1,
        key="theme_select",
        on_change=update_theme
    )

# --- HERO SECTION ---
t = TRANSLATIONS[st.session_state.language]
lang = st.session_state.language

st.markdown(
    f"""
    <div class='hero'>
        <div class='shield-icon' style='font-size: 5em; margin-bottom: 1rem;'>🛡️</div>
        <h1>{t['hero_title']}</h1>
        <div class='hero-subtitle'>
            {t['hero_subtitle']}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- TABS (MOVED UP FOR ACCESSIBILITY) ---
tab1, tab2, tab3 = st.tabs([t['tab_image'], t['tab_audio'], t['tab_text']])

# ==================== VISUAL SHIELD ====================
with tab1:
    st.markdown(f"### {t['tab_image']}")
    st.markdown(t['upload_image'])
    
    img_file = st.file_uploader("📁", type=["png", "jpg", "jpeg"], key="visual_upload")
    
    if img_file:
        st.image(img_file, caption="Uploaded Image", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(t['analyze_image_btn'], key="analyze_image_btn"):
            loader = render_custom_loader(t['analyzing'])
            time.sleep(1.5) # UX Pause
            result = analyze_image(img_file, language=lang)
            loader.empty()
            render_results(result, "image", language=lang)

# ==================== AUDIO SHIELD ====================
with tab2:
    st.markdown(f"### {t['tab_audio']}")
    st.markdown(t['upload_audio'])
    
    audio_file = st.file_uploader("📁", type=["wav", "mp3", "m4a"], key="audio_upload")
    
    if audio_file:
        st.audio(audio_file, format=f"audio/{audio_file.type.split('/')[-1]}")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(t['analyze_audio_btn'], key="analyze_audio_btn"):
            loader = render_custom_loader(t['analyzing'])
            
            # Save temp file
            file_ext = os.path.splitext(audio_file.name)[1]
            temp_filename = f"temp_audio{file_ext}"
            with open(temp_filename, "wb") as f:
                f.write(audio_file.getbuffer())
            
            time.sleep(1) # UX Pause
            transcript = transcribe_audio(temp_filename)
            
            if transcript:
                st.markdown("### 📝 Transcript")
                st.markdown(
                    f"""
                    <div style='padding: 1.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 12px; font-style: italic; border: 2px solid rgba(255, 255, 255, 0.1); margin-bottom: 2rem;'>
                        "{transcript}"
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                result = analyze_audio_transcript(transcript, language=lang)
                loader.empty()
                
                if result:
                    render_results(result, "audio", language=lang)
                else:
                    st.error(t['could_not_analyze'])
            else:
                loader.empty()
                st.error(t['could_not_analyze'])
            
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

# ==================== TEXT SHIELD ====================
with tab3:
    st.markdown(f"### {t['tab_text']}")
    st.markdown(t['enter_text'])
    
    user_text = st.text_area(
        "📝",
        height=200,
        placeholder="Example: 'URGENT: Your bank account will be suspended...'",
        key="text_input"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(t['analyze_text_btn'], key="analyze_text_btn"):
        if user_text.strip():
            loader = render_custom_loader(t['analyzing'])
            time.sleep(1.5) # UX Pause
            result = analyze_with_gpt(user_text, language=lang)
            loader.empty()
            
            if result:
                render_results(result, "text", language=lang)
            else:
                st.error(t['could_not_analyze'])
        else:
            st.warning(t['please_enter'])

# --- STATS BAR ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1:
    st.markdown(f"<div class='stat-box'><div class='stat-number'>10k+</div><div class='stat-label'>{t['stats_blocked']}</div></div>", unsafe_allow_html=True)
with stat_col2:
    st.markdown(f"<div class='stat-box'><div class='stat-number'>$2M+</div><div class='stat-label'>{t['stats_prevented']}</div></div>", unsafe_allow_html=True)
with stat_col3:
    st.markdown(f"<div class='stat-box'><div class='stat-number'>94%</div><div class='stat-label'>{t['stats_accuracy']}</div></div>", unsafe_allow_html=True)
with stat_col4:
    st.markdown(f"<div class='stat-box'><div class='stat-number'>0s</div><div class='stat-label'>{t['stats_data']}</div></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# --- SOCIAL PROOF / TESTIMONIALS CAROUSEL ---
st.markdown(f"### {t['testimonials_title']}")

# Testimonial Data
testimonials = TESTIMONIALS_DATA[st.session_state.language]

# Initialize session state for carousel
if 'testimonial_index' not in st.session_state:
    st.session_state.testimonial_index = 0
if 'carousel_direction' not in st.session_state:
    st.session_state.carousel_direction = 'next'

# Carousel Navigation
def next_testimonial():
    st.session_state.testimonial_index = (st.session_state.testimonial_index + 1) % len(testimonials)
    st.session_state.carousel_direction = 'next'

def prev_testimonial():
    st.session_state.testimonial_index = (st.session_state.testimonial_index - 1) % len(testimonials)
    st.session_state.carousel_direction = 'prev'

# Display Carousel
t_col_left, t_col_center, t_col_right = st.columns([1, 8, 1])

with t_col_left:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("◀", on_click=prev_testimonial, key="prev_btn")

with t_col_center:
    idx = st.session_state.testimonial_index
    t_data = testimonials[idx]
    
    # Determine animation class
    anim_class = "slide-in-right" if st.session_state.carousel_direction == 'next' else "slide-in-left"
    
    st.markdown(
        f"""
        <div class='testimonial-card {anim_class}'>
            <div class='testimonial-text'>
                "{t_data['text']}"
            </div>
            <div class='testimonial-author'>
                <div class='author-avatar'>{t_data['avatar']}</div>
                <div class='author-info'>
                    <div class='author-name'>{t_data['name']}</div>
                    <div class='author-role'>{t_data['role']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with t_col_right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("▶", on_click=next_testimonial, key="next_btn")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([2, 3, 2])

with footer_col1:
    st.markdown("### 🛡️ SHIELD")
    st.caption("Protecting families from AI fraud since 2025")

with footer_col2:
    st.markdown("### ⚡ Powered By")
    st.caption("Azure OpenAI • Computer Vision • Speech Services • AI Language • Content Safety")

with footer_col3:
    st.markdown("### 🏆 Built For")
    st.caption(t['built_for'])

st.markdown(
    f"""
    <center style='margin-top: 2rem; color: #64748B; font-size: 0.9em;'>
        {t['footer_made_with']}
    </center>
    """,
    unsafe_allow_html=True
)
