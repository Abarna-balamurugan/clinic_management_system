'''LIST OF MODULES'''
from codecs import namereplace_errors
import streamlit as st
import pandas as pd
from importlib.machinery import SourceFileLoader
import plotly.express as px 
from streamlit_option_menu import option_menu
import plotly.graph_objects as go 

CMS = SourceFileLoader("CMS","C:/Users/Lenovo/Desktop/endsem_project/CMS.py").load_module()
df_medicine = CMS.Med_Data("C:/Users/Lenovo/Desktop/endsem_project/med.csv")
df_bandages = CMS.Med_Data("C:/Users/Lenovo/Desktop/endsem_project/bandages.csv")


def page_designs():
    st.set_page_config(page_title="SSN CMS",
        layout = "wide"
    )
    st.markdown(
        r"""
        # Analysis :bar_chart:"""
    )
    st.markdown("---")

    st.caption("Data visualisation of different types of medical equipments and medicines versus stock and the amount being consumed")

page_designs()

def bargraphs(df):
    '''BAR GRAPHS'''
    st.header("BAR GRAPH VISUALISATION")

    def types_vs_stock(df):
        '''graph between types and stock'''

        stock_df = (
            df.df.groupby(by=["Type"]).sum()[["Stock"]].sort_values(by="Stock")
        )
        bar_graph_stock = px.bar(
            stock_df, 
            x = stock_df.index,
            y = "Stock",
            title = "<b>Stock vs Types<b>",
            color_discrete_sequence = ["#0083B8"]* len(stock_df),
            template = "plotly_white",
        )

        bar_graph_stock.update_layout(
            xaxis = dict(tickmode = "linear"),
            plot_bgcolor = "rgba(0,0,0,0)",
            yaxis = (dict(showgrid=False))
        )

        return bar_graph_stock,stock_df

    def types_vs_used(df):
        '''graph between types and used'''

        bar_df_used = (
            df.df.groupby(by=["Type"]).sum()[["Used"]].sort_values(by="Used")
        )

        bar_graph_used = px.bar(
            bar_df_used,
            x = bar_df_used.index,
            y = "Used",
            title = "<b>Used vs Types <b>",
            color_discrete_sequence = ["#0083B8"]* len(bar_df_used),
            template = "plotly_white"
        )

        bar_graph_used.update_layout(
            xaxis = dict(tickmode = "linear"),
            plot_bgcolor = "rgba(0,0,0,0)",
            yaxis = (dict(showgrid=False))
        )

        return bar_graph_used,bar_df_used


    col1,col2 = st.columns(2)
    col1.plotly_chart(types_vs_stock(df)[0],use_container_width=True)
    col2.plotly_chart(types_vs_used(df)[0],use_container_width=True)


    def types_table(df):
        st.header("DATA TABULATION")
        col3,col4 = st.columns(2)
        with col3:
            st.table(types_vs_stock(df)[1])

        with col4:
            st.table(types_vs_used(df)[1])

    types_table(df)


#bargraphs(df_medicine)


def piecharts(df):
    '''PIECHARTS'''
    st.header("PIECHART VISUALISATION")

    def types_used_stock(df):
        '''nested list of each type, its stock and amount used'''
        types_l = []
        for i in df.data:
            if i[2] in types_l:
                stock += i[6]
                used += i[5]
            else:
                stock = i[6]
                used = i[5]
                types_l.append([i[2],stock,used])  #type stock used 

        types,stock,used = zip(*types_l)
        return types,stock,used

    def medicines(type):
        '''Medicines in each type'''
        name_l = []
        for i in df.data:
            if i[2] == type:
                name_l.append(i[1])

        return name_l

    def stock_piechart(df):
        pie_chart_stock = go.Figure(
            go.Pie(
                labels = list(types_used_stock(df)[0]),
                values = list(types_used_stock(df)[1]),
                hoverinfo = "label+percent",
                textinfo = "value"
            )
        )

        return pie_chart_stock 

    def used_piechart(df):
        pie_chart_used = go.Figure(
            go.Pie(
                labels = list(types_used_stock(df)[0]),
                values = list(types_used_stock(df)[2]),
                hoverinfo = "label+percent",
                textinfo = "value"
            )
        )

        return pie_chart_used



    col6,col7 = st.columns(2)

    with col6:
        st.write(" ")
        st.write("Amount of stock left")
        st.plotly_chart(stock_piechart(df),use_container_width=True)

    with col7:
        st.write(" ")
        st.write("Amount Used")
        st.plotly_chart(used_piechart(df),use_container_width=True)

    def sidebar_operations():
        '''Sidebar operations'''
        with st.sidebar:
            st.write("charts for individual medicines")
            option = st.selectbox("select type of medicine",list(types_used_stock()[0]))
            if st.button("Sort"):
                medicines_l = medicines(option)
                option2 = st.selectbox("Choose medicine",medicines_l)
                if st.button("Generate Plot"):
                    for i in df.data:
                        if i[2] == option2:
                            stock = i[6]
                            used = i[5]
                    med_pie_chart = go.Figure(
                        go.Pie(
                            values = [stock,used],
                            textinfo = "value"
                        )
                    )

                    st.plotly_chart(med_pie_chart,use_container_width=True)



def main_sidebar():
    with st.sidebar:
        st.header("PLOT")
        option = st.selectbox("Select:",["Medicines","Medical Eqipment"])

        if option == "Medicines":
            df = df_medicine

        else:
            df = df_bandages

    bargraphs(df)
    piecharts(df)
    
temp1 = pd.read_csv("C:/Users/Lenovo/Desktop/endsem_project/med.csv")
temp2 = pd.read_csv("C:/Users/Lenovo/Desktop/endsem_project/bandages.csv")

temp = pd.concat([temp1,temp2])




main_sidebar()
def type_anl():
    st.header("TYPE WISE DEEP ANALYSIS")
    s = temp[temp.Type==st.selectbox("Select Type",list(set(temp.Type)))]
   
    bar_graph_stock = px.bar(
        s, 
        x = "Name",
        y = "Stock",
        color="Name",
        hover_data=["Name","Stock","Used","DOE"],
        title = "<b>TYPEWISE SPLIT<b>",
        #color_discrete_sequence = ["#FFFFFF"],
        template = "plotly_white")
    st.table(s)
    st.plotly_chart(bar_graph_stock)

    
type_anl()









