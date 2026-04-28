import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')
 
st.set_page_config(
    page_title="European Bank — Customer Retention Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1d24; border-right: 1px solid #2d3139; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="metric-container"] {
        background-color: #1a1d24; border: 1px solid #2d3139;
        border-radius: 8px; padding: 16px;
    }
    [data-testid="metric-container"] label { color: #9ca3af !important; font-size: 13px !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important; font-size: 26px !important; font-weight: 700 !important;
    }
    h1, h2, h3 { color: #ffffff !important; }
    hr { border-color: #2d3139 !important; }
    .section-label {
        font-size: 15px; font-weight: 700; color: #ffffff;
        margin: 20px 0 10px 0; padding-bottom: 6px;
        border-bottom: 1px solid #2d3139;
    }
    .page-title { font-size: 36px; font-weight: 800; color: #ffffff; margin-bottom: 4px; }
    .page-subtitle { font-size: 14px; color: #9ca3af; margin-bottom: 20px; }
    .insight-box {
        background-color: #1a1d24; border-left: 4px solid #c9a84c;
        padding: 12px 16px; border-radius: 4px; margin: 8px 0;
        font-size: 14px; color: #e0e0e0;
    }
    .rec-box {
        background-color: #1a1d24; border-left: 4px solid #2ecc71;
        padding: 12px 16px; border-radius: 4px; margin: 6px 0;
        font-size: 14px; color: #e0e0e0;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
 
# ── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank.csv")
    df['Churn'] = df['Exited']
    df['EngagementProfile'] = 'Other'
    df.loc[(df['IsActiveMember']==1) & (df['NumOfProducts']>=2), 'EngagementProfile'] = 'Active Engaged'
    df.loc[(df['IsActiveMember']==0) & (df['NumOfProducts']<=1), 'EngagementProfile'] = 'Inactive Disengaged'
    df.loc[(df['IsActiveMember']==1) & (df['NumOfProducts']==1), 'EngagementProfile'] = 'Active Low-Product'
    df.loc[(df['IsActiveMember']==0) & (df['Balance']>df['Balance'].median()), 'EngagementProfile'] = 'Inactive High-Balance'
    df['RelationshipStrengthIndex'] = (
        df['IsActiveMember'] * 0.4 +
        (df['NumOfProducts'] / df['NumOfProducts'].max()) * 0.3 +
        (df['Tenure'] / df['Tenure'].max()) * 0.2 +
        df['HasCrCard'] * 0.1
    ).round(3)
    df['AtRiskPremium'] = ((df['Balance'] > df['Balance'].quantile(0.75)) & (df['IsActiveMember'] == 0)).astype(int)
    df['AgeGroup'] = pd.cut(df['Age'], bins=[18,30,40,50,60,100], labels=['18-30','31-40','41-50','51-60','60+'])
    df['BalanceTier'] = pd.cut(df['Balance'], bins=5, labels=['Very Low','Low','Medium','High','Very High'])
    return df
 
df = load_data()
 
def dark_style():
    plt.rcParams.update({
        "figure.facecolor":"#1a1d24","axes.facecolor":"#1a1d24",
        "axes.edgecolor":"#2d3139","axes.labelcolor":"#9ca3af",
        "axes.titlecolor":"#ffffff","xtick.color":"#9ca3af","ytick.color":"#9ca3af",
        "text.color":"#ffffff","grid.color":"#2d3139","grid.linestyle":"--",
        "grid.alpha":0.5,"axes.grid":True,
        "font.size":11,           # FIX: increased from 10 → 11
        "axes.titlesize":13,      # FIX: explicit title size
        "axes.labelsize":11,      # FIX: explicit label size
        "xtick.labelsize":10,     # FIX: explicit tick size
        "ytick.labelsize":10,
    })
dark_style()
 
def insight(text):
    st.markdown(
        f"<div style='background-color:#223344; border-left:4px solid #4da6ff; "
        f"padding:12px 16px; border-radius:6px; margin:8px 0; "
        f"font-size:14px; color:#ffffff;'>"
        f"💡 <strong>Insight:</strong> {text}</div>",
        unsafe_allow_html=True
    )
 
def recommendation(text):
    st.markdown(
        f"<div style='background-color:#1f3d2b; border-left:4px solid #2ecc71; "
        f"padding:12px 16px; border-radius:6px; margin:8px 0; "
        f"font-size:14px; color:#ffffff;'>"
        f"✅ <strong>Recommendation:</strong> {text}</div>",
        unsafe_allow_html=True
    )
 
# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px 0;'>
        <div style='font-size:20px; font-weight:900; letter-spacing:2px; color:#ffffff;'>
            EUROPEAN <span style='color:#c9a84c;'>BANK</span>
        </div>
        <div style='font-size:10px; color:#c9a84c; letter-spacing:2px; margin-top:2px;'>
            RETENTION INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
 
    st.markdown("**📍 Geography**")
    all_geo = ["All"] + sorted(df["Geography"].unique().tolist())
    selected_geo = st.selectbox("Country", all_geo)
 
    st.markdown("**👤 Demographics**")
    all_gender = ["All"] + sorted(df["Gender"].unique().tolist())
    selected_gender = st.selectbox("Gender", all_gender)
 
    st.markdown("**🏦 Product & Engagement**")
    all_products = ["All"] + sorted(df["NumOfProducts"].unique().tolist())
    selected_products = st.selectbox("Number of Products", all_products)
    active_filter = st.selectbox("Member Status", ["All", "Active", "Inactive"])
 
    st.markdown("**💰 Financial**")
    bal_min, bal_max = int(df["Balance"].min()), int(df["Balance"].max())
    selected_balance = st.slider("Min Balance (€)", bal_min, bal_max, bal_min, step=1000)
    credit_min, credit_max = int(df["CreditScore"].min()), int(df["CreditScore"].max())
    selected_credit = st.slider("Min Credit Score", credit_min, credit_max, credit_min, step=10)
 
    st.markdown("---")
    st.markdown("**📊 Dashboard Module**")
    page = st.radio("", options=[
        "Engagement Overview",
        "Product Utilization",
        "High-Value Risk Analysis",
        "Retention Strength",
    ])
    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#9ca3af;'>Overall Churn Rate: {df['Churn'].mean()*100:.2f}%</div>", unsafe_allow_html=True)
 
# ── Apply Filters ─────────────────────────────────────────
fdf = df.copy()
if selected_geo != "All":      fdf = fdf[fdf["Geography"] == selected_geo]
if selected_gender != "All":   fdf = fdf[fdf["Gender"] == selected_gender]
if selected_products != "All": fdf = fdf[fdf["NumOfProducts"] == selected_products]
if active_filter == "Active":  fdf = fdf[fdf["IsActiveMember"] == 1]
if active_filter == "Inactive":fdf = fdf[fdf["IsActiveMember"] == 0]
fdf = fdf[fdf["Balance"] >= selected_balance]
fdf = fdf[fdf["CreditScore"] >= selected_credit]
 
# FIX: Safe churn rate — avoid division by zero if filters return empty
if len(fdf) == 0:
    st.warning("⚠️ No data matches the current filters. Please adjust your sidebar selections.")
    st.stop()
 
churn_rate = fdf['Churn'].mean() * 100
 
# ── Logo Header ───────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:10px 0 20px 0;'>
    <div style='font-size:38px; font-weight:900; letter-spacing:5px; color:#ffffff;'>
        EUROPEAN <span style='color:#c9a84c;'>BANK</span>
    </div>
    <div style='font-size:12px; color:#c9a84c; letter-spacing:4px; margin-top:4px;'>
        CUSTOMER ENGAGEMENT & RETENTION INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════
# PAGE 1 — ENGAGEMENT OVERVIEW
# ══════════════════════════════════════════════════════════
if page == "Engagement Overview":
    st.markdown('<div class="page-title">Engagement Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Customer engagement profiles and churn distribution across segments</div>', unsafe_allow_html=True)
 
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👥 Total Customers", f"{len(fdf):,}")
    c2.metric("⚠️ Churned",         f"{fdf['Churn'].sum():,}")
    c3.metric("✅ Retained",        f"{(fdf['Churn']==0).sum():,}")
    c4.metric("📉 Churn Rate",      f"{churn_rate:.2f}%")
    c5.metric("🏦 Avg Balance",     f"€{fdf['Balance'].mean():,.0f}")
    st.markdown("---")
 
    col_l, col_r = st.columns(2)
 
    with col_l:
        st.markdown('<div class="section-label">🍩 Churn Distribution</div>', unsafe_allow_html=True)
        retained = (fdf['Churn']==0).sum()
        churned  = fdf['Churn'].sum()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie([retained, churned],
            labels=[f'Retained\n({retained:,})', f'Churned\n({churned:,})'],
            colors=['#2ecc71','#e74c3c'], autopct='%1.1f%%', startangle=90,
            textprops={'color':'white','fontsize':12},
            wedgeprops={'edgecolor':'#1a1d24','linewidth':2})
        ax.set_title('Overall Churn Distribution', color='#ffffff', fontsize=14, fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r:
        st.markdown('<div class="section-label">🌍 Churn Rate by Geography</div>', unsafe_allow_html=True)
        geo_churn = fdf.groupby('Geography')['Churn'].mean() * 100
        colors_g = ['#e74c3c' if v > churn_rate else '#2ecc71' for v in geo_churn.values]
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(geo_churn.index, geo_churn.values, color=colors_g, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Churn Rate by Geography', color='#ffffff', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, geo_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=11, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    worst_geo = geo_churn.idxmax()
    best_geo  = geo_churn.idxmin()
    st.markdown("---")
    insight(f"1 in every {int(100/churn_rate)} customers is churning. "
            f"{worst_geo} has the highest churn at {geo_churn.max():.1f}% — "
            f"{geo_churn.max()-geo_churn.min():.1f} points above {best_geo} ({geo_churn.min():.1f}%). "
            f"A country-specific retention program is urgently needed.")
    st.markdown("---")
    col_l2, col_r2 = st.columns(2)
 
    with col_l2:
        st.markdown('<div class="section-label">🧩 Churn by Engagement Profile</div>', unsafe_allow_html=True)
        eng_churn = fdf.groupby('EngagementProfile')['Churn'].mean() * 100
        eng_churn = eng_churn.sort_values(ascending=True)
        colors_e  = ['#2ecc71' if v < churn_rate else '#e74c3c' for v in eng_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.barh(eng_churn.index, eng_churn.values, color=colors_e, edgecolor='#1a1d24', height=0.5)
        ax.axvline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_xlabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Churn Rate by Engagement Profile', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, eng_churn.values):
            ax.text(val+0.4, bar.get_y()+bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=10, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r2:
        st.markdown('<div class="section-label">👤 Churn by Age Group</div>', unsafe_allow_html=True)
        age_churn = fdf.groupby('AgeGroup', observed=True)['Churn'].mean() * 100
        colors_a  = ['#e74c3c' if v > churn_rate else '#2ecc71' for v in age_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(age_churn.index, age_churn.values, color=colors_a, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_xlabel('Age Group', fontsize=12)
        ax.set_title('Churn Rate by Age Group', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, age_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=10, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    # ── Insights & Recommendations — full width ──
    best_eng  = eng_churn.idxmin()
    worst_eng = eng_churn.idxmax()
    worst_age = age_churn.idxmax()
    st.markdown("### 🔍 Key Insights & Recommendations")
    insight(f"'{worst_eng}' customers churn at {eng_churn.max():.1f}% vs "
            f"'{best_eng}' at {eng_churn.min():.1f}%. "
            f"The {worst_age} age group has the highest churn at {age_churn.max():.1f}%.")
    recommendation("Launch a digital re-engagement campaign for all Inactive customers. "
                   f"Assign dedicated relationship managers to {worst_age} age group "
                   "with personalised financial planning and senior-friendly digital tools.")
 
# ══════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT UTILIZATION
# ══════════════════════════════════════════════════════════
elif page == "Product Utilization":
    st.markdown('<div class="page-title">Product Utilization Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Impact of product depth on customer churn and retention</div>', unsafe_allow_html=True)
 
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Customers", f"{len(fdf):,}")
    c2.metric("📉 Churn Rate",      f"{churn_rate:.2f}%")
    c3.metric("📦 Avg Products",    f"{fdf['NumOfProducts'].mean():.2f}")
    c4.metric("💳 Credit Card %",   f"{fdf['HasCrCard'].mean()*100:.1f}%")
    st.markdown("---")
 
    col_l, col_r = st.columns(2)
 
    with col_l:
        st.markdown('<div class="section-label">📦 Churn Rate by Number of Products</div>', unsafe_allow_html=True)
        prod_churn = fdf.groupby('NumOfProducts')['Churn'].mean() * 100
        colors_p   = ['#2ecc71' if v < churn_rate else '#e74c3c' for v in prod_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(prod_churn.index.astype(str), prod_churn.values,
            color=colors_p, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_xlabel('Number of Products', fontsize=12)
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Churn Rate by Product Count', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, prod_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f'{val:.1f}%', ha='center', fontsize=12, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r:
        st.markdown('<div class="section-label">👥 Customer Count by Products</div>', unsafe_allow_html=True)
        prod_count = fdf.groupby('NumOfProducts').size()
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(prod_count.index.astype(str), prod_count.values,
            color='#3498db', edgecolor='#1a1d24', width=0.5)
        ax.set_xlabel('Number of Products', fontsize=12)
        ax.set_ylabel('Number of Customers', fontsize=12)
        ax.set_title('Customer Distribution by Product Count', color='#ffffff', fontsize=13, fontweight='bold')
        for bar, val in zip(bars, prod_count.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
                f'{val:,}', ha='center', fontsize=11, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    st.markdown("---")
    col_l2, col_r2 = st.columns(2)
 
    with col_l2:
        st.markdown('<div class="section-label">💳 Active vs Inactive Member Churn</div>', unsafe_allow_html=True)
        active_churn = fdf.groupby('IsActiveMember')['Churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(['Inactive Members','Active Members'], active_churn.values,
            color=['#e74c3c','#2ecc71'], edgecolor='#1a1d24', width=0.4)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Churn: Active vs Inactive Members', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, active_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=13, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r2:
        st.markdown('<div class="section-label">🗺️ Geography × Products Heatmap</div>', unsafe_allow_html=True)
        pivot = fdf.groupby(['Geography','NumOfProducts'])['Churn'].mean().unstack() * 100
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.5, linecolor='#0e1117', ax=ax,
            annot_kws={'size':12,'color':'white'},
            cbar_kws={'label':'Churn Rate (%)'})
        ax.set_title('Churn Rate: Geography × Products', color='#ffffff', fontsize=13, fontweight='bold')
        ax.set_xlabel('Number of Products', fontsize=12)
        ax.set_ylabel('Geography', fontsize=12)
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    # ── Insights & Recommendations — full width ──
    if 2 in prod_churn.index:
        gap = abs(active_churn.iloc[1] - active_churn.iloc[0])
        st.markdown("### 🔍 Key Insights & Recommendations")
        insight(f"2-product customers have the lowest churn at {prod_churn.get(2,0):.1f}% — the sweet spot. "
                f"Active members churn {gap:.1f} percentage points less than inactive members. "
                "3-4 product customers churn at 83-100% — a product over-bundling crisis.")
    recommendation("Move 1-product customers to 2 products as a priority cross-sell action. "
                   "Implement a 30-day inactivity flag to trigger automatic outreach via SMS or email.")
 
# ══════════════════════════════════════════════════════════
# PAGE 3 — HIGH-VALUE RISK ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "High-Value Risk Analysis":
    st.markdown('<div class="page-title">High-Value Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Identifying at-risk premium customers — high balance, zero engagement</div>', unsafe_allow_html=True)
 
    at_risk = fdf[fdf['AtRiskPremium']==1]
 
    # FIX: safe metric for empty at_risk
    if len(at_risk) == 0:
        st.info("No at-risk premium customers match the current filters.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("⚠️ At-Risk Premium",  f"{len(at_risk):,}")
        c2.metric("📉 Their Churn Rate", f"{at_risk['Churn'].mean()*100:.1f}%")
        c3.metric("💰 Avg Balance",      f"€{at_risk['Balance'].mean():,.0f}")
        c4.metric("📊 % of Total",       f"{len(at_risk)/len(fdf)*100:.1f}%")
 
    st.markdown("---")
    insight(f"At-risk premium customers (Balance > €127,644 + Inactive) number {len(at_risk):,} "
            f"and churn at {at_risk['Churn'].mean()*100:.1f}% if data exists — "
            "significantly above the overall average. These are silent churners with high financial impact.")
    recommendation("Assign a dedicated relationship manager to every at-risk premium customer. "
                   "Offer exclusive benefits: priority service, fee waivers, and personalised investment advisory.")
 
    st.markdown("---")
    col_l, col_r = st.columns(2)
 
    with col_l:
        st.markdown('<div class="section-label">💰 Balance Distribution: Churned vs Retained</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        fdf[fdf['Churn']==0]['Balance'].hist(bins=30, ax=ax, color='#2ecc71',
            alpha=0.7, label='Retained', edgecolor='#1a1d24')
        fdf[fdf['Churn']==1]['Balance'].hist(bins=30, ax=ax, color='#e74c3c',
            alpha=0.7, label='Churned', edgecolor='#1a1d24')
        ax.set_xlabel('Balance (€)', fontsize=12)
        ax.set_ylabel('Number of Customers', fontsize=12)
        ax.set_title('Balance Distribution by Churn Status', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()
        insight("Churned customers are concentrated in the mid-to-high balance range. "
                "High balance alone does NOT guarantee loyalty — engagement is the missing factor.")
 
    with col_r:
        st.markdown('<div class="section-label">💳 Churn Rate by Balance Tier</div>', unsafe_allow_html=True)
        bal_churn  = fdf.groupby('BalanceTier', observed=True)['Churn'].mean() * 100
        colors_b   = ['#e74c3c' if v > churn_rate else '#2ecc71' for v in bal_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(bal_churn.index, bal_churn.values, color=colors_b, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_xlabel('Balance Tier', fontsize=12)
        ax.set_title('Churn Rate by Balance Tier', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, bal_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=10, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    # ── Insights — full width ──
    st.markdown("### 🔍 Key Insights & Recommendations")
    insight("Churned customers are concentrated in the mid-to-high balance range. "
            "High balance alone does NOT guarantee loyalty — active engagement is the missing factor. "
            "At-risk premium customers churn at 32.2% despite being the bank's most valuable segment.")
    recommendation("Assign a dedicated relationship manager to every at-risk premium customer. "
                   "Offer exclusive benefits: priority service, fee waivers, and investment advisory.")
 
    st.markdown("---")
    st.markdown('<div class="section-label">⚠️ At-Risk Premium Customer Details</div>', unsafe_allow_html=True)
    if len(at_risk) > 0:
        st.markdown(f"Showing **{min(300,len(at_risk))}** of **{len(at_risk):,}** at-risk premium customers")
        st.dataframe(
            at_risk[['CustomerId','Geography','Gender','Age','Balance','NumOfProducts',
                     'IsActiveMember','Tenure','CreditScore','RelationshipStrengthIndex','Churn']].head(300),
            use_container_width=True
        )
        csv = at_risk.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download At-Risk Customer List", csv, "at_risk_customers.csv", "text/csv")
    else:
        st.info("No at-risk customers in current filter selection.")
 
# ══════════════════════════════════════════════════════════
# PAGE 4 — RETENTION STRENGTH
# ══════════════════════════════════════════════════════════
elif page == "Retention Strength":
    st.markdown('<div class="page-title">Retention Strength Scoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Relationship Strength Index (RSI) and retention stability across engagement tiers</div>', unsafe_allow_html=True)
 
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Customers", f"{len(fdf):,}")
    c2.metric("📉 Churn Rate",      f"{churn_rate:.2f}%")
    c3.metric("🔗 Avg RSI",         f"{fdf['RelationshipStrengthIndex'].mean():.3f}")
    c4.metric("📅 Avg Tenure",      f"{fdf['Tenure'].mean():.1f} yrs")
    st.markdown("---")
 
    insight("RSI Formula: IsActiveMember×0.4 + (NumProducts/max)×0.3 + (Tenure/max)×0.2 + HasCrCard×0.1 — "
            "scores range from 0 (no relationship) to 1 (maximum engagement). "
            "Higher RSI = lower churn probability.")
 
    st.markdown("---")
    col_l, col_r = st.columns(2)
 
    with col_l:
        st.markdown('<div class="section-label">🔗 Churn by Relationship Strength Index</div>', unsafe_allow_html=True)
        rsi_bins  = pd.cut(fdf['RelationshipStrengthIndex'], bins=5,
            labels=['Very Weak','Weak','Moderate','Strong','Very Strong'])
        rsi_churn = fdf.groupby(rsi_bins, observed=True)['Churn'].mean() * 100
        colors_r  = ['#e74c3c' if v > churn_rate else '#2ecc71' for v in rsi_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(rsi_churn.index, rsi_churn.values, color=colors_r, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_xlabel('Relationship Strength Tier', fontsize=12)
        ax.set_title('Churn by Relationship Strength Index', color='#ffffff', fontsize=13, fontweight='bold')
        ax.tick_params(axis='x', rotation=15, labelsize=10)
        ax.legend(fontsize=11)
        for bar, val in zip(bars, rsi_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=10, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r:
        st.markdown('<div class="section-label">📅 Churn Rate by Tenure</div>', unsafe_allow_html=True)
        tenure_churn = fdf.groupby('Tenure')['Churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(tenure_churn.index, tenure_churn.values,
            marker='o', color='#3498db', linewidth=2.5, markersize=7)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_xlabel('Tenure (Years)', fontsize=12)
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Churn Rate by Customer Tenure', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    # ── Insights & Recommendations — full width ──
    st.markdown("### 🔍 Key Insights & Recommendations")
    insight("Tenure does NOT strongly reduce churn — long-term customers also churn at significant rates. "
            "Years with the bank alone do not guarantee loyalty; active engagement is the key driver.")
    recommendation("Prioritise customers with Very Weak or Weak RSI scores for immediate engagement programs — "
                   "offer product upgrades, loyalty rewards, and proactive relationship manager check-ins.")
 
    st.markdown("---")
    col_l2, col_r2 = st.columns(2)
 
    with col_l2:
        st.markdown('<div class="section-label">💳 Credit Card Stickiness</div>', unsafe_allow_html=True)
        card_churn = fdf.groupby('HasCrCard')['Churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(['No Credit Card','Has Credit Card'], card_churn.values,
            color=['#e74c3c','#3498db'], edgecolor='#1a1d24', width=0.4)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_title('Credit Card Stickiness Score', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, card_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=13, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_r2:
        st.markdown('<div class="section-label">🎯 Churn Rate by Credit Score</div>', unsafe_allow_html=True)
        cs_bins   = pd.cut(fdf['CreditScore'], bins=5,
            labels=['Poor','Fair','Good','Very Good','Excellent'])
        cs_churn  = fdf.groupby(cs_bins, observed=True)['Churn'].mean() * 100
        colors_cs = ['#e74c3c' if v > churn_rate else '#2ecc71' for v in cs_churn.values]
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(cs_churn.index, cs_churn.values, color=colors_cs, edgecolor='#1a1d24', width=0.5)
        ax.axhline(churn_rate, color='#c9a84c', linestyle='--', linewidth=1.5, label=f'Avg: {churn_rate:.1f}%')
        ax.set_ylabel('Churn Rate (%)', fontsize=12)
        ax.set_xlabel('Credit Score Band', fontsize=12)
        ax.set_title('Churn Rate by Credit Score Band', color='#ffffff', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        for bar, val in zip(bars, cs_churn.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{val:.1f}%', ha='center', fontsize=10, color='#ffffff', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    # ── Insights & Recommendations — full width ──
    st.markdown("### 🔍 Key Insights & Recommendations")
    diff = abs(card_churn.iloc[1] - card_churn.iloc[0])
    insight(f"Credit card ownership reduces churn by only {diff:.1f} percentage points — a weak signal. "
            "Credit score also has minimal impact on churn. "
            "Financial strength does NOT substitute for active engagement.")
    recommendation("Do not use credit score or card ownership as retention proxies. "
                   "Focus all retention resources on customers with low RSI scores, "
                   "regardless of their financial profile.")
 
# ── FOOTER ────────────────────────────────────────────────
st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("🏦 **UNIFIED MENTOR**")
    st.caption("Your Skill, Success & Journey")
with col2:
    st.caption("Mentored by [Sai Prasad Kagne](https://www.linkedin.com/in/saiprasad-kagne/)")
with col3:
    st.caption("Created by [Lakshmi Mahitha Noudu](https://www.linkedin.com/in/lakshmi-mahitha-noudu-490160268)")
with col4:
    st.caption("Version 1.0 | Last updated: April 2026")
 