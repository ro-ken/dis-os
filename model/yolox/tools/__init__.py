#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 改变当前工作路径到 yolox
os.chdir(os.path.split(os.path.realpath(__file__))[0] + '/../')