import streamlit as st
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="dRiv.IT App",
    page_icon="📍",
    layout="wide"
)

def main():
    # 2. Sidebar / Navigation (Optional)
    st.sidebar.title("Navigation")
    st.sidebar.info("Welcome to the dRiv.IT dashboard.")

    # 3. Header Section with Image
    # Adjust 'use_container_width' to False and set 'width' if you want a smaller logo
    try:
        banner_image = Image.open('image.png')
        st.image(banner_image, use_container_width=True)
    except FileNotFoundError:
        st.error("Error: 'image.png' not found. Please ensure the image is in the same directory.")

    # 4. Main Content Area
    st.title("Welcome to dRiv.IT")
    st.markdown("""
    Your central hub for navigation and regional mapping. 
    Use the tools below to explore the data.
    """)

    # 5. Example Layout (Columns)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Routes", value="1,240", delta="12")
    
    with col2:
        st.metric(label="Active Drivers", value="85", delta="-3")
        
    with col3:
        st.metric(label="Average ETA", value="14 min", delta="2 min")

    # 6. Placeholder for Map/Data
    st.subheader("Regional Overview")
    st.info("Interactive map component would be integrated here.")

if __name__ == "__main__":
    main()
