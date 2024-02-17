from vk import *


url = "https://vk.com/career.sibur"
id = get_owner_id(url)
print(id)
print(get_group_name(str(id)))