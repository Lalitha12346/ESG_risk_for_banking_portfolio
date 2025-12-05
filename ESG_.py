import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, Any

st.set_page_config(page_title="Revised ESG Performance Scorecard", page_icon="📈", layout="wide")

# --- Custom Styling (Injecting CSS for a cleaner look) ---
st.markdown("""
<style>
    .reportview-container .main {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
    }
    h2, h3, h4 {
        color: #2e6c80; /* A nice shade of blue */
    }
    /* Style for KPI boxes for visual separation */
    [data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* Use CSS for a color-coded grade/risk banner */
    .grade-A-plus, .grade-A, .grade-B-plus, .grade-B, .grade-C-plus, .grade-C {
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 1.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
    }
    /* RISK VIEW: Green/Yellow/Red reflects the ESG Score (High Score = Low Risk) */
    .grade-A-plus, .grade-A { background-color: #28a745; } /* Low Risk (High Score) */
    .grade-B-plus, .grade-B { background-color: #ffc107; color: black; } /* Medium Risk */
    .grade-C-plus, .grade-C { background-color: #dc3545; } /* High Risk (Low Score) */

</style>
""", unsafe_allow_html=True)

st.title("✨ Performance-Focused ESG Scorecard Dashboard")
st.markdown(
    "**Objective:** Evaluate your company's ESG performance based on new, performance-oriented criteria. Please complete all inputs.")

# --- Company Profile and Context ---
st.header("🏢 Company Profile and Context")
st.markdown("---")

# Define industry options for the selectbox
INDUSTRY_OPTIONS = [
    "Select Industry...",
    "Technology",
    "Financial Services",
    "Manufacturing",
    "Construction",
    "Energy & Utilities",
    "Healthcare",
    "Retail",
    "Other"
]

col_name, col_industry = st.columns([1, 1])

with col_name:
    st.text_input("Company Name:", key="company_name")
with col_industry:
    selected_industry = st.selectbox("Company Industry:", options=INDUSTRY_OPTIONS, key="company_industry")

st.text_area("✍️ Describe any significant ESG-related achievements or challenges not covered:",
             key="company_context", height=100)
st.markdown("---")

