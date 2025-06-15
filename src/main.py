import dearpygui.dearpygui as dpg
from preset_dictionaries import hiragana_romaji, dakuten_hiragana_romaji, handakuten_hiragana_romaji, katakana_romaji, dakuten_katakana_romaji, handakuten_katakana_romaji
from Selector import BiasedRandomSelector
from datetime import datetime
from platformdirs import user_data_dir
from os import makedirs, rmdir, remove, path
import json
from pyautogui import press
     

ttf_path = r".\src\resource\ZenMaruGothic-Black.TTF"
icon_path = r".\src\resource\icon.ico"
data_dir = user_data_dir(appname="hiragana_training", appauthor="thomaskkfung")
makedirs(data_dir, exist_ok=True)

data_file = path.join(data_dir, 'training_record.dat')
training_records = []
if path.exists(data_file):
    with open(data_file) as file:
        try:
            training_records = json.load(file)
        except json.JSONDecodeError:
            training_records = []
            remove(data_file)


def save_to_json(filepath, record):
    """
    Adds a new record to a JSON file. Creates the file if it doesn't exist.

    Args:
        filepath (str): The path to the JSON file.
        new_record (dict): The new record to add.
    """
    if not path.exists(filepath):
        with open(filepath, 'w') as file:
            json.dump([record], file, indent=4)
    else:
        try:
            with open(filepath, 'r+') as file:
                file_data = json.load(file)
                if not isinstance(file_data, list):
                    file_data = [file_data]
                file_data.append(record)
                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
        except json.JSONDecodeError:
            with open(filepath, 'w') as file:
                json.dump([record], file, indent=4)
            
dpg.create_context()
with dpg.font_registry():
    with dpg.font(ttf_path, 50, default_font=False) as title_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(title_font)

    with dpg.font(ttf_path, 20, default_font=True) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(default_font)

# Theme setup
with dpg.theme() as custom_listbox_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0,0)
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0, 0.5)

with dpg.theme() as button_selected_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0,119,200,153))

with dpg.theme() as button_normal_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 55, 255))
        
# Center Alignment theme
with dpg.theme() as button_as_text_center_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0.06 * 255, 0.06 * 255, 0.06 * 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0.06 * 255, 0.06 * 255, 0.06 * 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0.06 * 255, 0.06 * 255, 0.06 * 255, 255))

# set the window background colour
with dpg.theme() as window_theme_id:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0.06 * 255, 0.06 * 255, 0.06 * 255, 255))

options = {"平假名": False, "片假名": False, "濁音（平假名）": False, "濁音（片假名）": False, "半濁音（平假名）": False, "半濁音（片假名）": False}
options_to_dictionary = {"平假名": hiragana_romaji, "片假名": katakana_romaji, "濁音（平假名）": dakuten_hiragana_romaji, "濁音（片假名）": dakuten_katakana_romaji, "半濁音（平假名）": handakuten_hiragana_romaji, "半濁音（片假名）": handakuten_katakana_romaji}

# Callback function for custom listbox items
def custom_listbox_callback(sender):
    if button_selected_theme == dpg.get_item_theme(sender):
        dpg.bind_item_theme(sender, button_normal_theme)
        options[dpg.get_item_label(sender)] = False
    else:
        dpg.bind_item_theme(sender, button_selected_theme)
        options[dpg.get_item_label(sender)] = True

# Selection Window for different types of Japanese characters
with dpg.window(tag="Selection Window", pos=(0, 0), width=150, height=300, no_title_bar=True, no_resize=True, no_move=True):
    dpg.add_text("練習數量:")
    dpg.add_input_int(tag="Quiz Amount", default_value=10, width=-1, readonly=False, min_value=1, min_clamped=True, max_value=100, max_clamped=True)
    dpg.add_text("練習範圍:")
    with dpg.child_window(border=False) as custom_listbox:
        for item in options.keys():
            t = dpg.add_button(label=item, width=-1, callback=custom_listbox_callback)
            dpg.bind_item_theme(t, button_normal_theme)

    dpg.bind_item_theme(custom_listbox, custom_listbox_theme)

