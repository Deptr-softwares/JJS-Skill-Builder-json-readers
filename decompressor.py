import streamlit as st
import base64
import zstandard as zstd

def decompress(b64_string):
  #decompress from base64 to zstandard
  try:
    padding = len(b64_string) % 4
    if padding:
      b64_string += '=' * (4 - padding)

    decompressed_data = base64.b64decode(b64_string)
    dctx = zstd.ZstdDecompressor()

    decompressed = dctx.decompress(decompressed_data)

    try:
      return decompressed.decode('utf-8')
    except UnicodeDecodeError:
      return decompressed

  except Exception as e:
    return f"Error during processing: {str(e)}"

st.title("JJS sb data decompressor")
st.write("Paste you code below to see the raw JSON data; the JSON data will be reformatted for actual readability and editability")

input_data = st.text_area("Input sb data:", height=200)

if st.button("Decompress"):
    if input_data:
        result = decompress(input_data.strip())
        st.subheader("Decompressed data:")
        st.code(result, language='json')
        
        # Add a download button for the result
        st.download_button(
            label="Download Result as Text",
            data=result,
            file_name="decompressed_output.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please enter some data first!")
