#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os



for x in os.listdir('.'):
    print("* "+x)
    if(os.path.isdir(x)):
        for y in os.listdir(x):
            print(" * ["+y.replace(".md","")+"](78/"+x+"/"+y+")")
