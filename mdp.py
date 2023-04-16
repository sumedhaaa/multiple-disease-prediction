# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 15:40:27 2023

@author: Hp
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import database as db
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title='Multiple Disease Prediction' , page_icon='hospital',layout='wide')

#---hiding streamlit style------
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer{visibility:hidden;}
            header{visibility:hidden;}
            </style>
            """
            
st.markdown(hide_st_style,unsafe_allow_html=True)

#----load animation--------
def loadurl(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

lottie_pred=loadurl("https://assets8.lottiefiles.com/packages/lf20_gkgqj2yq.json")
#----log in page-------
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["fname"] for user in users]
passwords = [user["password"] for user in users]

hashed_passwords=stauth.Hasher(passwords).generate()



    
authenticator=stauth.Authenticate(names,usernames,hashed_passwords,"multiple_disease","abcdef",cookie_expiry_days=0)

name, authentication_status, username=authenticator.login("Login","main")

if authentication_status==False:
    st.error("Username/Password incorrect!")
    st.text("")
    st.text("")
    st.text("")
    st.subheader("If you dont have an account. Please Register!!!")
    if st.checkbox("Register"):
       with st.container():
            col1,col2=st.columns(2)
            with col1:
                fname=st.text_input("Enter your first name")
            with col2:
                lname=st.text_input("Enter your last name")
            with col1:
                username=st.text_input("Enter your username")
            with col1:
                email=st.text_input("Enter your email id")
            with col1:
                password=st.text_input("Enter password",type='password')
            if st.button("Submit"):
                st.success("Data Saved Successfully. Please log in now")
                db.insert(fname, lname, username, email, password,-1,-1,0)
if authentication_status==None:
    st.text("")
    st.text("")
    st.text("")
    st.subheader("If you dont have an account. Please Register!!!")
    if st.checkbox("Register"):
       with st.container():
            col1,col2=st.columns(2)
            with col1:
                fname=st.text_input("Enter your first name")
            with col2:
                lname=st.text_input("Enter your last name")
            with col1:
                username=st.text_input("Enter your username")
            with col1:
                email=st.text_input("Enter your email id")
            with col1:
                password=st.text_input("Enter password",type='password')
            if st.button("Submit"):
                st.success("Data Saved Successfully. Please log in now")
                db.insert(fname, lname, username, email, password,0,0,0)
if authentication_status:

     #loading the saved model
    #authenticator.logout("Logout", "main")
    
    
     
    diabetes_model=pickle.load(open('model/diabetes_model.sav','rb'))
    heart_disease_model=pickle.load(open('model/heart_disease_model.sav','rb'))
    parkinsons_model=pickle.load(open('model/parkinsons_model.sav','rb'))
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=['Home','Diabetes Prediction',
             'Heart Disease Prediction',
             'Parkinsons Prediction','Profile'],
            icons=['house','activity','heart','person','book'],
            )
    if (selected=='Home'):
      
        #--styling the homepage----
        st.subheader(f"Welcome {username} to Multiple Disease Prediction Website :wave:")
        col1,col2=st.columns(2)
        with col1:
            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.text("This website can predict three different diseases")
            st.text("namely: Diabetes, Heart Disease and Parkinsons.")
            
        with col2:
            st_lottie(lottie_pred,height=400,key='pred')
            
        
        
         
    if (selected=='Diabetes Prediction'):
        st.title('Diabetes Prediction using ML')
        
        col1, col2,col3=st.columns(3)
        
        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose level')
        with col3:
            BloodPressure = st.text_input('Blood Pressure Value')
        with col1:
            SkinThickness = st.text_input('Skin Thickness Value')
        with col2:
            Insulin = st.text_input('Insulin Level')
        with col3:
            BMI = st.text_input('BMI value')
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Predigree Function value')
        with col2:
            Age = st.text_input('Age of a person')
        
        
        #code for prediction
        diab_diagnosis=''
        
        #creating a button for prediction
        
        f=0;
        if st.button('Diabetes Test Result'):
            diab_prediction=diabetes_model.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])
            st.success(diab_prediction[0])
            is_diab=diab_prediction[0]
            if diab_prediction[0]==0:
                diab_diagnosis='This person does not have Diabetes'
                updates={"is_diab":0}
                db.update_user(username, updates)
            else:
                diab_diagnosis='This person has Diabetes'
                updates={"is_diab":1}
                db.update_user(username, updates)
            f=diab_prediction[0]
                
        st.success(diab_diagnosis)
        
        
        
    if (selected=='Heart Disease Prediction'):
        st.title('Heart Disease Prediction using ML')
        
        col1,col2,col3=st.columns(3)
        with col1:
            age=st.text_input('Age')
        with col2:
            sex=st.text_input('Sex')
        with col3:
            cp=st.text_input('Chest Pain Types')
        with col1:
            trestbps=st.text_input('Resting Blood Pressure')
        with col2:
            chol=st.text_input('Serum Cholestoral is mg/dL')
        with col3:
            fbs=st.text_input('Fasting Blood Sugar > 120 mg/dL')
        with col1:
            restecg=st.text_input('Resting Electrocardiography results')
        
        #code for prediction
        heart_diagnosis=''
        
        #creating a button for prediction
        
        
        if st.button('Heart Disease Test Result'):
            heart_prediction=heart_disease_model.predict([[age,sex,cp,trestbps,chol,fbs,restecg]])
            #print(diab_prediction[0])
            st.success(heart_prediction[0])
            if heart_prediction[0]==0:
                heart_diagnosis='This person does not have Heart Disease'
                updates={"is_heart":0}
                db.update_user(username, updates)
            else:
                heart_diagnosis='This person has Heart Disease'
                updates={"is_heart":0}
                db.update_user(username, updates)
                
        st.success(heart_diagnosis)
        
        
    if (selected=='Parkinsons Prediction'):
        
        st.title('Parkinsons Disease Prediction using ML')
        col1,col2,col3,col4,col5=st.columns(5)
        
        with col1:
            fo=st.text_input('MDVP:Fo(Hz)')
        with col2:
            fhi=st.text_input('MDVP:Fhi(Hz)')
        with col3:
            flo=st.text_input('MDVP:Flo(Hz)')
        with col4:
            Jitter_percent=st.text_input('MDVP:Jitter(%)')
        with col5:
            Jitter_Abs=st.text_input('MDVP:Jitter(Abs)')
        with col1:
            RAP=st.text_input('MDVP:RAP')
        with col2:
            PPQ=st.text_input('MDVP:PPQ')
        with col3:
            DDP=st.text_input('MDVP:DDP')
        with col4:
            Shimmer=st.text_input('MDVP:Shimmer')
        with col5:
            Shimmer_db=st.text_input('MDVP:Shimmer(db)')
        with col1:
            APQ3=st.text_input('Shimmer:APQ3')
        with col2:
            APQ5=st.text_input('Shimmer:APQ5')
        with col3:
            APQ=st.text_input('MDVP:APQ')
        with col4:
            DDA=st.text_input('Shimmer:DDA')
        with col5:
            NHR=st.text_input('NHR')
        with col1:
            HNR=st.text_input('HNR')
        with col2:
            RPDE=st.text_input('RPDE')
        with col3:
            DFA=st.text_input('DFA')
        with col4:
            s1=st.text_input('spread1')
        with col5:
            s2=st.text_input('spread2')
        with col1:
            d2=st.text_input('D2')
        with col2:
            PPE=st.text_input('PPE')
            
        #code for prediction
        parkinsons_diagnosis=''
        
        #creating a button for prediction
        
        
        if st.button('Parkinsons Disease Test Result'):
            parkinsons_prediction=parkinsons_model.predict([[age,sex,cp,trestbps,chol,fbs,restecg]])
            #print(diab_prediction[0])
            st.success(parkinsons_prediction[0])
            if parkinsons_prediction[0]==0:
                parkinsons_diagnosis='This person does not have Heart Disease'
                updates={"is_park":0}
                db.update_user(username, updates)
            else:
                parkinsons_diagnosis='This person has Heart Disease'
                updates={"is_park":1}
                db.update_user(username, updates)
                
        st.success(parkinsons_diagnosis)
        
    if (selected=='Profile'):
        user=db.get_user(username)
        fname=user['fname']
        lname=user['lname']
        col1,col2=st.columns(2)
        with col1:
            st.subheader(f'Name: {fname} {lname}                     ')
        with col2:
            authenticator.logout("Log out","main")
        d=user['is_diab']
        h=user['is_heart']
        p=user['is_park']
        if(d==1):
            st.text("")
            st.text("")
            st.subheader("Diabetes:")
            st.write("You have diabetes. To know more about how to keep it in control, click the link below")
            link = '[Click here](https://www.niddk.nih.gov/health-information/diabetes/overview/diet-eating-physical-activity#:~:text=Try%20to%20limit%20carbohydrates%20with,low%2Dfat%20or%20nonfat%20milk.)'
            st.markdown(link, unsafe_allow_html=True)
        elif d==-1:
            st.text("")
            st.text("")
            st.subheader("Diabetes:")
            st.write("You havent checked if you have diabetes or not. Take the diabetes test now. To know more about diabetes click below")
            link = '[Click here](https://www.cdc.gov/diabetes/basics/diabetes.html#:~:text=With%20diabetes%2C%20your%20body%20doesn,vision%20loss%2C%20and%20kidney%20disease.)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        else:
            st.text("")
            st.text("")
            st.subheader("Diabetes:")
            st.write("You dont have diabetes. Click the below link to know how to be healthy and avoid being a diabetic")
            link = '[Click here](https://www.mayoclinic.org/diseases-conditions/type-2-diabetes/in-depth/diabetes-prevention/art-20047639.)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        if(h==1):
            st.text("")
            st.text("")
            st.subheader("Heart Disease:")
            st.write("You have a heart disease. To know more about how to keep it in control, click the link below")
            link = '[Click here](https://www.betterhealth.vic.gov.au/health/conditionsandtreatments/heart-disease-and-food#:~:text=The%20Heart%20Foundation%20recommends%3A,in%20a%20heart%20healthy%20diet..)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        elif h==-1:
            st.text("")
            st.text("")
            st.subheader("Diabetes:")
            st.write("You havent checked if you have heart disease or not. Take the heart disease test now. To know more about heart disease click below")
            link = '[Click here](https://www.cdc.gov/heartdisease/about.htm#:~:text=What%20is%20heart%20disease%3F,can%20cause%20a%20heart%20attack..)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        else:
            st.text("")
            st.text("")
            st.subheader("Heart Disease:")
            st.write("You dont have heart disease. Click the below link to know how to be healthy and prevent heart disease")
            link = '[Click here](https://www.mayoclinic.org/diseases-conditions/heart-disease/in-depth/heart-disease-prevention/art-20046502.)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        if(p==1):
            st.text("")
            st.text("")
            st.subheader("Parkinsons Disease:")
            st.write("You have parkinsons disease. To know more about how to keep it in control, click the link below")
            link = '[Click here](https://www.healthline.com/health/parkinsons-disease/how-to-support)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        elif p==-1:
            st.text("")
            st.text("")
            st.subheader("Parkinsons Disease:")
            st.write("You havent checked if you have parkinsons disease or not. Take the psrkinsons disease test now. To know more about parkinsons disease click below")
            link = '[Click here](https://www.mayoclinic.org/diseases-conditions/parkinsons-disease/symptoms-causes/syc-20376055)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        else:
            st.text("")
            st.text("")
            st.subheader("Parkinsons Disease:")
            st.write("You dont have parkinsons disease. Click the below link to know how to be healthy and prevent parkinsons disease")
            link = '[Click here](https://www.umms.org/bwmc/news/2021/the-two-best-ways-to-prevent-parkinsons-disease)'
            st.markdown(link, unsafe_allow_html=True)
            st.text("")
        
        
        

        
    
        
