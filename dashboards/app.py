import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Real-Time Contact Center Intelligence",
    layout="wide"
)

# ---------------------------------------------------
# AUTO REFRESH
# ---------------------------------------------------
st_autorefresh(interval=5000, key="refresh")

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
engine = create_engine(
    "postgresql://postgres:Harinimagesh%40123@localhost:5432/ivr_warehouse"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_sql(
    "SELECT * FROM call_records",
    engine
)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.title("Dashboard Filters")

selected_queue = st.sidebar.multiselect(
    "Select Queue",
    options=df["queue_name"].unique(),
    default=df["queue_name"].unique()
)

selected_sentiment = st.sidebar.multiselect(
    "Select Sentiment",
    options=df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

# Apply Filters
df = df[
    (df["queue_name"].isin(selected_queue)) &
    (df["sentiment"].isin(selected_sentiment))
]

# ---------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------
df["anomaly"] = df["wait_time"] > 100

critical_calls = df[df["wait_time"] > 115]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("Real-Time Contact Center Intelligence Platform")

st.markdown("""
Enterprise-grade analytics dashboard for monitoring
customer support operations, SLA breaches, sentiment,
queue distribution, and anomaly detection in real time.
""")

st.markdown("---")

# ---------------------------------------------------
# ALERTS
# ---------------------------------------------------
if len(critical_calls) > 0:
    st.error(
        f"⚠ {len(critical_calls)} Critical Calls Detected with High Wait Time"
    )
else:
    st.success("✅ System Operating Normally")

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Calls",
        len(df)
    )

with col2:
    st.metric(
        "Average Wait Time",
        f"{round(df['wait_time'].mean(), 2)} sec"
    )

with col3:
    st.metric(
        "SLA Breaches",
        int(df["sla_breach"].sum())
    )

with col4:
    st.metric(
        "Avg Call Duration",
        f"{round(df['call_duration'].mean(), 2)} sec"
    )

st.markdown("---")

# ---------------------------------------------------
# LIVE TABLE
# ---------------------------------------------------
st.subheader("📞 Live Call Records")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ---------------------------------------------------
# QUEUE ANALYTICS
# ---------------------------------------------------
st.subheader("📊 Queue Distribution")

queue_data = (
    df["queue_name"]
    .value_counts()
    .reset_index()
)

queue_data.columns = ["queue_name", "count"]

queue_chart = px.bar(
    queue_data,
    x="queue_name",
    y="count",
    color="queue_name",
    title="Calls by Queue"
)

st.plotly_chart(
    queue_chart,
    use_container_width=True
)

# ---------------------------------------------------
# SENTIMENT ANALYTICS
# ---------------------------------------------------
st.subheader("😊 Customer Sentiment Analysis")

sentiment_chart = px.pie(
    names=df["sentiment"].value_counts().index,
    values=df["sentiment"].value_counts().values,
    title="Sentiment Distribution"
)

st.plotly_chart(
    sentiment_chart,
    use_container_width=True
)

# ---------------------------------------------------
# SLA BREACH ANALYTICS
# ---------------------------------------------------
st.subheader("🚨 SLA Breach Monitoring")

sla_chart = px.pie(
    names=["No Breach", "Breach"],
    values=[
        len(df[df["sla_breach"] == False]),
        len(df[df["sla_breach"] == True])
    ],
    title="SLA Breach Status"
)

st.plotly_chart(
    sla_chart,
    use_container_width=True
)

# ---------------------------------------------------
# WAIT TIME TREND
# ---------------------------------------------------
st.subheader("📈 Wait Time Analysis")

wait_chart = px.line(
    df.head(100),
    x="id",
    y="wait_time",
    title="Wait Time Trend"
)

st.plotly_chart(
    wait_chart,
    use_container_width=True
)

# ---------------------------------------------------
# CALL DURATION ANALYTICS
# ---------------------------------------------------
st.subheader("☎ Call Duration by Queue")

duration_chart = px.box(
    df,
    x="queue_name",
    y="call_duration",
    color="queue_name",
    title="Call Duration Distribution"
)

st.plotly_chart(
    duration_chart,
    use_container_width=True
)

# ---------------------------------------------------
# AGENT PERFORMANCE
# ---------------------------------------------------
st.subheader("🏆 Top Performing Agents")

agent_perf = (
    df.groupby("agent_id")["call_duration"]
    .mean()
    .reset_index()
)

agent_chart = px.bar(
    agent_perf.head(10),
    x="agent_id",
    y="call_duration",
    title="Average Call Duration by Agent",
    color="call_duration"
)

st.plotly_chart(
    agent_chart,
    use_container_width=True
)

# ---------------------------------------------------
# ANOMALY DETECTION TABLE
# ---------------------------------------------------
st.subheader("⚠ Anomaly Detection")

anomalies = df[df["anomaly"] == True]

st.write(
    f"Detected {len(anomalies)} abnormal calls with high wait times."
)

st.dataframe(
    anomalies[
        [
            "id",
            "queue_name",
            "wait_time",
            "call_duration",
            "sentiment"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------
st.subheader("⬇ Export Analytics Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="contact_center_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# SYSTEM ARCHITECTURE
# ---------------------------------------------------
st.markdown("---")

st.subheader("🏗 System Architecture")

st.markdown("""
Kafka Producer → Kafka Broker → Kafka Consumer → PostgreSQL → Streamlit Dashboard
""")

st.markdown("""
### Features
- Real-Time Streaming Analytics
- SLA Monitoring
- Customer Sentiment Analysis
- Queue Performance Monitoring
- Interactive BI Dashboard
- Anomaly Detection
- Automated Refresh Pipeline
- Operational Intelligence Reporting
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.caption(
    "Built using Kafka, PostgreSQL, Streamlit, Plotly, Docker, SQLAlchemy, and Python"
)