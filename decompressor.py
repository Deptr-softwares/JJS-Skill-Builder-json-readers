import streamlit as st
import base64
import zstandard as zstd
import json

def decompress(b64_string):
    # decompress from base64 to zstandard
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
        items = data if isinstance(data, list) else [data]

        for item in items:
            if isinstance(item, dict) and 'DATA' in item and isinstance(item['DATA'], str):
                try:
                    item['DATA'] = json.loads(item['DATA'])
                except json.JSONDecodeError:
                    pass
        return json.dumps(data, indent=4)
        
    except Exception as e:
        return f"Reformatting Error: {str(e)}"

def recompress(json_obj):
    import copy
    data_to_save = copy.deepcopy(json_obj)
    
    items = data_to_save if isinstance(data_to_save, list) else [data_to_save]
    for item in items:
        if isinstance(item, dict) and 'DATA' in item and isinstance(item['DATA'], dict):
            item['DATA'] = json.dumps(item['DATA'], separators=(',', ':'))
    
    final_json_str = json.dumps(data_to_save, separators=(',', ':'))
    cctx = zstd.ZstdCompressor()
    compressed_bytes = cctx.compress(final_json_str.encode('utf-8'))
    b64_output = base64.b64encode(compressed_bytes).decode('utf-8')
    return b64_output

st.title("JJS sb data reader")
st.write("Paste your code below to see the raw JSON data; the JSON data will be reformatted for actual readability and editability. You can use ctrl + f to find the branchs or tags you need to edit directly")

st.header("Decompress")
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
        
st.divider()

st.header("Recompress")
edited_json_text = st.text_area("Paste your edited JSON:", height=300)

if st.button("Recompress to JJS sb data"):
    try:
        if edited_json_text:
            edited_obj = json.loads(edited_json_text)
            new_b64 = recompress(edited_obj)
            st.success("Hope this helps :)!")
            st.code(new_b64, language='text')
            st.download_button("Download New Base64", new_b64, "compressed.txt", "text/plain")
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