# --- Define NEW Question Structure with Alphanumeric Numbering ---
detailed_questions: Dict[str, Any] = {
    "E": {
        "title": "A. ENVIRONMENTAL PERFORMANCE (15 Questions)",
        "sections": [
            ("1. Energy & Emissions", [
                "Is the company actively increasing the share of renewable energy in its total energy consumption?",
                "Does the company measure and manage Scope 1, 2, and 3 emissions as part of a structured emissions-reduction strategy?",
                "Has the company set measurable and time-bound GHG reduction targets aligned with industry or national climate goals?",
                "Does the company demonstrate year-on-year reduction or stable performance in Scope 1 and Scope 2 emissions?",
            ]),
            ("2. Water Management", [
                "Does the company show responsible water usage through reductions, recycling, or efficiency improvements?",
                "Does the company proactively assess and mitigate water-related risks in high water-stress regions?",
            ]),
            ("3. Waste & Resource Management", [
                "Is the company increasing the proportion of waste that is recycled or reused instead of sent to landfill?",
            ]),
            ("4. Pollution & Compliance", [
                "Has the company maintained a clean environmental compliance record with minimal or no penalties in the last three years?",
                "Does the company maintain certified environmental management systems (e.g., ISO 14001) to ensure continued compliance?",
            ]),
            ("5. Energy Efficiency & Biodiversity", [
                "Does the company actively implement energy-efficiency initiatives to reduce energy intensity over time?",
                "Has the company identified and taken steps to protect biodiversity in ecologically sensitive operating regions?",
            ])
        ]
    },
    "S": {
        "title": "B. SOCIAL PERFORMANCE (20 Questions)",
        "sections": [
            ("1. Workforce Composition & Diversity", [
                "Does the company demonstrate a healthy gender balance that is reasonable for the industry?",
                "Is the representation of women in managerial roles improving or maintained at a competitive level relative to industry norms?",
            ]),
            ("2. Employee Wellbeing, Training & Safety", [
                "Is the company’s workplace injury rate (LTI/LTIFR) low compared to industry benchmarks?",
                "Does the company provide sufficient annual training hours to support employee development across all levels?",
                "Is the company certified under recognized occupational health and safety standards (e.g., ISO 45001)?",
            ]),
            ("3. Human Rights & Labour Standards", [
                "Are there strong human-rights practices in place with no indicators of child or forced labour risks?",
                "Does the company consistently comply with statutory labour laws (working hours, wages, benefits)?",
                "Does the company have mechanisms to identify and address labour-related grievances effectively?",
            ]),
            ("4. Social Impact & Community Relations", [
                "Does the company deliver CSR initiatives that show measurable community impact?",
                "Does the company ensure timely and effective resolution of customer grievances?",
            ]),
            ("5. Pay Equality & Turnover", [
                "Is the gender pay gap within a reasonable range, indicating fair compensation practices?",
            ])
        ]
    },
    "G": {
        "title": "C. GOVERNANCE PERFORMANCE (15 Questions)",
        "sections": [
            ("1. Board Structure & Oversight", [
                "Does the company maintain a well-balanced board with adequate independent and women directors?",
                "Is there a competency matrix showing that board members possess relevant and diverse expertise?",
                "Is ESG oversight integrated at the board or senior leadership level?",
            ]),
            ("2. Ethical Business Conduct & Transparency", [
                "Does the company maintain an effective whistleblower mechanism with prompt investigations?",
                "Is the company actively training employees and directors on anti-corruption and ethical conduct?",
                "Does the company consistently publish audited financial statements without delays or qualifications?",
            ]),
            ("3. Executive Compensation", [
                "Is executive compensation aligned with long-term business sustainability and ESG goals?",
            ]),
            ("4. Risk Management & Internal Controls", [
                "Does the company identify and manage ESG-related risks through defined mitigation strategies?",
                "Does the company maintain a robust enterprise risk-management (ERM) framework?",
            ]),
            ("5. Compliance & Legal", [
                "Has the company maintained a strong legal compliance record with limited penalties or litigations?",
                "Does the company have a strong data-protection and cybersecurity program?",
            ]),
            ("6. Supply Chain Governance", [
                "Does the company evaluate suppliers for ESG risks and compliance?",
                "Has the company demonstrated awareness and mitigation of ESG risks within its supply chain?",
            ])
        ]
    }
}

# --- Industry-Specific Thresholds Definition (Kept for Social Scoring) ---
INDUSTRY_THRESHOLDS_MAP: Dict[str, Dict[str, float]] = {
    "Technology": {"div_high": 0.35, "div_medium": 0.20, "pay_gap_low": 0.08, "pay_gap_medium": 0.20,
                   "attrition_gap_low": 0.04, "attrition_gap_medium": 0.10},
    "Financial Services": {"div_high": 0.45, "div_medium": 0.30, "pay_gap_low": 0.10, "pay_gap_medium": 0.22,
                           "attrition_gap_low": 0.06, "attrition_gap_medium": 0.12},
    "Manufacturing": {"div_high": 0.20, "div_medium": 0.10, "pay_gap_low": 0.12, "pay_gap_medium": 0.28,
                      "attrition_gap_low": 0.08, "attrition_gap_medium": 0.15},
    "Construction": {"div_high": 0.15, "div_medium": 0.08, "pay_gap_low": 0.15, "pay_gap_medium": 0.30,
                     "attrition_gap_low": 0.10, "attrition_gap_medium": 0.20},
    "Energy & Utilities": {"div_high": 0.25, "div_medium": 0.15, "pay_gap_low": 0.10, "pay_gap_medium": 0.25,
                           "attrition_gap_low": 0.07, "attrition_gap_medium": 0.14},
    "Healthcare": {"div_high": 0.55, "div_medium": 0.40, "pay_gap_low": 0.05, "pay_gap_medium": 0.15,
                   "attrition_gap_low": 0.03, "attrition_gap_medium": 0.08},
    "Retail": {"div_high": 0.50, "div_medium": 0.35, "pay_gap_low": 0.08, "pay_gap_medium": 0.20,
               "attrition_gap_low": 0.05, "attrition_gap_medium": 0.12},
    "DEFAULT": {"div_high": 0.40, "div_medium": 0.25, "pay_gap_low": 0.10, "pay_gap_medium": 0.25,
                "attrition_gap_low": 0.05, "attrition_gap_medium": 0.12},
}

