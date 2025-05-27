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
st.markdown("Unggah sebuah gambar dan kami akan mengekstrak 5 warna paling dominan untuk Anda! **Klik pada tombol warna untuk menyalin kodenya.**")

uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Tampilkan gambar yang diunggah
    st.image(uploaded_file, caption="Gambar yang Diunggah", use_column_width=True)

    # Konversi Streamlit FileUploader ke format yang bisa dibaca OpenCV/PIL
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Ekstrak warna dominan
    dominant_colors = get_dominant_colors(image, num_colors=5)

    st.subheader("Palet Warna Dominan:")
    
    # JavaScript untuk menyalin ke clipboard dan menampilkan notifikasi
    st.markdown("""
        <script>
        function copyToClipboard(text, elementId) {
            navigator.clipboard.writeText(text).then(function() {
                const element = document.getElementById(elementId);
                const originalText = element.innerHTML;
                element.innerHTML = 'Copied!';
                setTimeout(() => {
                    element.innerHTML = originalText;
                }, 1000); // Kembali ke teks asli setelah 1 detik
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        }
        </script>
    """, unsafe_allow_html=True)

    # Buat container untuk palet warna
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, color_rgb in enumerate(dominant_colors):
        hex_code = rgb_to_hex(color_rgb)
        rgb_code = f"RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"
        
        # ID unik untuk setiap elemen yang bisa disalin agar notifikasi berfungsi
        hex_id = f"hex-code-{i}"
        rgb_id = f"rgb-code-{i}"

        with cols[i]:
            st.markdown(
                f"""
                <button 
                    style="
                        width: 100%;
                        height: 120px; /* Sedikit lebih tinggi agar teks bisa masuk */
                        background-color: {hex_code};
                        border: 2px solid {hex_code}; /* Border agar terlihat seperti tombol */
                        border-radius: 10px;
                        display: flex;
                        flex-direction: column; /* Tata letak vertikal untuk teks */
                        justify-content: center;
                        align-items: center;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                        cursor: pointer;
                        transition: all 0.2s ease-in-out; /* Efek transisi untuk hover */
                        color: {'#FFFFFF' if sum(color_rgb) < 382.5 else '#000000'}; /* Warna teks otomatis kontras */
                        font-family: 'Arial', sans-serif;
                        font-size: 1em;
                        font-weight: bold;
                        padding: 5px; /* Padding di dalam tombol */
                    "
                    onmouseover="this.style.transform='scale(1.03)'" /* Efek hover */
                    onmouseout="this.style.transform='scale(1)'" /* Efek hover kembali */
                    onclick="copyToClipboard('{hex_code}', '{hex_id}')"
                    title="Klik untuk menyalin kode Hex"
                >
                    <span id="{hex_id}" style="margin-bottom: 5px;">{hex_code}</span>
                    <span id="{rgb_id}" style="font-size: 0.8em; font-weight: normal;" 
                          onclick="event.stopPropagation(); copyToClipboard('{rgb_code}', '{rgb_id}');"
                          title="Klik untuk menyalin kode RGB"
                    >{rgb_code}</span>
                </button>
                """, 
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.write("Dibuat dengan ❤️ dan Streamlit.")