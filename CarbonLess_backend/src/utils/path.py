import pathlib



def get_root():
    return pathlib.Path(__file__).parent.parent.parent

def get_src():
    return get_root() / 'src'

def get_services():
    return get_src() / 'services'

if __name__ == '__main__':
    print(get_root())