# --- Fixed Performance Thresholds for NEW Metrics ---
PERFORMANCE_THRESHOLDS: Dict[str, float] = {
    "ghg_high": 500, "ghg_medium": 150,  # Tonnes CO2e: <=150=1, 151-500=0.5, >500=0
    "water_high": 10000, "water_medium": 50000,  # KL: <10k=1, 10k-50k=0.5, >50k=0 (Rough Example)
    "waste_haz_high": 10, "waste_haz_medium": 50,  # Tonnes: <10=1, 10-50=0.5, >50=0 (Rough Example)
    "renew_high": 0.50, "renew_medium": 0.20,  # % Renewable: >=50=1, 20-49=0.5, <20=0
    "csr_high": 1.10, "csr_medium": 1.00,  # CSR Utilisation: >=110%=1, 100-109=0.5, <100=0
}

# --- Initialize Response Containers ---
all_responses: list[int] = []  # Stores 0 or 1 for all Yes/No questions
env_responses: list[int] = []
social_responses: list[int] = []
gov_responses: list[int] = []
q_key_index = 1  # Used for unique key generation across all Streamlit radios


# --- Display Sections and Collect Responses ---

def collect_responses(category_key: str, response_list: list[int]):
    global q_key_index
    data = detailed_questions[category_key]

    # Calculate total questions in this category for the expander title
    total_q_count = sum(len(q) for _, q in data["sections"])

    with st.expander(f"**{data['title']}** - Click to answer {total_q_count} Questions", expanded=False):
        category_prefix = category_key

        for sub_index, (section_title, questions) in enumerate(data["sections"], 1):
            num_questions = len(questions)
            st.markdown(f"**{category_prefix}.{sub_index}. {section_title}** ({num_questions} questions)")

            for q_sub_index, q in enumerate(questions, 1):
                question_prefix = f"{category_prefix}.{sub_index}.{q_sub_index}"

                response = st.radio(
                    f"**{question_prefix}** {q}",
                    options=["Yes", "No"],
                    index=None,
                    key=f"q{q_key_index}_{category_key}",
                    horizontal=True
                )
                score_val = 1 if response == "Yes" else 0
                response_list.append(score_val)
                all_responses.append(score_val)
                q_key_index += 1


# 1. Environmental Section (A)
collect_responses("E", env_responses)

# 2. Social Section (B)
collect_responses("S", social_responses)

# 3. Governance Section (C)
collect_responses("G", gov_responses)

# --- D. MANDATORY SOCIAL INPUTS (NUMERIC ENTRIES) ---
st.header("🔢 D. Mandatory Workforce & Pay Inputs")
st.caption("These inputs drive calculations for Gender Diversity, Pay Equity, and Attrition Gap scores.")
st.markdown("---")

col_s1, col_s2, col_s3 = st.columns(3)

# S. Mandatory Inputs
with col_s1:
    male_employees = st.number_input("1. Male Employees:", min_value=0, step=1, key="male_count_new", value=500)
    female_employees = st.number_input("2. Female Employees:", min_value=0, step=1, key="female_count_new", value=200)
    avg_male_pay = st.number_input("3. Avg. Male Pay (₹):", min_value=0.0, step=10000.0,
                                   key="male_pay_new", value=1500000.0)

with col_s2:
    male_attrition = st.number_input("4. Male Attrition (Count):", min_value=0, step=1,
                                     key="male_attrition_new", value=50)
    female_attrition = st.number_input("5. Female Attrition (Count):", min_value=0, step=1,
                                       key="female_attrition_new", value=25)
    avg_female_pay = st.number_input("6. Avg. Female Pay (₹):", min_value=0.0, step=10000.0,
                                     key="female_pay_new", value=1300000.0)

with col_s3:
    women_manager_pct = st.number_input("7. % of women in managerial roles:", min_value=0.0, max_value=100.0,
                                        key="women_manager_pct", value=25.0)  # S.1.4
    employee_turnover_pct = st.number_input("8. Total Employee Turnover Rate (%):", min_value=0.0, max_value=100.0,
                                            key="employee_turnover_pct", value=15.0)  # S.5.2
