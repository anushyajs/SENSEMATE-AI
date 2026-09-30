
import streamlit as st
from PIL import Image
import io

# Optional YOLO import
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SENSEMATE",
    page_icon="👁️",
    layout="centered"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #ffffff;
    text-align: center;
}

.subtitle {
    font-size: 21px;
    color: #b8c7d9;
    text-align: center;
}

.description {
    text-align: center;
    color: #c5cbd5;
    font-size: 16px;
}

.result-box {
    background-color: #172c42;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #35a7ff;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: #888888;
    font-size: 13px;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown('<div class="main-title">SENSEMATE</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Your Everyday AI Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'An assistive technology prototype designed to help people '
    'understand everyday surroundings.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")
st.info("📷 Upload an image to begin.")


# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear photo of an everyday object."
)


# ---------------- MODEL LOADING ----------------

@st.cache_resource
def load_model():
    if not YOLO_AVAILABLE:
        return None

    return YOLO("yolov8n.pt")


# ---------------- IMAGE PROCESSING ----------------

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.success("Image uploaded successfully!")

    st.subheader("Your Image")

    st.image(
        image,
        caption="Uploaded image",
        use_container_width=True
    )

    st.write(
        f"Image dimensions: {image.width} × {image.height} pixels"
    )

    st.divider()

    st.subheader("🔍 Understand Your Surroundings")

    user_question = st.text_input(
        "What would you like to know?",
        placeholder="Example: What objects are in this picture?"
    )

    if st.button("Identify Objects", use_container_width=True):

        if not YOLO_AVAILABLE:

            st.error(
                "Object detection package is not installed. "
                "Add ultralytics to requirements.txt and redeploy."
            )

        else:

            try:
                with st.spinner("SENSEMATE is analyzing the image..."):

                    model = load_model()
                    results = model.predict(image, verbose=False)

                    detected_objects = []

                    for result in results:
                        for box in result.boxes:

                            class_id = int(box.cls[0])
                            confidence = float(box.conf[0])

                            object_name = model.names[class_id]

                            detected_objects.append({
                                "name": object_name,
                                "confidence": confidence
                            })

                st.subheader("✨ Analysis Results")

                if detected_objects:

                    st.success(
                        f"Found {len(detected_objects)} object detection(s)."
                    )

                    for item in detected_objects:

                        st.markdown(
                            f"""
                            <div class="result-box">
                                <h4>👁️ {item['name'].title()}</h4>
                                <p>Detection confidence:
                                {item['confidence'] * 100:.1f}%</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.subheader("🗣️ Voice-Friendly Description")

                    names = [
                        item["name"].title()
                        for item in detected_objects
                    ]

                    description = (
                        "SENSEMATE detected: "
                        + ", ".join(names)
                        + "."
                    )

                    st.write(description)

                    if st.button("🔊 Read Description"):

                        escaped_text = (
                            description.replace("\\", "\\\\")
                            .replace("'", "\\'")
                        )

                        st.components.v1.html(
                            f"""
                            <script>
                            const message = new SpeechSynthesisUtterance(
                                '{escaped_text}'
                            );
                            window.speechSynthesis.speak(message);
                            </script>
                            """,
                            height=0
                        )

                else:
                    st.warning(
                        "No objects were detected. "
                        "Try uploading a clearer image."
                    )

            except Exception as error:
                st.error(f"Analysis error: {error}")

    if user_question:
        st.caption(
            "Your question: " + user_question
        )

        st.info(
            "Question-based AI understanding will be integrated "
            "in the next development stage."
        )


else:

    st.markdown(
        """
        <div class="result-box">
        <h3>🌍 How SENSEMATE Works</h3>
        <p>1. Upload an image.</p>
        <p>2. Identify visible everyday objects.</p>
        <p>3. Display detected information.</p>
        <p>4. Provide a voice-friendly description.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- FOOTER ----------------

st.markdown(
    '<div class="footer">'
    'SENSEMATE | Assistive AI Prototype'
    '</div>',
    unsafe_allow_html=True
)
