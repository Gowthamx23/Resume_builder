import streamlit as st
import json
import os
from src.resume_builder import analyze_posting, generate_resume
from src.utils import load_profiles, save_profile, delete_profile, get_ui_styles

PROFILES_FILE = "profiles.json"
st.set_page_config(page_title="Job Posting Analyser & Resume Builder", layout="wide")

# Apply dark theme CSS
st.markdown(get_ui_styles(), unsafe_allow_html=True)

# Initialize profiles
if not os.path.exists(PROFILES_FILE):
    with open(PROFILES_FILE, "w") as f:
        json.dump({}, f)

def main():
    st.markdown('<div class="title">Internship/Job Posting Analyser & Resume Builder</div>', unsafe_allow_html=True)

    # Sidebar for navigation
    option = st.sidebar.selectbox("Choose an Option", ["Create New Profile", "Use Existing Profile", "Manage Profiles"])

    profiles = load_profiles(PROFILES_FILE)

    if option == "Create New Profile":
        st.subheader("Create New Profile")
        with st.form("new_profile_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            education = st.text_area("Education (e.g., B.S. Computer Science, XYZ University, 2023)")
            skills = st.text_area("Skills (comma-separated, e.g., Python, Java, SQL)")
            experience = st.text_area("Experience (e.g., Software Intern, ABC Corp, 2024)")
            submitted = st.form_submit_button("Save Profile")
            if submitted:
                if name and email:
                    profile = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "education": education,
                        "skills": skills.split(",") if skills else [],
                        "experience": experience
                    }
                    save_profile(PROFILES_FILE, name, profile)
                    st.success(f"Profile for {name} saved!")
                else:
                    st.error("Name and email are required.")

    elif option == "Use Existing Profile":
        st.subheader("Use Existing Profile")
        if not profiles:
            st.warning("No profiles found. Create a new profile first.")
        else:
            selected_name = st.selectbox("Select Profile", list(profiles.keys()))
            if selected_name:
                profile = profiles[selected_name]
                st.markdown(f"**Selected Profile**: {selected_name}")
                posting = st.text_area("Paste Job/Internship Posting", height=200)
                if st.button("Analyze Posting & Build Resume"):
                    if posting:
                        with st.spinner("Analyzing posting..."):
                            keywords = analyze_posting(posting)
                            resume_content = generate_resume(profile, keywords)
                        st.session_state["resume_content"] = resume_content
                        st.session_state["profile_name"] = selected_name

                # Resume editing and download
                if "resume_content" in st.session_state:
                    st.subheader("Edit Resume")
                    edited_resume = st.text_area("Resume Content (LaTeX)", st.session_state["resume_content"], height=400)
                    if st.button("Download Resume as PDF"):
                        with st.spinner("Generating PDF..."):
                            try:
                                pdf_path = f"resume_{st.session_state['profile_name']}.pdf"
                                with open("temp_resume.tex", "w") as f:
                                    f.write(edited_resume)
                                os.system(f"latexmk -pdf temp_resume.tex -outdir=output")
                                output_pdf = "output/temp_resume.pdf"
                                if os.path.exists(output_pdf):
                                    with open(output_pdf, "rb") as f:
                                        st.download_button(
                                            "Download PDF Resume",
                                            f,
                                            file_name=pdf_path,
                                            mime="application/pdf"
                                        )
                                    st.success("PDF generated successfully!")
                                else:
                                    st.error("Failed to generate PDF.")
                            except Exception as e:
                                st.error(f"PDF generation failed: {str(e)}")

    elif option == "Manage Profiles":
        st.subheader("Manage Profiles")
        if not profiles:
            st.warning("No profiles found.")
        else:
            for name, profile in profiles.items():
                with st.expander(f"Profile: {name}"):
                    st.write(f"Email: {profile['email']}")
                    st.write(f"Phone: {profile['phone']}")
                    st.write(f"Education: {profile['education']}")
                    st.write(f"Skills: {', '.join(profile['skills'])}")
                    st.write(f"Experience: {profile['experience']}")
                    if st.button(f"Delete {name}", key=f"delete_{name}"):
                        delete_profile(PROFILES_FILE, name)
                        st.success(f"Profile {name} deleted!")
                        st.rerun()

if __name__ == "__main__":
    main()