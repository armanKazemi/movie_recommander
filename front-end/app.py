import streamlit as sl
from textFormatter import *
from api import *
from PIL import Image
import time

sl.title(print_title())
sl.text(print_course())

sl.sidebar.title(print_sidebar_title())
sl.sidebar.subheader(print_seperator())
sl.sidebar.text(print_ln())
sl.sidebar.header(print_sidebar_header1())
sl.sidebar.text(print_sidebar_section1())
sl.sidebar.text(print_ln())
sl.sidebar.header(print_sidebar_header2())
sl.sidebar.text(print_sidebar_section2())
sl.sidebar.text(print_ln())
sl.sidebar.header(print_sidebar_header3())
sl.sidebar.text(print_sidebar_section3())

sl.text(print_ln())

img = Image.open(print_intro_image_path())
sl.image(img, width=500)

sl.text(print_ln())

method = sl.selectbox(print_method_radio(), ('By User', 'By Text Search'))

sl.subheader(print_section_header1())

sl.text(print_ln())

if method == 'By User':
    count_range = sl.radio(print_range_radio(), ('small', 'medium', 'large', 'huge'))
    if count_range == 'small':
        slider_range_start = 1
        slider_range_end = 200
    elif count_range == 'medium':
        slider_range_start = 200
        slider_range_end = 400
    elif count_range == 'large':
        slider_range_start = 400
        slider_range_end = 600
    elif count_range == 'huge':
        slider_range_start = 600
        slider_range_end = 671
    choice_count = sl.slider(print_range_slider(), slider_range_start, slider_range_end)
    users = get_random_users(choice_count, )

    users = [''] + users
    user = sl.selectbox(print_selector_text(), users)
    text = sl.text_input(print_text_search())

    sl.text(print_ln())
    submit_key = sl.button(print_submit())
    while not submit_key:
        pass

    submitted = False
    if submit_key:
        submit_key = False
        if len(user) < 1:
            sl.error(print_movies_not_selected())
        else:
            with sl.spinner(print_choices_submission()):
                time.sleep(3)
            sl.success(print_done())
            submitted = True

    sl.text(print_ln())

    sl.subheader(print_section_header2())

    sl.text(print_ln())
    start_key = sl.button(print_start())

    while not start_key:
        pass
    # start_key = False

    if not submitted:
        sl.error(print_choices_not_submitted())
    else:
        if len(text) > 0:
            titles = text_search(text)
            titles = [''] + titles
            sl.text(print_ln())

            movie = sl.selectbox(print_select_movie(), titles)
            continue_key = sl.button(print_continue())

            while not continue_key:
                pass
            continue_key = False

            if len(movie) < 1:
                sl.error(print_select_movie())
            else:
                with sl.spinner((print_model_working())):
                    time.sleep(5)
                sl.success(print_done_table())
                sl.table(user_movie_search(user, movie))
        else:
            sl.text(print_ln())
            with sl.spinner((print_model_working())):
                time.sleep(5)
            sl.success(print_done_table())
            sl.table(user_search(user))
else:
    text = sl.text_input(print_text_search_input())

    sl.text(print_ln())

    sl.subheader(print_section_header2())

    sl.text(print_ln())

    start = sl.button(print_start())

    if start:
        if len(text) < 1:
            sl.error(print_text_is_empty())
        else:
            sl.text(print_ln())
            titles = text_search(text)
            titles = [''] + titles
            sl.text(print_ln())
            movie = sl.selectbox(print_select_movie(), titles)

            continue_key = sl.button(print_continue())

            while not continue_key:
                pass
            continue_key = False

            if len(movie) < 1:
                sl.error(print_select_movie())
            else:
                with sl.spinner((print_model_working())):
                    time.sleep(5)
                sl.success(print_done_table())
                sl.table(movie_search(movie))
