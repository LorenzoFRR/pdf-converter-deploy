import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io
import os

st.title("Conversor de PDF - Dark Mode")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Arraste ou selecione um arquivo PDF", type="pdf")

if uploaded_file:
    # Obter o caminho original do arquivo
    input_filename = uploaded_file.name
    input_path = os.path.abspath(input_filename)  # Caminho original
    output_filename = os.path.splitext(input_filename)[0] + "_darkmode.pdf"

    # Ler o PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    output_doc = fitz.open()

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Inverter cores (modo negativo)
        inverted_img = ImageOps.invert(img.convert("RGB"))

        # Converter de volta para PDF
        img_bytes = io.BytesIO()
        inverted_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Criar nova página no PDF de saída
        new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=img_bytes)

    # Salvar na mesma pasta do arquivo original
    output_path = os.path.join(os.path.dirname(input_path), output_filename)
    output_doc.save(output_path)
    output_doc.close()
    doc.close()

    st.success(f"Arquivo salvo como: {output_path}")

    # Link para download
    with open(output_path, "rb") as f:
        st.download_button("Baixar PDF Convertido", f, file_name=output_filename, mime="application/pdf")
