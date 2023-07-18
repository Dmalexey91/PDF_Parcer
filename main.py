import fitz, pytesseract, cv2, os

def GetFilelist(ext):
    Filelist = []
    for file in os.listdir(directory):
        if file.endswith(ext):
            Filelist.append(file)
    return Filelist

def extract_text(doc):
    Text = ''
    for current_page in range(len(doc)):
        page = doc.load_page(current_page)
        page_text = page.get_text("text")
        if page_text != '':
            Text += "Стр. " + str((current_page + 1)) + "\nСодержание;\n\n" + page_text
    return Text

def extract_image(doc, fitz):
    page_count = 0
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.colorspace == None:
                continue
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            path = Folderdict[doc.name]
            filename = 'Image_'+str(img[0])+'.jpg'
            pix1.save(path+'\\'+filename)
            page_count += 1
    return True

def recognitiontext(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    CombText = ''
    for image in os.listdir(path):
        if image.endswith('jpg') or image.endswith('jpeg'):
            try:
                fullpath = path+'\\'+image
                image = cv2.imread(fullpath)
                string = pytesseract.image_to_string(image, lang='rus')
                CombText = CombText + string
            except:
                print('Не удалось распознать изображение: '+str(image))
    return CombText

#Основной исполняемый код
directory = 'C:\Temp' #Вынести в переменные окружения, чтобы запускать из вне
if directory != '':
    #1. Получаем список всех PDF в указанном каталоге
    PDFFilelist = GetFilelist('pdf')
    Folderdict = {}

    DocCount = 0
    for file in PDFFilelist:
        pdf_document = directory + '\\' + file
        doc = fitz.open(pdf_document)

        # Создаём папку для каждого файла
        path = doc.name[0: -4]
        if not os.path.exists(path):
            os.makedirs(path)
        Folderdict[doc.name] = path

        #2. Вытаскиваем текст из картинок
        if 1==1:
            ResultExtImage = extract_image(doc, fitz)  # Извлекаем фотографии из файла
            #ResultExtImage = False
            if ResultExtImage:
                CombText = recognitiontext(path)
                if CombText != '':
                    with open(path+"\\TextFromImages.txt", "w") as output:
                        output.write(CombText)
            else:
                print('Для документа '+doc.name+' не удалось распознать изображения')

        #3. Вытаскиваем простой текст
        if 1==1:
            Text = extract_text(doc)
            if Text != '':
                with open(path + "\\Text.txt", "w") as output:
                    output.write(Text)

        DocCount += 1
        print('Обработано файлов: '+str(DocCount))