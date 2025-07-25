# HR Analytics & Attrition Risk Prediction Dashboard

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-blue?logo=streamlit)](https://hr-analyticsai-in-business-9erm3kef6xxniet783cm8c.streamlit.app/)

A complete HR analytics solution built with **Pandas, Plotly, Scikit-learn**, and deployed via **Streamlit**. This project analyzes employee data to uncover workforce trends, department performance, salary structures, and predicts attrition risk using machine learning.

---

## 📊 Business Use Case

This dashboard serves corporate HR needs, supporting:

- 👨‍💼 Workforce Planning  
- 💰 Compensation & Salary Strategy  
- 🚀 Promotion Path & Talent Development  
- 🏢 Departmental Allocation  
- 🧑‍⚖️ Manager Effectiveness  
- 📊 Gender Equity and Diversity Monitoring  
- 🔮 Attrition Risk Prediction  

---

## 📂 Dataset Overview

The system integrates data from:

- `employee.csv` – Personal and hire information  
- `department.csv` – Department metadata  
- `department_employee.csv` – Historical department assignments  
- `department_manager.csv` – Managers per department  
- `salary.csv` – Historical salary data  
- `title.csv` – Job titles  
- `current_employee_snapshot.csv` – Cleaned, joined view for current employees  

---

## 📈 Key Insights

### ✅ Tenure & Retention
- Departments with the **longest average employee tenure** indicate healthy work culture.
- Departments with **short tenure** may signal high turnover.

### ✅ Salary Analysis
- **Total salary paid per department** reveals resource allocation.
- **Salary growth over time** shows overall compensation trends.
- **Top 10 highest paid employees** per department help spot outliers.

### ✅ Gender & Diversity
- **Gender distribution by department/title** highlights equity issues.
- **Title-based tenure** explores role stability across the company.

### ✅ Hiring Trends
- Visualize **employee hires per year**.

---

## 🔮 Machine Learning: Attrition Risk Prediction

We define **attrition risk** as employees with `company_tenure < 13 years`.

### 🔢 Features Used
- `salary_amount`  
- `salary_percentage_change`  
- `department_tenure`  
- `title_tenure`  
- `gender`, `title`, `dept_name` (categorical)

---

## 🤖 Model Selection & Evaluation

| Model               | AUC Score |
|--------------------|-----------|
| Logistic Regression| 0.836     |
| Random Forest      | 0.848     |
| XGBoost            | 0.852     |
| **Gradient Boosting**  | **0.855** ✅ |

> **Why Gradient Boosting?**
> - Best AUC score (0.855)
> - Handles non-linear relationships
> - Better performance than Random Forest on this dataset
> - Seamless integration with scikit-learn pipelines

We used `GradientBoostingClassifier` with:
```python
GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
```

✅ Deployed on **Streamlit Cloud**  
🔗 **Live App**: [https://hr-analyticsai-in-business-9erm3kef6xxniet783cm8c.streamlit.app/](https://hr-analyticsai-in-business-9erm3kef6xxniet783cm8c.streamlit.app/)

To deploy yourself:

1. Fork or clone this repo.
2. Ensure you have `requirements.txt` with:
    ```txt
    streamlit>=1.25
    pandas>=1.5
    scikit-learn>=1.2
    plotly>=5.10
    joblib>=1.2
    xgboost>=1.7
    ```
3. Push to GitHub and deploy via [Streamlit Cloud](https://streamlit.io/cloud).
