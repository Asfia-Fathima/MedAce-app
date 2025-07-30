import streamlit as st
import PyPDF2
import pandas as pd
from PIL import Image
import io
import matplotlib.pyplot as plt
import seaborn as sns
import easyocr

# OCR function - fixed to accept image bytes
def extract_text_easyocr(image_bytes):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_bytes, detail=0)
    return "\n".join(result)

# Page settings
st.set_page_config(page_title="MedAce", layout="wide")
st.title("🩺 MedAce - Smart Medical Report Analyzer")
st.write("Welcome! Upload your Medical Report to begin.")

# Two columns
left_col, right_col = st.columns([1, 2])

# ---- LEFT COLUMN: Upload ----
with left_col:
    st.header("Upload Report")
    uploaded_file = st.file_uploader(
        "Choose a Medical Report",
        type=["pdf", "csv", "png", "jpg", "jpeg", "txt"],
        help="Upload your medical report here (PDF, Image, or Text). Max Size: 10MB"
    )
    if uploaded_file:
        st.success("File Uploaded Successfully.")
        st.markdown(f"**Filename:** `{uploaded_file.name}`")

# ---- RIGHT COLUMN: Analysis ----
with right_col:
    st.header("Report Summary")

    if uploaded_file:
        st.markdown("### Extracted Report Details:")
        report_text = st.session_state.get("report_text", "")
        if report_text:
            st.text_area("Full Report Text", report_text, height=300)
        else:
            st.warning("Scroll Below for Extracted text")

        st.markdown("### Trends Over Time:")
        st.info("Once you upload more reports, we'll show your health trends here.")

        # Download Button
        st.markdown("Download Your Summary:")
        buffer = io.StringIO(report_text if report_text else "No content extracted.")
        st.download_button(
            label="Download Summary as .txt",
            data=buffer.getvalue(),
            file_name="medace_summary.txt",
            mime="text/plain"
        )
    else:
        st.info("Analysis and visualizations will appear here once a file is uploaded.")

# ---- File-Specific Display ----
if uploaded_file:
    file_name = uploaded_file.name.lower()

    # PDF files
    if file_name.endswith(".pdf"):
        with st.spinner("Extracting text from PDF..."):
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.session_state["report_text"] = text
            st.success("Extraction complete!")
        with st.expander("Extracted Text from PDF"):
            st.write(text if text else "No readable text found.")

    # CSV files
    elif file_name.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["report_text"] = df.to_csv(index=False)
            st.markdown("Report Table:")
            st.dataframe(df)

            if "age" in df.columns and "chol" in df.columns:
                # Scatter Plot
                st.markdown("Cholesterol vs Age")
                fig1, ax1 = plt.subplots()
                sns.scatterplot(data=df, x="age", y="chol", hue="sex", palette="Set2", ax=ax1)
                ax1.set_title("Cholesterol Levels by Age")
                ax1.set_xlabel("Age")
                ax1.set_ylabel("Cholesterol (mg/dL)")
                st.pyplot(fig1)

                # Histogram
                st.markdown("Cholesterol Distribution")
                fig2, ax2 = plt.subplots()
                sns.histplot(data=df, x="chol", bins=30, kde=True, color='skyblue', ax=ax2)
                ax2.axvline(240, color='red', linestyle='--', label='High Cholesterol (240 mg/dL)')
                ax2.set_title("Cholesterol Distribution in Patients")
                ax2.set_xlabel("Cholesterol (mg/dL)")
                ax2.set_ylabel("Number of Patients")
                ax2.legend()
                st.pyplot(fig2)
            else:
                st.warning("CSV does not contain expected columns like 'age' and 'chol'.")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

        # Cholesterol Bar Chart by Gender
        if "sex" in df.columns and "chol" in df.columns:
            st.markdown("Average Cholesterol by Gender")
            gender_map = {0: 'Female', 1: 'Male'}
            df['gender_label'] = df['sex'].map(gender_map)
            avg_chol = df.groupby("gender_label")["chol"].mean().reset_index()
            fig3, ax3 = plt.subplots()
            sns.barplot(data=avg_chol, x="gender_label", y="chol", palette="coolwarm", ax=ax3)
            ax3.set_title("Average Cholesterol Levels by Gender")
            ax3.set_xlabel("Gender")
            ax3.set_ylabel("Average Cholesterol (mg/dL)")
            st.pyplot(fig3)

    # Text files
    elif file_name.endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")
        st.session_state["report_text"] = content
        st.markdown("Text File Content:")
        st.text_area("Report Content", content, height=300)

    # Image files
    elif file_name.endswith((".png", ".jpg", ".jpeg")):
        st.markdown("📸 Uploaded Image:")
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

        with st.spinner("🔍 Extracting text from image using OCR..."):
            try:
                # Convert image to bytes for easyocr
                image = Image.open(uploaded_file).convert("RGB")
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="JPEG")
                image_bytes = image_bytes.getvalue()

                text = extract_text_easyocr(image_bytes)
                st.session_state["report_text"] = text
                st.success("✅ Text extraction complete!")
                with st.expander("📝 Extracted Text"):
                    st.text_area("OCR Result", text, height=300)
                chatbot_on = True
            except Exception as e:
                st.error(f"Failed to extract text: {e}")
    else:
        st.warning("Unsupported file type uploaded.")

# ---- Sidebar ----
with st.sidebar:
    st.title("MedAce")
    st.markdown("Navigation")
    st.page_link("https://medace-app-intrtjskaqsuzyedtqrcfh.streamlit.app/", label="Home", icon="🏠")
    
    chatbot_on = st.checkbox("💬 Chat with MedAce")
    st.button("My Report History (coming soon)")
    st.divider()
    st.markdown("Need help? [Contact us](mailto:fathimasfia09@gmail.com)")

# ---- Chatbot Feature ----
if 'chatbot_on' in locals() and chatbot_on:
    st.markdown("---")
    st.header("💬 Chat with MedAce")
    try:
        from chatbot_ai import run_chatbot_ui
        run_chatbot_ui()
    except Exception as e:
        st.error(f"Failed to load chatbot: {e}")
