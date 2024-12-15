import './EntityList.css';
import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken } from '../../general/web_ops';
import { setCookieInfo, deleteCookie } from '../../general/cookie_ops';

export default function EntityList() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const name = queryParams.get('name');

    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    const [entityes, setEnt] = useState(null);
    const [curPage, setPage] = useState(1);
    const [paginatorBtnsDisable, setPaginatorBtns] = useState({prev: true, next: true})

    console.log(`AddSale state: ${curPage} ${paginatorBtnsDisable}`);
    console.log(paginatorBtnsDisable)

    let apiPath;
    let headerName;
    let nameField;
    let responseField;
    let shortName;

    switch (name) {
        case 'countries':
            apiPath = name;
            headerName = 'стран';
            nameField = 'country_name';
            shortName = 'country';
            responseField = name;
            break;
        case 'tours':
            apiPath = name;
            headerName = 'туров';
            nameField = 'tour_title';
            shortName = 'tour';
            responseField = name;
            break;
        case 'offers':
            apiPath = name;
            headerName = 'акций';
            nameField = 'offer_title';
            shortName = 'offer';
            responseField = 'special_offers';
            break;
        default:
            apiPath = 'categories';
            responseField = 'categories';
            headerName = 'категорий';
            shortName = 'category';
            nameField = 'category_title';
    }

    const updatePage = (btn) => {
        setEnt(null);
        if(btn == 'prev'){
            setPage(curPage -1)
        }
        else{
            setPage(curPage +1)
        }
        const fetchData = async () => {
            const result = await fetchEntList();
            const entList = result[responseField];
            const pageBtns = {prev: !result.prev_page, next: !result.next_page}
            if (entList) {
                setEnt(entList);
                setPaginatorBtns(pageBtns);
            }
        };
        fetchData();
    }

    const tryReq = useCallback(async (token) => {
        let response = await fetch(`http://127.0.0.1:8000/api/admin_panel/${apiPath}?page=${curPage}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json;charset=utf-8',
                'Authorization': `Bearer ${token}`
            },
        });
        return response;

    }, [apiPath, curPage]);
    const fetchEntList = useCallback(async () => {

        let result = [];
        try {
            let token = userData.access_token;
            console.log("CHECK")
            let check = await checkToken(userData?.access_token)
            if (!check) {
                console.log("Refresh")
                let refresh = await refreshToken(userData?.refresh_token)
                if (!refresh) {
                    deleteCookie();
                    setUserData(null);
                    alert("Авторизируйтесь повторно");
                    navigate("/login");
                    return result;
                }
                let newUserData = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role }
                setCookieInfo(newUserData);
                setUserData(newUserData);
                token = refresh;
            }
            console.log("SUCCESS to refresh")
            let response = await tryReq(token);

            console.log(result);
            if (response.status === 200) {
                result = await response.json()
            } else {
                alert(`Произошла ошибка при загрузке данных.`);
            }
            return result;
        } catch (e) {
            alert(`Не удалось. Попробуйте позже`);
            return result;
        }

    }, [userData, navigate, responseField, setUserData, tryReq]); // зависимости, если есть

    useEffect(() => {
        const fetchData = async () => {
            const result = await fetchEntList();
            const entList = result[responseField];
            const pageBtns = {prev: !result.prev_page, next: !result.next_page}
            if (entList) {
                setEnt(entList);
                setPaginatorBtns(pageBtns);
            }
        };
        fetchData();
    }, [fetchEntList]);

    let listData;
    if (entityes) {
        listData = entityes.map(item => 
            <div key={item[`${shortName}_id`]} className='entity-list-element'>
                <div className='entity-name'>{item[nameField]}</div>
                <div style={{ paddingRight: '50px' }}>
                    <a href={`/admin/${apiPath}/1/edit`} className='element-btn'>Изменить</a>
                    <a href={`/admin/${apiPath}/1/delete`} className='element-btn'>Удалить</a>
                </div>
            </div>
        )
    } else {
        listData = <div>Загрузка</div>
    }

    return <>
        <div key='entity-container' className='entity-container' style={{ backgroundColor: '#D9D9D9' }}>
            <div style={{ display: 'flex', justifyContent: "space-between", alignItems: 'center' }}>
                <h2>Список {headerName}</h2>
                <div style={{ paddingRight: '50px' }}><a href={`/admin/${apiPath}/add`} className='element-btn'>Добавить</a></div>
            </div>
            <div className='entity-list'>
                {listData}
            </div>
            <div className='paginator'>
                <button disabled={paginatorBtnsDisable.prev} onClick={() => updatePage('prev')}>Prev</button>
                <button disabled={paginatorBtnsDisable.next} onClick={() => updatePage('next')}>Next</button>
            </div>
        </div>
    </>
}

