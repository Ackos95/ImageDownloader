#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2


class ArgumentException(Exception):
    """ Derived Exception class (used in internal class) """

    pass


class ImageDownloader:
    """ ImageDownloader class, should be main class for web scraping (NOT FINISHED) """

    _target_url = ""
    _target_folder = ""
    __target_tag = ""

    def __init__(self, url, folder):
        raise NotImplemented()
        self._target_url = url
        self._target_folder = folder
        self.__target_tag = self.__TagGenerator()

    def download_images(self):
        raise NotImplemented()
        url = urllib2.urlopen(self._target_url)
        f = file("test_parser.txt", 'w')
        html_text = url.read()
        f.write(html_text)
        f.close()
        for image in re.finditer(self.__target_tag.get_regex(), html_text):
            print
            print image.group(1) if image.group(1) is not None else image.group(2)


    class __TagGenerator:
        """
            Inner private class __TagGenerator

            This class is constructed in order to create regex expression for html parsing.
            It is designed not to have many "outworld" connections and interactions, but
            that it can be fairly easily modified so that it provides more outworld interactions
            (e.g. not to search only for <img> tags and "src", "orig" and "class" atributes).

            I realize that it would be much easier just to type in regex as a string, but this way
            I ensured that this code may be reused (more generic code).

            Use:
                obj = __TagGenerator("class_name") # class_name if you want to filter tags
                obj.get_regex() # which will return regex object

            @author Acko
        """

        # public constants
        OR = "|"
        EMPTY = ""
        ANYTHING = ".+"
        LAZY = "?"
        NOT_VISIBLE = 0
        VISIBLE = 1
        NO_CONTENT = ".+?"

        # private strings
        __source_group = "" # "(?:(?:src)|(?:orig)-\"(.+?)\")"
        __class_group = ""
        __main_re = ""

        def __init__(self, class_name=None):
            """ 
                Constructor of class.

                It creates (hard coded...) two main regex substrings (groups), and also main regex string,
                using __create_main() method.

                params:
                    class_name -> (string) filter for img tags, default None
            """

            # r"(?:(?:(?:src)|(?:orig))=\"(.+?)\")"
            self.__source_group = self.__create_group([self.__create_group([self.__create_group(["src"], []), self.__create_group(["orig"], [])], [self.OR]), \
                                                            "=\"", self.__create_group([self.NO_CONTENT], [], self.VISIBLE), "\""], \
                                                        [self.EMPTY, self.EMPTY, self.EMPTY])
            # r"(?:class=\"(?:{{class}})\")"
            self.__class_group = None if class_name is None \
                                    else self.__create_group(["class=\"", self.__create_group([class_name], []), "\""], \
                                                            [self.EMPTY, self.EMPTY])
            self.__main_re = self.__create_main()

        def __create_group(self, group_content, group_binder, visibility=NOT_VISIBLE):
            """
                Private method for building regex-valid string group representation.

                params:
                    group_content -> (list) should contain all elements of a group in string representation,
                                        either in group shape or "clean" string
                    group_binder -> (list) defines how group_content elements will be binded in group. It must
                                        contain one element less then group_content and n-th element of this list
                                        represents bind between n-th and (n + 1)-th element of group_content.
                                        Values should be constants defined in this class. (in order for this to work propertly)
                    visibility -> (int) defines if group will be returned in re.match (find...) or not. Also should be
                                        used constants from this class to ensure predictable app behaviour

                throws:
                    ArgumentException -> if lengths of group_content and group_binder does not match appropriatly

                return:
                    (string) group representation.
            """
            
            if len(group_content) - 1 != len(group_binder):
                raise ArgumentException("group_content and group_binder arrays must have n:n-1 length relation!")

            ret_string = "(" + ("?:" if visibility == self.NOT_VISIBLE else "")
            for index, content in enumerate(group_content):
                ret_string += content
                if index != len(group_content) - 1:
                    ret_string += group_binder[index]
            ret_string += ")"

            return ret_string

        def __create_main(self):
            """
                Creates main regex string expression.

                Depending on __class_group atribute it either creates all img tag search or img tag filtered by class serach.

                return:
                    (string) final regex expression representation
            """
            if self.__class_group is None:
                return self.__create_group(["<img", self.__source_group, ">"], [self.ANYTHING + self.LAZY, self.ANYTHING + self.LAZY])
            else:
                # (?:(?:s AND c)|(?:c AND s))
                return self.__create_group(["<img", self.__create_group([self.__source_group, self.__class_group], [self.ANYTHING + self.LAZY]),\
                                                self.__create_group([self.__class_group, self.__source_group], [self.ANYTHING + self.LAZY]), ">"],\
                                            [self.ANYTHING + self.LAZY, self.OR, self.ANYTHING + self.LAZY])

        def get_regex(self):
            """ Main public function, should be used from outside, it returns regex object for matching (re.match, re.find...) """

            return re.compile(self.__main_re, re.DOTALL)


if __name__ == '__main__':
    """ Testing and debugging """
#    i = ImageDownloader("http://localhost:8080/myProjects/Test/test_html.html", "")
    i = ImageDownloader("https://www.google.rs", "")
    i.download_images()