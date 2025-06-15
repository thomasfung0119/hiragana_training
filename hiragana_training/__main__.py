# import GUI library
import dearpygui.dearpygui as dpg

# Import necessary modules
from hiragana_dicts import hiragana_romaji, dakuten_hiragana_romaji, handakuten_hiragana_romaji, katakana_romaji, dakuten_katakana_romaji, handakuten_katakana_romaji
from data_file_manipulation import read_from_json, init_paths
from callbacks import start_quiz, start_review, remove_and_quit
from themes import load_themes
from fonts import load_fonts


def main():
    # Initialize paths and read training records
    paths = init_paths()
    training_records = read_from_json(paths["data_file"])
    options = {"平假名": False, "片假名": False, "濁音（平假名）": False, "濁音（片假名）": False, "半濁音（平假名）": False, "半濁音（片假名）": False}
    options_to_dictionary = {"平假名": hiragana_romaji, "片假名": katakana_romaji, "濁音（平假名）": dakuten_hiragana_romaji, "濁音（片假名）": dakuten_katakana_romaji, "半濁音（平假名）": handakuten_hiragana_romaji, "半濁音（片假名）": handakuten_katakana_romaji}

    # Create Dear PyGui context and load fonts and themes
    dpg.create_context()
    font_registry = dpg.font_registry()
    fonts = load_fonts(dpg.font, dpg.add_font_range_hint, dpg.mvFontRangeHint_Chinese_Full, font_registry, paths["font"])
    dpg.bind_font(fonts["default_font"])
    themes = load_themes(dpg)

    # Callback function for custom listbox items
    def custom_listbox_callback(sender, app_data, user_data):
        if themes["button_selected_theme"] == dpg.get_item_theme(sender):
            dpg.bind_item_theme(sender, themes["button_normal_theme"])
            options[dpg.get_item_label(sender)] = False
        else:
            dpg.bind_item_theme(sender, themes["button_selected_theme"])
            options[dpg.get_item_label(sender)] = True

    # Selection Window for different types of Japanese characters
    with dpg.window(tag="Selection Window", pos=(0, 0), width=150, height=300, no_title_bar=True, no_resize=True, no_move=True):
        dpg.add_text("練習數量:")
        dpg.add_input_int(tag="Quiz Amount", default_value=10, width=-1, readonly=False, min_value=1, min_clamped=True, max_value=100, max_clamped=True)
        dpg.add_text("練習範圍:")
        with dpg.child_window(border=False) as custom_listbox:
            for item in options.keys():
                t = dpg.add_button(label=item, width=-1, callback=custom_listbox_callback)
                dpg.bind_item_theme(t, themes["button_normal_theme"])

        dpg.bind_item_theme(custom_listbox, themes["custom_listbox_theme"])

    # Primary Window for the main interface
    with dpg.window(tag="Primary Window", pos=(150, 0), width=500, height=300, no_title_bar=True, no_resize=True, no_move=True):
        dpg.add_button(label="五十音練習！", tag="Primary Window Title", width=-1, height=100)
        dpg.bind_item_font("Primary Window Title", fonts["title_font"])
        dpg.bind_item_theme("Primary Window Title", themes["button_as_text_center_theme"])
        
        dpg.add_text("", tag="Primary Window Top Text", wrap=480)

        dpg.add_button(label="開始練習", tag="Practise Button", width=-1, callback=lambda: start_quiz(options, options_to_dictionary, training_records, paths["data_file"], themes))
        dpg.add_button(label="記録確認", tag="Review Button", width=-1, callback=lambda: start_review(training_records, themes, fonts))
        dpg.add_button(label="刪除記録", tag="Remove Button", width=-1, callback=remove_and_quit, user_data=paths["data_dir"])
        dpg.add_text("", tag="Primary Window Text", color=(255, 0, 0, 255))
        dpg.bind_item_theme("Primary Window", themes["window_theme_id"])

    # Run the Dear PyGui application
    dpg.create_viewport(title='Japanese Learning', small_icon=paths["icon"], large_icon=paths["icon"], width=665, height=340, resizable=True, vsync=True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()