import './EntityList.css';
import React from 'react';
import { useLocation } from 'react-router-dom';

export default function EntityList() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const name = queryParams.get('name');

    let apiPath;
    let headerName;

    switch (name) {
        case 'countries':
            apiPath = name;
            headerName = 'стран';
            break;
        case 'tours':
            apiPath = name;
            headerName = 'туров';
            break;
        case 'offers':
            apiPath = name;
            headerName = 'акций';
            break;
        default:
            apiPath = 'categories';
            headerName = 'категорий';
    }

    return <>
        <div className='entity-container' style={{backgroundColor: '#D9D9D9'}}>
            <div style={{display: 'flex', justifyContent:"space-between", alignItems: 'center'}}>
                <h2>Список {headerName}</h2>
                <div style={{paddingRight: '50px'}}><a href={`/admin/${apiPath}/add`} className='element-btn'>Добавить</a></div>
            </div>
            <div className='entity-list'>
                <div className='entity-list-element'>
                    <div className='entity-name'>Наименование сущности</div>
                    <div style={{ paddingRight: '50px' }}>
                        <a href={`/admin/${apiPath}/1/edit`} className='element-btn'>Изменить</a>
                        <a href={`/admin/${apiPath}/1/delete`} className='element-btn'>Удалить</a>
                    </div>
                </div>
            </div>
        </div>
    </>
}

