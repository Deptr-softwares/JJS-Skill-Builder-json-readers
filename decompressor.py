import streamlit as st
import base64
import zstandard as zstd
import json

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

def reformat(raw_json_string):
  try:
    data = json.loads(raw_json_string)
    properties = data if isinstance(data, list) else [data]

    for property in properties:
      if 'DATA' in property and isinstance(property['DATA'], str):
        try:
          property['DATA'] = json.loads(property['DATA'])
        except json.JSONDecodeError:
          pass
        return json.dumps(data, indent=4)
  except Exception as e:
    return f"Reformatting Error: {str(e)}"

st.title("JJS sb data decompressor")
st.write("Paste you code below to see the raw JSON data; the JSON data will be reformatted for actual readability and editability")

input_data = st.text_area("Input sb data:", height=200)

if st.button("Decompress"):
  if input_data:
    raw_json = decompress(input_data)
    formatted_json = reformat(raw_json)
        
    st.subheader("Results:")  
    tab1, tab2 = st.tabs(["Raw JSON", "Readable JSON"])
        
    with tab1:
      st.code(raw_json, language='json')
      st.download_button("Download raw text", raw_json, "raw_data.txt", "text/plain")
            
    with tab2:
      st.code(formatted_json, language='json')
      st.download_button("Download formatted text", formatted_json, "formatted_data.txt", "text/plain")
  else:
    st.warning("Enter some data first folks")
