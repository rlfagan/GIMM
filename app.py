import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys

# Function to check and install missing dependencies
def install_requirements():
    required_packages = ["streamlit", "pandas", "matplotlib"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

# Function to calculate maturity level based on score
def calculate_maturity(score):
    if score >= 18:
        return "Advanced"
    elif score >= 12:
        return "Intermediate"
    else:
        return "Basic"

def main():
    st.title("Container Security Maturity Model Assessment")
    st.write("Answer the following questions to determine your organization's maturity level.")

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

    total_score = 0
    category_scores = {}

    for category, questions in categories.items():
        st.subheader(category)
        score = 0
        for question in questions:
            answer = st.radio(question, ("Yes", "No"), index=1)
            if answer == "Yes":
                score += 1
        category_scores[category] = score
        total_score += score

    maturity_level = calculate_maturity(total_score)

    st.subheader("Assessment Result")
    st.write(f"Your overall maturity level: **{maturity_level}**")

    # Display category breakdown
    df = pd.DataFrame(list(category_scores.items()), columns=["Category", "Score"])
    st.table(df)

    # Plot a bar chart
    fig, ax = plt.subplots()
    ax.barh(df["Category"], df["Score"], color='skyblue')
    ax.set_xlabel("Score")
    ax.set_title("Maturity Breakdown by Category")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
