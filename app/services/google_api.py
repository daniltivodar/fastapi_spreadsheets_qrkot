from copy import deepcopy
from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core.config import (
    COLUMN_COUNT,
    COLUMN_COUNT_ERROR,
    DATETIME_FORMAT,
    ROW_COUNT,
    ROW_COUNT_ERROR,
    settings,
    SPREADSHEETS_URL,
    TABLE_TITLE,
)

JSON_BODY_TEMPLATE = dict(
    properties=dict(
        title=TABLE_TITLE.format(
            date_time=dt.now().strftime(DATETIME_FORMAT),
        ),
        locale='ru_RU',
    ),
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=ROW_COUNT,
                columnCount=COLUMN_COUNT,
            ),
        ),
    )],
)
TABLE_VALUES_TEMPLATE = [
    [TABLE_TITLE.format(date_time=dt.now().strftime(DATETIME_FORMAT))],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]


async def spreadsheets_create(
    wrapper_services: Aiogoogle, json_body_template=JSON_BODY_TEMPLATE,
) -> str:
    json_body = deepcopy(json_body_template)
    json_body['properties']['title'] = TABLE_TITLE.format(
        date_time=dt.now().strftime(DATETIME_FORMAT),
    )
    spreadsheet_id = (
        await wrapper_services.as_service_account(
            (await wrapper_services.discover(
                'sheets', 'v4',
            )).spreadsheets.create(
                json=json_body,
            ),
        )
    )['spreadsheetId']
    return (
        spreadsheet_id,
        SPREADSHEETS_URL.format(spreadsheet_id=spreadsheet_id),
    )


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle,
) -> None:
    await wrapper_services.as_service_account(
        (await wrapper_services.discover('drive', 'v3')).permissions.create(
            fileId=spreadsheet_id,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email,
            },
            fields='id',
        ),
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, charity_projects: list, wrapper_services: Aiogoogle,
) -> None:
    table_values_body = deepcopy(TABLE_VALUES_TEMPLATE)
    table_values_body[0] = TABLE_TITLE.format(
        date_time=dt.now().strftime(DATETIME_FORMAT),
    )
    table_values = [
        *table_values_body,
        *[
            list(map(str, charity_project))
            for charity_project in charity_projects
        ],
    ]
    if ROW_COUNT < len(table_values):
        raise ValueError(ROW_COUNT_ERROR.format(row_count=ROW_COUNT))
    if COLUMN_COUNT < max(len(columns) for columns in table_values):
        raise ValueError(COLUMN_COUNT_ERROR.format(column_count=COLUMN_COUNT))
    await wrapper_services.as_service_account(
        (await wrapper_services.discover(
            'sheets', 'v4',
        )).spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values,
            },
        ),
    )
