def create_table(date,cursor,database):
    cursor.execute(f'use {database}')
    cursor.execute(f"show tables")
    tables=cursor.fetchall()
    table_names = [t[0] for t in tables]
    if str(date) not in table_names:
        cursor.execute(f"create table `{str(date)}` (name varchar(100),time_of_attend time)")


def check_and_add(name,date,cursor,time):
    cursor.execute(f'select name from `{str(date)}`')
    students=cursor.fetchall()
    student_name=[s[0] for s in students]
    if name not in student_name:
        cursor.execute(f'insert into `{str(date)}` values (%s,%s)',(name,str(time).split('.')[0]))
        return True
    else:
        return False
    
def add_person(name,image_path,data):
    import face_recognition
    try:
        img_array=face_recognition.load_image_file(image_path)
        img_vector=face_recognition.face_encodings(img_array)
        if name in data and img_vector:
            print("The person already exist.")
            vector=img_vector[0]
            data[name]=vector
            print(f"New face updated for the person {name}")
            return data
    
        if img_vector:
            vector=img_vector[0]
            data[name]=vector
            return data
        
    except Exception:
        return None
    
def show_students(date,cursor):
    import pandas as pd
    cursor.execute(f'select * from {str(date)}')
    data=cursor.fetchall()
    new=[(i,str(j)) for i,j in data]
    if data:
        df=pd.DataFrame(new,columns=['Name',"Time"])
        return df
    else:
        return None

def export_students_csv(date, cursor):
    import pandas as pd
    cursor.execute(f'select * from {str(date)}')
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['Name', 'Time'])
        return df.to_csv(index=False).encode('utf-8')  # returns CSV in bytes
    else:
        return None        
