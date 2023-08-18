import streamlit as st
import pandas as pd 
from CMS import *
from streamlit_option_menu import option_menu
df_medicine = Med_Data("C:/Users/Lenovo/Desktop/endsem_project/med.csv")
df_bandages = Med_Data("C:/Users/Lenovo/Desktop/endsem_project/bandages.csv")

def page_design():

    st.set_page_config(page_title="SSN CMS",
        page_icon=":smiley:",layout = "wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        r"""
        # Medicine Inventory 
        """
    )

    st.caption("Inventory of all the medicines/medical equipments are displayed here.")

page_design()

def navigation_bar():
    '''Horizontal navigation bar operations'''

    selected = option_menu(
        menu_title = None, 
        options = ["Medicines","Tools","Expired","Empty","Almost expired","Almost empty"],
        icons = ["thermometer","bandaid-fill","x","bucket-fill","exclamation","droplet-half"],
        default_index = 0,
        orientation = "horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#586e75", "font-family": "Permanent Marker"},
            "icon": {"color": "black", "font-size": "20px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#7d959d"},
            "nav-link-selected": {"background-color": "#7d959d"}
        }

    )

    if selected == "Medicines":

        col1, col2, col3,col4 = st.columns(4)
        col1.metric("EXPIRED",len(df_medicine.expired()[0].index))
        col2.metric("OUT OF STOCK",len(df_medicine.empty_stock()[0].index))
        col3.metric("CLOSE TO EXPIRY",len(df_medicine.reach_expiry()[0].index))
        col4.metric("ALMOST EMPTY",len(df_medicine.low_stock()[0].index))

        st.markdown("---")

        st.header("MEDICINES")
        option = st.selectbox("Order this table by:",["ID","Name","Types","Used","Stock"])
        with st.container():

            if option == "ID":
                table = df_medicine.order("ID")

            elif option == "Name":
                table = df_medicine.order("Name")

            elif option == "Types":
                table = df_medicine.order("Type")

            elif option == "Stock":
                table = df_medicine.order("Stock")

            elif option == "Used":
                table = df_medicine.order("Used")

            st.table(df_medicine.df)

            #st.dataframe(df.df.style.applymap(color_medicineleft, subset=['Left']))

    elif selected == "Tools":

        col5, col6, col7,col8 = st.columns(4)
        col5.metric("EXPIRED",len(df_bandages.expired()[0].index))
        col6.metric("OUT OF STOCK",len(df_bandages.empty_stock()[0].index))
        col7.metric("CLOSE TO EXPIRY",len(df_bandages.reach_expiry()[0].index))
        col8.metric("ALMOST EMPTY",len(df_bandages.low_stock()[0].index))

        st.markdown("---")

        st.header("BANDAGES AND INJECTIONS")
        option = st.selectbox("Order this table by:",["ID","Name","Types","Used","Stock"])
        with st.container():
            if option == "ID":
                bandage_table = df_bandages.order("ID")

            elif option == "Name":
                bandage_table = df_bandages.order("Name")

            elif option == "Types":
                bandage_table = df_bandages.order("Type")

            elif option == "Stock":
                bandage_table = df_bandages.order("Stock")

            elif option == "Used":
                bandage_table = df_bandages.order("Used")

            st.table(df_bandages.df)

        

    elif selected == "Expired":
        col9,col10 = st.columns(2)
        col9.metric("MEDICINES EXPIRED",len(df_medicine.expired()[0].index))
        col10.metric("EQUIPMENT EXPIRED",len(df_bandages.expired()[0].index))
        st.markdown("---")
        st.error("The following medicines are way past their expiry date. replace them immediately.")
        col17,col18 = st.columns(2)
        with col17:
            st.write("Medicines")
            st.table(df_medicine.expired()[0])

        with col18:
            st.write("Medical Equipment")
            st.table(df_bandages.expired()[0])

    elif selected == "Empty":
        col11,col12 = st.columns(2)
        col11.metric("MEDICINES OUT OF STOCK",len(df_medicine.empty_stock()[0].index))
        col12.metric("EQUIPMENT OUT OF STOCK",len(df_bandages.empty_stock()[0].index))
        st.markdown("---")
        
        st.error("The following medicines are out of stock. Restock immediately.")

        col19,col20 = st.columns(2)
        with col19:
            st.write("Medicines")
            st.table(df_medicine.empty_stock()[0])

        with col20:
            st.write("Medical Equipment")
            st.table(df_bandages.empty_stock()[0])

    elif selected == "Almost expired":
        col13,col14 = st.columns(2)
        col13.metric("MEDICINES CLOSE TO EXPIRY",len(df_medicine.reach_expiry()[0].index))
        col14.metric("EQUIPMENT CLOSE TO EXPIRY",len(df_bandages.reach_expiry()[0].index))
        st.markdown("---")
        st.warning("The following medicines are close to expiry")

        col21,col22 = st.columns(2)
        with col21:
            st.write("Medicines")
            st.table(df_medicine.reach_expiry()[0])

        with col22:
            st.write("Medical Equipment")
            st.table(df_bandages.reach_expiry()[0])

    else:
        col15,col16 = st.columns(2)
        col15.metric("MEDICINES ALMOST EMPTY",len(df_medicine.low_stock()[0].index))
        col16.metric("EQUIPMENT ALMOST EMPTY",len(df_bandages.low_stock()[0].index))
        st.markdown("---")
        st.warning("The following medicines are dangerously low in stock")
        col23,col24 = st.columns(2)
        with col23:
            st.write("Medicines")
            st.table(df_medicine.low_stock()[0])

        with col24:
            st.write("Medical Equipment")
            st.table(df_bandages.low_stock()[0])

    hide_menu_style = """

            <style>

            #MainMenu {visibility: hidden; }

            footer {visibility: hidden;}

            </style>

            """

    st.markdown(hide_menu_style, unsafe_allow_html=True)

navigation_bar()

def sidebar():
    '''Sidebar operations'''
    with st.sidebar:
        st.title("Medicine Prescription")

        option = st.selectbox("Select:",["Medicines","Medical Equipment"])

        if option == "Medicines":
            df = df_medicine 

        elif option == "Medical Equipment":
            df = df_bandages 

        name = st.text_input("Enter Medicine:")
        value = st.number_input("Enter No.",step=1,min_value=0)
        counter = 0 

        for i in df.data:
            if i[1] == name:
                counter += 1 
                if i[6] < value:
                    st.error("Not enough in stock.")

                else:
                    if st.button("Prescribe"):
                        if i in df.expired()[1]:
                            st.error("Medicine Expired")

                        elif i in df.reach_expiry()[1] or i in df.low_stock()[1]:

                            if i in df.reach_expiry()[1]:
                                st.warning("Medicine is close to expiry. Are you sure you want to prescribe?")

                            elif i in df.low_stock()[1]:
                                st.warning("Medicine is low in stock. Are you sure you want to prescribe?")

                            col6,col7 = st.columns(2)
                            with col6:
                                if st.checkbox("Yes"):
                                    df.update(i[0],"Stock",i[6]-value)
                                    st.success("Updated")
                            with col7:
                                if st.checkbox("No"):
                                    pass
                                    #st.info("Choose another medicine")

                        elif i in df.empty_stock()[1]:
                            st.error("Out of Stock")

                        else:
                            df.update(i[0],"Stock",i[6]-value)
                            st.success("Updated")

        if name == "":
            pass 

        elif counter == 0:
            st.error("No such medicine found.")      

sidebar()

