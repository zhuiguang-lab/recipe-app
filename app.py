import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="我的食谱小本本", page_icon="📖")

st.title("📖 我的食谱小本本")
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

recipes = load_recipes()

with st.sidebar:
    st.header("➕ 添加新食谱")
    with st.form("add_recipe"):
        name = st.text_input("菜名*", placeholder="例如：番茄炒蛋")
        ingredients = st.text_area("食材*", placeholder="番茄 2个\n鸡蛋 3个\n盐 适量")
        steps = st.text_area("步骤*", placeholder="1. 番茄切块\n2. 鸡蛋打散\n3. 炒熟出锅")
        tags = st.text_input("标签（用空格分隔）", placeholder="家常 快手 酸甜")
        
        submitted = st.form_submit_button("保存食谱")
        
        if submitted and name:
            new_recipe = {
                "name": name,
                "ingredients": ingredients,
                "steps": steps,
                "tags": tags
            }
            recipes.append(new_recipe)
            save_recipes(recipes)
            st.success(f"✅ {name} 已保存！")
            st.rerun()

search_term = st.text_input("🔍 搜索食谱（输入菜名或食材）", placeholder="例如：番茄 或 红烧")

if search_term:
    filtered_recipes = []
    for recipe in recipes:
        if (search_term.lower() in recipe['name'].lower() or 
            search_term.lower() in recipe['ingredients'].lower()):
            filtered_recipes.append(recipe)
else:
    filtered_recipes = recipes

st.caption(f"共找到 {len(filtered_recipes)} 个食谱")

for idx, recipe in enumerate(filtered_recipes):
    with st.expander(f"🍽️ {recipe['name']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥬 食材")
            st.text(recipe['ingredients'])
        
        with col2:
            st.subheader("📝 步骤")
            st.text(recipe['steps'])
        
        if recipe['tags']:
            st.subheader("🏷️ 标签")
            st.caption(recipe['tags'])

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