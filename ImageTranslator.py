import cv2
import pytesseract
import numpy as np
import io
import craft_text_detector as craft_detector
from text_binarization import textBin 

from PIL import ImageGrab
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from googletrans import Translator

import urllib

pytesseract.pytesseract.tesseract_cmd = 'D:/Programs/tesseract-ocr/tesseract.exe'
tra =Translator()
EASYOCR =[
    'abq',#Abaza
    'ady',#Adyghe
    'af',#Afrikaans
    'ang',#Angika
    'ar',#Arabic
    'as',#Assamese
    'ava',#Ar
    'az',#Azerbaijani
    'be',#Belarusian
    'bg',#Bulgarian
    'bh',#Bihari
    'bho',#Bhojpuri
    'bn',#Bengali
    'bs',#Bosnian
    'ch_sim',#Simplified Chinese
    'ch_tra',#Traditional Chinese
    'che',#Chechen
    'cs',#Czech
    'cy',#Welsh
    'da',#Danish
    'dar',#Dargwa
    'de',#German
    'en',#English
    'es',#Spanish
    'et',#Estonian
    'fa',#Persian (Farsi)
    'fr',#French
    'ga',#Irish
    'gom',#Goan Konkani
    'hi',#Hindi
    'hr',#Croatian
    'hu',#Hungarian
    'id',#Indonesian
    'inh',#Ingush
    'is',#Icelandic
    'it',#Italian
    'ja',#Japanese
    'kdb',#Kabardian
    'ko',#Korean
    'ku',#Ku#rdish
    'la',#Latin
    'lbe',#Lak
    'lez',#Lezghian
    'lt',#Lithuanian
    'lv',#Latvian
    'mah',#Magahi
    'mai',#Maithili
    'mi',#Maori
    'mn',#Mongolian
    'mr',#Marathi
    'ms',#Malay
    'mt',#Maltese
    'ne',#Nepali
    'new',#Newari
    'nl',#Dutch
    'no',#Norwegian
    'oc',#Occitan
    'pl',#Polish
    'pt',#Portuguese
    'ro',#Romanian
    'ru',#Russian
    'rs_cyrillic',#Serbian (cyrillic)
    'rs_latin',#Serbian (latin)
    'sck',#Nagpuri
    'sk',#Slovak 
    'sl',#Slovenian
    'sq',#Albanian
    'sv',#Swedish
    'sw',#Swahili
    'ta',#Tamil
    'tab',#Tabassaran
    'th',#Thai
    'tl',#Tagalog
    'tr',#Turkish
    'ug',#Uyghur
    'uk',#Ukranian
    'ur',#Urdu
    'uz',#Uzbek
    'vi'#Vietnamese 

]

