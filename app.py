import os
from dotenv import load_dotenv
import streamlit as st
from visual_shield import analyze_image

load_dotenv()

st.set_page_config(page_title="SHIELD | Family Scam Defense", page_icon="🛡️", layout="centered")

# --- Styles ---
st.markdown(
    """
    <style>
    .stButton>button {width: 100%; background:#ff4b4b; color:white; height:3em; border-radius:10px; font-weight:700;}
    .card {padding:1rem; border:1px solid #e5e7eb; border-radius:10px; background:#f8fafc;}
    .verdict-safe {color:#16a34a; font-weight:700;}
    .verdict-warn {color:#f59e0b; font-weight:700;}
    .verdict-risk {color:#dc2626; font-weight:700;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ SHIELD")
st.subheader("On-demand scam checks for family (Visual · Audio · Text)")
st.info("Privacy by design: on-demand only, no retention, PII redaction planned.")

tab1, tab2, tab3 = st.tabs(["📷 Visual Shield", "🎤 Audio Shield", "💬 Text Shield"])

with tab1:
    st.header("Scan Screen or Letter")
    st.write("Upload a screenshot/photo of a popup, WhatsApp image, or letter.")
    img_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    
    if img_file:
        if st.button("Analyze Image"):
            with st.spinner("Analyzing with Azure AI..."):
                result = analyze_image(img_file)
            
            # Determine color based on verdict
            v_label = result.get("verdict_label", "UNKNOWN").upper()
            
            # Display Verdict
            if "RISK" in v_label:
                st.error(f"### 🚨 VERDICT: {v_label}")
            elif "CAUTION" in v_label:
                st.warning(f"### ⚠️ VERDICT: {v_label}")
            else:
                st.success(f"### ✅ VERDICT: {v_label}")

            # Confidence Meter
            score = result.get("confidence_score", 0)
            st.progress(score / 100, text=f"AI Confidence: {score}%")
            
            # Summary
            st.markdown(f"**Analysis:** {result.get('summary')}")
            
            st.markdown("---")
            
            # Columns for Flags and Advice
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🚩 Red Flags")
                flags = result.get("red_flags", [])
                if flags:
                    for flag in flags:
                        st.error(f"• {flag}")
                else:
                    st.write("No specific red flags detected.")
                    
            with col2:
                st.markdown("#### ✅ What to do")
                advice = result.get("advice", [])
                if advice:
                    for step in advice:
                        st.success(f"• {step}")
                else:
                    st.write("Proceed with caution.")

with tab2:
    st.header("Scan Phone Call (coming soon)")
    st.write("Upload a short recording; we’ll transcribe and check for scam scripts.")
    st.warning("Audio Shield wiring pending. Tomorrow’s task: Speech-to-Text + intent prompt.")

with tab3:
    st.header("Scan Message Text (coming soon)")
    st.write("Paste SMS/Email/WhatsApp content; we’ll check for phishing/urgency/OTP asks.")
    st.warning("Text Shield wiring pending. After audio, we add Content Safety + intent prompt.")

st.markdown("---")
st.caption("Built on Azure OpenAI, Vision, Speech, Content Safety. On-demand. No always-on listening.")