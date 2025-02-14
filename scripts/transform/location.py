import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "utilities"))
import util
import aws_read_write

def transform_location(): 
    
    dest_table_name = 'location'
    source = 'fdic'
    csv_file_name = source + '_' + dest_table_name + '.csv'
    raw_s3_object_name= 'data/raw_data/' + csv_file_name
    
    # selected banks from FDIC
    CERT_LIST = [24735, 59017, 21761, 628, 29147, 27389, 3511, 5146, 18409, 33947, 7213, 3510, 34968, 57803]

    location_df = aws_read_write.get_csv(bucket_name=util.S3_BUCKET_NAME, object_name=raw_s3_object_name)

    clean_location = location_df[location_df.CERT.isin(CERT_LIST)].sort_values('NAME')[['CERT','NAME','MAINOFF','OFFNAME','ESTYMD','SERVTYPE','ADDRESS','COUNTY','CITY','STNAME','ZIP','LATITUDE','LONGITUDE']].rename(columns={'CERT':'fdic_cert_id', 'NAME':'company_name', 'MAINOFF':'main_office', 'OFFNAME':'branch_name', 'ESTYMD':'established_date', 'SERVTYPE':'service_type', 'STNAME':'state'})
    clean_location.columns = [x.lower() for x in clean_location.columns]
    clean_location['established_date'] = pd.to_datetime(clean_location['established_date'])
    clean_location['service_type'] = clean_location['service_type'].replace({11:'Full Service Brick and Mortar Office', 12:'Full Service Retail Office', 13:'Full Service Cyber Office', 14:'Full Service Mobile Office', 15:'Full Service Home/Phone Banking', 16:'Full Service Seasonal Office', 21:'Limited Service Administrative Office', 22:'Limited Service Military Facility', 23:'Limited Service Facility Office', 24:'Limited Service Loan Production Office', 25:'Limited Service Consumer Credit Office', 26:'Limited Service Contractual Office', 27:'Limited Service Messenger Office', 28:'Limited Service Retail Office', 29:'Limited Service Mobile Office', 30:'Limited Service Trust Office'})
    clean_location['zip'] = clean_location['zip'].astype(str)
    clean_location.loc[~clean_location.state.isin(['Puerto Rico','Virgin Islands Of The U.S.']) & clean_location.zip.apply(lambda x: len(x)!=5), 'zip'] = clean_location['zip'].str.zfill(5)

    return clean_location

def load_clean_location():
    clean_location = transform_location()
    dest_table_name = 'location'
    csv_file_name = dest_table_name + '.csv'
    util.load_clean_data(clean_location, csv_file_name)
    
    
def transform(table_name='all'):
    if table_name == 'all':
        load_clean_location()
    elif table_name == 'location':
        load_clean_location()
    else:
        print('Invalid table name')
