import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

from src.asr import transcribe
from src.sentiment import get_sentiment
from src.semantic import semantic_search

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Product Feedback Intelligent System", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.card { background:#1f2933; padding:16px; border-radius:14px; margin-bottom:16px; }
.meta { color:#9ca3af; font-size:13px; }
.trend { padding:12px; border-bottom:1px solid #2f3b47; }
</style>
""", unsafe_allow_html=True)

# ---------------- UTIL ----------------
def product_emoji(product):
    p = str(product).lower()
    if "phone" in p or "iphone" in p or "samsung" in p:
        return "📱"
    if "car" in p:
        return "🚗"
    if "laptop" in p or "mac" in p:
        return "💻"
    if "headphone" in p:
        return "🎧"
    return "📦"

def safe_read(path, cols):
    if not os.path.exists(path):
        return pd.DataFrame(columns=cols)
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=cols)

# ---------------- DATA ----------------
os.makedirs("data", exist_ok=True)

POSTS = "data/posts.csv"
COMMENTS = "data/comments.csv"

posts_df = safe_read(POSTS, ["post_id","name","product","feedback","sentiment","date","likes","dislikes"])
comments_df = safe_read(COMMENTS, ["post_id","name","comment","date"])

# ---------------- HEADER ----------------
st.markdown("## 🛒 Product Feedback Intelligent System")

menu = st.radio("Navigation", ["Home", "Trending"], horizontal=True)

query = st.text_input("🔎 AI Semantic Search")

if query:
    idx = semantic_search(query, posts_df["feedback"].tolist())
    posts_df = posts_df.iloc[idx]

# ---------------- HOME ----------------
if menu == "Home":
    feed_col, write_col = st.columns([3,1])
else:
    feed_col = st.container()

# ---------------- WRITE PANEL (HOME ONLY) ----------------
if menu == "Home":
    with write_col:
        st.markdown("### ✍️ Write your product feedback")

        name = st.text_input("Your name")
        product = st.text_input("Product name")
        mode = st.radio("Feedback type", ["Text","Audio"])
        text = ""

        if mode == "Text":
            text = st.text_area("Write feedback")
        else:
            audio = st.file_uploader("Upload audio", type=["wav","mp3"])
            if audio:
                with open("temp.wav","wb") as f:
                    f.write(audio.read())
                text = transcribe("temp.wav")

        if st.button("Post Feedback"):
            if name and product and text:
                sentiment = get_sentiment(text)
                posts_df.loc[len(posts_df)] = [
                    len(posts_df)+1, name, product, text,
                    sentiment, datetime.now().strftime("%Y-%m-%d %H:%M"),
                    0, 0
                ]
                posts_df.to_csv(POSTS, index=False)
                st.rerun()

# ---------------- FEED ----------------
with feed_col:
    for _, row in posts_df[::-1].iterrows():
        emoji = product_emoji(row["product"])

        st.markdown(f"""
        <div class="card">
            <h4>{emoji} {row['product']} — {row['sentiment']}</h4>
            <p>{row['feedback']}</p>
            <div class="meta">👤 {row['name']} • 🕒 {row['date']}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        if c1.button(f"👍 {row['likes']}", key=f"l{row.post_id}"):
            posts_df.loc[posts_df.post_id==row.post_id,"likes"]+=1
            posts_df.to_csv(POSTS, index=False)
            st.rerun()

        if c2.button(f"👎 {row['dislikes']}", key=f"d{row.post_id}"):
            posts_df.loc[posts_df.post_id==row.post_id,"dislikes"]+=1
            posts_df.to_csv(POSTS, index=False)
            st.rerun()

        # ---------- COMMENTS ----------
        st.markdown("**💬 Comments**")
        post_comments = comments_df[comments_df.post_id==row.post_id]

        for _, c in post_comments.iterrows():
            st.write(f"👤 **{c.name}**: {c.comment}")

        cname = st.text_input("Name", key=f"cn{row.post_id}")
        ctext = st.text_input("Comment", key=f"ct{row.post_id}")
        if st.button("Add Comment", key=f"cb{row.post_id}"):
            comments_df.loc[len(comments_df)] = [
                row.post_id, cname, ctext,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ]
            comments_df.to_csv(COMMENTS, index=False)
            st.rerun()

        # ---------- POPULAR COMMENTS ----------
        if len(post_comments) > 0:
            st.markdown("🔥 **Popular comments**")
            st.write(post_comments["comment"].head(2).tolist())

        # ---------- LIKE/DISLIKE GRAPH ----------
# if st.button("📊 View Like/Dislike Graph", key=f"g{row.post_id}"):
#     fig, ax = plt.subplots()
#     ax.bar(["Likes","Dislikes"], [row.likes, row.dislikes])
#     ax.set_title("User Reactions")
#     st.pyplot(fig)

#      st.divider()

# ---------------- TRENDING ----------------
if menu == "Trending":
    st.subheader("🔥 Trending Products")

    trend = posts_df.groupby("product").agg(
        likes=("likes","sum"),
        posts=("post_id","count"),
        users=("name", lambda x:", ".join(set(x)))
    ).sort_values(by=["likes","posts"], ascending=False)

    for p, r in trend.iterrows():
        st.markdown(f"""
        <div class="trend">
            <h4>{product_emoji(p)} {p}</h4>
            👍 Likes: {r.likes}<br>
            📝 Posts: {r.posts}<br>
            👥 Users: {r.users}
        </div>
        """, unsafe_allow_html=True)