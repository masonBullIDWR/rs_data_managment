#%%
'''Copy an image collection asset on EE to a different asset'''
import ee 
import subprocess
from dateutil.relativedelta import *

gcloud_project = 'idwr-450722'

ee.Authenticate()
ee.Initialize(project = gcloud_project)

oldMETRIC = ee.ImageCollection('projects/id-dwr-metric-data/assets/METRIC')
newMETRIC = ee.ImageCollection('projects/idwr-450722/assets/METRIC')
newMETid = newMETRIC.get('system:id').getInfo()

for i in list(oldMETRIC.toList(oldMETRIC.size()).getInfo()):
    image = i
    imgID = image.get('id').getInfo()
    fileName = str.split(imgID, '/')[len(str.split(imgID, '/'))-1]
    newFile = newMETid + '/' + fileName
    command = '''earthengine cp {image} {newMETRIC}'''.format(image = imgID.strip(), newMETRIC =  newFile)
    print('trying to copy from ' + imgID + ' to ' + newFile)
    result = subprocess.run(command)
    if result.returncode == 0:
        print(f'Return Code: {result.returncode} for uploading {imgID}. Command executed properly. See Google Earth Engine Task Manager for more detail.')
    else:
        print(f'Return Code: {result.returncode} for uploading {imgID}. Command did not execute properly. Run command in CLI for detailed error.')
        break
