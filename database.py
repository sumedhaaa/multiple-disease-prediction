# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 09:34:48 2023

@author: Hp
"""
import os

from deta import Deta
from dotenv import load_dotenv

load_dotenv(".env")
DETA_KEY=os.getenv("DATA_KEY")

deta=Deta(DETA_KEY)

db=deta.Base("users")

def insert(fname,lname,username,email,password,is_diab,is_heart,is_park):
    return db.put({"key":username,"fname":fname,"lname":lname,"email":email,"password":password,"is_diab":is_diab,"is_heart":is_heart,"is_park":is_park})

def fetch_all_users():
    res=db.fetch()
    return res.items

def update_user(username,updates):
    return db.update(updates,username)

def get_user(username):
    return db.get(username)