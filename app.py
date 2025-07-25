import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(layout='wide', page_title='HR Analytics Dashboard')

# --- Load Data ---
@st.cache_data

def load_data():
    dfCE = pd.read_csv("current_employee_snapshot.csv")
    dfE = pd.read_csv("employee.csv")
    dfS = pd.read_csv("salary.csv")
    return dfCE, dfE, dfS

dfCE, dfE, dfS = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("HR Analytics Dashboard")
page = st.sidebar.selectbox("Choose Analysis", [
    "Overview",
    "Attrition Prediction",
    "Department Insights",
    "Salary Insights",
    "Diversity Metrics",
    "Hiring Trends"
])

# --- Overview Page ---
if page == "Overview":
    st.title("📊 Workforce Overview")
    st.dataframe(dfCE.head())

    st.subheader("Total Employees by Department")
    dept_counts = dfCE['dept_name'].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Count']
    fig = px.bar(dept_counts, x='Department', y='Count', color='Count')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Highest Paid Employees per Department")
    top_earners = dfCE.sort_values(['dept_name', 'salary_amount'], ascending=[True, False])\
                      .groupby('dept_name').head(10).reset_index(drop=True)
    fig = px.bar(
        top_earners,
        x='salary_amount',
        y='employee_id',
        color='dept_name',
        orientation='h',
        title='Top 10 Highest Paid Employees per Department',
        hover_data=['title', 'gender', 'dept_name']
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Attrition Prediction":
    st.title("🔍 Attrition Risk Prediction (Gradient Boosting Model)")

    # Load updated model
    model = joblib.load("retention_model.pkl")

    # Input UI
    st.subheader("Enter Employee Details:")
    gender = st.selectbox("Gender", ["Male", "Female"])
    title = st.selectbox("Job Title", dfCE['title'].dropna().unique())
    dept_name = st.selectbox("Department", dfCE['dept_name'].dropna().unique())

    salary = st.number_input("Salary Amount (USD)", value=50000)
    pct_change = st.number_input("Salary % Change", value=5.0)
    dept_tenure = st.slider("Department Tenure (years)", 0.0, 25.0, 3.0)
    title_tenure = st.slider("Title Tenure (years)", 0.0, 25.0, 2.0)

    if st.button("Predict Risk"):
        input_df = pd.DataFrame([{
            'salary_amount': salary,
            'salary_percentage_change': pct_change,
            'department_tenure': dept_tenure,
            'title_tenure': title_tenure,
            'gender': gender,
            'title': title,
            'dept_name': dept_name
        }])
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]

        risk_label = '⚠️ High Risk' if prediction == 1 else '✅ Low Risk'
        st.markdown(f"### Prediction: {risk_label}")
        st.markdown(f"**Attrition Probability:** `{proba:.2%}`")

# --- Department Insights Page ---
elif page == "Department Insights":
    st.title("🏢 Departmental Tenure Trends")
    dept_tenure = dfCE.groupby('dept_name')['department_tenure'].mean().reset_index()
    fig = px.bar(dept_tenure, x='dept_name', y='department_tenure', color='department_tenure',
                 title="Average Tenure per Department", labels={'department_tenure': 'Years'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Tenure by Job Title")
    title_tenure = dfCE.groupby('title')['company_tenure'].mean().reset_index()
    fig = px.bar(title_tenure, x='company_tenure', y='title', orientation='h',
                 title='Average Company Tenure by Title', color='company_tenure')
    st.plotly_chart(fig, use_container_width=True)

# --- Salary Insights Page ---
elif page == "Salary Insights":
    st.title("💰 Salary Analytics")

    st.subheader("Salary Distribution")
    fig1 = px.histogram(dfCE, x='salary_amount', nbins=40, title="Salary Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Salary by Department")
    fig2 = px.box(dfCE, x='dept_name', y='salary_amount', title="Salary by Department", color='dept_name')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Salary by Department and Title")
    dept_title_salary = dfCE.groupby(['dept_name', 'title'])['salary_amount'].mean().reset_index()
    fig3 = px.bar(dept_title_salary, x='dept_name', y='salary_amount', color='title',
                 barmode='group', title='Avg Salary by Department and Title')
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Average Salary Growth Over Time")
    dfS['from_date'] = pd.to_datetime(dfS['from_date'])
    dfS['year'] = dfS['from_date'].dt.year
    avg_salary_per_year = dfS.groupby('year')['amount'].mean().reset_index()
    fig4 = px.line(avg_salary_per_year, x='year', y='amount', markers=True,
                  title='Average Salary Growth Over Time')
    st.plotly_chart(fig4, use_container_width=True)

# --- Diversity Metrics Page ---
elif page == "Diversity Metrics":
    st.title("🧑‍🤝‍🧑 Gender Diversity Metrics")

    st.subheader("Gender by Department")
    gender_dist = dfCE.groupby(['dept_name', 'gender']).size().reset_index(name='count')
    fig = px.bar(gender_dist, x='dept_name', y='count', color='gender', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Title by Gender")
    title_gender = dfCE.groupby(['title', 'gender']).size().reset_index(name='count')
    fig = px.bar(title_gender, x='title', y='count', color='gender', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# --- Hiring Trends Page ---
elif page == "Hiring Trends":
    st.title("📈 Hiring Trends Over Time")
    dfE['hire_date'] = pd.to_datetime(dfE['hire_date'])
    dfE['hire_year'] = dfE['hire_date'].dt.year
    hire_counts = dfE['hire_year'].value_counts().sort_index().reset_index()
    hire_counts.columns = ['hire_year', 'employee_count']
    fig = px.line(hire_counts, x='hire_year', y='employee_count', markers=True,
                  title='Employees Hired per Year')
    st.plotly_chart(fig, use_container_width=True)
