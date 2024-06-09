import json
import random

class Constant:
    # Number of days in a week
    DAYS_NUM = 5
    # Number of working hours per day
    DAY_HOURS = 10
    # Total available time slots
    TOTAL_SLOTS = DAYS_NUM * DAY_HOURS

def generate_classes(profs, courses, groups, rooms, num_classes, max_classes_per_room, total_slots):
    classes = []
    class_counter = 0
    room_schedule = {room['name']: [] for room in rooms}
    total_time_used = 0
    
    while class_counter < num_classes and total_time_used < total_slots:
        prof = random.choice(profs)['id']
        course = random.choice(courses)['id']
        room = random.choice(rooms)
        room_name = room['name']
        room_size = room['size']
        duration = random.randint(1, 3)  # Duration từ 1 đến 3 giờ
        group = random.choice(groups)
        group_id = group['id']
        group_size = group['size']
        
        if random.random() > 0.5:
            group_field = group_id
            total_group_size = group_size
        else:
            selected_groups = random.sample([g for g in groups], k=random.randint(2, 3))
            group_field = [g['id'] for g in selected_groups]
            total_group_size = sum(g['size'] for g in selected_groups)
        total_group_size = group_size if isinstance(group_field, int) else sum(g['size'] for g in groups if g['id'] in group_field)

        # Kiểm tra nếu phòng đã đủ lớp học trong ngày hoặc tổng thời gian đã sử dụng vượt quá giới hạn
        if len(room_schedule[room_name]) >= max_classes_per_room or total_time_used + duration > total_slots:
            continue
        
        # Kiểm tra nếu tổng số sinh viên vượt quá sức chứa của phòng
        if total_group_size > room_size:
            continue

        # Thêm lớp học vào lịch phòng
        room_schedule[room_name].append({
            'professor': prof,
            'course': course,
            'duration': duration,
            'group': group_field
        })
        classes.append({
            'professor': prof,
            'course': course,
            'duration': duration,
            'group': group_field
        })
        class_counter += 1
        total_time_used += duration
    
    return classes

# Đọc dữ liệu từ file JSON
with open('GaSchedule.json', 'r') as file:
    original_data = json.load(file)

# Trích xuất danh sách các đối tượng từ dữ liệu gốc
profs = [item['prof'] for item in original_data if 'prof' in item]
courses = [item['course'] for item in original_data if 'course' in item]
rooms = [item['room'] for item in original_data if 'room' in item]
groups = [item['group'] for item in original_data if 'group' in item]

# Xác định số lớp học tối đa có thể xếp lịch trong một ngày dựa trên các phòng học và thời gian học
max_classes_per_room = 10  # Giả sử mỗi phòng có thể chứa 10 lớp học mỗi ngày

# Sinh 30 bộ dữ liệu với số lượng lớp học tăng dần
for i in range(25):
    num_classes = (i + 1) * 3  # Số lớp học tăng dần, mỗi bộ dữ liệu thêm 3 lớp học
    total_slots = len(rooms) * Constant.TOTAL_SLOTS
    classes = generate_classes(profs, courses, groups, rooms, num_classes, max_classes_per_room, total_slots)
    
    # Tạo bộ dữ liệu
    data = []
    data.extend({'prof': prof} for prof in profs)
    data.extend({'course': course} for course in courses)
    data.extend({'room': room} for room in rooms)
    data.extend({'group': group} for group in groups)
    data.extend({'class': cl} for cl in classes)
    
    # Lưu vào tệp
    with open(f'GaSchedule_subset_{i+1}.json', 'w') as file:
        json.dump(data, file, indent=4)

print("Done generating datasets.")
