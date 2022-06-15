#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import os

from yolox.exp import Exp as MyExp


class Exp(MyExp):
    def __init__(self):
        super(Exp, self).__init__()


        # model config
        self.num_classes = 80
#        self.depth = 1.33
#        self.width = 1.25
        self.depth = 0.33
        self.width = 0.50
        
        self.exp_name = os.path.split(os.path.realpath(__file__))[1].split(".")[0]
        print('exp name', self.exp_name)
        # dataloader config
        self.input_size = (640, 640)
        self.random_size = (18, 32)
        self.train_ann = "annotations_traino.json"
        self.val_ann = "annotations_valo.json"

        # training config
#        self.max_epoch = 80
        self.max_epoch = 5
        self.warmup_epochs = 1
        self.basic_lr_per_img = 0.001 / 64.0
        self.no_aug_epochs = 10

        self.print_interval = 20
#        self.eval_interval = 5
        self.eval_interval = 1
        
        # testing config
        self.test_size = (640, 640)
        self.test_conf = 0.1
        self.nmsthre = 0.7
