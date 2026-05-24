import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="ИАС - Контроль тарификации",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_contract_data(period):
    np.random.seed(42)
    
    contracts = [
        "Д001-АО", "Д002-АО", "Д003-АО", "Д004-АО", "Д005-АО",
        "Д006-АО", "Д007-АО", "Д008-АО", "Д009-АО", "Д010-АО"
    ]
    clients = [
        "ООО Ромашка", "ИП Иванов", "ООО Лютик", "ЗАО Техно", "ООО Строй",
        "ООО Альфа", "ИП Петров", "ООО Бета", "ЗАО Гамма", "ООО Дельта"
    ]
    
    data = []
    for i, (contract, client) in enumerate(zip(contracts, clients)):
        hour_limit = np.random.choice([5, 10, 15, 20])
        
        if period == "Март 2026":
            actual_hours = hour_limit + np.random.choice([-2, -1, 0, 1, 2, 3, 4])
        elif period == "Февраль 2026":
            actual_hours = hour_limit + np.random.choice([-1, 0, 1, 2, 3])
        else:
            actual_hours = hour_limit + np.random.choice([-2, -1, 0, 1, 2])
        
        actual_hours = max(0, actual_hours)
        
        subscription_fee = hour_limit * 50
        excess_rate = 80 if hour_limit <= 10 else 100
        excess_hours = max(0, actual_hours - hour_limit)
        excess_amount = excess_hours * excess_rate
        
        if i < 3:
            segment = "Крупный бизнес"
        elif i < 7:
            segment = "Средний бизнес"
        else:
            segment = "Малый бизнес"
        
        data.append({
            "contract_number": contract,
            "client_name": client,
            "segment": segment,
            "subscription_fee": subscription_fee,
            "hour_limit": hour_limit,
            "actual_hours": actual_hours,
            "excess_hours": excess_hours,
            "excess_rate": excess_rate,
            "excess_amount": excess_amount,
            "limit_exceeded": excess_hours > 0
        })
    
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_profitability_data():
    np.random.seed(42)
    
    clients = [
        "ООО Ромашка", "ИП Иванов", "ООО Лютик", "ЗАО Техно", "ООО Строй",
        "ООО Альфа", "ИП Петров", "ООО Бета", "ЗАО Гамма", "ООО Дельта"
    ]
    months = ["Январь 2026", "Февраль 2026", "Март 2026"]
    
    data = []
    for client in clients:
        for month in months:
            revenue = np.random.randint(500, 5000)
            cost = revenue - np.random.randint(-2000, 2000)
            cost = max(100, cost)
            margin = revenue - cost
            profitability = (margin / revenue * 100) if revenue > 0 else 0
            
            data.append({
                "client_name": client,
                "month": month,
                "revenue": revenue,
                "cost": cost,
                "margin": margin,
                "profitability": round(profitability, 1)
            })
    
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_excess_trend():
    months = ["Окт 2025", "Ноя 2025", "Дек 2025", "Янв 2026", "Фев 2026", "Мар 2026"]
    excess_hours = [45, 62, 38, 55, 70, 48]
    return pd.DataFrame({"month": months, "excess_hours": excess_hours})

@st.cache_data(ttl=3600)
def load_rate_recommendation():
    data = [
        {"contract_number": "Д001-АО", "total_hours": 120, "total_cost": 4800, "current_rate": 70, "subscription_fee": 500, "hour_limit": 5},
        {"contract_number": "Д002-АО", "total_hours": 80, "total_cost": 3200, "current_rate": 55, "subscription_fee": 300, "hour_limit": 5},
        {"contract_number": "Д003-АО", "total_hours": 60, "total_cost": 2400, "current_rate": 45, "subscription_fee": 200, "hour_limit": 5},
        {"contract_number": "Д004-АО", "total_hours": 200, "total_cost": 10000, "current_rate": 60, "subscription_fee": 800, "hour_limit": 10},
        {"contract_number": "Д005-АО", "total_hours": 40, "total_cost": 1800, "current_rate": 50, "subscription_fee": 400, "hour_limit": 5},
    ]
    return pd.DataFrame(data)

def calculate_recommended_rate(total_cost, total_hours, target_margin):
    if total_hours > 0:
        return total_cost / (total_hours * (1 - target_margin))
    return 0