def start_quiz(options, options_to_dictionary):
    start_time = datetime.now()
    available_options = dict()
    for key, value in options.items():
        if value: available_options.update(options_to_dictionary[key])

    if not available_options:
        dpg.set_value("Primary Window Text", "請至少選擇一個練習範圍...")
        return None
    else:
        dpg.set_value("Primary Window Text", "")
    
    
    selector = BiasedRandomSelector(available_options.items())
    selector.random_hiragana()
    counter = dpg.get_value("Quiz Amount")
    correct_count = 0
    incorrect_count = 0
    incorrect_items = dict()

    def quiz_callback(sender, app_data, user_data):
        nonlocal counter, correct_count, incorrect_count, incorrect_items
        if selector.selected_item[1] == dpg.get_value("Quiz Input"):
            dpg.set_value("Quiz Result", "正解です!")
            correct_count += 1
        else:
            dpg.set_value("Quiz Result", f"間違っています!(ノへ￣、)\n上一題目:{selector.selected_item[0]}\n輸入答案:{dpg.get_value("Quiz Input")}\n正確答案:{selector.selected_item[1]}")
            incorrect_count += 1
            incorrect_items[selector.selected_item[0]] = selector.selected_item[1]
        selector.random_hiragana()
        dpg.set_value("Quiz Character", selector.selected_item[0])
        counter -= 1
        dpg.set_value("Quiz Counter", "剩餘題目數量: " + str(counter))
        dpg.set_value("Quiz Input", "")
        press('tab') 
        if counter == 0:
            dpg.delete_item("Quiz Window")

            dpg.configure_item("Primary Window Title", height=60)

            incorrect_str = "["
            for item, answer in incorrect_items.items():
                incorrect_str += f"{item}:{answer}, "
            incorrect_str = incorrect_str[:-2] + "]"
            final_text = f"總共答題數: \t{dpg.get_value('Quiz Amount')}\n答對題數:\t\t{correct_count}\n答錯題數:\t\t{incorrect_count}\n錯誤五十音:\t{incorrect_str}" if incorrect_count > 0 else "恭喜！答對了所有題目！"
            dpg.set_value("Primary Window Top Text", final_text)
            
            save_dict = {"date": start_time.strftime("%Y-%m-%d %H:%M:%S"), "total": dpg.get_value("Quiz Amount"), "correct": correct_count, "incorrect": incorrect_count, "incorrect_items": incorrect_items}
            save_to_json(data_file, save_dict)
            training_records.append(save_dict)

            dpg.set_item_label("Practise Button", "重新開始")

    with dpg.window(label="Quiz Window", pos=(150, 0), width=500, height=300, tag="Quiz Window", no_title_bar=True, no_resize=True, no_move=True):
        dpg.add_text("剩餘題目數量: " + str(counter), tag="Quiz Counter", color=(0, 255, 0, 255))
        with dpg.group(horizontal=True):
            dpg.add_text("問題:")
            dpg.add_text(selector.selected_item[0], tag="Quiz Character", color=(0, 119, 200, 255))
        
        with dpg.group(horizontal=True):
            dpg.add_text("答え:")
            dpg.add_input_text(tag="Quiz Input", width=300, callback=quiz_callback, on_enter=True)
            dpg.add_button(label="Submit", width=100, callback=quiz_callback)

        dpg.add_text("", tag="Quiz Result", color=(0, 255, 0, 255))

    dpg.bind_item_theme("Quiz Window", window_theme_id)

def start_review(training_records):
    pointer = len(training_records) - 1
    
    def create_review(record):
        mark = round(record["correct"]/record["total"]*100, 2)
        incorrect_str = "["
        for item, answer in record["incorrect_items"].items():
            incorrect_str += f"{item}:{answer}, "
        incorrect_str = incorrect_str[:-2] + "]"

        final_text = f"總共得分:\t{mark}\n總共答題:\t{record["total"]}\n答對題數:\t{record["correct"]}\n答錯題數:\t{record["incorrect"]}\n錯誤五十音:\t{incorrect_str}"
        dpg.set_item_label("Review Window Content", final_text)
        dpg.set_item_label("Review Title", f"練習日期:{record["date"]}")
        

    def exit_callback(sender, app_data, user_data):
        dpg.delete_item("Review Window")

    def last_callback(sender, app_data, user_data):
        nonlocal pointer
        pointer -= 1
        create_review(training_records[pointer])
        if pointer == 0:
            dpg.hide_item(sender)
        if pointer != len(training_records) - 1:
            dpg.show_item("Next Button")

    def next_callback(sender, app_data, user_data):
        nonlocal pointer
        pointer += 1
        create_review(training_records[pointer])
        if pointer != 0:
            dpg.show_item("Last Button")
        if pointer == len(training_records) - 1:
            dpg.hide_item(sender)
    
    with dpg.window(label="Review Window", pos=(150, 0), width=500, height=300, tag="Review Window", no_title_bar=True, no_resize=True, no_move=True):
        
        dpg.add_button(label="", tag="Review Window Content", width=400, height=240, pos=(50, 20))
        dpg.bind_item_theme("Review Window Content", button_as_text_center_theme)

        dpg.add_button(label="", tag="Review Title", width=-1, height=60, pos=(0, 0))
        dpg.bind_item_font("Review Title", title_font)
        dpg.bind_item_theme("Review Title", button_as_text_center_theme)
        
        dpg.add_button(label="<", width=33, pos=(10, 130), callback=last_callback, tag="Last Button")
        dpg.add_button(label=">", width=33, pos=(457, 130), callback=next_callback, tag="Next Button", show=False)
        dpg.add_button(label="返回主頁", width=100, pos=(390, 262), callback=exit_callback)
    dpg.bind_item_theme("Review Window", window_theme_id)
    create_review(training_records[pointer])

def remove_and_quit(sender, app_data):
    try:
        rmdir(data_dir)
        print(f"Directory '{data_dir}' removed successfully.")
    except OSError as e:
        print(f"Error removing directory '{data_dir}': {e}")
    dpg.destroy_context()
    dpg.stop_dearpygui()  

with dpg.window(tag="Primary Window", pos=(150, 0), width=500, height=300, no_title_bar=True, no_resize=True, no_move=True):
    dpg.add_button(label="五十音練習！", tag="Primary Window Title", width=-1, height=100)
    dpg.bind_item_font("Primary Window Title", title_font)
    dpg.bind_item_theme("Primary Window Title", button_as_text_center_theme)
    
    dpg.add_text("", tag="Primary Window Top Text", wrap=480)

    dpg.add_button(label="開始練習", tag="Practise Button", width=-1, callback=lambda: start_quiz(options, options_to_dictionary))
    dpg.add_button(label="記録確認", tag="Review Button", width=-1, callback=lambda: start_review(training_records))
    dpg.add_button(label="刪除記録", tag="Remove Button", width=-1, callback=remove_and_quit)
    dpg.add_text("", tag="Primary Window Text", color=(255, 0, 0, 255))
dpg.bind_item_theme("Primary Window", window_theme_id)

dpg.create_viewport(title='Japanese Learning', small_icon=icon_path, large_icon=icon_path, width=665, height=340, resizable=True, vsync=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
