"""
///
APP:
Поиск картинок: просто брать дефолтные директории


////////
ROADMAP:
Добавить поддержку поиска файлов в:
- Gallery/Downloads
- VK (брать все файлы из VK/Downloads и com.vkontakte.android и проверять их на дубли)
- WHATSAPP
- TELEGRAM (брать все файлы из файловой системы и брать все файлы из папки Telegram/images и проверять их на дубли)

* и все это сравнить с файлами в папках (DCIM/Pictures/Downloads)
* DEFAULT_DIR_NAMES cюда нужно как то добавить видимые сходу директории (Telegram/Telegram Images, VK/...) и удалить директорию 
Telegram из аттрибута _default_images_dirs

Добавить опции:
- * возможность выбирать опционально в каких дефолтных директориях искать (к примеру искать только в галерее , не затрагивая мессенджеры)
- * самоунтичтожение программы из системы

- поиск по регулярке
- указание кастомных директорий



///////////////////
ПРОИЗВОДИТЕЛЬНОСТЬ:
1. Есть ли смысл в методе _recognize_files_type() сменить добавление в список на добавление в какую нибудь более производительную структуру данных.
2. Попробовать переписать классы на dataclassses


/////
BUGS:
1. Изменить название всех переменных , которые называются dir на другое , т.к. это встроенная функция самого языка.

////////////////
IMAGES SEARCHER:
1. Сделать соотношение удаленных файлов к папкам. 
(Это делается через словари , т.е. {telegram: (<files>), gallery: (<files>)})

2. Сделать ассоциацию файлов галлереи, картинок и 

/////////////
RESTORE DATA:

"""

t = [(1, 2), (3, 4)]

for a, b in t:
    print(a, b)


