from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
from get_names import send_names

''' 
this app automatic login in to a website and cut the hours of the people who forgot to clock out
in lunch time
'''

# list_for_test = ['test employee 1', "test employee 2"]

####################################### Basic settings #########################################
SET_TIME = '11:50'
SET_TIME_DIV = 'AM'
set_date = date.strftime(date.today(), "%m/%d/%Y")                  # today in format mm/dd/yyyy
USERNAME = ''
PASSWORD = ""
NOTE = f'Automatic System - Forgot to clock out for Lunch - Administrator - {set_date}'
################################################################################################

browser = webdriver.Firefox()
browser.get('https://www.timestation.com/Login.asp')


def login_page():
    ''' login in to website autetification '''
    
    email_field = browser.find_element_by_css_selector('#eMail')
    password_field = browser.find_element_by_css_selector('#Password')
    summit_field = browser.find_element_by_css_selector('.ButtonGreen')

    email_field.clear()
    email_field.send_keys(USERNAME)
    password_field.clear()
    password_field.send_keys(PASSWORD)
    summit_field.click()


def select_employees_website():
    ''' click the employees link inside of the website after login in.'''

    employee_css = '.menu-main > li:nth-child(2) > a:nth-child(1)'
    employee_button_ = browser.find_element_by_css_selector(employee_css)
    employee_button_.click()


def select_names(name):
    ''' this scroll the website and click the checkbox with their name'''

    info_name = browser.find_element_by_link_text(name)
    href_link = info_name.get_attribute('href')
    href_link.split('=')
    id_number = href_link.split('=')
    xpath_path = f".//input[@value={id_number[1]}]"
    for_click = browser.find_element_by_xpath(xpath_path)
    for_click.location_once_scrolled_into_view
    for_click.click()


def select_box(id, text):
    ''' open select items and select them. '''

    action_find = browser.find_element_by_id(id)
    action_find.location_once_scrolled_into_view
    action_tab = Select(action_find)
    action_tab.select_by_visible_text(text)


def select_names_flow(names):
    '''  this function gets in a list of names that will loop in it. '''

    for name in names:
        select_names(name=name)

    select_box(id='employeeAction', text='Check-Out')                # to select the action bar
    select_box(id='TimeOut_Hour', text=SET_TIME.split(':')[0])       # this input the hour to field
    select_box(id='TimeOut_Minute', text=SET_TIME.split(':')[1])     # this input the minutes to field
    select_box(id='TimeOut_AMPM', text=SET_TIME_DIV)                 # this input the AM or PM in field
    date_field = browser.find_element_by_id('TimeOut_Date')
    note_field = browser.find_element_by_id('Notes')
    date_field.send_keys(set_date)
    note_field.send_keys(NOTE)
    browser.find_element_by_name('Submit').click()


if __name__ == "__main__":

    login_page()
    select_employees_website()
    names = send_names()
    list_of_names = names                     # import data from get_names.py
    select_names_flow(names=list_of_names)    # this accept a list of names to be change.

    #  this created a log in a text file
    try:
        with open('NameChangeLog.txt', 'w') as file_log:
            for name in list_of_names:
                file_log.write(name)

    except:
        with open('NameChangeLog.txt', 'a') as file_log:
            for name in list_of_names:
                file_log.write(name)

    finally:
        (print(x) for x in names)       
        print('everything was change successfully ')
        browser.close()
