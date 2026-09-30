import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="SENSEMATE",
    page_icon="👁️",
    layout="centered"
)

st.title("SENSEMATE")
st.subheader("Your Everyday AI Companion")

st.write(
    "An assistive technology concept designed "
    "to help visually impaired people understand "
    "everyday surroundings."
)

st.info("Upload an image to begin.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded image",
        use_container_width=True
    )

    st.success("Image uploaded successfully!")

    st.write(
        "Image understanding and voice assistance "
        "will be added in the next development stage."
    )

st.caption(
    "SENSEMATE | Initial prototype interface"
)
