import json
import uuid
import random
import string
import os
import time

class ModGenerator:
    def __init__(self):
        self.creature_data = self.load_creature_data()
        self.creature_groups = self.group_creatures_by_level()
        self.auto_id_counter = 2
        self.auto_result_id_counter = 4097

    def load_creature_data(self):
        """Load creature data from the provided list"""
        data = """01|3430|Khủng Long Hóa Thạch Thường|3431|Khủng Long Hóa Thạch|3432|Khủng Long Hóa Thạch Siêu Cấp
02|3433|Sóc Bay Nhỏ|3434|Sóc Bay Nhanh Nhẹn|3435|Sóc Bay Láu Cá
03|3436|Kỳ Lân|3437|Thần Kỳ Lân|3438|Kỳ Lân May Mắn
04|3439|Chocobo|3440|Chocobo Thông Minh|3441|Chocobo Nghịch Ngợm
05|3442|Chú Voi Con|3443|Voi Vui Vẻ|3444|Voi Lễ Hội
06|3445|Sư Tử Biển Thủy Thủ|3446|Sư Tử Biển Thuyền Trưởng|3447|Boss Sư Tử Biển
07|3454|Mèo Thần Tài|3455|Mèo Phát Lộc|3456|Mèo Vũ Sư
08|3457|Bạch Mã|3458|Thiên Mã|3459|Thần Mã
09|3460|Kiệu Tre Cổ Điển|3461|Kiệu Vàng|3462|Kiệu Hoa Đào
10|3469|Mộc Long Thần|3470|Hỏa Long Thần|3471|Hắc Long Thần
11|3478|Trăng Rằm|3479|Trăng Ngọc|3480|Tiên Trăng
12|3483|Xe Tuần Lộc Gỗ|3484|Xe Tuần Lộc Vàng|3485|Xe Tuần Lộc Băng
13|3487|Pony Motor|||
14|3488|Bò May Mắn|||
15|3490|Transcendent Peak|3491|Ngọn Lửa Phương Bắc|3492|Chân Trời Trôi Dạt
16|3495|Bộ Bộ Liên Hoa|3496|Hoa Bay Tuyết Nhảy|3497|Kính Hoa Thủy Nguyệt
17|4501|Hươu Trắng Nhạt|4502|Sắc Màu Nirvana|4503|Vua Hươu
18|4505|Xe Bí Ngô Ma Thuật|4506|Xe Bí Ngô Hoàng Gia|4507|Xe Bí Ngô Cổ Tích
19|4509|Chong Chóng|4510|Xoắn Ốc Ba Lá|
20|4512|Thiên Nga Xám|4513|Thiên Nga Sao|4514|Thiên Nga Tiên
21|4517|Máy Bay Chiến Đấu|4518|Diều Hâu Đen|
22|4520|Cánh Phản Lực|4521|Diều Hâu Trắng|
23|4523|Bánh Xe Sấm Sét|||
24|4525|Boro Đại Dương|4526|Boro Đại Dương - Tiến Hóa|
25|4528|Seadrake|4529|Seadrake - Phát Triển|
26|4531|Rồng Đỏ Rực|4532|Rồng Vàng Kim|4533|Rồng Hư Không
27|4535|Nhạc Hội Petite|4536|Fluttering Shadow|
28|4539|Đêm Ả Rập|4540|Thảm Bay Ba Tư|4541|Thảm Ma Thuật Của Các Vì Sao
29|4543|Cúc Cu|4544|Kim Thuật Sư Quạ|4545|Chim Cắt Chiến Đấu
30|4547|Sóng Âm Mạnh Nhất|4548|Nhạc Điện Tử Vô Hạn|
31|4550|Hoa Trong Mây|4551|Vũ Điệu Hoa Yunmeng|
32|4553|Thủy Vân Du|4554|Túy Hoa Âm|
33|4556|Cún Mochi|||
34|4560|Hoàng Đế Colt Siêu Âm|4561|Hoàng Đế Colt Lục Hành|4562|Hoàng Đế Rồng
35|4564|Tiểu Hổ|4565|Hổ Con Xuống Núi|4566|Hổ Uy Phong
36|4572|Tinh Ngữ Tâm Nguyện|4573|Đèn Lồng|4574|Xuân Phong Yến Ngữ
37|4576|Thuyền Sa Mạc|4577|Sứ Giả Ốc Đảo|4578|Thần Lạc Hoa Lệ
38|4580|Giấc Mơ Hạnh Phúc|4581|Chân Dung|
39|4583|Chìa Khóa Trục Ảnh|4584|Chìa Khóa Mộng Li|4585|Chìa Khóa Vũ Huy
40|4587|Trường Kiếm Xích Tiêu|4588|Thánh Kiếm Hiên Viên|
41|4590|Thời Gian Thư Giãn|4591|Thời Khắc Trẻ Thơ|4592|Thời Khắc Mộng Ảo
42|4594|Tiểu Hồ Ly Đáng Yêu|4595|Hồ Ly Lanh Lợi|4596|Hồ Ly Ảo Ảnh
43|4598|Xe Mui Trần Mèo Yêu|||
44|4602|Sứ Giả Ốc Đảo|4603|Thần Lạc Hoa Lệ|
45|4606|Xanh Biếc|4607|Tử Dạ|4608|Thiều Quang
46|4610|Ánh Trăng Mật Ong|4611|Ngóng Nỗi Tương Tư|4612|Hoa Quế Trong Trăng
47|4614|Chuông Tím Buồn|4615|Hồn Bướm Dạo Mộng|4616|Lời Linh Lan Trong Gió
48|4618|Ván Lướt Sóng Phong|4619|Hành Động Phong Cực Hạn|
49|4623|Bé Heo|4624|Heo Bay Lô Lô|4625|Heo Cyberpunk
50|4628|Thỏ Ngọc Lưu Vân|4629|Thỏ Phúc Tới Nhà|
51|4632|Hộp Bột Mịn|4633|Hộp Cất Giữ Sao|4634|Đôi Cánh Giấc Mơ
52|4636|Tuyết Lưu Ly|4637|Băng Giá Nở Rộ|
53|4644|Xe Biến hình Mini|||
54|4646|Sách Lễ Mừng|||
55|4648|Thú Lộc Cộc|||
56|4650|Hương Bánh Đong Đưa|||
57|4654|Bồng Bềnh|||
58|4656|Ghế Tiểu Thư|||
59|4664|Âm Thanh Diệu Kỳ|4665|Hộp Nhạc Theo Đuổi Ngôi Sao|4666|Ngôi Sao Âm Nhạc
60|4668|Mầm Lá Ngọc|4669|Cành Du Dương|4670|Mộng Tuổi Thơ
61|4672|Vỏ Sò Lấp Lánh|4673|Giấc Mộng Phù Quang|4674|Ánh Sao San Hô
62|4682|Làn Mây Mộng Ảo|4683|Bóng Mộng Cảnh|4684|Làn Mây Tiên Cảnh"""
        
        creatures = {}
        for line in data.strip().split('\n'):
            parts = line.split('|')
            if len(parts) >= 3:
                # Parse each creature variant
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts) and parts[i] and parts[i+1]:
                        copy_id = int(parts[i])
                        name = parts[i+1]
                        creatures[copy_id] = name
        
        return creatures
    
    def group_creatures_by_level(self):
        """Group creatures by their base name and return the highest level copy_id for each"""
        data = """01|3430|Khủng Long Hóa Thạch Thường|3431|Khủng Long Hóa Thạch|3432|Khủng Long Hóa Thạch Siêu Cấp
02|3433|Sóc Bay Nhỏ|3434|Sóc Bay Nhanh Nhẹn|3435|Sóc Bay Láu Cá
03|3436|Kỳ Lân|3437|Thần Kỳ Lân|3438|Kỳ Lân May Mắn
04|3439|Chocobo|3440|Chocobo Thông Minh|3441|Chocobo Nghịch Ngợm
05|3442|Chú Voi Con|3443|Voi Vui Vẻ|3444|Voi Lễ Hội
06|3445|Sư Tử Biển Thủy Thủ|3446|Sư Tử Biển Thuyền Trưởng|3447|Boss Sư Tử Biển
07|3454|Mèo Thần Tài|3455|Mèo Phát Lộc|3456|Mèo Vũ Sư
08|3457|Bạch Mã|3458|Thiên Mã|3459|Thần Mã
09|3460|Kiệu Tre Cổ Điển|3461|Kiệu Vàng|3462|Kiệu Hoa Đào
10|3469|Mộc Long Thần|3470|Hỏa Long Thần|3471|Hắc Long Thần
11|3478|Trăng Rằm|3479|Trăng Ngọc|3480|Tiên Trăng
12|3483|Xe Tuần Lộc Gỗ|3484|Xe Tuần Lộc Vàng|3485|Xe Tuần Lộc Băng
13|3487|Pony Motor|||
14|3488|Bò May Mắn|||
15|3490|Transcendent Peak|3491|Ngọn Lửa Phương Bắc|3492|Chân Trời Trôi Dạt
16|3495|Bộ Bộ Liên Hoa|3496|Hoa Bay Tuyết Nhảy|3497|Kính Hoa Thủy Nguyệt
17|4501|Hươu Trắng Nhạt|4502|Sắc Màu Nirvana|4503|Vua Hươu
18|4505|Xe Bí Ngô Ma Thuật|4506|Xe Bí Ngô Hoàng Gia|4507|Xe Bí Ngô Cổ Tích
19|4509|Chong Chóng|4510|Xoắn Ốc Ba Lá|
20|4512|Thiên Nga Xám|4513|Thiên Nga Sao|4514|Thiên Nga Tiên
21|4517|Máy Bay Chiến Đấu|4518|Diều Hâu Đen|
22|4520|Cánh Phản Lực|4521|Diều Hâu Trắng|
23|4523|Bánh Xe Sấm Sét|||
24|4525|Boro Đại Dương|4526|Boro Đại Dương - Tiến Hóa|
25|4528|Seadrake|4529|Seadrake - Phát Triển|
26|4531|Rồng Đỏ Rực|4532|Rồng Vàng Kim|4533|Rồng Hư Không
27|4535|Nhạc Hội Petite|4536|Fluttering Shadow|
28|4539|Đêm Ả Rập|4540|Thảm Bay Ba Tư|4541|Thảm Ma Thuật Của Các Vì Sao
29|4543|Cúc Cu|4544|Kim Thuật Sư Quạ|4545|Chim Cắt Chiến Đấu
30|4547|Sóng Âm Mạnh Nhất|4548|Nhạc Điện Tử Vô Hạn|
31|4550|Hoa Trong Mây|4551|Vũ Điệu Hoa Yunmeng|
32|4553|Thủy Vân Du|4554|Túy Hoa Âm|
33|4556|Cún Mochi|||
34|4560|Hoàng Đế Colt Siêu Âm|4561|Hoàng Đế Colt Lục Hành|4562|Hoàng Đế Rồng
35|4564|Tiểu Hổ|4565|Hổ Con Xuống Núi|4566|Hổ Uy Phong
36|4572|Tinh Ngữ Tâm Nguyện|4573|Đèn Lồng|4574|Xuân Phong Yến Ngữ
37|4576|Thuyền Sa Mạc|4577|Sứ Giả Ốc Đảo|4578|Thần Lạc Hoa Lệ
38|4580|Giấc Mơ Hạnh Phúc|4581|Chân Dung|
39|4583|Chìa Khóa Trục Ảnh|4584|Chìa Khóa Mộng Li|4585|Chìa Khóa Vũ Huy
40|4587|Trường Kiếm Xích Tiêu|4588|Thánh Kiếm Hiên Viên|
41|4590|Thời Gian Thư Giãn|4591|Thời Khắc Trẻ Thơ|4592|Thời Khắc Mộng Ảo
42|4594|Tiểu Hồ Ly Đáng Yêu|4595|Hồ Ly Lanh Lợi|4596|Hồ Ly Ảo Ảnh
43|4598|Xe Mui Trần Mèo Yêu|||
44|4602|Sứ Giả Ốc Đảo|4603|Thần Lạc Hoa Lệ|
45|4606|Xanh Biếc|4607|Tử Dạ|4608|Thiều Quang
46|4610|Ánh Trăng Mật Ong|4611|Ngóng Nỗi Tương Tư|4612|Hoa Quế Trong Trăng
47|4614|Chuông Tím Buồn|4615|Hồn Bướm Dạo Mộng|4616|Lời Linh Lan Trong Gió
48|4618|Ván Lướt Sóng Phong|4619|Hành Động Phong Cực Hạn|
49|4623|Bé Heo|4624|Heo Bay Lô Lô|4625|Heo Cyberpunk
50|4628|Thỏ Ngọc Lưu Vân|4629|Thỏ Phúc Tới Nhà|
51|4632|Hộp Bột Mịn|4633|Hộp Cất Giữ Sao|4634|Đôi Cánh Giấc Mơ
52|4636|Tuyết Lưu Ly|4637|Băng Giá Nở Rộ|
53|4644|Xe Biến hình Mini|||
54|4646|Sách Lễ Mừng|||
55|4648|Thú Lộc Cộc|||
56|4650|Hương Bánh Đong Đưa|||
57|4654|Bồng Bềnh|||
58|4656|Ghế Tiểu Thư|||
59|4664|Âm Thanh Diệu Kỳ|4665|Hộp Nhạc Theo Đuổi Ngôi Sao|4666|Ngôi Sao Âm Nhạc
60|4668|Mầm Lá Ngọc|4669|Cành Du Dương|4670|Mộng Tuổi Thơ
61|4672|Vỏ Sò Lấp Lánh|4673|Giấc Mộng Phù Quang|4674|Ánh Sao San Hô
62|4682|Làn Mây Mộng Ảo|4683|Bóng Mộng Cảnh|4684|Làn Mây Tiên Cảnh"""
        
        highest_level_creatures = {}
        for line in data.strip().split('\n'):
            parts = line.split('|')
            if len(parts) >= 3:
                creatures_in_group = []
                
                # Parse each creature variant in the group
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts) and parts[i] and parts[i+1]:
                        copy_id = int(parts[i])
                        name = parts[i+1]
                        creatures_in_group.append({
                            'copyid': copy_id,
                            'name': name,
                            'position': i // 2  # Position in line determines level (0, 1, 2...)
                        })
                
                if creatures_in_group:
                    # Get the highest level (last non-empty) creature for this group
                    highest_level = max(creatures_in_group, key=lambda x: x['position'])
                    highest_level_creatures[highest_level['copyid']] = highest_level['name']
        
        return highest_level_creatures

    def generate_files(self, id_value, copyid_value, author_value, item_name):
        """Generate mod files synchronously"""
        try:
            # Add small delay to simulate processing
            time.sleep(0.1)
            
            random_filename = ''.join(random.choices(string.digits, k=10))
            uuid_value = str(uuid.uuid4())
            start_result_id = self.auto_result_id_counter
            self.auto_result_id_counter += 1
            
            # Main mod file
            main_mod_data = {
                "PhysicsActor": [],
                "avatarInfo": [],
                "foreign_ids": [],
                "mod_desc": {
                    "author": author_value,
                    "filename": random_filename,
                    "uuid": uuid_value,
                    "version": "1"
                },
                "property": {
                    "copyid": copyid_value,
                    "id": id_value
                },
                "set_ai": [{"name": "swimming", "priority": 1}]
            }
            
            # Ride file
            ride_data = {
                "property": {
                    "id": id_value,
                    "copyid": copyid_value
                }
            }
            
            # Crafting file
            crafting_data = {
                "PhysicsActor": [],
                "avatarInfo": [],
                "foreign_ids": [
                    {
                        "id": start_result_id,
                        "key": f"{author_value}{uuid_value.replace('-', '')}{random_filename}"
                    }
                ],
                "mod_desc": {
                    "author": author_value,
                    "filename": ''.join(random.choices(string.digits, k=10)),
                    "uuid": uuid_value,
                    "version": "1"
                },
                "property": {
                    "CraftingItemID": 11000,
                    "copyid": copyid_value,
                    "id": start_result_id + 1,
                    "material_count1": 1,
                    "material_count2": 0,
                    "material_count3": 0,
                    "material_count4": 0,
                    "material_count5": 0,
                    "material_count6": 0,
                    "material_count7": 0,
                    "material_count8": 0,
                    "material_count9": 0,
                    "material_id1": 101,
                    "material_id2": 0,
                    "material_id3": 0,
                    "material_id4": 0,
                    "material_id5": 0,
                    "material_id6": 0,
                    "material_id7": 0,
                    "material_id8": 0,
                    "material_id9": 0,
                    "result_count": 1,
                    "result_id": start_result_id,
                    "type": 0
                }
            }
            
            # Item file
            item_data = {
                "PhysicsActor": {
                    "EditType": 2,
                    "ModelScale": 1,
                    "ShapeID": 0,
                    "ShapeVal1": 50,
                    "ShapeVal2": 0,
                    "ShapeVal3": 0
                },
                "avatarInfo": [],
                "foreign_ids": [
                    {
                        "id": start_result_id,
                        "key": f"{author_value}{uuid_value.replace('-', '')}{random_filename}"
                    }
                ],
                "itemskills": [
                    {
                        "ChargeTime": 1.5,
                        "ChargeType": 0,
                        "Cooldown": 5,
                        "Costs": [
                            {
                                "CostTarget": 10100,
                                "CostType": 1,
                                "CostVal": 0
                            }
                        ],
                        "Functions": [
                            {
                                "CallNum": 1,
                                "Duration": 0,
                                "IsFollow": 0,
                                "MobID": id_value
                            }
                        ],
                        "RangeType": 0,
                        "RangeVal1": 1000,
                        "RangeVal2": 300,
                        "RangeVal3": 300,
                        "SkillType": 1,
                        "TargetCamp": 0,
                        "name": "feature_call_monster",
                        "priority": 0,
                        "templateid": 103
                    }
                ],
                "mod_desc": {
                    "author": author_value,
                    "filename": ''.join(random.choices(string.digits, k=10)),
                    "uuid": uuid_value,
                    "version": "1"
                },
                "property": {
                    "copyid": 10100,
                    "describe": "",
                    "icon": "*11653",
                    "id": start_result_id,
                    "model": "*11653",
                    "name": item_name,
                    "orignid": start_result_id,
                    "stack_max": 1
                }
            }
            
            generated_files = {
                f"{copyid_value}du.json": (json.dumps(main_mod_data, indent=2, ensure_ascii=False), "actor"),
                f"{copyid_value}duride.json": (json.dumps(ride_data, indent=2, ensure_ascii=False), "horse"),
                f"craft{copyid_value}.json": (json.dumps(crafting_data, indent=2, ensure_ascii=False), "crafting"),
                f"item{copyid_value}.json": (json.dumps(item_data, indent=2, ensure_ascii=False), "item")
            }
            
            return {
                'files': generated_files,
                'uuid': uuid_value,
                'random_filename': random_filename,
                'id': id_value,
                'copyid': copyid_value,
                'author': author_value,
                'item_name': item_name,
                'result_id_used': start_result_id
            }
            
        except Exception as e:
            print(f"Error in generate_files: {str(e)}")
            return None
