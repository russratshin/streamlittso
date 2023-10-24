import streamlit as st
import pandas as pd
import numpy as np
import json
import time

st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                /*
                * {
                    overflow: hidden;
                }
                [data-testid="stForm"] {
                    border: solid 1xp #ff00ff;
                    overflow: auto;
                }
                */
                .stApp {
                    border: solid 0px #ff0000;
                    height: 100vh !important;
                }
                body iframe:first-of-type {
                    height: calc(100vh - 240px) !important;
                }
                [data-testid="stVerticalBlock"] >div:nth-child(2) {
                    height: 0px !important;
                }
                [data-testid="stVerticalBlock"] >div:nth-child(3) {
                    height: 0px !important;
                }
                [data-testid="stVerticalBlock"] >div:nth-child(4) {
                    height: 0px !important;
                }
        </style>
        """, unsafe_allow_html=True)

session = get_active_session()
# conn = st.experimental_connection('snowpark')
s_query = "SELECT TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME AS TABLE_NAME FROM information_schema.tables WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY 1;"
# df = conn.query(s_query, ttl=600)
df = session.sql(s_query).collect()

with st.container():

    with st.form("my_form"):

        col1, col2 = st.columns([3, 1])

        with col1:
            st.image("https://sl.thoughtspot.com/images/ts_logo_word_400.png",width=200)

        with col2:

            col1a, col2a = st.columns([6, 1])

            with col1a:            
                my_color = st.selectbox('Select a Table', df["TABLE_NAME"], label_visibility="collapsed", index=0)

            with col2a:
                submitted = st.form_submit_button('Submit')
                if submitted:
                    iframe = st.empty()
with st.container():

    src = "https://searchlight.tseapps.com/index.php?streamlit=1&xcode=" + str(time.time())
    iframe = st.components.v1.iframe(src, height=1000, scrolling=False)

    st.components.v1.html("""
        <script>
            // alert('hi');
            parent.frames[0].postMessage('{ "state" : "spin" }',"*");
            int_spin = setInterval(function() {
                parent.frames[0].postMessage('{ "state" : "spin" }',"*");
            }, 1000);
            var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
            var eventer = window[eventMethod];
            var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
            // Listen to message from child window
            eventer(messageEvent,function(e) {
                var key = e.message ? "message" : "data";
                var data = e[key];
                var o_json = JSON.parse(e.data);
                if (o_json["state"] == "ready") {
                    clearInterval(int_spin);
                }
            },false);
        </script>
        """, height=0, width=0)


    a_color = my_color.split(".")
    my_color_1 = ""
    for my_color_0 in a_color:
        my_color_1 += "\"" + my_color_0 + "\"."
    my_color_1 = my_color_1[0:len(my_color_1) - 1]
    s_query = "SELECT * FROM " + my_color_1 + " d LIMIT 10000;"
    df_data = conn.query(s_query, ttl=600)
    df_data = df_data.fillna(value='Null')
    o_df_data = json.loads(df_data.to_json(orient='table', index=False))

    st.components.v1.html("""
        <script>
            int_hello = setInterval(function() {
                parent.frames[0].postMessage('{ "state" : "hello" }',"*");
            }, 1000);
            var o_data = """ + str(o_df_data) + """
            var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
            var eventer = window[eventMethod];
            var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
            // Listen to message from child window
            eventer(messageEvent,function(e) {
                var key = e.message ? "message" : "data";
                var data = e[key];
                var o_json = JSON.parse(e.data);
                if (o_json["state"] == "ready") {
                    clearInterval(int_hello);
                    parent.frames[0].postMessage(JSON.stringify(o_data),"*");
                    o_data = {};
                }
                //run function//
            },false);
        </script>
        """, height=0, width=0)
    
