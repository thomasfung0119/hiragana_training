def load_themes(dpg):
    """
    Load custom themes for the Dear PyGui application.
    This function sets up themes for listboxes, buttons, and the main window.
    """
    
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

    return {
        "custom_listbox_theme" : custom_listbox_theme,
        "button_selected_theme" : button_selected_theme,
        "button_normal_theme" : button_normal_theme,
        "button_as_text_center_theme" : button_as_text_center_theme,
        "window_theme_id" : window_theme_id,
    }