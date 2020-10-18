# MIT License

# Copyright (c) 2020 haruna

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#https://github.com/eggplants/deepl-cli

import sys
import time
from textwrap import dedent
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class DeepLArgCheckingError(Exception):
    pass

class DeepLPageLoadError(Exception):
    pass

class DeepL:
    def __init__(self,text,src_lang,dest_lang):
        self.src_lang=src_lang
        self.dest_lang=dest_lang
        self.text=text

    def internet_on(self):
        """Check an internet connection."""

        try:
            response = urlopen('https://www.google.com/', timeout=10)
            return True
        except:
            return False

    def validate(self):
        """Check cmdarg and stdin."""

        fr_langs = {'', 'auto', 'ja', 'en', 'de', 'fr', 'es', 'pt', 'it', 'nl', 'pl', 'ru', 'zh'}
        to_langs = fr_langs - {'', 'auto'}

        if self.src_lang == self.dest_lang:
            # raise err if <fr:lang> == <to:lang>
            raise DeepLArgCheckingError('Two languages cannot be same.')

        if len(self.text) > 5000:
            # raise err if stdin > 5000 chr
            raise DeepLArgCheckingError('limit of script is less than 5000 chars(Now: %d chars).'%len(self.text))

        self.fr_lang = ('auto' if   self.src_lang[0] == ''
                               else self.src_lang[0]
                       )[0]
        self.to_lang = self.dest_lang

    def translate(self):
        """Open a deepl page and throw a request."""

        if not self.internet_on():
            raise DeepLPageLoadError('Your network seem to be offline.')

        self.validate()
        
        o = Options()
        # o.binary_location = '/usr/bin/google-chrome'
        o.add_argument('--headless')    # if commented. window will be open
        o.add_argument('--disable-gpu')
        o.add_argument('--disable-dev-shm-usage')
        o.add_argument('--remote-debugging-port=9222')
        o.add_argument('--disable-setuid-sandbox')
        o.add_argument('--user-agent='\
            'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) '\
            'AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1'
        )

        d = webdriver.Chrome(
             executable_path="D:/Programs/chromedriver.exe",
             options=o
        )
        d.get('https://www.deepl.com/translator#%s/%s/_'%(self.fr_lang, self.to_lang))
        try:
            WebDriverWait(d, 15).until(
                EC.presence_of_all_elements_located
            )
        except TimeoutException as te:
            raise DeepLCLIPageLoadError(te)

        input_area = d.find_element_by_xpath(
            '//textarea[@dl-test="translator-source-input"]'
        )
        input_area.clear()
        input_area.send_keys(self.text)

        # Wait for the translation process
        time.sleep(10) # fix needed

        output_area = d.find_element_by_xpath(
            '//textarea[@dl-test="translator-target-input"]'
        )
        res = output_area.get_attribute('value').rstrip()
        d.quit()
        return res
