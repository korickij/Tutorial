from pathlib import Path
import sys
import shutil

# функція для перекладу назви
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[c] = l
    TRANS[c.upper()] = l.upper()

    
FILE_EXT = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
	'video': ['AVI', 'MP4', 'MOV', 'MKV'],
	'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
	'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
	'archives': ['ZIP', 'GZ', 'TAR']
}  # словник для порівнянь розширень файлів
    
    
def translate(name):
    translit_name = ""
    for char in name:
        if char in TRANS:
            translit_name += TRANS[char]
        elif char.isdigit():
            translit_name += char
        elif char.isalpha() and char.isascii():
            translit_name += char    
        else:
            translit_name += "_"
    #translit_name = translit_name.translate(TRANS)
    return translit_name


def process_file_image(file_path, dest_path): 
    #print(f"Run process_file_image({file_path=}, {dest_path=})")
    dest_dir = Path(dest_path)
    dest_dir.mkdir(parents=True, exist_ok=True) 
    name, ext = file_path.stem, file_path.suffix.lower()
    new_name = translate(name) + ext
    dest_file = dest_dir / new_name
    shutil.copy(file_path, dest_file)


def process_file_videos(file_path, dest_path):
    dest_dir = Path(dest_path)
    dest_dir.mkdir(parents=True, exist_ok=True) 
    name, ext = file_path.stem, file_path.suffix.lower()
    new_name = translate(name) + ext
    dest_file = dest_dir / new_name
    shutil.copy(file_path, dest_file)

def process_file_documents(file_path, dest_path):
    dest_dir = Path(dest_path)
    dest_dir.mkdir(parents=True, exist_ok=True) 
    name, ext = file_path.stem, file_path.suffix.lower()
    new_name = translate(name) + ext
    dest_file = dest_dir / new_name
    shutil.copy(file_path, dest_file)

def process_file_audio(file_path, dest_path):
    dest_dir = Path(dest_path)
    dest_dir.mkdir(parents=True, exist_ok=True) 
    name, ext = file_path.stem, file_path.suffix.lower()
    new_name = translate(name) + ext
    dest_file = dest_dir / new_name
    shutil.copy(file_path, dest_file)  

def process_file_archives(file_path, dest_path):
    dest_dir = Path(dest_path) # створюємо об'єкт `Path` -->folder / "archives" --> /desktop/hlam/archives
    dest_dir.mkdir(parents=True, exist_ok=True) # створюємо папку /desktop/hlam/archives
    new_dir_name = translate(file_path.stem) #+ ext # нормалізуємо назву файлів
    dest_file = dest_dir / new_dir_name # створюємо шлях з новим (переведеним) іменем
    new_file_path = dest_dir / file_path.name # шлях архів в нову папку
    shutil.copy(file_path, new_file_path) # копіюємо архів в нову папку /desktop/hlam/archives/nazva_arhiva
    shutil.unpack_archive(new_file_path, dest_file)  # розпаковка 
    new_file_path.unlink() # видаляєм архів

    # тут походу треба ще весь вміст архіва нормалізувать назви??
    # тіпа пройтись ще циклом, бля.....


# def process_file_archives(file_path, dest_path):
#     dest_dir = Path(dest_path)
#     dest_dir.mkdir(parents=True, exist_ok=True)
#     name = file_path.stem
#     ext = file_path.suffix.lower()
#     new_name = translate(name) + ext
#     dest_file = dest_dir / new_name
#     shutil.copy(file_path, dest_dir)

# def process_file_unknown(file_path, dest_path):
# 	pass  


def find_files(folder, exclude_folders):
# функція що буде шукати файли в заданій папкі folder виключаю папки exclude_folders.
#     повертає список файлів.

    if not folder.exists():
        return

    result = []
    
    for item in folder.iterdir():
        if item in exclude_folders:
            continue
        
        if item.is_file():
            result.append(item)
        elif item.is_dir():
            result.extend(find_files(item, exclude_folders))
    return result
            

def delete_empty_folders(folder):
     
    for item in folder.iterdir():
        if item.is_file():
            continue
        if item.is_dir():
            delete_empty_folders(item)
            if not any (item.iterdir()):
                item.rmdir()

    
    
if __name__ == "__main__":  
    
    folder = Path(sys.argv[1])
    
    dest_folders = {
    	"images": folder / "images",
         "documents": folder / "documents",
         "audio": folder / "audio",
         "video": folder / "video",
         "archives": folder / "archives",
    }
	# генерим список папок що будемо пропускати на основі dest_folders
    exclude_folders = list(dest_folders.values())


	# тут робим пошук всіх файлів
    all_files = find_files(folder, exclude_folders)
	# далі з all_files будемо виводить список файлів які були в заданій папкі
    
    # print("="*10)
    # print(f"dir: {folder}")
    # print("All files:")
    # for f in all_files:
    #     print(f)
    # print("="*10)

    
    # тепер перебираємо всі файли і опрацьовуємо
    known_extensions = set()
    unknown_extensions = set()
    for file_path in all_files:
        #print(f"{file_path=}")
        extension = file_path.suffix.upper()
        #print(f"{extension=}")
        extension_strip = extension.strip(".")
        #print(f"{extension_strip=}")
        if extension_strip in FILE_EXT['images']:
            known_extensions.add(extension)
            process_file_image(file_path, dest_folders["images"])  # <----- аналогічно для решти, передаємо dest_path
        elif extension_strip in FILE_EXT['video']:
            known_extensions.add(extension)
            process_file_videos(file_path, dest_folders["video"])
        elif extension_strip in FILE_EXT['documents']:
            known_extensions.add(extension)
            process_file_documents(file_path, dest_folders["documents"])
        elif extension_strip in FILE_EXT['audio']:
            known_extensions.add(extension)
            process_file_audio(file_path, dest_folders["audio"])
        elif extension_strip in FILE_EXT['archives']:
            known_extensions.add(extension)
            process_file_archives(file_path, dest_folders["archives"])
        else:
            unknown_extensions.add(extension)
            #process_file_unknown(file_path)
        #print("-"*10)
     
    files_in_folders = {}
    # далі можна пройтись по dest_folders і вив
    for name, folder_path in dest_folders.items():
        files_in_folders[name] = find_files(folder_path, [])
    
    # тепер є список файлів в кожній папкі files_in_folders, можна вивести в консоль
    # ...
    
    # тут можна запустити рекурсивну функцію яка буде видаляти пусті папки
    delete_empty_folders(folder)
    
    # ну і щось ще що забули)

    print(f"files in folders= {files_in_folders}")
    print("="*10)
    print(f"known_extensions={known_extensions}")
    print("="*10)
    print(f"unknown_extensions={unknown_extensions}")

