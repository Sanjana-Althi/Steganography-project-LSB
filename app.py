import streamlit as st
import numpy as np
from PIL import Image
import io

# === Logo ===
st.markdown(
    """
    <div style='text-align: center; padding-bottom: 10px;'>
        <img src='data:image/jpeg;base64,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' height='500',width='500'/>
    </div>
    """,
    unsafe_allow_html=True
)

# === Title ===
st.title("🔐 LSB Steganography using XOR")
st.caption("Hide and retrieve secret messages securely in images.")

# === ASCII Mapping ===
d = {chr(i): i for i in range(256)}
c = {i: chr(i) for i in range(256)}

# === LSB Encode ===
def encode_message(image_array, text, key):
    x_enc = image_array.copy()
    n = m = z = kl = 0
    l = len(text)

    for i in range(l):
        char_val = d[text[i]] ^ d[key[kl]]
        for bit_pos in range(8):
            bit = (char_val >> (7 - bit_pos)) & 1
            x_enc[n, m, z] = (x_enc[n, m, z] & ~1) | bit
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m == x_enc.shape[1]:
                    n += 1
                    m = 0
        kl = (kl + 1) % len(key)
    return x_enc

# === LSB Decode ===
def decode_message(image_array, length, key):
    n = m = z = kl = 0
    decrypt = ""

    for i in range(length):
        val = 0
        for bit_pos in range(8):
            bit = image_array[n, m, z] & 1
            val = (val << 1) | bit
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m == image_array.shape[1]:
                    n += 1
                    m = 0
        orig_char = c[val ^ d[key[kl]]]
        decrypt += orig_char
        kl = (kl + 1) % len(key)
    return decrypt

# === Streamlit UI ===
uploaded_file = st.file_uploader("📁 Upload a PNG image", type=["png"])
text = st.text_input("💬 Enter secret message")
key = st.text_input("🔑 Enter encryption key", type="password")
mode = st.radio("⚙️ Choose mode", ["Encode", "Decode"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    if mode == "Encode":
        if st.button("🔐 Encode Message"):
            if text and key:
                encoded_array = encode_message(image_array, text, key)
                stego_image = Image.fromarray(encoded_array)
                st.image(stego_image, caption="📷 Stego Image")

                # Allow download
                buf = io.BytesIO()
                stego_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button("📥 Download Stego Image", byte_im, file_name="stego_image.png")
            else:
                st.warning("Please enter both a secret message and a key.")
    else:
        length = st.number_input("🔢 Length of hidden message", min_value=1, step=1)
        if st.button("🕵️ Decode Message"):
            if key:
                message = decode_message(image_array, length, key)
                st.success(f"Decoded Message: {message}")
            else:
                st.warning("Please enter the decryption key.")
