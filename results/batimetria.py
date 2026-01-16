import streamlit as st
import matplotlib.pyplot as plt

def show(results):
    st.subheader("📊 Batimetría")

    for k, v in results["stats"].items():
        st.metric(k.replace("_", " ").title(), round(v, 2))

    fig, ax = plt.subplots()
    results["dataset"].plot(ax=ax, cmap="viridis")
    st.pyplot(fig)

    return fig
