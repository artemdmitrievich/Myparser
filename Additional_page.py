from Main_info_crypto_parser import Additional_CoinGecko_info


class Additional_page:

    # Функция обновления страницы additional
    def _Update_additional_page(self):
        Current_additional = Additional_CoinGecko_info()

        # Обновление таблицы криптовалют, с наибольшим ростом
        Current_greatest_growth_crypto = Current_additional.get_greatest_growth_crypto()
        # Обновление названий
        if len(Current_greatest_growth_crypto[0][0][0]) > 16:
            self.Max_growth_name_label_1.setText(
                Current_greatest_growth_crypto[0][0][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_1.setText(
                " " * ((30 - len(Current_greatest_growth_crypto[0][0][0])) // 2)
                + Current_greatest_growth_crypto[0][0][0]
            )
        if len(Current_greatest_growth_crypto[0][1][0]) > 16:
            self.Max_growth_name_label_2.setText(
                Current_greatest_growth_crypto[0][1][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_2.setText(
                " " * ((30 - len(Current_greatest_growth_crypto[0][1][0])) // 2)
                + Current_greatest_growth_crypto[0][1][0]
            )
        if len(Current_greatest_growth_crypto[0][2][0]) > 16:
            self.Max_growth_name_label_3.setText(
                Current_greatest_growth_crypto[0][2][0][0:15] + "..."
            )
        else:
            self.Max_growth_name_label_3.setText(
                " " * ((30 - len(Current_greatest_growth_crypto[0][2][0])) // 2)
                + Current_greatest_growth_crypto[0][2][0]
            )
        # Обновление времени
        self.Max_growth_time_label_1.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        self.Max_growth_time_label_2.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        self.Max_growth_time_label_3.setText(
            " " * 12 + Current_greatest_growth_crypto[1]
        )
        # Обновление стоимости
        self.Max_growth_cost_label_1.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][0][1]
        )
        self.Max_growth_cost_label_2.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][1][1]
        )
        self.Max_growth_cost_label_3.setText(
            " " * 8 + "$ " + Current_greatest_growth_crypto[0][2][1]
        )
        # Обновление увеличения
        self.Max_growth_change_label_1.setText(
            " " * 7 + Current_greatest_growth_crypto[0][0][2]
        )
        self.Max_growth_change_label_2.setText(
            " " * 7 + Current_greatest_growth_crypto[0][1][2]
        )
        self.Max_growth_change_label_3.setText(
            " " * 7 + Current_greatest_growth_crypto[0][2][2]
        )

        # Обновление таблицы самых популярных криптовалют
        Current_popular_crypto = Current_additional.get_popular_crypto()
        # Обновление названий
        if len(Current_popular_crypto[0][0][0]) > 16:
            self.Popular_name_label_1.setText(
                Current_popular_crypto[0][0][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_1.setText(
                " " * ((30 - len(Current_popular_crypto[0][0][0])) // 2)
                + Current_popular_crypto[0][0][0]
            )
        if len(Current_popular_crypto[0][1][0]) > 16:
            self.Popular_name_label_2.setText(
                Current_popular_crypto[0][1][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_2.setText(
                " " * ((30 - len(Current_popular_crypto[0][1][0])) // 2)
                + Current_popular_crypto[0][1][0]
            )
        if len(Current_popular_crypto[0][2][0]) > 16:
            self.Popular_name_label_3.setText(
                Current_popular_crypto[0][2][0][0:15] + "..."
            )
        else:
            self.Popular_name_label_3.setText(
                " " * ((30 - len(Current_popular_crypto[0][2][0])) // 2)
                + Current_popular_crypto[0][2][0]
            )
        # Обновление времени
        self.Popular_time_label_1.setText(" " * 12 + Current_popular_crypto[1])
        self.Popular_time_label_2.setText(" " * 12 + Current_popular_crypto[1])
        self.Popular_time_label_3.setText(" " * 12 + Current_popular_crypto[1])
        # Обновление стоимости
        self.Popular_cost_label_1.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][0][1]
        )
        self.Popular_cost_label_2.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][1][1]
        )
        self.Popular_cost_label_3.setText(
            " " * 8 + "$ " + Current_popular_crypto[0][2][1]
        )
        # Обновление значений изменения стоимости
        self.Popular_change_label_1.setText(" " * 7 + Current_popular_crypto[0][0][2])
        self.Popular_change_label_2.setText(" " * 7 + Current_popular_crypto[0][1][2])
        self.Popular_change_label_3.setText(" " * 7 + Current_popular_crypto[0][2][2])
        # Вызов функции для обновления иконок и стилей у самых популярных криптовалют
        self.__Create_Icon_and_Style(Current_popular_crypto)

    # Обновляет иконки и стили у самых популярных криптовалют
    def __Create_Icon_and_Style(self, Current_popular_crypto):
        if Current_popular_crypto[0][0][3] == "down":
            self.Popular_change_label_1.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_1.setIcon(self.Icon_trending_down)
        if Current_popular_crypto[0][1][3] == "down":
            self.Popular_change_label_2.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_2.setIcon(self.Icon_trending_down)
        if Current_popular_crypto[0][2][3] == "down":
            self.Popular_change_label_3.setStyleSheet(
                "color: rgb(255,0,0);\n"
                "font-size: 16px;\n"
                "font-weight: bold;\n"
                "background-color: rgb(157, 0, 255);"
            )
            self.Popular_Icon_Button_3.setIcon(self.Icon_trending_down)