def calculate_recommended_rate_excess(total_cost, total_hours, subscription_fee, hour_limit, target_margin):
    excess_hours = max(0, total_hours - hour_limit)
    if excess_hours > 0:
        required_revenue = total_cost / (1 - target_margin)
        return (required_revenue - subscription_fee) / excess_hours
    return 0

with st.sidebar:
    st.title("📊 ИАС")
    st.markdown("### Контроль тарификации")
    st.divider()
    
    page = st.radio(
        "Навигация",
        ["📋 Контроль лимитов", "💰 Анализ доходности", "🎯 Рекомендация ставки"],
        index=0
    )
    
    if st.button("🔄 Очистить кэш данных"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.caption("Информационно-аналитическая система")
    st.caption("v1.0 | Учёт и контроль тарификации")

if page == "📋 Контроль лимитов":
    st.title("📋 Контроль лимитов по договорам")
    st.caption("Оперативный контроль соблюдения договорных лимитов часов")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        period = st.selectbox(
            "📅 Отчётный период",
            ["Март 2026", "Февраль 2026", "Январь 2026"],
            index=0
        )
        show_only_exceeded = st.checkbox("🔴 Показать только договоры с превышением", value=False)
    
    df = load_contract_data(period)
    
    if show_only_exceeded:
        df_filtered = df[df["limit_exceeded"] == True]
    else:
        df_filtered = df.copy()
    
    st.markdown("### 📊 Ключевые показатели")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("Всего договоров", len(df_filtered))
    
    with kpi2:
        total_excess = df_filtered["excess_amount"].sum()
        st.metric("Сумма доплаты", f"{total_excess:,.0f} BYN")
    
    with kpi3:
        avg_hours = df_filtered["actual_hours"].mean()
        st.metric("Средние часы на договор", f"{avg_hours:.1f}")
    
    with kpi4:
        exceed_count = df_filtered["limit_exceeded"].sum()
        st.metric("Договоров с превышением", exceed_count)
    
    st.divider()
    
    st.markdown("### 📋 Сводная таблица договоров")
    
    display_df = df_filtered[[
        "contract_number", "client_name", "segment",
        "subscription_fee", "hour_limit", "actual_hours",
        "excess_hours", "excess_amount"
    ]].copy()
    
    display_df.columns = [
        "Договор", "Клиент", "Сегмент",
        "Абон. плата (BYN)", "Лимит (ч)", "Факт (ч)",
        "Превышение (ч)", "Доплата (BYN)"
    ]
    
    def highlight_exceed(row):
        if row["Превышение (ч)"] > 0:
            return ["background-color: #ffcccc"] * len(row)
        return [""] * len(row)
    
    styled_df = display_df.style.apply(highlight_exceed, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    st.markdown("### 📧 Уведомление о превышениях")
    exceed_df = df[df["limit_exceeded"] == True].copy()
    
    col_alert1, col_alert2 = st.columns([2, 1])
    
    with col_alert1:
        if not exceed_df.empty:
            st.warning(f"⚠️ Обнаружено **{len(exceed_df)}** договоров с превышением лимита!")
            exceed_list = exceed_df[["contract_number", "client_name", "excess_hours", "excess_amount"]].copy()
            exceed_list.columns = ["Договор", "Клиент", "Превышение (ч)", "Доплата (BYN)"]
            st.dataframe(exceed_list, use_container_width=True, height=150)
        else:
            st.success("✅ Превышений лимита не обнаружено")
    
    with col_alert2:
        if not exceed_df.empty:
            if st.button("📧 Отправить уведомление бухгалтеру", use_container_width=True, type="primary"):
                st.balloons()
                st.success("✅ Уведомление отправлено на почту бухгалтера!")
                with st.expander("📄 Превью отправленного письма"):
                    st.markdown("**Кому:** accountant@company.by  \n**Тема:** Уведомление о превышении лимитов по договорам")
                    st.dataframe(exceed_list, use_container_width=True)
                    st.caption("_Это демонстрационное уведомление. В реальной системе письмо уходит на SMTP-сервер._")
        else:
            st.button("📧 Отправить уведомление", disabled=True, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 🔍 Детализация по договору")
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        selected_contract = st.selectbox(
            "Выберите договор для детализации",
            df["contract_number"].tolist()
        )
    
    if selected_contract:
        contract_info = df[df["contract_number"] == selected_contract].iloc[0]
        st.info(f"**Договор:** {selected_contract} | **Клиент:** {contract_info['client_name']} | **Превышение:** {contract_info['excess_hours']} ч")
        
        requests_data = pd.DataFrame([
            {"Дата": "15.03.2026", "Вид услуги": "Консультация", "Часы": 1.5, "Биллируемость": "Да"},
            {"Дата": "16.03.2026", "Вид услуги": "Обновление", "Часы": 0.5, "Биллируемость": "Нет"},
            {"Дата": "18.03.2026", "Вид услуги": "Доработка", "Часы": 2.0, "Биллируемость": "Да"},
        ])
        st.dataframe(requests_data, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 📈 Динамика превышений по месяцам")
    trend_df = load_excess_trend()
    
    fig = px.bar(
        trend_df,
        x="month",
        y="excess_hours",
        title="Превышение лимита часов по месяцам",
        labels={"month": "Месяц", "excess_hours": "Превышение (часы)"},
        color="excess_hours",
        color_continuous_scale="Reds"
    )
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    col_exp1, col_exp2 = st.columns([1, 3])
    with col_exp1:
        if st.button("📎 Экспорт в Excel", use_container_width=True):
            st.success("✅ Отчёт экспортирован (demo)")

elif page == "💰 Анализ доходности":
    st.title("💰 Анализ доходности клиентов")
    st.caption("Оценка рентабельности и ранжирование клиентов")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        period = st.selectbox(
            "📅 Отчётный период",
            ["Март 2026", "Февраль 2026", "Январь 2026"],
            index=0
        )
    with col_f2:
        segment_filter = st.multiselect(
            "🏢 Сегмент клиентов",
            ["Крупный бизнес", "Средний бизнес", "Малый бизнес"],
            default=["Крупный бизнес", "Средний бизнес", "Малый бизнес"]
        )
    
    df = load_contract_data(period)
    df_profit = load_profitability_data()
    df_filtered = df[df["segment"].isin(segment_filter)]
    
    st.markdown("### 📊 Ключевые показатели")
    kpi_p1, kpi_p2, kpi_p3 = st.columns(3)
    
    with kpi_p1:
        total_revenue = df_filtered["subscription_fee"].sum() + df_filtered["excess_amount"].sum()
        st.metric("Общая выручка", f"{total_revenue:,.0f} BYN")
    with kpi_p2:
        avg_profitability = 18.5
        st.metric("Средняя рентабельность", f"{avg_profitability:.1f}%")
    with kpi_p3:
        active_clients = len(df_filtered["client_name"].unique())
        st.metric("Активных клиентов", active_clients)
    
    st.divider()
    
    col_top1, col_top2 = st.columns(2)
    
    period_for_chart = "Март 2026"
    df_chart = df_profit[df_profit["month"] == period_for_chart].copy()
    df_top5 = df_chart.nlargest(5, "margin")
    df_bottom5 = df_chart.nsmallest(5, "margin")
    
    with col_top1:
        st.markdown("### 🟢 Топ-5 прибыльных клиентов")
        fig_top = px.bar(
            df_top5,
            x="client_name",
            y="margin",
            title="Маржинальная прибыль",
            labels={"client_name": "Клиент", "margin": "Прибыль (BYN)"},
            color="margin",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col_top2:
        st.markdown("### 🔴 Топ-5 убыточных клиентов")
        fig_bottom = px.bar(
            df_bottom5,
            x="client_name",
            y="margin",
            title="Маржинальная прибыль",
            labels={"client_name": "Клиент", "margin": "Прибыль (BYN)"},
            color="margin",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 📋 Ранжирование клиентов по доходности")
    
    summary_df = df_filtered[[
        "client_name", "segment", "subscription_fee", "excess_amount"
    ]].copy()
    summary_df["total_revenue"] = summary_df["subscription_fee"] + summary_df["excess_amount"]
    summary_df = summary_df.rename(columns={
        "client_name": "Клиент",
        "segment": "Сегмент",
        "subscription_fee": "Абон. плата (BYN)",
        "excess_amount": "Доплата (BYN)",
        "total_revenue": "Общая выручка (BYN)"
    })
    
    np.random.seed(42)
    summary_df["Рентабельность (%)"] = np.random.uniform(-15, 45, len(summary_df)).round(1)
    
    def highlight_loss(row):
        if row["Рентабельность (%)"] < 0:
            return ["background-color: #ffcccc"] * len(row)
        return [""] * len(row)
    
    styled_summary = summary_df.style.apply(highlight_loss, axis=1)
    st.dataframe(styled_summary, use_container_width=True, height=400)
    st.caption("💰 Красным выделены клиенты с отрицательной рентабельностью")

elif page == "🎯 Рекомендация ставки":
    st.title("🎯 Рекомендация часовой ставки")
    st.caption("Расчёт экономически обоснованной ставки на основе исторических данных (формулы 1.5 и 1.6)")
    
    df_rate = load_rate_recommendation()
    
    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        selected_contract = st.selectbox(
            "Выберите договор",
            df_rate["contract_number"].tolist()
        )
    with col_sel2:
        target_margin = st.slider(
            "Целевая рентабельность (%)",
            min_value=10, max_value=50, value=30, step=5
        ) / 100
    
    if selected_contract:
        contract_data = df_rate[df_rate["contract_number"] == selected_contract].iloc[0]
        total_hours = contract_data["total_hours"]
        total_cost = contract_data["total_cost"]
        current_rate = contract_data["current_rate"]
        subscription_fee = contract_data["subscription_fee"]
        hour_limit = contract_data["hour_limit"]
        
        excess_hours = max(0, total_hours - hour_limit)
        
        recommended_rate = calculate_recommended_rate(total_cost, total_hours, target_margin)
        recommended_rate_excess = calculate_recommended_rate_excess(total_cost, total_hours, subscription_fee, hour_limit, target_margin)
        
        st.markdown("### 📊 Общая рекомендуемая ставка (на все часы)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Текущая ставка", f"{current_rate:.2f} BYN/ч")
        with col2:
            st.metric("Рекомендуемая ставка (общая)", f"{recommended_rate:.2f} BYN/ч")
        with col3:
            delta = recommended_rate - current_rate
            st.metric("Изменение", f"{delta:+.2f} BYN/ч", delta_color="normal" if delta >= 0 else "inverse")
        
        with st.expander("📐 Формула расчёта (1.5)"):
            st.latex(r"R_{rec} = \frac{S_{total}}{H_{bill} \cdot (1 - R_{target})}")
            st.markdown(f"**Подстановка:** {total_cost:.0f} / ({total_hours:.0f} × (1 - {target_margin:.2f})) = {recommended_rate:.2f}")
        
        st.markdown("---")
        st.markdown("### 📊 Расчёт для сверхлимитных часов (абонентская модель)")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Абонентская плата", f"{subscription_fee:.2f} BYN/мес")
        with col5:
            st.metric("Лимит часов", f"{hour_limit} ч/мес")
        with col6:
            st.metric("Сверхлимитные часы", f"{excess_hours} ч")
        
        if excess_hours > 0:
            st.metric("Рекомендуемая ставка (сверхлимит)", f"{recommended_rate_excess:.2f} BYN/ч")
            delta_excess = recommended_rate_excess - current_rate
            if delta_excess > 0:
                st.warning(f"⚠️ Для достижения целевой рентабельности {target_margin*100:.0f}% сверхлимитную ставку рекомендуется повысить с {current_rate:.2f} до {recommended_rate_excess:.2f} BYN/ч (+{delta_excess:.2f} BYN/ч).")
            elif delta_excess < 0:
                st.success(f"✅ Текущая сверхлимитная ставка обеспечивает рентабельность выше {target_margin*100:.0f}%. Можно рассмотреть её снижение на {abs(delta_excess):.2f} BYN/ч.")
            else:
                st.info("Текущая ставка оптимальна.")
            
            with st.expander("📐 Формула расчёта для сверхлимитных часов (1.6)"):
                st.latex(r"R_{rec}^{excess} = \frac{ \frac{S_{total}}{1 - R_{target}} - A }{ \max(0, H_{bill} - L) }")
                st.markdown(f"**Подстановка:** ({total_cost:.0f} / (1 - {target_margin:.2f}) - {subscription_fee:.0f}) / {excess_hours} = {recommended_rate_excess:.2f}")
        else:
            st.info("Сверхлимитные часы отсутствуют (фактические часы не превышают лимит). Расчёт для сверхлимитной части не производится.")
        
        if st.button("📎 Экспорт результатов в Excel", use_container_width=True):
            st.success("✅ Результат экспортирован (demo)")
    
    st.caption("Расчёт выполнен на основе агрегированных данных за последние 12 месяцев.")