# TODO : check for duplicate images, dropdown menu for state and city
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import pandas as pd
from  PIL import Image
import glob
import email, smtplib, ssl
from email.utils import COMMASPACE

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    #_prediction_code
import numpy as np
import cv2
# import glob
from keras.models import Sequential
from keras.models import load_model
from keras.utils import np_utils
global size
import os

# Import writer class from csv module
from csv import writer

def load_image(image_file):
    img=Image.open(image_file)
    return img

def login():
    st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
    st.markdown('<h1 class="font"><center>Welcome to India\'s Road Health Safety Management Platform<center></h1>', unsafe_allow_html=True)

    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Check if the username and password are correct
        if username == "abc" and password == "123":
            st.success("Logged in!")
            st.session_state["logged_in"] = True
        else:
            st.error("Incorrect username or password")
    
    st.image("streamlit_app_gallery-main/assets/maingif.gif",width=700)
def model(image):
    global im, result, percentage , imageName , solution, size
    # OG size = 300
    size = 300
    model = Sequential()
    model = load_model('streamlit_app_gallery-main/full_model.h5')
    
    ## load Testing data : non-pothole 
    nonPotholeTestImages = image
    test2 = [cv2.imread(img,0) for img in nonPotholeTestImages]
    # train2[train2 != np.array(None)]
    for i in range(0,len(test2)):
        test2[i] = cv2.resize(test2[i],(size,size))
    temp4 = np.asarray(test2)

    X_test = []
    #X_test.extend(temp3)
    X_test.extend(temp4)
    X_test = np.asarray(X_test)

    X_test = X_test.reshape(X_test.shape[0], size, size, 1)



    #y_test1 = np.ones([temp3.shape[0]],dtype = int)
    y_test2 = np.zeros([temp4.shape[0]],dtype = int)

    y_test = []
    #y_test.extend(y_test1)
    y_test.extend(y_test2)
    y_test = np.asarray(y_test)

    y_test = np_utils.to_categorical(y_test)


    print("")
    X_test = X_test/255
    tests = model.predict(X_test)
    for i in range(len(X_test)):
    	print(">>> Predicted %d = %s" % (i,tests[i]))
    result = tests[i]  
    percentage = float("{0:.2f}".format(result[1] * 100))
    if result[1] > 0.60:
        result="Pot Hole Detected"
    else:
        result="Pot Hole Not Detected"
    return (percentage,result) 

def send_email(usermail):
    # Set up email parameters
    to_addr = usermail
    from_addr = 'ishitagupta19@gnu.ac.in'
    subject = "Information regarding Potholes in Ahmedabad"
    body = "Please find the below attachment which has information regarding Pot holes in Ahmedabad in the form of Visual Graphics"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ishitagupta19@gnu.ac.in'
    smtp_password = 'ddtyoohrsnrcexoh'
    file_paths =glob.glob('streamlit_app_gallery-main/dashboard/*.html')
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = COMMASPACE.join([to_addr])
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            file_content = file.read()
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