st.markdown("---")

# --- F. CORE PERFORMANCE METRICS (QUANTITATIVE) - NEW SECTION ---
st.header("📈 E. Core Performance Metrics (Environmental & Governance)")
st.caption("Quantitative inputs driving performance scores.")
st.markdown("---")

# E. Numeric Inputs
st.subheader("E.1 Environmental Metrics")
col_e1, col_e2 = st.columns(2)
with col_e1:
    ghg_emissions = st.number_input("1. Total GHG emissions (tonnes CO₂e):", min_value=0.0, key="ghg_emissions_new",
                                    value=300.0)  # E.1.5
    water_consumption = st.number_input("2. Annual water consumption (kilolitres):", min_value=0.0,
                                        key="water_consumption", value=15000.0)  # E.2.3
with col_e2:
    hazardous_waste = st.number_input("3. Total hazardous waste generated (tonnes):", min_value=0.0,
                                      key="hazardous_waste", value=15.0)  # E.3.2
    renewable_pct = st.number_input("4. % of total energy from renewable sources:", min_value=0.0, max_value=100.0,
                                    key="renewable_pct", value=30.0)  # E.5.3

# S. Numeric Inputs
st.subheader("E.2 Social & Governance Metrics")
col_s_g1, col_s_g2 = st.columns(2)
with col_s_g1:
    workplace_injuries = st.number_input("5. Total workplace injuries/accidents last year:", min_value=0, step=1,
                                         key="workplace_injuries", value=1)  # S.2.3
    csr_utilisation_pct = st.number_input("6. CSR utilisation vs mandated (%):", min_value=0.0, step=1.0,
                                          key="csr_utilisation_pct", value=105.0)  # S.4.2
with col_s_g2:
    whistleblower_resolved = st.number_input("7. Whistleblower complaints resolved:", min_value=0, step=1,
                                             key="whistleblower_resolved", value=5)  # G.4.3
    regulatory_noncompliance = st.number_input("8. Regulatory non-compliance incidents (3 years):", min_value=0,
                                               step=1, key="regulatory_noncompliance", value=0)  # G.5.2
st.markdown("---")

# --- Initialize Score Calculation Logic ---
# FIX: Recalculate the total number of non-numeric questions for comparison
total_disclosure_questions = sum(
    len(questions)
    for category_data in detailed_questions.values()
    for _, questions in category_data["sections"]
)


def get_grade_class(score: float) -> str:
    """Returns a CSS class for the grade banner based on the ESG Score."""
    if score >= 90:
        return "grade-A-plus"
    elif score >= 80:
        return "grade-A"
    elif score >= 70:
        return "grade-B-plus"
    elif score >= 60:
        return "grade-B"
    elif score >= 50:
        return "grade-C-plus"
    else:
        return "grade-C"


