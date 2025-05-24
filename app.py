import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

def get_dominant_colors(image, num_colors=5):
    """
    Ekstrak warna dominan dari sebuah gambar menggunakan K-Means.

    Args:
        image (numpy.array): Gambar dalam format OpenCV (BGR).
        num_colors (int): Jumlah warna dominan yang ingin diekstrak.

    Returns:
        list: Daftar warna dominan dalam format RGB.
    """
    # Mengubah ukuran gambar untuk mempercepat pemrosesan
    # (Opsional, tergantung ukuran gambar)
    image_resized = cv2.resize(image, (150, 150), interpolation=cv2.INTER_AREA)
    
    # Mengubah gambar dari BGR ke RGB (karena Streamlit dan K-Means lebih umum dengan RGB)
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    # Reshape gambar menjadi daftar piksel
    pixels = image_rgb.reshape(-1, 3)

    # Terapkan K-Means clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=0, n_init=10)
    kmeans.fit(pixels)

    # Dapatkan pusat cluster (warna dominan)
    dominant_colors = kmeans.cluster_centers_

    # Konversi pusat cluster ke integer (RGB)
    dominant_colors = dominant_colors.astype(int)

    return dominant_colors

def rgb_to_hex(rgb):
    """Konversi tuple RGB ke string Hex."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

st.set_page_config(
    page_title="Color Picker dari Gambar",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🎨 Color Picker dari Gambar")
st.markdown("Unggah sebuah gambar dan kami akan mengekstrak 5 warna paling dominan untuk Anda!")

uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Tampilkan gambar yang diunggah
    st.image(uploaded_file, caption="Gambar yang Diunggah", use_column_width=True)

    # Konversi Streamlit FileUploader ke format yang bisa dibaca OpenCV/PIL
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1) # Membaca gambar dalam format BGR (OpenCV default)

    # Ekstrak warna dominan
    dominant_colors = get_dominant_colors(image, num_colors=5)

    st.subheader("Palet Warna Dominan:")
    
    # Buat container untuk palet warna
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, color_rgb in enumerate(dominant_colors):
        hex_code = rgb_to_hex(color_rgb)
        
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    height: 100px;
                    background-color: {hex_code};
                    border-radius: 10px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                ">
                </div>
                <p style="text-align: center; font-weight: bold; margin-top: 10px;">{hex_code}</p>
                <p style="text-align: center; font-size: 0.9em;">RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})</p>
                """, 
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.write("Dibuat dengan ❤️ dan Streamlit.")