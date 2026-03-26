# app.py
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="企业法人关系识别",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 企业-法人关系识别智能体")
st.markdown("输入公司名或法人姓名，自动判断工商关联关系")

# 工商信息查询（公开接口）
def query_entity(keyword):
    try:
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php"
        params = {
            "query": keyword,
            "resource_id": 6871
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]
    except Exception as e:
        return None
    return None

# 关系判断
def analyze_relation(name_a, info_a, name_b, info_b):
    result = {
        "是否有关联": "否",
        "关系类型": "无",
        "关联详情": "未查询到关联信息",
        "可信度": "中"
    }

    a_str = json.dumps(info_a, ensure_ascii=False)
    b_str = json.dumps(info_b, ensure_ascii=False)

    if name_b in a_str or name_a in b_str:
        result["是否有关联"] = "是"
        if "法人" in a_str or "法人" in b_str:
            result["关系类型"] = "法定代表人"
        elif "股东" in a_str or "股东" in b_str:
            result["关系类型"] = "股东"
        else:
            result["关系类型"] = "工商关联"
        result["关联详情"] = f"{name_a} 与 {name_b} 存在工商登记关联"
        result["可信度"] = "高"
    return result

# 界面
col1, col2 = st.columns(2)
with col1:
    ent1 = st.text_input("名称1", placeholder="公司/法人")
with col2:
    ent2 = st.text_input("名称2", placeholder="公司/法人")

if st.button("🔍 识别关系"):
    if not ent1 or not ent2:
        st.warning("请输入两个名称")
    else:
        with st.spinner("正在查询..."):
            info1 = query_entity(ent1)
            info2 = query_entity(ent2)
            res = analyze_relation(ent1, info1, ent2, info2)

            st.success("查询完成")
            st.json(res)

            with st.expander("查看原始信息"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(ent1)
                    st.json(info1)
                with c2:
                    st.write(ent2)
                    st.json(info2)