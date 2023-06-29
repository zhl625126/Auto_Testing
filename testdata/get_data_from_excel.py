import logging
import pandas as pd
import allure

@allure.step('將excel替換成dataframe,並且修改字串內容')
def checkout_info(path, name):
    df = pd.read_excel(fr'{path}', sheet_name=name)
    logging.info('change NaN to empty str')
    df = df.fillna('')
    for column in df.columns:
        for i in range(len(df[column])):
            if 'chars' in str(df.loc[i, column]):
                value = df.loc[i, column]

                df.loc[i, column] = 'j' * int(value.split(' ')[0])
                logging.info(f"將 chars替換成{int(value.split(' ')[0])}個j")

    logging.info('Modify delivery time to element text')
    df.loc[df['Deliver Time'] == 'Anytime', 'Deliver Time'] = '不指定'
    df.loc[df['Deliver Time'] == 'Morning', 'Deliver Time'] = '08:00-12:00'
    df.loc[df['Deliver Time'] == 'Afternoon', 'Deliver Time'] = '14:00-18:00'

    logging.info('Modify security code to int')
    mask_sc = df['Security Code'] != ''
    df.loc[mask_sc, 'Security Code'] = df.loc[mask_sc, 'Security Code'].astype(float).astype(int)

    logging.info('Modify Mobile to right format')
    df['Mobile'] = df['Mobile'].apply(lambda x: '0' + str(x) if x != '' else '').str.rstrip('.0')

    logging.info(f'將dataframe轉換成字典,並組成一個list')
    info_dict = df.to_dict(orient='records')

    return info_dict

@allure.step('將excel替換成dataframe,並且修改字串內容')
def create_product_info(path, name):
    df = pd.read_excel(fr'{path}', sheet_name=name)

    logging.info('change NaN to empty str')
    df = df.fillna('')
    for column in df.columns:
        for i in range(len(df[column])):
            if 'chars' in str(df.loc[i, column]):
                value = df.loc[i, column]

                df.loc[i, column] = 'j' * int(value.split(' ')[0])
                logging.info(f"將 chars替換成{int(value.split(' ')[0])}個j")

    df.loc[df['Title'] == '連衣裙', 'Title'] = '連衣裙jjj'
    logging.info('change 連衣裙 to 連衣裙jjj')

    df.loc[df['Title'] == '連身裙', 'Title'] = '連身裙jjj'
    logging.info('change 連衣裙 to 連衣裙jjj')

    logging.info('split color and size column to list')

    df['Colors'] = df['Colors'].str.split(', ')
    df['Sizes'] = df['Sizes'].str.split(', ')

    logging.info(f'將dataframe轉換成字典,並組成一個list')
    info_dict = df.to_dict(orient='records')

    return info_dict


