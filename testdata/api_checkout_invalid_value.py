import logging
import pandas as pd
import allure

@allure.step('將excel替換成dataframe,並且修改字串內容')
def checkout_info(path, name):
    df = pd.read_excel(fr'{path}', sheet_name=name, dtype=str)
    logging.info('change NaN to empty str')
    df = df.fillna('')
    for column in df.columns:
        for i in range(len(df[column])):
            if 'chars' in df.loc[i, column]:
                value = df.loc[i, column]

                df.loc[i, column] = 'j' * int(value.split(' ')[0])
                logging.info(f"將 chars替換成{int(value.split(' ')[0])}個j")

    logging.info(f'將dataframe轉換成字典,並組成一個list')
    info_dict = df.to_dict(orient='records')
    logging.info(f'{info_dict}')
    return info_dict

