import streamlit as st
import pandas as pd
import json
import os

# 设置页面标题和图标（浏览器标签页显示）
st.set_page_config(page_title="追光食谱云记本", page_icon="📖")

# 页面主标题
st.title("📖 追光食谱云记本")
st.markdown("> *可上传、可搜索的在线食谱工具*")
st.markdown("---")

DATA_FILE = 'recipes.json'

def load_recipes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_recipes(recipes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

# 初始化数据
if 'recipes' not in st.session_state:
    st.session_state.recipes = load_recipes()
if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None

recipes = st.session_state.recipes

# ========== 左侧：添加/编辑食谱 ==========
with st.sidebar:
    is_editing = st.session_state.editing_index is not None
    
    if is_editing:
        st.header("✏️ 编辑食谱")
        recipe_to_edit = recipes[st.session_state.editing_index]
    else:
        st.header("➕ 添加新食谱")
        recipe_to_edit = {"name": "", "ingredients": "", "steps": "", "tags": ""}
    
    with st.form("add_recipe"):
        name = st.text_input("菜名*", value=recipe_to_edit["name"], placeholder="例如：番茄炒蛋")
        ingredients = st.text_area("食材*", value=recipe_to_edit["ingredients"], placeholder="番茄 2个\n鸡蛋 3个\n盐 适量")
        steps = st.text_area("步骤*", value=recipe_to_edit["steps"], placeholder="1. 番茄切块\n2. 鸡蛋打散\n3. 炒熟出锅")
        tags = st.text_input("标签（用空格分隔）", value=recipe_to_edit["tags"], placeholder="家常 快手 酸甜")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_btn = st.form_submit_button("✅ 保存" if not is_editing else "✏️ 更新")
        if is_editing:
            with col2:
                cancel_btn = st.form_submit_button("❌ 取消编辑")
        
        if submit_btn and name:
            new_recipe = {
                "name": name,
                "ingredients": ingredients,
                "steps": steps,
                "tags": tags
            }
            if is_editing:
                recipes[st.session_state.editing_index] = new_recipe
                st.success(f"✏️ {name} 已更新！")
                st.session_state.editing_index = None
            else:
                recipes.append(new_recipe)
                st.success(f"✅ {name} 已保存！")
            save_recipes(recipes)
            st.rerun()
        
        if is_editing and cancel_btn:
            st.session_state.editing_index = None
            st.rerun()

# ========== 右侧：搜索和展示 ==========
search_term = st.text_input("🔍 搜索食谱（输入菜名或食材）", placeholder="例如：番茄 或 红烧")

if search_term:
    filtered_recipes = []
    for idx, recipe in enumerate(recipes):
        if (search_term.lower() in recipe['name'].lower() or 
            search_term.lower() in recipe['ingredients'].lower()):
            filtered_recipes.append((idx, recipe))
else:
    filtered_recipes = [(idx, recipe) for idx, recipe in enumerate(recipes)]

st.caption(f"共找到 {len(filtered_recipes)} 个食谱")

# 显示食谱列表
for original_idx, recipe in filtered_recipes:
    with st.expander(f"🍽️ {recipe['name']}"):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.subheader("🥬 食材")
            st.text(recipe['ingredients'])
            st.subheader("📝 步骤")
            st.text(recipe['steps'])
            if recipe['tags']:
                st.subheader("🏷️ 标签")
                st.caption(recipe['tags'])
        
        with col2:
            if st.button("✏️ 编辑", key=f"edit_{original_idx}"):
                st.session_state.editing_index = original_idx
                st.rerun()
        
        with col3:
            if st.button("🗑️ 删除", key=f"del_{original_idx}"):
                recipes.pop(original_idx)
                save_recipes(recipes)
                if st.session_state.editing_index == original_idx:
                    st.session_state.editing_index = None
                st.rerun()

# 显示统计信息
if recipes:
    st.markdown("---")
    st.subheader("📊 小统计")
    
    all_tags = []
    for recipe in recipes:
        if recipe['tags']:
            all_tags.extend(recipe['tags'].split())
    
    if all_tags:
        tag_counts = pd.Series(all_tags).value_counts()
        st.write("热门标签：", ", ".join([f"{tag}({count})" for tag, count in tag_counts.head(5).items()]))
    
    st.caption(f"📚 一共有 {len(recipes)} 个食谱")
else:
    st.info("👋 还没有食谱，请先在左侧添加一些吧！")
