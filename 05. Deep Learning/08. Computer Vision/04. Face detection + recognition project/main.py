import streamlit as st
import face_recognition
import pymysql
import pickle
import autoattend_functions
import datetime
st.title('AutoAttend: Automatic Attendence Marking System')
if 'cursor' not in st.session_state:
    with open('face_vector.pkl','rb') as obj1:
        st.session_state['data']=pickle.load(obj1)
    st.session_state['connector']=pymysql.connect(host='localhost',
                                                  user='root',
                                                  password='12345',
                                                  database='ml_feb_mar',
                                                  autocommit=True)
    st.session_state['cursor']=st.session_state['connector'].cursor()
d=datetime.datetime.now().date()
t=str(datetime.datetime.now().time()).split('.')[0]
autoattend_functions.create_table(d,st.session_state['cursor'],'ml_feb_mar')

frame=st.camera_input('AutoAttend')
c1,c2,c3=st.columns([3,3,5])
with c1:
    button=st.button('Mark Attendence')
with c2:
    show_students=st.button("Today's Attendence")
    show_all_students=st.button("Show all students")
    if show_all_students:
        for i in st.session_state['data']:
            st.write(i)

with c3:
    name1=st.text_input('Enter your name: ')
    addface=st.button('Add face')
    deleteFace=st.button("Remove person")
    if deleteFace and name1:
        data=st.session_state['data']
        if name1 in data:
            del data[name1]
            with open('face_vector.pkl','wb') as obj1:
                pickle.dump(data,obj1)
                st.write(f"Face of {name1} removed from the database.")
        else:
            st.warning("No such person exists in the database.")

download_button = st.button("Download Today's Attendance")

if download_button:
    csv_data = autoattend_functions.export_students_csv(d, st.session_state['cursor'])
    if csv_data:
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"{d}_attendance.csv",
            mime="text/csv"
        )
    else:
        st.warning("No attendance marked yet.")
if frame and button:
    img_array=face_recognition.load_image_file(frame)
    res=face_recognition.face_encodings(img_array)
    if res:
        data=st.session_state['data']
        face_vector=res[0]
        bool_array=face_recognition.compare_faces(face_vector,list(data.values()),tolerance=0.5)
        if True in bool_array:
            ind=bool_array.index(True)
            name=list(data.keys())[ind]
            autoattend_success=autoattend_functions.check_and_add(name,d,st.session_state['cursor'],t)
            if autoattend_success:
                st.success(f"Attendence of {name} marked.")
            else:
                st.warning(f"Attendence already marked for {name}")
        else:
            st.warning('Unknown face')
    else:
        st.warning("No face detected.")
elif not frame and button:
    st.warning('Capture your face first.')
elif frame and addface and name1:
    face=face_recognition.load_image_file(frame)
    new_vector=face_recognition.face_encodings(face)
    if new_vector:
        if name1 not in st.session_state['data']:
            st.session_state['data'][name1]=new_vector[0]
            data=st.session_state['data']
            with open('face_vector.pkl','wb') as obj1:
                pickle.dump(data,obj1)
                st.write(f"Face of {name1} added to the database.")
        else:
            st.warning('Same person {name1} already added in the database.')
    else:
        st.warning('No face detected. Try Again.')

if show_students:
    table=autoattend_functions.show_students(d,st.session_state['cursor'])
    if table is not None:
        st.dataframe(table)
    else:
        st.warning('No attendence marked yet.')