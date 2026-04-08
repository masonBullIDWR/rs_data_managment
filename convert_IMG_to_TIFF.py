#%%
'''Code to convert IMG data files to TIFF files'''
import pathlib as pl
import os
import multiprocessing as mp

directory = pl.Path('X:/Spatial/METRIC')

def process(i):
        input = str(i)
        fileName = str.split(str.split(str(i), '\\')[len(str.split(str(i), '\\'))-1], '.')[0]
        output = str('D:/METRIC/' + fileName + '.tif')
        command = '''gdal_translate -of GTiff {input} {output}'''.format(input = input, output = output)
        os.system(command=command)

files = [i for i in list(directory.glob('**/*et.img'))]

if __name__ == '__main__':
    p = mp.Pool(4)
    p.map(process, files)

