from fastapi import FastAPI
from ..backend.models import db,Users,Filer,Stacks
app=FastAPI()
students=[
    {'name':'Student 1'}
]