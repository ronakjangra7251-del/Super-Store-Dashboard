import pandas as pd
import streamlit as st
import plotly.express as px
import ingestion

from ingestion import load_data
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)    


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#             PAGE LAYOUT                #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#



st.set_page_config(page_title = "SuperStore Dashboard",layout = "wide",page_icon= ":bar_chart:")
st.title("SuperStore DashBoard",)
st.divider()



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#             DATA FETCHING               #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# read data from source and handle exception     
df=load_data()
F_df = df.copy()
F_df["years"] = pd.to_datetime(F_df["Order Date"]).dt.year
F_df["month"] = pd.to_datetime(F_df["Order Date"]).dt.month_name()

# extra variables used for different purposes
variables = ["Sales","Quantity"]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#              Filter Block                     #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
st.sidebar.title("Filters")
selection_mode = st.sidebar.radio("Select_mode",options = ["single","multi"],horizontal = True)



def Filter(df):
    global selection_mode
    
    years = st.sidebar.pills("Year",
                             options = F_df.years.unique(),
                             selection_mode = selection_mode, 
                             width = 150)
    
    with st.sidebar.expander("Location Filter"):
        region = st.multiselect("Region",
                                options = df.Region.unique())
        state = st.multiselect("State",
                              options = df.State.unique())
        
    with st.sidebar.expander("Category Filter"):
        category= st.multiselect(
                    "Category",
                    options = df.Category.unique(),
                    default= df.Category.unique())
        
        sub_category = st.multiselect("Sub_Category",
                                      options = df["Sub-Category"].unique())     
    with st.sidebar.expander("Segment Filter"):
        segment = st.multiselect("Segment",
                                 options = df.Segment.unique(),
                                 default = df.Segment.unique())
    return years,state,category,sub_category,segment,region

# get filters'

years,state,category,sub_category,segment,region= Filter(df)


if region:
    F_df = F_df[F_df.Region.isin(region)]
    
if state:
    F_df = F_df[F_df.State.isin(state)]
    
if category:
    F_df = F_df[F_df.Category.isin(category)]

if sub_category:
    F_df = F_df[F_df["Sub-Category"].isin(sub_category)]

if segment:
    F_df = F_df[F_df.Segment.isin(segment)]
if years:
    if selection_mode == "multi":
        F_df = F_df[F_df.years.isin(years)]
    else:
        F_df = F_df[F_df.years == years]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#             KPIs and Charts                     #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#


#lets create sum KPIs

orders = len(F_df)
Total_profit = F_df['Profit'].sum().round(2)
Total_Sales = F_df['Sales'].sum().round(2)
Avg_discount =F_df['Discount'].mean().round(2)



columns = st.columns(4,)
columns[0].metric("Total_Orders",orders,border = True)
columns[1].metric("Total_profit",Total_profit,border = True)
columns[2].metric("Total_sales",Total_Sales,border = True)
columns[3].metric("Average_Discount",f"{(Avg_discount*100).round(2)}%",border = True)


# creating sales trend over time and profit trend with line charts 

tab1, tab2 = st.tabs(["Sales Trend", "Profit Trend"])

with tab1:
    grp = F_df.groupby(["Category","month"])["Sales"].sum().reset_index()
    fig = px.line(grp,x = "month",y = "Sales",
                  title = "Sales Trend Category_Wise",
                  color = "Category",
                 markers =True)
    with st.container(border = True):
           st.plotly_chart(fig)
    
    
    

with tab2:
    grp = F_df.groupby(["Category","month"])["Profit"].sum().reset_index()
    fig = px.line(grp, x = "month",y= "Profit",
                  title = "Profit Trend Category_Wise",
                 color = "Category",
                 markers = True)
    with st.container(border = True):
        st.plotly_chart(fig)



#creating bar charts of sales and profit wrt to country
cols = st.columns([2,1],border = True,)

with cols[0]:
    F_df_melted = F_df.melt(id_vars = "State",
                            value_vars = ["Sales","Profit"],
                            var_name ="Metric",
                            value_name = "Value")
    fig = px.bar(F_df_melted,x="State",
                 y="Value", color = "Metric",
                 barmode = "group",
                 title = "Sales & Profit by State")
    fig.update_layout(xaxis_title = "State",yaxis_title = "Amount")
    st.plotly_chart(fig)
with cols[1]:
    Value = st.radio("Select_Value",options = variables, horizontal = True)
    data = F_df.groupby(["Category","Sub-Category"])[Value].sum().reset_index()
    fig = px.sunburst(data,path = ["Category","Sub-Category"],
                         values = Value,
                     title="Category to Sub_Categroy Distribution")
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig)


#showing dataframe if required'

cols = st.columns([2,1],border = True)
with cols[0]:
    with st.expander("Preview Data",expanded = True):
        st.dataframe(df)
        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#         download data                    #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
with cols[1]:
    st.subheader("📥 Download Data")
    
    name = st.text_input("Enter your Name: ")
    email = st.text_input("Enter your Email: ")
    
    csv = df.to_csv(index= False).encode("utf=8")
    
    if st.button("Download File"):
        if name.strip() and email.strip():
            with open("logs/logs_download.txt","a") as f:
                f.write(f"'{datetime.now()} = {name} ({email}) downlaodf data.csv\n'")
            try:
                sender_email = st.secrets["email"]["sender"]
                sender_password = st.secrets["email"]["password"]
    
                msg = MIMEMultipart()
                msg["from"] = sender_email
                msg["To"] = email
                msg["Subject"] = "SuperStore Data Download Confirmation"
                body = f"'Hi {name},\n\nThank you for downloading the SuperStore data!'"
                msg.attach(MIMEText(body,"plain"))
    
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email,sender_password)
                server.sendmail(sender_email,email,msg.as_string())
                server.quit()
    
                st.success("File download and confirmation mail sent.")
            except Exception as e:
                st.error(f"Email could not be sent: {e}")
        else:
            st.warning("Please provide both Name and Email before Downloading.")
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#                feedback section                    #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
st.divider()
st.subheader("Feedback")

feedback = st.text_area("Your Comment")
rating= st.feedback(options = "stars")

if st.button("Submit Feedback"):
    if feedback.strip():
        with open("logs/logs_feedback.txt","a") as f:
            f.write(f"'{datetime.now()} = {name} ({email})- Rating: {rating} - Feedback: {feedback}\n'")
    else:
        st.warning("Pleae enter feedback before sumitting.")
            
            



