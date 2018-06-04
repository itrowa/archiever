from app import db  # 获取在app中定义好了的SQLAlchemy对象

db.drop_all()
db.create_all()

from app import Plan
from patches import *

g1 = get_init_data()

p1 = Plan(name='Dormitory 1st floor', 
          desc="Shenzhen University Yunshan Xuan floor plan, this is where I lived in.", 
          body="What is the recommended way to create dynamic URLs in Javascript files when using flask? In the jinja2 templates and within the python views url_for is used, what is the recommended way to do this in .js files? Since they are not interpreted by the template engine.",
          data=g1,
          graph='static/sample.svg')

db.session.add(p1)
db.session.commit()

# at last, be sure to check print(p1.id) is not None!
