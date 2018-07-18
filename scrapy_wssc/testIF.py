import re

if __name__ == '__main__':
    pattern1 = re.compile(r'^\/(\d+)\/(\d+)\/(\d+_?\d+).html$')
    pattern2 = re.compile(r'^\/(\d+)\/(\d+)\/(\d+).html$')
    if re.match(pattern1, '/11/11/121223_1.html', flags=0):

        print str(int(pattern1.search('/11/11/121223_1.html').group(3).split("_")[1]) + 1)