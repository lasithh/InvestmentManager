import datetime


def saveFile(textContent, fileName, date=None, extension='txt'):
    if date is None:
        date = datetime.date.today()
    dateStr = date.strftime('_%d_%m_%Y')

    text_file = open(fileName + dateStr + '.' + extension, "w+")

    text_file.write(textContent)
    text_file.close()