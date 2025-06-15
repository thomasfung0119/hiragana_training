import PyInstaller.__main__

PyInstaller.__main__.run([
    r'hiragana_training\__main__.py',
    r'--onefile',
    r'--nowindowed'
])