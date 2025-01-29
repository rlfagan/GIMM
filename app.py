import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys

def install_requirements():
    required_packages = ["streamlit", "pandas", "matplotlib"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

def calculate_maturity(score):
    if score >= 18:
        return "Advanced"
    elif score >= 12:
        return "Intermediate"
    else:
        return "Basic"

def main():
    st.set_page_config(layout="wide")
    
    if "assessment_started" not in st.session_state:
        st.session_state.assessment_started = False
    
    if not st.session_state.assessment_started:
        st.title("Container Security Maturity Model Assessment")
        st.write("### Introduction")
        st.write("The **Container Security Maturity Model Assessment** helps organizations determine their **security posture** across key areas such as **image management, automation, vulnerability management, and compliance**.")
        st.write("This assessment evaluates adherence to best practices and calculates a maturity level based on the responses.")
        
        st.write("### Key Areas of Assessment")
        st.markdown("""
        1️⃣ **Image Management**
        - Centralized catalog of pre-approved images.
        - Policies for outdated image retirement.
        - Inclusion of Helm charts, sidecars, and proxies in governance.
        
        2️⃣ **Automation & Standardization**
        - Automated image rotation and security scanning.
        - Tracking image retirements and additions.
        - CI/CD pipeline integration with security tools.
        
        3️⃣ **Registry Hygiene**
        - Removal of outdated and unused images from registries.
        - Proper tagging and lifecycle management.
        - Centralized inventory reporting.
        
        4️⃣ **Security & Vulnerability Management**
        - SBOM signing and attestation enforcement.
        - Scanning language-level dependencies for vulnerabilities.
        - CI/CD security policy enforcement.
        - Integration with tools like Snyk, Grype, and Wiz.
        
        5️⃣ **Developer Workflow & Adoption**
        - Requirement for developers to use pre-approved images.
        - Availability of security-aligned tools.
        - Security best practices embedded in development workflows.
        
        6️⃣ **Supply Chain & Compliance**
        - Compliance with FIPS and regulatory requirements.
        - Software verification using Sigstore Cosign.
        - Secure provenance policies for deployed images.
        
        7️⃣ **Tooling & Integration**
        - Container images pulled from approved registries.
        - Implementation of dynamic inventory scanning.
        - Policy enforcement through tools like Kyverno.
        """)
        
        st.write("### Summary of Impact")
        st.markdown("""
        - A **low score** in any category suggests security gaps that could increase risks.
        - A **high score** means the organization is implementing best practices effectively.
        - The assessment helps organizations **prioritize improvements** in key security areas.
        """)
        
        st.write("### Why This Model Matters")
        st.markdown("""
        - Encourages **step-by-step maturity improvement**.
        - Identifies **gaps in security posture**.
        - Helps organizations achieve **secure, compliant, and automated container security**.
        - Ensures **continuous security enhancements** aligned with modern DevSecOps principles.
        """)
        
        if st.button("Start Assessment"):
            st.session_state.assessment_started = True
            st.rerun()
    else:
        categories = {
            "Image Management": [
                "Do you maintain a centralized catalog of pre-approved images?",
                "Do you enforce policies for outdated image retirement?",
                "Are Helm charts, sidecars, and proxies included in the image governance process?",
            ],
            "Automation & Standardization": [
                "Do you have automated image rotation and security scanning?",
                "Are image retirements and additions tracked?",
                "Is your CI/CD pipeline integrated with security scanning tools?",
            ],
            "Registry Hygiene": [
                "Are outdated and unused images removed from registries?",
                "Are image repositories well-organized with proper tagging and lifecycle management?",
                "Do you have a single pane of glass for inventory reporting?",
            ],
            "Security & Vulnerability Management": [
                "Are SBOM signing and attestation enforced?",
                "Are language-level dependencies scanned for vulnerabilities?",
                "Are CI/CD pipelines enforcing security policies?",
                "Is independent image validation integrated using tools like Snyk, Grype, Wiz?",
            ],
            "Developer Workflow & Adoption": [
                "Are developers required to use pre-approved images?",
                "Do developers have access to tools that align with secure workflows?",
                "Are security best practices embedded into the development lifecycle?",
            ],
            "Supply Chain & Compliance": [
                "Are FIPS and other compliance requirements addressed in image policies?",
                "Are software components verified using Sigstore Cosign?",
                "Are all deployed images backed by secure provenance policies?",
            ],
            "Tooling & Integration": [
                "Are all container images pulled from approved registries?",
                "Is dynamic inventory scanning implemented?",
                "Are policy-based enforcements (e.g., Kyverno) active?",
            ]
        }
        
        if "current_step" not in st.session_state:
            st.session_state.current_step = 0
        if "category_scores" not in st.session_state:
            st.session_state.category_scores = {category: 0 for category in categories.keys()}
        
        category_names = list(categories.keys())
        current_step = st.session_state.current_step
        
        if current_step < len(category_names):
            category = category_names[current_step]
            st.subheader(category)
            
            score = 0
            for question in categories[category]:
                answer = st.radio(question, ("Yes", "No"), index=1, key=f"{category}_{question}")
                if answer == "Yes":
                    score += 1
            
            st.session_state.category_scores[category] = score
            
            if st.button("Next Category"):
                st.session_state.current_step += 1
                st.rerun()
        else:
            total_score = sum(st.session_state.category_scores.values())
            maturity_level = calculate_maturity(total_score)
            
            st.subheader("Assessment Result")
            st.write(f"Your overall maturity level: **{maturity_level}**")
            
            df = pd.DataFrame(list(st.session_state.category_scores.items()), columns=["Category", "Score"])
            st.write("### Category Breakdown")
            st.dataframe(df)
            
            fig, ax = plt.subplots()
            ax.barh(df["Category"], df["Score"], color='skyblue')
            ax.set_xlabel("Score")
            ax.set_title("Maturity Breakdown by Category")
            st.pyplot(fig)
            
            if st.button("Restart Assessment"):
                st.session_state.assessment_started = False
                st.session_state.current_step = 0
                st.session_state.category_scores = {category: 0 for category in categories.keys()}
                st.rerun()

if __name__ == "__main__":
    main()
