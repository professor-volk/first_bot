from database import database as db

d = {'student': ' 444755,wer, @qwe', 'subject': 'ert', 'name_less': 'Name', 
     'data_less': '22/10/2024', 'time_start': '12:30', 'time_end': '13:30', 
     'price': '1000', 'memo_less': '0', 'memo_pay': True}
db.add_lesson(int(d['student'].split(',')[0]), d['subject'], d['name_less'], 
                  d['data_less'], d['time_start'] +' - ' + d['time_end'], 
                  int(d['price']), int(d['memo_less']), d['memo_pay'], 
                  7812730819)


