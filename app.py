
import streamlit as st
from PIL import Image
from ultralytics import YOLO

st.set_page_config(
    page_title="SENSEMATE",
    page_icon="👁️",
    layout="centered"
)

st.title("👁️ SENSEMATE")
st.subheader("Your Everyday AI Companion")

st.write(
    "Upload a photo and SENSEMATE will identify "
    "the objects it can recognize."
)

@st.cache_resource
def load_model():
    return YOLO("yolo26n.pt")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Your uploaded image",
             use_container_width=True)

    if st.button("🔍 Identify Objects"):

        with st.spinner("SENSEMATE is analyzing the image..."):

            try:
                model = load_model()
                results = model.predict(image, conf=0.25)

                result = results[0]
                detected = []

                for box in result.boxes:
                    class_id = int(box.cls[0])
                    name = result.names[class_id]
                    confidence = float(box.conf[0]) * 100

                    detected.append((name, confidence))

                if detected:
                    st.success("Objects identified!")

                    st.subheader("What I can see:")

                    for name, confidence in detected:
                        st.write(
                            f"👁️ {name.title()} "
                            f"— {confidence:.1f}% model confidence"
                        )

                    annotated = result.plot()[:, :, ::-1]

                    st.image(
                        annotated,
                        caption="Detected objects",
                        use_container_width=True
                    )

                    st.info(
                        "This is an AI prediction, not a guarantee "
                        "that every object has been identified correctly."
                    )

                else:
                    st.warning(
                        "I could not identify an object clearly. "
                        "Try another image."
                    )

            except Exception as e:
                st.error(f"Error loading or running the model: {e}")

st.divider()

st.caption("SENSEMATE | AI-assisted everyday understanding")
