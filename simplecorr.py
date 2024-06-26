import streamlit as st
from PIL import Image
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import seaborn as sns
import io

icon = Image.open("misc/logo.png")

# Page Configuration
st.set_page_config (
    page_title = "SimpleCorr",
    page_icon = icon,
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

st.title('SimpleCorr')
st.write('A simple tool for checking correlation!')

uploaded_file = st.file_uploader("Upload your data")
index = st.checkbox("Data contains index column")

index_value = False

if index:
    index_value = True

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    list_file_name = uploaded_file.name.split(".")
    file_name = list_file_name[0].title()

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
    plt.title(file_name + " Correlation Matrix", size=15, pad=20, fontweight="bold")
    sns.heatmap(my_matrix, cmap="Blues", vmin=0, vmax=1,annot=True, fmt="0.2f", square=True, cbar=False)

    st.write(fig)

    fn = file_name + '_simplecorr.png'
    img = io.BytesIO()
    plt.savefig(img, format='png')
 
    btn = st.download_button(
    label="Download plot as image",
    data=img,
    file_name=fn,
    mime="image/png"
    )
