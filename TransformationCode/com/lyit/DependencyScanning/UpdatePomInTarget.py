from bs4 import BeautifulSoup as beautifulSoup
import codecs

class UpdatePomInTarget:

    def update_pom(self, pom_location, service_name):
        with open(pom_location, "r") as file:
            file_content = file.readlines()
            content = "".join(file_content)
            beautify_content = beautifulSoup(content, "lxml")
            beautify_content.find('name').string = service_name

        file_pointer = codecs.open(pom_location, "w", "utf-8")
        file_pointer.write(str(beautify_content))
        file_pointer.close()
