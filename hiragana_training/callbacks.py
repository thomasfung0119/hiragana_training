import dearpygui.dearpygui as dpg
from biased_random_selector import BiasedRandomSelector
from datetime import datetime
from pyautogui import press
from data_file_manipulation import save_to_json
from os import rmdir

def remove_and_quit(sender, app_data, user_data):
    try:
        rmdir(user_data)
        print(f"Directory '{user_data}' removed successfully.")
    except OSError as e:
        print(f"Error removing directory '{user_data}': {e}")
    dpg.destroy_context()
    dpg.stop_dearpygui()  

def start_quiz(options, options_to_dictionary, training_records, data_file, themes):
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

    dpg.bind_item_theme("Quiz Window", themes["window_theme_id"])

def start_review(training_records, themes, fonts):
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
        dpg.bind_item_theme("Review Window Content", themes["button_as_text_center_theme"])

        dpg.add_button(label="", tag="Review Title", width=-1, height=60, pos=(0, 0))
        dpg.bind_item_font("Review Title", fonts["title_font"])
        dpg.bind_item_theme("Review Title", themes["button_as_text_center_theme"])
        
        dpg.add_button(label="<", width=33, pos=(10, 130), callback=last_callback, tag="Last Button")
        dpg.add_button(label=">", width=33, pos=(457, 130), callback=next_callback, tag="Next Button", show=False)
        dpg.add_button(label="返回主頁", width=100, pos=(390, 262), callback=exit_callback)
    dpg.bind_item_theme("Review Window", themes["window_theme_id"])
    create_review(training_records[pointer])
