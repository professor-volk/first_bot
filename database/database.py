from datetime import date

student_for_teacher = {
    #'user_name': int,
    'name': str,
    'subject': str
}

lesson_dict = {
    'student_name': str,
    'subject_name': str,
    'lesson_name': str,
    'date_less': date,
    'time_of_week': int,
    'time_less': [str, str],
    'price_per_hour': int,
    'memo_less': int,
    'memo_pay': bool
}

teacher_dict = {
    'status': str,
    'students': {}
}

student_dict = {
    
}

user_db = {

}

#example
'''
id = 123456
user_db[id] = deepcopy(teacher_dict)
user_db[id]['status'] = 'teacher'
user_db[id]['@user_name'] = deepcopy(student_for_teacher)
user_db[id]['@user_name']['name'] = 'Иван'
user_db[id]['@user_name']['subject'] = ['Математика', 'Информатика']
user_db[id]['less_1'] = deepcopy(lesson_dict)
user_db[id]['less_1']['student_name'] = 'Иван'
user_db[id]['less_1']['subject_name'] = 'Математика'
user_db[id]['less_1']['lesson_name'] = 'Математика ОГЭ'
user_db[id]['less_1']['date_less'] = date(2024,10,13)
user_db[id]['less_1']['time_of_week'] = 1
user_db[id]['less_1']['time_less'] = ['12:30','14:00']
user_db[id]['less_1']['price_per_hour'] = 1000
user_db[id]['less_1']['memo_less'] = 2
user_db[id]['less_1']['memo_pay'] = True
{123456: {
        'status': 'teacher', 
        '@user_name': {
                    'name': 'Иван', 
                    'subject': ['Математика', 'Информатика']}, 
        'less_1': {
                'student_name': 'Иван', 
                'subject_name': 'Математика', 
                'lesson_name': 'Математика ОГЭ', 
                'date_less': datetime.date(2024, 10, 13), 
                'time_of_week': 1, 
                'time_less': ['12:30', '14:00'], 
                'price_per_hour': 1000, 
                'memo_less': 2, 
                'memo_pay': True}}}
'''