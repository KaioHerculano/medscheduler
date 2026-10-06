import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_rotation_group(
    async_client: AsyncClient,
) -> None:
    payload = {
        'name': 'Analgesia Rotativa Teste',
        'spacing_hours': 2,
    }
    create_response = await async_client.post(
        '/medications/groups/rotation', json=payload
    )
    assert create_response.status_code == 201
    group_data = create_response.json()
    assert group_data['name'] == payload['name']
    assert group_data['spacing_hours'] == 2
    assert 'id' in group_data

    list_response = await async_client.get('/medications/groups/rotation')
    assert list_response.status_code == 200
    groups = list_response.json()
    assert len(groups) == 1
    assert groups[0]['name'] == payload['name']


@pytest.mark.asyncio
async def test_create_and_list_medications(async_client: AsyncClient) -> None:
    group_response = await async_client.post(
        '/medications/groups/rotation',
        json={'name': 'Grupo A', 'spacing_hours': 2},
    )
    group_id = group_response.json()['id']

    med_payload = {
        'name': 'Toragesic Teste',
        'category': 'ANALGESIC',
        'min_interval_hours': 6,
        'is_as_needed': False,
        'notes': 'Sublingual',
        'rotation_group_id': group_id,
    }

    create_med_response = await async_client.post(
        '/medications/', json=med_payload
    )
    assert create_med_response.status_code == 201
    med_data = create_med_response.json()
    assert med_data['name'] == 'Toragesic Teste'
    assert med_data['category'] == 'ANALGESIC'
    assert med_data['rotation_group_id'] == group_id

    list_med_response = await async_client.get('/medications/')
    assert list_med_response.status_code == 200
    medications = list_med_response.json()
    assert len(medications) == 1
    assert medications[0]['name'] == 'Toragesic Teste'
