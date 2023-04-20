url = "http://632b-34-172-43-2.ngrok-free.app"

COLORS = [
    # 17 undertones https://lospec.com/palette-list/17undertones
    '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

button_style = '''
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007AFF, stop:1 #3F51B5);
    border-radius: 15px;
    color: white;
    font-size: 16px;
    padding: 10px 20px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1A8FFF, stop:1 #606FCA);
}
QPushButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0066CC, stop:1 #2B3E87);
}
'''

imagebox_style = ("""
    background-image: url("./bkgrnd.png");
    border: none;
    border-radius: 10px;
    padding: 20px;
""")
imagebox_style_2 = ("""
    background-image: url("./yellow_bkgrnd.jpg");
    border: none;
    border-radius: 10px;
    padding: 20px;
""")

Tab_StyleSheet = ("""
            QTabBar::tab {
                background-color: #222;
                color: red;
                height: 60px;
                width: 150px;
                font-size: 15px;
                padding-left: 10px;
                padding-right: 10px;
                margin-top: 15px;
                margin-bottom: -1px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }

            QTabBar::tab:selected {
                background-color: #FFF;
                color: #222;
            }

            QTabBar::tab:!selected {
                margin-top: 15px;
                margin-bottom: -1px;
                background-color: #444;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }

            QTabBar::tab:hover {
                background-color: #555;
            }

            QTabBar::tab:selected {
                border-color: #9B9B9B;
                border-bottom-color: #FFF;
            }
        """)
