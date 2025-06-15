def load_fonts(font, add_font_range_hint, fontRange, font_registry, ttf_path):
    """
    Load custom fonts into Dear PyGui.

    Args:
        ttf_path (str): The path to the TTF font file.
    """

    if not ttf_path:
        raise ValueError("Font path cannot be empty.")

    if not isinstance(ttf_path, str):
        raise TypeError("Font path must be a string.")

    if not ttf_path.endswith('.ttf'):
        raise ValueError("Font file must have a .ttf extension.")
    
    
    # Create a font registry context
    with font_registry:
        with font(ttf_path, 50, default_font=False) as title_font:
            add_font_range_hint(fontRange)

        with font(ttf_path, 20, default_font=True) as default_font:
            add_font_range_hint(fontRange)
    
    return {
        "title_font": title_font,
        "default_font": default_font
    }