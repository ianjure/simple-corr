import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import seaborn as sns
import io

im = Image.open("misc\logo.png")

# Page Configuration
st.set_page_config (
    page_title = "SimpleCorr",
    page_icon = im,
    initial_sidebar_state = "collapsed"
    )

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    </style>
    """

st.markdown(hide_menu_style, unsafe_allow_html = True)

add_logo("logo.jpg", height=300)

st.title('SimpleCorr')
st.write('A simple tool for checking correlation!')

uploaded_file = st.file_uploader("Upload your data")
index = st.checkbox("Data contains index column")

index_value = False

if index:
    index_value = True

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    if index_value == True:
        data.drop(columns=data.columns[0], axis=1, inplace=True)

    cols_list = data.columns.tolist()

    data_dict = {}

    for column in cols_list:
        if (is_numeric_dtype(data[column]) == True) & (data[column].dtypes.name != 'bool'):
            val_list = data[column].values.tolist()
            col_dic = {column:val_list}
            data_dict.update(col_dic)
    
    dataframe = pd.DataFrame.from_dict(data_dict)
    st.write(dataframe)

    my_matrix = dataframe.corr(method="spearman").round(2)

    fig = plt.figure(figsize=(10,8)) #width, height
    sns.heatmap(my_matrix, cmap="Blues", vmin=0, vmax=1,annot=True, fmt="0.2f", square=True, cbar=False)

    st.write(fig)

    fn = 'plot_simplecorr.png'
    img = io.BytesIO()
    plt.savefig(img, format='png')
 
    btn = st.download_button(
    label="Download plot as image",
    data=img,
    file_name=fn,
    mime="image/png"
    )
