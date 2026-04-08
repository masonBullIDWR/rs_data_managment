#%%
'''Code to upload images from a Google Storage Bucket to an EE asset'''
import ee 
import pathlib as pl
import subprocess
from datetime import datetime, timezone
from dateutil.relativedelta import *

gcloud_project = 'idwr-450722'

ee.Authenticate()
ee.Initialize(project = gcloud_project)

#%%upload images to ee assets

#path to local directory with files to upload. The files are actually housed in GSB, but the metadata comes from this directory
parentPath = pl.Path('D:/METRIC/MonthlyMETRIC/to_upload')

#asset path in EE
eePath = 'projects/idwr-450722/assets/METRIC/'

#Currently, this is set up to load METRIC GeoTiffs to the METRIC asset on EE, edit as needed for other images
for f in parentPath.glob('*_et.tif'):
    name = f.name

    #set start and end dates in Unix milliseconds
    date = name.split('_')[1]
    start_date = datetime.strptime(date,'%Y%m').astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = int(start_date.timestamp()*1000)
    end_date = start_date+relativedelta(months=+1)+relativedelta(days=-1)
    end_time = int(end_date.timestamp()*1000)

    ee_asset_path = eePath + name.split('.')[0]
    path = int(name.split('_')[0].split('p')[-1])

    #this command requires a Google Storage Bucket to function
    command = '''earthengine upload image --asset_id={ee_asset_path} --property path={path} --time_start={start_time} --time_end={end_time} --pyramiding_policy=mean gs://metric_ee_upload/{name}'''.format(
        ee_asset_path = ee_asset_path, 
        f = f, 
        start_time = start_time, 
        end_time = end_time, 
        name = name, 
        path = path)
    
    print('trying to upload ' + name)
    result = subprocess.run(command)
    if result.returncode == 0:
        print(f'Return Code: {result.returncode} for uploading {name}. Command executed properly. See Google Earth Engine Task Manager for more detail.')
    else:
        print(f'Return Code: {result.returncode} for uploading {name}. Command did not execute properly. Run command in CLI for detailed error.')
        break