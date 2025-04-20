from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    return (
        await wrapper_services.as_service_account(
            (await wrapper_services.discover(
                'sheets', 'v4',
            )).spreadsheets.create(
                json={
                    'properties': {
                        'title': f'Отчет на {dt.now().strftime(FORMAT)}',
                        'locale': 'ru_RU',
                    },
                    'sheets': [{
                        'properties': {
                            'sheetType': 'GRID',
                            'sheetId': 0,
                            'title': 'Лист1',
                            'gridProperties': {
                                'rowCount': 100,
                                'columnCount': 11,
                            },
                        },
                    }],
                },
            ),
        )
    )['spreadsheetId']


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
    table_values = [
        ['Отчёт от', dt.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    for charity_project in charity_projects:
        table_values.append(
            [
                str(charity_project['charity_project_name']),
                str(charity_project['close_time']),
                str(charity_project['description']),
            ],
        )
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
