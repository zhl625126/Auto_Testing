import ast
import logging
import pandas as pd
import allure


@allure.step('將excel替換成dataframe,並且修改字串內容')
def modify_product_excel(path, name):

    df = pd.read_excel(path, sheet_name=name, dtype=str)
    logging.info('change NaN to empty str')
    df = df.fillna('')
    for column in df.columns:
        for i in range(len(df[column])):
            if 'chars' in df.loc[i, column]:
                value = df.loc[i, column]

                df.loc[i, column] = 'j' * int(value.split(' ')[0])
                logging.info(f"將 chars替換成{int(value.split(' ')[0])}個j")


    logging.info('Color column change to list')
    for j, value in enumerate(df['ColorIDs']):
        if value != "":
            converted_value = [num for num in value.split(",")]
            df.at[j, 'ColorIDs'] = converted_value
        else:
            df.at[j, 'ColorIDs'] = []

    logging.info('Sizes column change to list')
    for j, value in enumerate(df['Sizes']):
        if value != "":
            converted_value = [num for num in value.split(",")]
            df.at[j, 'Sizes'] = converted_value
        else:
            df.at[j, 'Sizes'] = []

    df['other_images'] = df[['Other Image 1', 'Other Image 2']].apply(lambda x: [v for v in x if v != ''], axis=1)

    logging.info(f'將dataframe轉換成字典,並組成一個list')
    info_dict = df.to_dict(orient='records')
    logging.info(f'excel info is: {info_dict}')

    return info_dict


