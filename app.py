import streamlit as st
import numpy as np
from PIL import Image

# ASCII maps
d = {chr(i): i for i in range(256)}
c = {i: chr(i) for i in range(256)}

# ---------- ENCODE ----------
def encode_image(img, text, key):
    img = np.array(img)
    h, w, _ = img.shape

    text_len = len(text)
    binary_len = format(text_len, '016b')  # store length in 16 bits

    data = binary_len
    for i, ch in enumerate(text):
        val = d[ch] ^ d[key[i % len(key)]]
        data += format(val, '08b')

    idx = 0
    for i in range(h):
        for j in range(w):
            for k in range(3):
                if idx < len(data):
                    img[i][j][k] = (img[i][j][k] & 0xFE) | int(data[idx])
                    idx += 1

    return Image.fromarray(img)

# ---------- DECODE ----------
def decode_image(img, key):
    img = np.array(img)
    h, w, _ = img.shape

    bits = ""
    for i in range(h):
        for j in range(w):
            for k in range(3):
                bits += str(img[i][j][k] & 1)

    msg_len = int(bits[:16], 2)
    bits = bits[16:]

    message = ""
    for i in range(msg_len):
        byte = bits[i*8:(i+1)*8]
        val = int(byte, 2)
        ch = c[val ^ d[key[i % len(key)]]]
        message += ch

    return message
st.set_page_config(page_title="LSB Steganography", layout="centered")

st.title("🔐 LSB Steganography using XOR")
st.caption("Hide and retrieve secret messages inside images")

tab1, tab2 = st.tabs(["🔒 Encode", "🔓 Decode"])

with tab1:
    img_file = st.file_uploader("Upload PNG Image", type=["png"])
    text = st.text_area("Enter Secret Message")
    key = st.text_input("Enter Encryption Key", type="password")

    if st.button("Encode"):
        if img_file and text and key:
            img = Image.open(img_file)
            encoded = encode_image(img, text, key)
            st.image(encoded, caption="Encoded Image")
            encoded.save("encoded.png")
            with open("encoded.png", "rb") as f:
                st.download_button("Download Image", f, "encoded.png")
        else:
            st.error("All fields are required")

with tab2:
    img_file = st.file_uploader("Upload Encoded Image", type=["png"])
    key = st.text_input("Enter Decryption Key", type="password")

    if st.button("Decode"):
        if img_file and key:
            img = Image.open(img_file)
            message = decode_image(img, key)
            st.success("Hidden Message:")
            st.code(message)
        else:
            st.error("Image and key required")


           
