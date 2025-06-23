import streamlit as st
import numpy as np
from PIL import Image
import io

# === Logo ===
st.markdown(
    """
    <div style='text-align: center; padding-bottom: 10px;'>
        <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSF_W4m27oeZ-CdXD8gKYN5-86Q7bIzRt-QWqKYv6BsLXXwir-YvhUkyKw&s' height='300' width='500'/>
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
            
