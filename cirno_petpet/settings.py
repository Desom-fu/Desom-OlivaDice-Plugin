"""基础设置"""
BASE_PATH = [".", "plugin", "data"]
PIC_PATH = [".", "data", "images", "PetPetFrames" , "temp"]
output_pic_name = 'tempPetPet-{member_id}.gif'
recheck = r"^摸\s*(?:\[CQ:at,qq=(\d{5,10})\]|(\d{5,10}))\s*$"

frame_spec = [
    (27, 31, 86, 90),
    (22, 36, 91, 90),
    (18, 41, 95, 90),
    (22, 41, 91, 91),
    (27, 28, 86, 91)
]

squish_factor = [
    (0, 0, 0, 0),
    (-7, 22, 8, 0),
    (-8, 30, 9, 6),
    (-3, 21, 5, 9),
    (0, 0, 0, 0)
]

squish_translation_factor = [0, 20, 34, 21, 0]
frames = tuple([f'data/images/PetPetFrames/frame{i}.png' for i in range(5)])
url = 'http://q1.qlogo.cn/g?b=qq&nk={member_id}&s=640'

# import re
# def checkpetpet(retext , check_text):
#     match = re.search(retext , check_text)
#     if match:
#         return match.group(1)
#     else:
#         return False
    
# print(checkpetpet(recheck , "摸 [CQ:at,qq=1173911191]"))