#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13.10.2020 12:25 CET

@author: zocker_160
@comment: Interface for all image classes to simplify handling of multiple file types
"""

class ImgInterface():
    def get_Image_parts(self) -> list:
        raise NotImplementedError
    
    def write_file(self, binary, filename: str) -> None:
        """writes file AND ADDS FILE EXTENTION AUTOMATICALLY!!"""
        raise NotImplementedError
