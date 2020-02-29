import os
import hashlib
import zipfile
import random

def create_confusion(fname, content = 'qwertyuiop123456'):
    '''
    Create a file without meaningful content, just for changing MD5 after packing files.
    创建一个用于在压缩后改变压缩文件MD5的文件（以防和百度网盘已有的压缩文件MD5重合被批量和谐）
    '''
    f= open(fname,'w')
    f.write(content)
    f.close()

def random_str():
    '''
    Return a 4 char random string.
    创建四位随机字符，改变文件名
    '''
    seed = 'QWERTYUIOPSADFGHJKLZXCVBNM1234567890'
    string = ''
    for i in range(4):
        current_pos = random.random()
        char = seed[int(len(seed) * current_pos)]
        string += char
    return string

def check_md5(existed_file):
    '''
    Check MD5 in existed file, return a string with MD5
    检查已有文件的MD5，避免翻车（虽然zip每次打包因为时间戳问题，md5都不一样，但是以防万一）
    '''
    with open(existed_file, 'rb') as f:
        content = f.read()
        md5 = hashlib.md5(content).hexdigest()
    return md5

def get_files(confusion, scriptname, path = './'):
    '''
    Return a list with files in selected path
    返回目录下文件列表
    '''
    files = os.listdir(path)
    files.remove(confusion)
    files.remove(scriptname)
    return files

def from_newname(origional, random_str):
    '''
    Create a name with random chars for new file
    为压缩文件创造一个包含随机字符的名字
    '''
    suffix_ls = ['.txt', '.mp4', '.doc', 'docx', '.mp3', '.jpg', '.png', '.jpeg', '.gif', '.avi']
    for i in range(len(suffix_ls)):
        if origional.endswith(suffix_ls[i]):
            # reverse string
            name_rev = origional[::-1]
            suffix_rev = suffix_ls[i][::-1]
            fullname_rev = name_rev.replace(suffix_rev, '', 1)
            fullname = fullname_rev[::-1]
            new_name = fullname + random_str + '.zip'
            return new_name
        return origional


def zip_files(origional, confusion, newname):
    '''
    Zip origional file with confusion file together to change the MD5 of origional file
    将原文件和混淆用文件打包，改变打包后文件的MD5
    '''
    f = zipfile.ZipFile(newname, 'w')
    f.write(origional, compress_type = zipfile.ZIP_DEFLATED)
    f.write(confusion, compress_type = zipfile.ZIP_DEFLATED)
    f.close()

if __name__ == '__main__':
    confusion_name = 'baidusima'
    create_confusion(confusion_name)
    rand = random_str()
    flist = get_files(confusion_name, 'core.py')
    existed_zips = []
    for existed_file in flist:
        if existed_file.endswith('.zip'):
            existed_zips.append(existed_file)
    no_zipped_file = [file for file in flist if file not in existed_zips]

    del_list = []
    for file in no_zipped_file:
        newname = from_newname(file, rand)
        zip_files(file, newname, newname)
        nf_md5 = check_md5(newname)
        if existed_zips !=[]:
            for onezip in existed_zips:
                if nf_md5 == check_md5(onezip):
                    del_list.append(newname)
                    break
    print(del_list)
    for file in del_list:
        os.remove(file)