# --- Calculate Score ---
if st.button("🚀 Calculate Detailed ESG Risk and Dashboard"):
    # 1. Input Validation (Using st.empty for cleaner error display)
    error_placeholder = st.empty()
    if selected_industry == "Select Industry...":
        error_placeholder.error("🛑 **Input Error:** Please select a valid Industry.")
        st.stop()

    # The length of all_responses is populated across multiple calls, check against the expected total.
    if len(all_responses) != total_disclosure_questions:
        error_placeholder.error(
            f"⚠️ **Input Error:** Please answer all {total_disclosure_questions} Yes/No questions. ({len(all_responses)} answered)")
        st.stop()

    # All checks passed, clear error placeholder
    error_placeholder.empty()

    # Get thresholds based on selected industry or default
    thresholds_key = selected_industry if selected_industry in INDUSTRY_THRESHOLDS_MAP else "DEFAULT"
    TH = INDUSTRY_THRESHOLDS_MAP[thresholds_key]
    PT = PERFORMANCE_THRESHOLDS  # Performance Thresholds

    # ----------------------------------------------------
    # --- 1. DISCLOSURE SCORES (A, B, C) ---
    # ----------------------------------------------------

    env_score_sum = sum(env_responses)
    social_disclosure_sum = sum(social_responses)
    gov_score_sum = sum(gov_responses)
    total_disclosure_score = sum(all_responses)

    # ----------------------------------------------------
    # --- 2. PERFORMANCE METRIC SCORES (D & F) ---
    # ----------------------------------------------------

    # A. GENDER DIVERSITY (D.1, D.2)
    total_employees = male_employees + female_employees
    if total_employees > 0:
        gender_diversity_pct = female_employees / total_employees
        if gender_diversity_pct > TH['div_high']:
            diversity_score = 1.0
        elif gender_diversity_pct >= TH['div_medium']:
            diversity_score = 0.5
        else:
            diversity_score = 0.0
    else:
        gender_diversity_pct = 0.0
        diversity_score = 0.0

    # B. PAY EQUITY (D.3, D.6)
    if avg_male_pay > 0:
        pay_gap = (avg_male_pay - avg_female_pay) / avg_male_pay
        if pay_gap <= TH['pay_gap_low']:
            pay_equity_score = 1.0
        elif pay_gap <= TH['pay_gap_medium']:
            pay_equity_score = 0.5
        else:
            pay_equity_score = 0.0
    else:
        pay_gap = 0.0
        pay_equity_score = 0.0

    # C. ATTRITION GAP (D.4, D.5)
    male_attrition_rate = (male_attrition / male_employees) if male_employees > 0 else 0.0
    female_attrition_rate = (female_attrition / female_employees) if female_employees > 0 else 0.0
    attrition_gap = abs(male_attrition_rate - female_attrition_rate)

    if attrition_gap <= TH['attrition_gap_low']:
        attrition_score = 1.0
    elif attrition_gap <= TH['attrition_gap_medium']:
        attrition_score = 0.5
    else:
        attrition_score = 0.0

    # D. GHG Emissions Score (E.1)
    if ghg_emissions <= PT['ghg_medium']:
        ghg_score = 1.0
    elif ghg_emissions <= PT['ghg_high']:
        ghg_score = 0.5
    else:
        ghg_score = 0.0

    # E. Renewable Energy Score (E.4)
    renewable_ratio = renewable_pct / 100
    if renewable_ratio >= PT['renew_high']:
        renewable_score = 1.0
    elif renewable_ratio >= PT['renew_medium']:
        renewable_score = 0.5
    else:
        renewable_score = 0.0

    # F. Hazardous Waste Score (E.3)
    if hazardous_waste <= PT['waste_haz_high']:
        waste_score = 1.0
    elif hazardous_waste <= PT['waste_haz_medium']:
        waste_score = 0.5
    else:
        waste_score = 0.0

    # G. Water Consumption Score (E.2 - Lower is better)
    if water_consumption <= PT['water_high']:
        water_score = 1.0
    elif water_consumption <= PT['water_medium']:
        water_score = 0.5
    else:
        water_score = 0.0

    # H. CSR Utilisation Score (E.6)
    csr_ratio = csr_utilisation_pct / 100
    if csr_ratio >= PT['csr_high']:
        csr_score = 1.0
    elif csr_ratio >= PT['csr_medium']:
        csr_score = 0.5
    else:
        csr_score = 0.0

    # I. Regulatory Compliance Score (E.8 - Lower is better)
    if regulatory_noncompliance == 0:
        compliance_score = 1.0
    elif regulatory_noncompliance <= 2:
        compliance_score = 0.5
    else:
        compliance_score = 0.0

    # J. Injury Score (E.5)
    if workplace_injuries == 0:
        injury_score = 1.0
    elif workplace_injuries <= 2:
        injury_score = 0.5
    else:
        injury_score = 0.0

    # K. Employee Turnover Rate (D.8)
    if employee_turnover_pct <= 10.0:
        turnover_score = 1.0
    elif employee_turnover_pct <= 20.0:
        turnover_score = 0.5
    else:
        turnover_score = 0.0

    # L. Whistleblower Resolved (E.7)
    # C.2.2 is the 4th question in gov_responses (index 3)
    whistleblower_mechanism_disclosed = gov_responses[3] if len(gov_responses) > 3 else 0
    if whistleblower_mechanism_disclosed == 1 and whistleblower_resolved > 0:
        whistleblower_score = 1.0
    elif whistleblower_mechanism_disclosed == 1:
        whistleblower_score = 0.5  # Mechanism exists, but no resolutions (neutral)
    else:
        whistleblower_score = 0.0

    # TOTAL PERFORMANCE METRICS (Unweighted for simplicity/correct identification of worst metric)
    unweighted_performance_metrics = {
        "Gender Diversity Score": diversity_score,
        "Pay Equity Score": pay_equity_score,
        "Attrition Equality Score": attrition_score,
        "GHG Emissions Score": ghg_score,
        "Renewable Energy Score": renewable_score,
        "Hazardous Waste Score": waste_score,
        "Water Consumption Score": water_score,
        "CSR Utilisation Score": csr_score,
        "Regulatory Compliance Score": compliance_score,
        "Workplace Injury Score": injury_score,
        "Employee Turnover Score": turnover_score,
        "Whistleblower Score": whistleblower_score,
    }

    # ----------------------------------------------------
    # --- 3. WEIGHTED SCORE CALCULATION (UNIFORM WEIGHT=3) ---
    # ----------------------------------------------------

    DISCLOSURE_WEIGHT = 1
    # UNIFORM weight for all performance metrics, as requested
    PERFORMANCE_WEIGHT = 3

    # Calculate Weighted Performance Scores (All use the same weight)
    performance_metrics_weighted = {
        k: v * PERFORMANCE_WEIGHT for k, v in unweighted_performance_metrics.items()
    }

    # Calculate Max Weighted Scores (All use the same weight)
    max_scores = {
        k: PERFORMANCE_WEIGHT for k in unweighted_performance_metrics.keys()
    }

    total_weighted_performance_score = sum(performance_metrics_weighted.values())
    TOTAL_PERFORMANCE_METRICS_COUNT = len(unweighted_performance_metrics)
    TOTAL_PERFORMANCE_METRICS_WEIGHTED = TOTAL_PERFORMANCE_METRICS_COUNT * PERFORMANCE_WEIGHT

    TOTAL_WEIGHTED_MAX_SCORE = (total_disclosure_questions * DISCLOSURE_WEIGHT) + TOTAL_PERFORMANCE_METRICS_WEIGHTED

    total_weighted_score = (total_disclosure_score * DISCLOSURE_WEIGHT) + total_weighted_performance_score

    # Final Score and Risk Score
    score = (total_weighted_score / TOTAL_WEIGHTED_MAX_SCORE) * 100
    risk_score = 100 - score  # ESG Risk is the inverse of the ESG Score

    # --- ESG Grade Logic ---
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B+"
    elif score >= 60:
        grade = "B"
    elif score >= 50:
        grade = "C+"
    else:
        grade = "C"

    # --- Calculate Percentage Variables for Output ---
    env_pct = env_score_sum / len(env_responses) * 100 if len(env_responses) > 0 else 0
    social_pct = social_disclosure_sum / len(social_responses) * 100 if len(social_responses) > 0 else 0
    gov_pct = gov_score_sum / len(gov_responses) * 100 if len(gov_responses) > 0 else 0

    # Attrition Rate (Total)
    total_attrition = male_attrition + female_attrition
    total_attrition_rate = (total_attrition / total_employees) * 100 if total_employees > 0 else 0

    # --- Display Summary Results ---
    st.markdown("---")
    st.header("✅ ESG Risk Management Dashboard")
    company_name = st.session_state.get('company_name', 'Unnamed Company')
    st.subheader(f"Results for: **{company_name}** ({thresholds_key} Industry)")

    ## 1. SCORE BANNER
    grade_class = get_grade_class(score)
    col_score, col_grade = st.columns(2)
    with col_score:
        # DISPLAY RISK SCORE
        st.markdown(
            f"<div class='{grade_class}'>📉 OVERALL ESG RISK: **{risk_score:.1f}%**</div>",
            unsafe_allow_html=True
        )
    with col_grade:
        # DISPLAY ESG GRADE
        st.markdown(
            f"<div class='{grade_class}'>⭐ ESG GRADE: **{grade}**</div>",
            unsafe_allow_html=True
        )

    st.caption(
        f"Performance Score: {score:.1f}% (100% - Risk Score) | All performance metrics are uniformly weighted **{PERFORMANCE_WEIGHT}x**.")
    # Progress bar reflects the Performance Score (higher = better)
    st.progress(int(score))

    st.markdown("---")

    ## 2. RISK ALERTS
    st.subheader("🚨 Risk Alerts")
    alerts = []
    if pay_gap > TH['pay_gap_medium']:
        alerts.append("High **Gender Pay Inequity** Risk (Gap exceeds medium industry threshold)")
    if regulatory_noncompliance > 0:
        alerts.append("Significant **Compliance** Risk (Non-compliance incidents recorded in the last 3 years)")
    if ghg_emissions > PT['ghg_high']:
        alerts.append("Severe **Carbon Emissions** Risk (GHG exceeds 500 Tonnes CO₂e)")
    if renewable_ratio < PT['renew_medium']:
        alerts.append("Moderate **Climate Transition** Risk (Low adoption of renewable energy sources)")
    if workplace_injuries > 2:
        alerts.append("High **Operational Safety** Risk (Multiple workplace injuries recorded)")

    if alerts:
        alert_cols = st.columns(min(3, len(alerts)))  # Limit to 3 columns for better layout
        for i, alert in enumerate(alerts):
            alert_cols[i % len(alert_cols)].error(alert)
    else:
        st.success("🎉 No immediate, high-priority risk alerts triggered.")

    st.markdown("---")

    ## 3. DASHBOARD KPI CARDS
    st.subheader("💎 Key Performance Indicators (KPIs)")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.metric("Gender Diversity", f"{gender_diversity_pct * 100:.1f}%",
                help="Percentage of female employees in the workforce.")
    # Use delta to show how far the pay gap is from 0% (ideal)
    kpi2.metric("Gender Pay Gap", f"{pay_gap * 100:.1f}%",
                delta=f"vs Target {TH['pay_gap_low'] * 100:.1f}%", delta_color="inverse",
                help="Difference between average male and female pay (Male higher). Lower is better.")
    kpi3.metric("GHG Emissions", f"{ghg_emissions:.0f} tCO₂e",
                delta=f"vs High {PT['ghg_high']:.0f} tCO₂e", delta_color="inverse",
                help="Total Scope 1 & 2 Emissions.")
    kpi4.metric("Renewable Energy %", f"{renewable_pct:.1f}%",
                delta=f"vs Target {PT['renew_high'] * 100:.0f}%",
                help="Percentage of total energy sourced from renewables.")
    kpi5.metric("Workplace Injuries", f"{workplace_injuries:.0f}",
                delta="0 is ideal", delta_color="inverse",
                help="Total workplace injuries/accidents last year. Lower is better.")

    st.markdown("---")

    ## 4. DETAILED BREAKDOWN & VISUALS
    st.write("### 📊 Performance and Disclosure Breakdown")

    # Detailed scores in an expander
    with st.expander("📝 Disclosure vs. Performance Breakdown", expanded=False):
        st.markdown(
            f"**Total Disclosure Score:** {total_disclosure_score}/{total_disclosure_questions} Questions Answered")
        st.markdown(
            f"**Total Performance Score (Weighted):** {total_weighted_performance_score}/{TOTAL_PERFORMANCE_METRICS_WEIGHTED} Weighted Performance Points")
        st.markdown("---")

        # Disclosure Scores
        st.markdown("#### Disclosure Completion")
        col_disc1, col_disc2, col_disc3 = st.columns(3)
        col_disc1.info(f"**Environmental:** {env_score_sum}/{len(env_responses)} ({env_pct:.1f}% Yes)")
        col_disc2.info(f"**Social:** {social_disclosure_sum}/{len(social_responses)} ({social_pct:.1f}% Yes)")
        col_disc3.info(f"**Governance:** {gov_score_sum}/{len(gov_responses)} ({gov_pct:.1f}% Yes)")

        st.markdown("#### Unweighted Performance Metric Results (Score out of 100%)")
        col_d1, col_d2, col_d3 = st.columns(3)

        # Use unweighted scores for displaying % performance here
        performance_list = list(unweighted_performance_metrics.items())

        for i, (metric_name, score_val) in enumerate(performance_list):
            display_score = score_val * 100

            if i < 4:
                col_d = col_d1
            elif i < 8:
                col_d = col_d2
            else:
                col_d = col_d3

            # Use formatted text for the performance score
            col_d.metric(f"**{i + 1}.** {metric_name.replace(' Score', '')}", f"{display_score:.1f}%")

    ## Interactive Plotly Charts Section
    st.write("### 📈 Visual Metrics")

    col_charts1, col_charts2 = st.columns(2)

    # 1. GENDER DIVERSITY PIE CHART (Plotly)
    with col_charts1:
        if total_employees > 0:
            df_diversity = pd.DataFrame({
                'Gender': ['Male', 'Female'],
                'Count': [male_employees, female_employees]
            })
            fig1 = px.pie(
                df_diversity,
                values='Count',
                names='Gender',
                title='1. Workforce Gender Diversity',
                color_discrete_sequence=['#1f77b4', '#ff7f0e']  # Blue/Orange
            )
            fig1.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
            st.plotly_chart(fig1, use_container_width=True)

    # 2. CORE ENVIRONMENTAL PERFORMANCE RADAR CHART (New)
    with col_charts2:
        df_env_radar = pd.DataFrame(dict(
            r=[ghg_score * 100, renewable_score * 100, water_score * 100, waste_score * 100],
            theta=['GHG Score', 'Renewable Energy Score', 'Water Mgmt Score', 'Waste Mgmt Score'],
            Metric=['Environmental'] * 4
        ))
        fig_radar_env = px.line_polar(
            df_env_radar,
            r='r',
            theta='theta',
            line_close=True,
            range_r=[0, 100],
            color_discrete_sequence=['#28a745'],  # Green
            title="2. Core Environmental Performance Radar"
        )
        fig_radar_env.update_traces(fill='toself')
        st.plotly_chart(fig_radar_env, use_container_width=True)

    # 3. GENDER PAY BAR CHART
    chart3, chart4 = st.columns(2)
    with chart3:
        if avg_male_pay > 0 or avg_female_pay > 0:
            df_pay = pd.DataFrame({
                'Gender': ['Male', 'Female'],
                'Average Pay (₹)': [avg_male_pay, avg_female_pay]
            })
            fig3 = px.bar(
                df_pay,
                x='Gender',
                y='Average Pay (₹)',
                title='3. Average Annual Pay Comparison',
                color='Gender',
                color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'},
                text='Average Pay (₹)'
            )
            fig3.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            fig3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            st.plotly_chart(fig3, use_container_width=True)

    # 4. SOCIAL & GOVERNANCE PERFORMANCE BAR CHART
    with chart4:
        df_social_gov = pd.DataFrame({
            'Metric': ['Pay Equity Score', 'Injury Score', 'Compliance Score', 'Turnover Score'],
            'Score (%)': [pay_equity_score * 100, injury_score * 100, compliance_score * 100, turnover_score * 100]
        })
        fig4 = px.bar(
            df_social_gov,
            x='Metric',
            y='Score (%)',
            title='4. Key Social & Governance Performance Scores',
            color='Metric',
            color_discrete_sequence=px.colors.qualitative.Set1,
            range_y=[0, 100]
        )
        fig4.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    ## 5. TOP AREA FOR IMPROVEMENT (Single Worst Core Metric)
    st.header("🎯 Highest Priority Area for Improvement")

    # Filter for only Core Performance Metrics
    core_performance_data = {
        k.replace(' Score', ''): v * 100 for k, v in unweighted_performance_metrics.items()
    }

    # Sort parameters by score (ascending)
    sorted_core_improvement = sorted(core_performance_data.items(), key=lambda item: item[1])

    # Get the weakest metric (the one with the lowest score)
    if sorted_core_improvement:
        weakest_param, weakest_score = sorted_core_improvement[0]

        # Display ONLY the parameter and the instruction to improve it
        st.markdown(f"### 🛑 Worst Core Performance Metric: **{weakest_param}**")

        st.info(
            f"**Action:** The parameter **{weakest_param}** is the weakest performance metric. You must prioritize efforts to improve it."
        )
    else:
        st.success(
            "All core performance metrics are currently excellent or not enough data was provided to calculate a weakest metric.")