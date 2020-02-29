import os
import zipfile

def get_path(basedir):
    '''
    Return path list
    basedir: string
    '''
    return os.listdir(basedir)

def get_name(fname):
    '''
    Delete suffix
    fname:string
    return a string
    '''
    suffixs = ['.txt', '.mp4', '.doc', '.docx', '.mp3', '.jpg', '.png', '.jpeg', '.gif', '.avi']
    for i in range(len(suffixs)):
        if fname.endswith(suffixs[i]):
            name_rev = fname[::-1]
            suffix_rev = suffixs[i][::-1]
            fullname_rev = name_rev.replace(suffix_rev, '', 1)
            fullname = fullname_rev[::-1]
            return fullname
    return fname

def zip(zip_name, zipped_dir, fpath):
    '''
    Zip file
    zip_name: string, zipped_dir: string, fpath:string
    '''
    nf = zipfile.ZipFile(zipped_dir + '/' + zip_name + '.zip', 'a')
    nf.write(fpath, compress_type = zipfile.ZIP_DEFLATED)

if __name__ == '__main__':
    zipped_dir = './zipped'
    if not os.path.exists(zipped_dir):
        os.mkdir(zipped_dir)
    basedir = './zip'
    paths = get_path(basedir)
    for path in paths:
        fname = get_name(path)
        path = basedir + '/' + path
        print('Zipping ' + fname)
        zip(fname, zipped_dirr, path)
        print(fname + ' zipped')
    print('\n' + 'Finished')

os.system("pause")