OCR_LANG={
            #Tesseract #EasyOCR
    'afr': ['afr']            #Afrikaans
    'amh': ['amh']              #Amharic
    'ara': ['ara']              #Arabic
    'asm': ['asm']             #Assamese
    'aze': ['aze']              #Azerbaijani
    'aze_cyrl': ['aze_cyrl']         
    'bel': ['bel']              #Belarusian
    'ben': ['ben']              #Bengali
    'bod': ['bod']              #Tibetan
    'bul': ['bul']              #Bulgarian
    'cat': ['cat']              #Catalan
    'ceb': ['ceb']              #Cebuano 
    'ces': ['ces']              #Czech
    'chi_sim': ['chi_sim']           #Chinese
    'chi_sim_vert': ['chi_sim_vert'] #Vertical Chinese
    'chi_tra':['chi_tra']           #Traditional Chinese 
    'chi_tra_vert': ['chi_tra_vert']#Traditional Chinese verctical 
    'chr': ['chr']             #Cherokee
    'cos': ['cos']             #Corsican
    'sim': ['sim']             #Mende (Papua New Guinea)
    'dan': ['dan']             #Danish
    'deu': ['deu']             #German
    'div': ['div']             #Divehi
    'dzo': ['dzo']             #Dzongkha
    'ell': ['ell']             #Mordern Greek
    'eng': ['eng']            #English
    'enm': ['enm']             #Middle English
    'est': ['est']             #Estonian
    'eus': ['eus']             #Basque
    'fao': ['fao']             #Faroese
    'fas': ['fas']             #Persian
    'fin': ['fin']             #Finnish
    'fra': ['fra']            #French
    'frk': ['frk']             #Frankish 
    'frm': ['frm']            #Middle French
    'fry': ['fry']             #Western Frisian
    'gla': ['gla']             #Scottish Gaelic
    'gle': ['gle']             #Irish
    'glg': ['glg']             #Galician
    'grc': ['grc']             #Ancient Greek
    'quj': ['quj']             #Gujuarati
    'hat': ['hat']             #Haitian
    'heb': ['heb']             #Hebrew
    'hin': ['hin']             #Hindi
    'hrv': ['hrv']             #Croatian
    'hun': ['hun']             #Hungarian
    'hye': ['hye']             #Armenian
    'iku': ['iku']             #Inuktitut 
    'ind': ['ind']             #Indonesian
    'isl': ['isl']             #Icelandic
    'ita': ['ita']             #Italian
    'ita_old': ['ita_old']      #Old Italian
    'jav': ['jav']              #Javanese
    'jpn': ['jpn']              #Japanese
    'jpn_vert': ['jpn_vert']    #Vertcial Japanese
    'kan': ['kan']             #Kannada
    'kat': ['kat']             #Georgian
    'kat_old': ['kat_old']     #Old Georgian
    'kaz': ['kaz']             #Kazakh
    'khm': ['khm']             #Khmer
    'kir': ['kir']             #Kirghiz 
    'kmr': ['kmr']             #Northern Kurdish
    'kor': ['kor']             #Korean
    'kor_vert': ['kor_vert']   #Vertical Korean
    'lao': ['lao']             #Lao
    'lat': ['lat']             #Latin
    'lav': ['lav']             #Latvian
    'lit': ['lit']             #Lithuanian 
    'ltz': ['ltz']            #Luxembourgish 
    'mal': ['mal']             #Malayalam 
    'mar': ['mar']             #Marathi 
    'mkd': ['mlt']            #Macedonian 
    'mlt': ['mlt']             #Maltese 
    'mon': ['mon']            #Mongolian 
    'mri': ['mri']             #Maori 
    'msa': ['msa']             #Malay 
    'mya': ['mya']             #Burmese 
    'nep': ['nep']             #Nepali 
    'nld': ['nld']             #Dutch
    'nor': ['nor']             #Norvegian
    'oci': ['oci']             #Occitan 
    'ori': ['ori']             #Oriya 
    'pan': ['pan']             #Panjabi 
    'pol': ['pol']             #Polish 
    'por': ['por']            #Portuguese 
    'pus': ['pus']             #Pushto 
    'que': ['que']             #Quechua 
    'ron': ['ron']             #Romanian 
    'rus': ['rus']             #Russian
    'san': ['san']             #Sanskrit 
    'sin': ['sin']             #Sinhala 
    'slk': ['slk']             #Slovak 
    'slv': ['slv']             #Slovenian 
    'snd': ['snd']            #Sindhi 
    'spa': ['spa']             #Spanish 
    'spa_old': ['spa_old']      #Old Spanish
    'sqi': ['sqi']             #Albanian 
    'srp': ['srp']             #Serbian 
    'srp_latn': ['srp_latn']   #Latin Serbian
    'sun': ['sun']              #Sundanese 
    'swa': ['swa']             #Swahili 
    'swe': ['swe']             #Swedish
    'syr': ['syr']             #Syriac 
    'tam': ['tam']             #Tamil
    'tat': ['tat']             #Tatar
    'tel': ['tgk']             #Telugu
    'tgk': ['tgk']             #Tajiik
    'tha': ['tha']             #Thai 
    'tir': ['tir']             #Tigrinya 
    'ton': ['ton']             #Tonga 
    'tur': ['tur']             #Turkish 
    'uig': ['uig']             #Uighur 
    'ukr': ['ukr']             #Ukrainian 
    'urd': ['urd']             #Urdu
    'urb': ['urb']             #Urubú-Kaapor
    'uzb_cyrl': ['uzb_cyrl']   #Cyrillic Urubú-Kaapor
    'vie': ['vie']              #Vietnamese 
    'yid': ['yid']             #Yiddish 
    'yor': ['yor']             #Yoruba 
}

