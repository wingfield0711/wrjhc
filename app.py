import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calc_engine import calculate_flight_plan

st.set_page_config(page_title="无人机航测航线规划器", page_icon="🚁", layout="wide")

st.title("🚁 无人机航测航线规划器")
st.caption("教学示意模型 | 科学内核：GSD与航高正反算、重叠度与外业成本联动分析")

# 三段式结构：介绍页 -> 交互主体 -> 参考来源
tab_intro, tab_main, tab_ref = st.tabs(["📖 介绍页（实验概述与推导）", "⚙️ 交互主体（规划与仿真）", "🔗 参考来源"])

# ================= 1. 介绍页 =================
with tab_intro:
    st.markdown("""
    ## 核心概念与设计意图
    - **实验目的**：本工具将航测设计延伸为 **测区范围设定 ➔ 自动反算航高 ➔ 重叠度调试 ➔ 成本与效率感知** 的完整设计链。
    
    - **推导公式**：
    1. 地面分辨率与相对航高：`GSD = (a * H) / f  ➔  H = (GSD * f) / a` （a为像元大小，f为焦距）
    2. 旁向航线间距：`Ly = Sy * (1 - py)` （Sy为地面覆盖高度，py为旁向重叠度）
    3. 航向拍照间隔时间：`Δt = [Sx * (1 - px)] / v` （Sx为地面覆盖宽度，px为航向重叠度，v为飞行速度）
    """)

# ================= 2. 交互主体 =================
with tab_main:
    col_map, col_ctrl = st.columns([1.5, 1.0])
    
    with col_ctrl:
        st.subheader("🎯 航测参数设置")
        target_gsd = st.number_input("目标 GSD (cm/px)", value=2.0, min_value=0.5, step=0.5)
        
        camera_type = st.selectbox("相机选择", ["大疆Mavic 3 Enterprise", "Phantom 4 RTK", "iPhone 主摄（通用参考）"])
        
        if camera_type == "大疆Mavic 3 Enterprise":
            focal_mm, sensor_w, sensor_h, px_w, px_h = 12.5, 17.3, 13.0, 5280, 3956
        elif camera_type == "Phantom 4 RTK":
            focal_mm, sensor_w, sensor_h, px_w, px_h = 8.8, 13.2, 8.8, 5472, 3848
        else:
            focal_mm, sensor_w, sensor_h, px_w, px_h = 6.86, 9.8, 7.3, 4000, 3000
            
        st.subheader("⚙️ 重叠度调节（滑块联动）")
        overlap_h = st.slider("航向重叠度 (%)", 50, 90, 75, 5) / 100.0
        overlap_s = st.slider("旁向重叠度 (%)", 30, 85, 60, 5) / 100.0

    with col_map:
        st.subheader("🗺️ 1. 测区范围与可视化图示")
        # 补全原文档丢失的滑块代码
        side_length_km = st.slider("设定测区边长 (km)", 0.1, 5.0, 1.0, 0.1)
        area_km2 = side_length_km ** 2
        st.info(f"当前测区面积：**{area_km2:.2f} km²** (近似正方形)")
        
        # 计算
        res = calculate_flight_plan(
            area_km2=area_km2,
            target_gsd_cm=target_gsd,
            focal_length_mm=focal_mm,
            sensor_w_mm=sensor_w,
            sensor_h_mm=sensor_h,
            pixel_w=px_w,
            pixel_h=px_h,
            overlap_heading=overlap_h,
            overlap_side=overlap_s
        )
        
        # 数据展示
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("设计航高 (H)", f"{res['flight_height_m']} m")
        m2.metric("拍照间隔时间", f"{res['photo_interval_s']} s")
        m3.metric("预估总照片数", f"{res['total_photos']} 张")
        m4.metric("预计外业耗时", f"{res['flight_time_min']} 分钟")
        
        st.warning(f"📌 **航线参数摘要**: 航线间距 `Ly = {res['dy']}m`, 航向拍照间距 `Lx = {res['dx']}m`; 共需布设 **{res['num_lines']} 条航线**, 总航程 **{res['total_distance_km']} km**.")

    st.divider()
    
    # ================= 3. 挑战任务 =================
    st.subheader("🔥 3. 挑战任务演练区 (1 km², 1 cm 分辨率)")
    if st.button("🚀 一键加载挑战任务"):
        c_res = calculate_flight_plan(1.0, 1.0, 12.5, 17.3, 13.0, 5280, 3956, 0.80, 0.70)
        st.error(f"⚠️ **1cm 分辨率挑战结果**: 航高降至 **{c_res['flight_height_m']}m** | 照片数暴增至 **{c_res['total_photos']} 张** | 耗时长达 **{c_res['flight_time_min']} 分钟**! 直观反映了精度与成本的矛盾。")

# ================= 4. 参考来源 =================
with tab_ref:
    st.markdown("""
    1. **测绘学正反算公式**：来源于《摄影测量学》（第三版），测绘出版社。
    2. **相机物理参数**：
       - 大疆 Mavic 3 Enterprise：焦距 12.5mm，CMOS 尺寸 4/3 英寸。
       - 查证日期：2026 年 10 月。
    """)