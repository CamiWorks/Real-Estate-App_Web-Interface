import os
import re
import all_templates
from geo import set_geolocation
from geo import set_geolocation_area

# from real_estate import get_commercial_estate # Still checking for implementation.
from real_estate import get_demographic_information
from real_estate import get_residential_estate
from real_estate import get_scores_information


def main():
    users_address = input("Address: ")
    my_report = Report(users_address)
    my_report.creating_web_report()


class Report:
    def __init__(self, address: str) -> None:
        self.address = address
        self.pin_point = set_geolocation(address)
        self.area_point = set_geolocation_area(self.pin_point[0], self.pin_point[1])
        self.folder_name = address.replace(" ", "_").strip()
        self.folder_name = self.folder_name.replace(",", "")
        self.folder_name = f"REPORT_{self.folder_name}"

    # DEMOGRAPHICS DATA PROCESSING

    def demogra_data(self) -> dict:
        self.geo_info = get_demographic_information(
            self.pin_point[0], self.pin_point[1]
        )
        x = self.geo_info["data"]["attributes"]
        # Dictionary of data
        self.geo_data = {}

        for _ in x.values():
            header = _["category_name"]["en"]
            if header == "Mother tongue":
                break
            data_variables_titles = _["variables"]
            self.geo_data[header] = []
            for _ in data_variables_titles.values():
                section_title = _["name"]["en"]
                section_data = _["value"]
                self.geo_data[header].append(
                    fix_order_of_data(section_title, section_data)
                )
        print("Geo pulled Successfully")

    # PIN-POINT SCORE PROCESSING DATA

    def average_sectore_score(self) -> float:
        self.score_data = get_scores_information(self.pin_point[0], self.pin_point[1])
        values_sum = []
        list_scores = self.score_data["data"]["attributes"]
        for _ in list_scores.values():
            if _["value"] == int:
                change = float(_["value"])
                values_sum.append(change)
            else:
                values_sum.append(_["value"])
        self.final_score_listing = sum(values_sum) / len(values_sum)
        print(f"Score pulled Successfully")

    # RESIDENTIAL DATA PROCESSING LISTING

    def residential_list(self) -> list:
        self.residential_data = get_residential_estate(
            self.area_point[0],
            self.area_point[1],
            self.area_point[2],
            self.area_point[3],
        )
        my_prices = []
        my_list = self.residential_data["Results"]
        for i in range(len(my_list)):
            my_prices.append(my_list[i]["Property"]["Price"])
        index = 0
        for price in my_prices:
            price = price.replace("$", "").replace(",", "")
            x = re.search(r"[1-9]+,*[0-9]*", price)
            my_prices[index] = x.group(0)
            my_prices[index] = int(my_prices[index])
            index = index + 1
        self.final_price_listing = sum(my_prices) / len(my_prices)
        print(f"Listing pulled Successfully")

    # CREATING THE WEB REPORT

    def creating_web_report(self):
        self.residential_list()
        self.average_sectore_score()
        self.demogra_data()
        self.address
        self.final_js = ""
        html_data = ""
        js_function_name = ""

        def js_string():
            with open("script_template.txt", "r") as jsFile:
                js_text = jsFile.read()
                return js_text

        for header in self.geo_data:

            reader = js_string()

            if header.lower() == "income":
                reader = reader.replace("(CHART_TYPE)", "ColumnChart")
            else:
                reader = reader.replace("(CHART_TYPE)", "PieChart")

            reader = reader.replace("(TITLE_OF_THE_CHART)", header)
            html_header = header.replace(" ", "_")
            reader = reader.replace("(HTML_ID_CHART)", f"{html_header}_id")
            html_data += f'<div id="{html_header}_id"></div>'
            js_function_name = f"{html_header}_f"
            reader = reader.replace("#FUNTION_NAME#", js_function_name)

            data_container = []

            for data in self.geo_data[header]:
                for _ in data:
                    data_container.append([_, data[_]])
            reader = reader.replace("(DATA_CONTENT_PAIRS)", str(data_container))
            self.final_js += reader

        # Create the folder
        os.makedirs(self.folder_name, exist_ok=True)

        # Create and write to the text file
        file_path = os.path.join(self.folder_name, "script.js")

        with open(file_path, "w") as file:
            file.write(
                "google.charts.load('current', {'packages':['corechart']});"
                + self.final_js
            )

        # Create and write to the text file
        file_path = os.path.join(self.folder_name, "index.html")

        with open(file_path, "w") as htmlFile:
            html = all_templates.html()
            html = html.replace(
                "(TITLE_REPORT)", all_templates.html_title(self.address)
            )
            html = html.replace("(CONTENT_DEMOGRAPHICS)", html_data)
            html = html.replace(
                "(LISTING_REPORT)",
                f"<h3>Average price of a home is:</h3><p><span>${'{:,}'.format(round(self.final_price_listing, 2))}</span></p>",
            )
            html = html.replace(
                "(SCORE_REPORT)",
                f"<h3>The overall score for residential property is:</h3><p><span>{round(self.final_score_listing, 1)} / 5</span></p>",
            )
            htmlFile.write(html)

        # Create and write to the text file
        file_path = os.path.join(self.folder_name, "styles.css")

        with open(file_path, "w") as cssFile:
            cssFile.write(all_templates.css_tempalte())

        self.__str__()

    # SUCCESS

    def __str__(self) -> str:
        print(f"Your report is ready !!!")


# Fixing order of data
def fix_order_of_data(a, b) -> dict:
    if type(a) == type("string"):
        return {a: b}
    else:
        return {b: a}


if __name__ == "__main__":
    main()
