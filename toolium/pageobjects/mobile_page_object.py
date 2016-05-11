# -*- coding: utf-8 -*-
u"""
Copyright 2016 Telefónica Investigación y Desarrollo, S.A.U.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""

import importlib

from toolium.driver_wrapper import DriverWrappersPool
from toolium.pageobjects.page_object import PageObject


class MobilePageObject(PageObject):
    def __new__(cls, driver_wrapper=None):
        """Instantiate android or ios page object from base page object depending on driver configuration

        Base, Android and iOS page objects must be defined with following structure:
            FOLDER/base/MODULE_NAME.py
                class BasePAGE_OBJECT_NAME(MobilePageObject)
            FOLDER/android/MODULE_NAME.py
                class AndroidPAGE_OBJECT_NAME(BasePAGE_OBJECT_NAME)
            FOLDER/ios/MODULE_NAME.py
                class IosPAGE_OBJECT_NAME(BasePAGE_OBJECT_NAME)

        :param driver_wrapper: driver wrapper instance
        :returns: android or ios page object instance
        """
        if cls.__name__.startswith('Base'):
            __driver_wrapper = driver_wrapper if driver_wrapper else DriverWrappersPool.get_default_wrapper()
            __os_name = 'ios' if __driver_wrapper.is_ios_test() else 'android'
            __module_name = cls.__module__.replace('.base.', '.{}.'.format(__os_name))
            __class_name = cls.__name__.replace('Base', __os_name.capitalize())
            return getattr(importlib.import_module(__module_name), __class_name)(__driver_wrapper)
        else:
            return super(MobilePageObject, cls).__new__(cls, driver_wrapper)