# Define the main page with a sidebar menu
def main():

    #Add a logo (optional) in the sidebar
    logo = Image.open(r'streamlit_app_gallery-main/assets/1.jpg')
    profile = Image.open(r'streamlit_app_gallery-main/assets/2.jpg')

    st.markdown("""
        <style>
          .sidebar .sidebar-content {
            height: 100vh !important;
            overflow:auto;
          }
        </style>""", unsafe_allow_html=True)

    with st.sidebar:
    
        choose = option_menu("Road Health", ["Report A Pot Hole","Dashboard", "Automated Email", "Contact"],
                             icons=['camera fill','bar-chart-line-fill', 'envelope-plus-fill','person lines fill'],
                             menu_icon="app-indicator",
                             styles={
            "container": {"background-color": "black"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"color":"white","font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
        )


    logo = Image.open(r'streamlit_app_gallery-main/assets/1.jpg')
    profile = Image.open(r'streamlit_app_gallery-main/assets/2.jpg')

    if choose == "Report A Pot Hole":
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Found a Pot Hole ? <br>Be a Responsible Citizen and Report it !</p>', unsafe_allow_html=True)

        with col2:               # To display brand logo
            st.image(logo,  width=300)
        address=st.text_input("Area : ")
        zipcode=st.text_input("ZipCode : ")
        print('--------------------',zipcode)
        city=st.text_input("City : ")
        state=st.text_input("State/Province : ")

        df = pd.DataFrame(columns=['address','zipcode','city','state','percentage','image'])
                    
        #Add file uploader to allow users to upload photos
        image_file = st.file_uploader("", type=['jpg','png','jpeg'])
        if image_file is not None:
            with open(os.path.join("./streamlit_app_gallery-main/static","1.jpg"),"wb") as f: 
                f.write(image_file.getbuffer())         
            st.success("File Uploaded")
            
            # image = Image.open(uploaded_file)
            percentage,result=model(glob.glob('./streamlit_app_gallery-main/static/*.JPG'))

            col1, col2 = st.columns( [0.5, 0.5])
            with col1:
                st.markdown('<p style="text-align: center;">Image Uploaded</p>',unsafe_allow_html=True)
                st.image(glob.glob('streamlit_app_gallery-main/static/*.JPG'),width=300)
                input_image = glob.glob('streamlit_app_gallery-main/static/*.JPG')

            with col2:
                st.markdown('<p style="text-align: center;">Pot Hole Detection Results</p>',unsafe_allow_html=True)
                st.write("Precentage : "+str(percentage)+"%")
                st.write("Result : "+str(result))
                if str(result)== "Pot Hole Detected":
                    print('---------------------------\nHHHHHHHHHHHHiiiiiiiiiiiiii')
                    print(zipcode)
                    imframe = Image.open(input_image[0])
                    npframe = np.array(imframe.getdata())
                    df=pd.read_csv('test.csv')
                    print('hhhhhhhhhhhhhhhhhhhhh',df.columns.values)
                    row=[address,zipcode,city,state,percentage,npframe]
                    print(df)
                    # print('IMage : ',df['image'])
                    # for i in df['image']:
                    #     # i=np.array(i)
                    #     # print(i)
                    #     # print(type(i))
                    #     # print(type(npframe))
                    #     # comparison = i == npframe
                    #     # if comparison.all():
                    #     npframe=str(npframe)
                    #     # print('strr',str(i))
                    #     print('sttt',npframe)
                    #     print(type(npframe))
                    #     if i==npframe:
                    #         print('------------ same')
                    #         st.write('The image is already present in our dataset !')
                    #     else:
                    #         with open('test.csv', 'a') as f_object:
                    #             writer_object = writer(f_object)
                    #             writer_object.writerow(row)
                    #             f_object.close()
                    with open('streamlit_app_gallery-main/test.csv', 'a') as f_object:
                                writer_object = writer(f_object)
                                writer_object.writerow(row)
                                f_object.close()
                st.write("Thank you for being a Responsible citizen !")
                if str(result)!= "Pot Hole Not Detected":                    
                    st.write("The Report is Sent to the Government and action would be taken soon!")

    elif choose == "Dashboard":
    #Add the cover image for the cover page. Used a little trick to center the image
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Information About Pot Holes in Gujarat</p>', unsafe_allow_html=True)

        with col2:               # To display brand logo

            st.image(logo, width=130 )
        df=pd.read_csv("streamlit_app_gallery-main/test.csv")
        # city_counts=df['city'].value_counts()
        # city_names=city_counts.index.tolist()
        # city_counts=city_counts.tolist()
        # print(city_counts, type(city_counts))
        st.subheader('City-Wise and Area-Wise Analysis')
        alt.renderers.enable('png')

        city_counts = df['city'].value_counts()

        city = st.sidebar.selectbox('Select a city', city_counts.index.tolist())

        filtered_df = df[df['city'] == city]

        # Count the number of records for each state in the selected country
        area_counts = filtered_df['area'].value_counts()

        area = st.sidebar.multiselect('Select areas', area_counts.index.tolist(), default=area_counts.index.tolist())

        filtered_df = filtered_df[filtered_df['area'].isin(area)]

        filtered_state_counts = filtered_df['area'].value_counts()

        bar_chart = alt.Chart(filtered_df).mark_bar().encode(
        x='area',
        y=alt.Y('count()', axis=alt.Axis(title='Number Of Pot-Holes')),
        color=alt.Color('area')
        ).properties(
        width=600,
        height=400
        )

        st.write('City:', city)
        st.altair_chart(bar_chart, use_container_width=True)

        # Export the chart as a PNG file
        filename = f"streamlit_app_gallery-main/dashboard/{city}_{'_'.join(area)}.html"
        bar_chart.save(filename)
        st.write(f"Chart saved as {filename}")
    
    elif choose == "Automated Email":
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Want all this information on your Mail ?</p>', unsafe_allow_html=True)

        st.subheader('Don\'t worry we\'ve got this')     

        subject = "Information regarding Potholes in Ahmedabad"
        body = "Please find the below attachment which has information regarding Pot holes in Ahmedabad in the form of Visual Graphics"
        sender_email = "ishitagupta19@gnu.ac.in"
        with st.form("email form"):
            usermail=st.text_input("Please enter your Email")
            submit_res=st.form_submit_button(label='Get Email')
        if submit_res:
            send_email(usermail)
            # receiver_email = usermail
            # password = "ddtyoohrsnrcexoh"

            # message = MIMEMultipart()
            # message["From"] = sender_email
            # message["To"] = receiver_email
            # message["Subject"] = subject
            # message["Bcc"] = receiver_email  # Recommended for mass emails

            # # Add body to email
            # message.attach(MIMEText(body, "plain"))
            # file=glob.glob('dashboard/*.PDF')
            # for filename in file:
            #     print('File-----------------',filename)
            #     # filename = "generated output.docx"  # In same directory as script

            # # Open PDF file in binary mode
            #     with open(filename, "rb") as attachment:
            #         part = MIMEBase("application", "octet-stream")
            #         part.set_payload(attachment.read())

            #     encoders.encode_base64(part)

            #     # Add header as key/value pair to attachment part   
            #     part.add_header(
            #         "Content-Disposition",
            #         f"attachment; filename= {filename}",
            #         )

            #     message.attach(part)
            # text = message.as_string()

            # context = ssl.create_default_context()
            # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            #     server.login(sender_email, password)
            #     server.sendmail(sender_email, receiver_email, text)

    elif choose == "Contact":
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Contact Us ?</p>', unsafe_allow_html=True)
        with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
            #st.write('Please help us improve!')
            Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
            Email=st.text_input(label='Please Enter Your Email') #Collect user feedback
            Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
            submitted = st.form_submit_button('Submit')
            if submitted:
                st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')

# Run the application
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    main()