class ImageTranslator():
    """
    The main class of the translator 
    
    Args: img This can be file,bytes or URL
        ocr: 'EasyOCR' or 'Tesseract'
    """
    def __init__(self,img,ocr):

        self.img= self.__reformat_input(img)
        self.img_out=self.img.copy()
        self.text=[]
        self.mask_paragraph=None
        self.ocr=ocr

    def processing(self):
        self.mask_paragraph=self.__detect_text(self.img)
        paragraphs=self.__detect_paragraph()
        #Apply Binarization and ocr
        for paragraph in paragraphs:
            binary=textBin(paragraph['image'])
            paragraph['image']=binary.processing()

            self.text.append(self.__run_ocr(paragraph))

        for i in range(0,len(self.text)):
            x=self.text[i]['x']
            y=self.text[i]['y']
            w=self.text[i]['w']
            h=self.text[i]['h']
            if self.text[i]['string'] !='':
                cv2.rectangle(self.img_out, (x,y), (x+w, y+h), (255, 255,255), -1)
                self.text[i]=self.__translate_text(self.text[i])
                self.__apply_translation(self.text[i])


    def __detect_text(self,img):
        """
        Return a mask from the text location
        """
        blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
        prediction_result=self.__craft(img)
        boxes=prediction_result['boxes']

        for box in boxes:
            point1=tuple(box[0])
            point2=tuple(box[2])
            cv2.rectangle(blank_image, point1, point2, (255,255,255), -1)

        return blank_image

    def __detect_paragraph(self):
        """
        Return a dict with cropped paragraph and location
        """
        paragraph=[]
        img=self.img.copy()

        #Find contours
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))  
        dilated = cv2.dilate(cv2.cvtColor(self.mask_paragraph,cv2.COLOR_BGR2GRAY), kernel, iterations=9) 
        contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        for contour in contours:

            [x, y, w, h] = cv2.boundingRect(contour)
            cropped=img[y :y +  h , x : x + w]

            cropped=cv2.bitwise_and(cropped,self.mask_paragraph[y :y +  h , x : x + w])

            #Apply binarization
            paragraph.append({
                'image':cropped,
                'x':x,
                'y':y,
                'w':w,
                'h':h
            })
            return paragraph
        
    def __run_ocr(self,paragraph):
        """
        Run OCR between Tesseract and EasyOCR
        """
        if self.ocr=='EasyOCR':
            return self.__run_easyocr(paragraph)
        elif self.ocr=='Tesseract':
            return self.__run_tesserract(paragraph)

    def __run_tesserract(self,paragraph):
        """
        Run tesseract OCR
        """
        boxes = pytesseract.image_to_data(paragraph['image'])
        string=''
        x,y,w,h=(0,0,0,0)
        first=True
        for a,b in enumerate(boxes.splitlines()):
            if a!=0:
                b = b.split()
                if len(b)==12: 
                    if first== True:
                        x=int(b[6])
                        y=int(b[7])
                        w =int(b[8])
                        h =int(b[9])
                        first=False
                    string=string +str(b[11])+' '
        return {
                'x':x+paragraph['x']-45,
                'y':y+paragraph['y']-20,
                'w':w,
                'h':h,
                'string':string,
                'image': paragraph['image'],
                'max_width':paragraph['w']
                }
    def __run_easyocr(self,paragraph):
        """
        Run EasyOCR
        """
        reader = easyocr.Reader(['en'])
        result = reader.readtext(paragraph['image'])
        #1|----------------------------|2
        # |                            |
        #4|----------------------------|3
        #[[[x1,y1],[x2,y2][x3,y3],[x4,y4],'I am currently working in an image translator project.'],0.031xxx]
        x=result[0][0][0][0]
        y=result[0][0][0][1]
        w=result[0][0][2][0]-x
        h=result[0][0][2][1]-y
        string=''
        for res in result:
            string+=res[1]
        return {
            'x':x+paragraph['x']-45,
            'y':y+paragraph['y']-20,
            'w':w,
            'h':h,
            'string':string,
            'image':paragraph['image'],
            'max_width':paragraph['w']

        }

    def __craft(self,img):
        """
        Return a predication of text location
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if img.shape[0] == 2:
            img = img[0]
        if img.shape[2] == 4:
            img = img[:, :, :3]

        refine_net= craft_detector.load_refinenet_model(cuda=False)
        craft_net = craft_detector.load_craftnet_model(cuda=False)
        prediction_result = craft_detector.get_prediction(image=img,craft_net=craft_net,
        refine_net=refine_net,text_threshold=0.7,link_threshold=0.4,low_text=0.4,cuda=False,
        long_size=1280) 

        return prediction_result

    def __reformat_input(self,image):
        """
        Reformat the input image
        """
        if type(image) == str:
            if image.startswith('http://') or image.startswith('https://'):
                #Read bytes from url
                image=urllib.request.urlopen(image).read()

            nparr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif type(image) == np.ndarray:
            if len(image.shape) == 2: 
                img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif len(image.shape) == 3 and image.shape[2] == 3:
                img = image
            elif len(image.shape) == 3 and image.shape[2] == 4:
                img = image[:,:,:3]
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            print('[Warning] Invalid input type. Suppoting format = string(file path or url), bytes, numpy array')
        return img

    def __text_wrap(text, font, max_width):
        """
        Wrap the into multiple lines
        """
        lines = []
        # If the width of the text is smaller than image width
        # we don't need to split it, just add it to the lines array
        # and return
        if font.getsize(text)[0] <= max_width:
            lines.append(text) 
        else:
            # split the line by spaces to get words
            words = text.split(' ')  
            i = 0
            # append every word to a line while its width is shorter than image width
            while i < len(words):
                line = ''         
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                # when the line gets longer than the max width do not append the word, 
                # add the line to the lines array
                lines.append(line)    
        return lines

    def __translate_text(self,text):
        """
        Translate the text
        """
        string= tra.translate(text['string'],dest='fr').text

        text['translated_string']=string
        return text
    
    def __apply_translation(self,text):
        """
        Apply the translation on img_out
        """

        im_pil = Image.fromarray(self.img_out)
        draw = ImageDraw.Draw(im_pil)

        font_file_path = 'Cantarell.ttf'
        font_size=int(h*1.1)
        font = ImageFont.truetype(font_file_path, size=font_size, encoding="unic")

        lines = text_wrap(text['translated_string'], font,text['max_width'])
        line_height = font.getsize('hg')[1]
        for line in lines:
            draw.text((text['x'], text['y']), line, fill=(0,0,0), font=font)
            y = y + line_height
        self.img_out = np.asarray(im_pil)



test=ImageTranslator('https://i.stack.imgur.com/vrkIj.png','Tesseract')
test.processing()

