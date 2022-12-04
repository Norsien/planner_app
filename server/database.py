from mongoengine import connect
from models import Plane

connect('planner1', host='127.0.0.1', port=27017)