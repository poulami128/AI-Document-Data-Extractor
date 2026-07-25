import streamlit as st
import json
import pandas as pd
from parser import extract_text_from_pdf
from extractor import extract_document_data
from qa import ask_question

st.set_page_config(
    page_title="AI Document Data Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Data Extractor")

st.write("Upload any PDF document and extract structured information using Gemini AI.")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("✅ PDF Uploaded Successfully")

    if st.button("Extract Information"):

        with st.spinner("📖 Reading PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        st.session_state["document_text"] = extracted_text

        with st.spinner("🤖 Gemini is analysing the document..."):
            result = extract_document_data(extracted_text)

        st.session_state["result"] = result


if "result" in st.session_state:

    result = st.session_state["result"]

    st.success("✅ Extraction Completed")

    st.divider()

    # ---------------- Document Type ----------------

    st.subheader("📄 Document Type")
    st.info(result.get("document_type", "Unknown"))

    # ---------------- Summary ----------------

    st.subheader("📝 Summary")
    st.write(result.get("summary", "No summary available."))

    st.divider()

    with st.expander("📋 View AI Extraction Results", expanded=False):

            # ---------------- Key Information ----------------

        st.subheader("📋 Key Information")

        key_info = result.get("key_information", {})

        if isinstance(key_info, dict):

            for key, value in key_info.items():

                title = key.replace("_", " ").title()

                st.markdown(f"### {title}")

                if isinstance(value, dict):

                    for k, v in value.items():

                        if isinstance(v, list):

                            st.markdown(f"**{k.replace('_',' ').title()}**")

                            for item in v:
                                st.write("•", item)

                        else:

                            st.write(f"**{k.replace('_',' ').title()}:** {v}")

                elif isinstance(value, list):

                    for item in value:

                        if isinstance(item, dict):

                            cols = st.columns(2)

                            items = list(item.items())

                            for i, (k, v) in enumerate(items):
                                cols[i % 2].write(
                                    f"**{k.replace('_',' ').title()}**: {v}"
                                )

                            st.markdown("---")

                        else:

                            st.write("•", item)

                else:

                    st.write(value)

        st.divider()

        # ---------------- Entities ----------------

        st.subheader("🏷️ Entities")

        entities = result.get("entities", [])

        if entities:
            st.write(", ".join(entities))
        else:
            st.info("No entities found.")

        # ---------------- Dates ----------------

        st.subheader("📅 Dates")

        dates = result.get("dates", [])

        if dates:
            for d in dates:
                st.write("•", d)
        else:
            st.info("No dates found.")

        # ---------------- Numbers ----------------

        st.subheader("🔢 Important Numbers")

        numbers = result.get("numbers", [])

        if numbers:
            for n in numbers:
                st.write("•", n)
        else:
            st.info("No numbers found.")

        # ---------------- Keywords ----------------

        st.subheader("🔑 Keywords")

        keywords = result.get("keywords", [])

        if keywords:
            st.write(" | ".join(keywords))
        else:
            st.info("No keywords found.")
    st.divider()

    # ---------------- Downloads ----------------

    json_data = json.dumps(result, indent=4)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="extracted_data.json",
            mime="application/json"
        )

    with col2:

        try:

            csv_dict = {
                "Document Type": result.get("document_type", ""),
                "Summary": result.get("summary", ""),
                "Entities": ", ".join(result.get("entities", [])),
                "Dates": ", ".join(result.get("dates", [])),
                "Numbers": ", ".join(map(str, result.get("numbers", []))),
                "Keywords": ", ".join(result.get("keywords", []))
            }

            if isinstance(result.get("key_information"), dict):
                csv_dict.update(result["key_information"])

            df = pd.DataFrame([csv_dict])

            csv = df.to_csv(index=False)

            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name="extracted_data.csv",
                mime="text/csv"
            )

        except Exception:

            st.warning("CSV could not be generated.")

    st.divider()

    # ---------------- Ask AI ----------------

    st.header("🤖 AI Document Assistant")

    st.caption("💡 Try asking:")
    st.markdown("""
    - What is this document about?
    - Summarize this document.
    - What are the key skills?
    - Which role suits this resume?
    - What projects are mentioned?
    - What certifications are listed?
    """)

    question = st.text_input("Ask anything about this document")

    if st.button("Ask AI"):

        if question.strip():

            with st.spinner("🤖 Thinking..."):

                answer = ask_question(
                    st.session_state["document_text"],
                    question
                )

            st.success(answer)