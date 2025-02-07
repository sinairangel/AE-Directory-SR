import streamlit as st
import pandas as pd
from pathlib import Path
from utils.data_handler import load_problems
from utils.recommendation import get_recommended_problems

def init_page_config():
    """Initialize the Streamlit page configuration"""
    st.set_page_config(
        page_title="Aerospace Projects",
        page_icon="🚀",
        layout="wide"
    )

def load_css() -> None:
    """Load and apply custom CSS styling"""
    try:
        css_path = Path('style.css')
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            st.error("Style file not found. Some visual elements may not display correctly.")
    except Exception as e:
        st.error(f"Error loading styles: {str(e)}")

def main():
    init_page_config()
    load_css()

    st.markdown("""
        <h1 style='text-align: center; color: #64ffda; font-size: 3rem;'>
            Aerospace Projects
        </h1>
    """, unsafe_allow_html=True)

    # Skills Input Section
    st.subheader("Enter Your Skills")

    col1, col2, col3 = st.columns(3)

    with col1:
        programming_skills = st.multiselect(
            "Programming Languages",
            ["Python", "C++", "Java", "MATLAB", "Fortran"]
        )

    with col2:
        aerospace_skills = st.multiselect(
            "Aerospace Knowledge",
            ["Aerodynamics", "Propulsion", "Structures", "Control Systems", "Orbital Mechanics"]
        )

    with col3:
        tool_skills = st.multiselect(
            "Tools & Software",
            ["CAD", "CFD", "FEA", "Git", "Linux"]
        )

    # Combine all skills
    all_skills = ", ".join(programming_skills + aerospace_skills + tool_skills)

    if all_skills:
        # Create user profile for recommendations
        user_profile = {
            'username': 'user',
            'skills': all_skills,
            'experience_level': 3  # Default middle experience level
        }

        # Get project recommendations
        problems = load_problems()
        recommendations = get_recommended_problems(user_profile, problems)

        # Display recommended projects
        st.subheader("Recommended Projects")

        for rec in recommendations:
            project = rec['problem']
            match_score = rec['match_score']

            st.markdown(f"""
            <div class='problem-card'>
                <div class='card-header'>
                    <h3>{project['title']}</h3>
                    <span class='organization-badge'>{project['company']}</span>
                </div>
                <p class='description'>{project['description']}</p>
                <div class='project-meta'>
                    <div class='match-score'>
                        <span>Match Score: {match_score:.1f}%</span>
                    </div>
                    <div class='difficulty'>
                        <span>Difficulty: {'⭐' * project['difficulty']}</span>
                    </div>
                    <div class='skills'>
                        <strong>Required Skills:</strong> {project['skills_required']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
