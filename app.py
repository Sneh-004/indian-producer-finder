import streamlit as st
import search_layer
from run_pipeline import run
from extraction import extract_cards
from ranking import rank_cards
from outreach import seller_enquiry, mailto_link

st.set_page_config(page_title="Indian Producer Finder", layout="wide")
st.title("Indian Producer Finder")
st.caption("Discover overlooked Indian producers, cooperatives, SHGs and GI-associated suppliers")

if search_layer.USE_MOCK:
    st.warning("Mock mode: showing sample data. Add a SerpApi key to .env for real results.")

with st.sidebar:
    st.header("Your need")
    product = st.text_input("Product", "handwoven saree")
    region = st.text_input("Region", "Odisha")
    quantity = st.number_input("Quantity", min_value=1, value=500)
    buyer_company = st.text_input("Your company", "Demo Retail Pvt Ltd")
    buyer_name = st.text_input("Your name", "Your Name")
    go = st.button("Find suppliers", type="primary")

if go:
    with st.spinner("Searching..."):
        out = run(product, region)
        cards, news = extract_cards(out)
        ranked, removed = rank_cards(cards)
    st.session_state["data"] = {
        "out": out, "ranked": ranked, "removed": removed,
        "news": news, "product": product,
    }

data = st.session_state.get("data")
if not data:
    st.info("Enter a product and region in the sidebar, then click Find suppliers.")
else:
    st.subheader(f"{len(data['ranked'])} suppliers found, {len(data['removed'])} aggregators removed")

    with st.expander("Searches the agent ran"):
        for item in data["out"]:
            st.write(f"**{item['step']['engine']}**: {item['step']['query']}")

    for i, c in enumerate(data["ranked"], 1):
        with st.expander(f"{i}. {c['name']}  (score {c['score']})", expanded=(i == 1)):
            st.write(f"**Type:** {c['type']}  |  **GI mention:** {'Yes' if c['gi'] else 'No'}")
            if c["address"]:
                st.write(f"**Address:** {c['address']}")
            if c["phone"]:
                st.write(f"**Phone:** {c['phone']}")
            if c["link"]:
                st.write(f"**Website:** {c['link']}")
            st.write("**Why this supplier:**")
            for r in c["reasons"]:
                st.write(f"- {r}")

            st.markdown("---")
            st.write("**Draft enquiry email** (review before sending)")
            subject, body = seller_enquiry(c, data["product"], quantity, buyer_company, buyer_name)
            to_email = st.text_input("Seller email", key=f"email_{i}",
                                     placeholder="Not found - enter manually")
            st.text_area("Email text", f"Subject: {subject}\n\n{body}", height=250, key=f"body_{i}")
            if to_email:
                st.link_button("Approve and open in email app", mailto_link(to_email, subject, body))

    if data["news"]:
        st.subheader("Recent news")
        for n in data["news"][:5]:
            st.write(f"- [{n['title']}]({n['link']})")