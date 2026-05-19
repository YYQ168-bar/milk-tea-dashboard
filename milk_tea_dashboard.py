import streamlit as st
import plotly.graph_objects as go

# 页面标题
st.set_page_config(page_title="奶茶店财务看板", layout="wide")
st.title("🧋 奶茶店财务预测看板")

# 侧边栏：所有可调整的参数
st.sidebar.header("📊 调整假设参数")

revenue_base = st.sidebar.number_input("今年收入 (万元)", value=100, step=10)
growth_rate = st.sidebar.slider("年收入增长率", 0.0, 0.30, 0.10, 0.01)
margin = st.sidebar.slider("毛利率", 0.3, 0.8, 0.60, 0.01)
rent = st.sidebar.number_input("年房租 (万元)", value=20, step=5)
salary_base = st.sidebar.number_input("今年工资 (万元)", value=15, step=5)
salary_growth = st.sidebar.slider("工资年增长率", 0.0, 0.15, 0.05, 0.01)
tax_rate = st.sidebar.slider("所得税率", 0.0, 0.35, 0.20, 0.01)
years = st.sidebar.slider("预测年数", 1, 5, 3)

# 财务模型计算逻辑
def calculate(revenue, growth, margin, rent, salary, salary_growth, tax, years):
    results = []
    for year in range(1, years + 1):
        revenue = revenue * (1 + growth)
        gross_profit = revenue * margin
        salary = salary * (1 + salary_growth)
        ebit = gross_profit - rent - salary
        tax_amt = ebit * tax
        net_profit = ebit - tax_amt
        results.append({
            "年份": year,
            "收入": round(revenue, 1),
            "毛利": round(gross_profit, 1),
            "工资": round(salary, 1),
            "税前利润": round(ebit, 1),
            "净利润": round(net_profit, 1)
        })
    return results

# 运行模型
data = calculate(revenue_base, growth_rate, margin, rent, salary_base, salary_growth, tax_rate, years)

# 展示关键指标（卡片）
col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 第1年净利润", f"{data[0]['净利润']} 万元")
col2.metric("📊 第2年净利润", f"{data[1]['净利润']} 万元" if years >= 2 else "—")
col3.metric("🎯 第3年净利润", f"{data[2]['净利润']} 万元" if years >= 3 else "—")
final_profit = data[-1]['净利润']
initial_profit = data[0]['净利润']
growth_rate_str = f"+{((final_profit/initial_profit)-1)*100:.1f}%" if years > 1 else "—"
col4.metric("🚀 期末 vs 首年", growth_rate_str)

# 展示趋势图
st.subheader("📈 净利润趋势")
fig = go.Figure()
years_list = [d["年份"] for d in data]
profits = [d["净利润"] for d in data]
fig.add_trace(go.Scatter(x=years_list, y=profits, mode='lines+markers', name='净利润'))
fig.update_layout(yaxis_title="万元", xaxis_title="年份")
st.plotly_chart(fig, use_container_width=True)

# 展示详细数据表
st.subheader("📋 详细预测表")
st.dataframe(data)