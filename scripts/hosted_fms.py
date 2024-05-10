import streamlit as st
from utils import *


def main():
    """Main function for app"""
    st.set_page_config(page_title="Amazon Bedrock Playpen", layout="wide")
    css = '''
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                # padding-left: 5rem;
                # padding-right: 5rem;
            }
            #divshell {
                background-color: #f0f2f6;
                border-top-right-radius: 7px;
                border-top-left-radius: 7px;
                border-bottom-right-radius: 7px;
                border-bottom-left-radius: 7px;
            }
        </style>
    '''
    st.write(css, unsafe_allow_html=True)
    st.header("Foundation models hosted on Amazon Bedrock")
    # Generate the table of Bedrock FMs
    df, unique_providers, color_map = generate_bedrock_fm_table()
    # Selecting a provider to filter by
    col1, col2, col3, col4, col5 = st.columns(5) # Control width of st.selectbox
    with col1:
        selected_provider = st.selectbox('Select a Foundation Model Provider:', options=np.append(["ALL"], unique_providers))
    # Filter DataFrame by selected provider
    filtered_df = df if selected_provider == "ALL" else df[df['Provider'] == selected_provider]
    provider = f"{len(unique_providers)} providers" if selected_provider == "ALL" else selected_provider
    # Apply the styling
    styled_df = filtered_df.style.apply(lambda x: colorize_rows(x, color_map), axis=1)
    st.markdown(f"<b>{len(filtered_df.index)}</b> foundation model variants from <b>{provider}</b>", unsafe_allow_html=True)
    #st.markdown(html, unsafe_allow_html=True)
    st.dataframe(styled_df, hide_index=True, use_container_width=True)


# Main  
if __name__ == "__main__":
    main()