import './EntityList.css';
import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken, sendData } from '../../general/web_ops';
import { setCookieInfo, deleteCookie } from '../../general/cookie_ops';

export default function EntityList() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const name = queryParams.get('name');

    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    const [state, setState] = useState({entityes: null, page: 1, paginatorBtnsDisable: {prev: true, next: true}})
    
    console.log(state)

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

    const updatePage = (pageNum) => {
        setState({...state, entityes: null})
        const fetchData = async () => {
            const result = await fetchEntList(pageNum);
            const entList = result[responseField];
            const pageBtns = {prev: !result.prev_page, next: !result.next_page}
            if (entList) {
                setState({...state, entityes: entList, paginatorBtnsDisable: pageBtns, page: pageNum})
                // setEnt(entList);
                // setPaginatorBtns(pageBtns);
            }
        };
        fetchData();
    }

    const deleteItem = async (url) => {
        let result; 
        result = window.confirm("Вы уверены?");
        if(!result){return};
        const data = {"acceptance": true}
        const response = await sendData(userData, url, JSON.stringify(data), "DELETE");
        if (response.data) {
            console.log(response)
            alert("Успешно!");
            if(state.entityes.length > 1){
                updatePage(state.page)
            }
            else{
                updatePage(state.page - 1)
            }
        }
        else {
            if (response.action === "unauth") {
                deleteCookie();
                setUserData(null);
                alert(response.message);
                navigate("/login");
            }
            else {
                alert(response.message);
            }
        }
    };

    const tryReq = useCallback(async (token, page) => {
        let response = await fetch(`http://127.0.0.1:8000/api/admin_panel/${apiPath}?page=${page}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json;charset=utf-8',
                'Authorization': `Bearer ${token}`
            },
        });
        return response;

    }, [apiPath]);
    const fetchEntList = useCallback(async (page) => {

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
            let response = await tryReq(token, page);

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

    }, [userData, navigate, setUserData, tryReq]); // зависимости, если есть

    useEffect(() => {
        const fetchData = async () => {
            const result = await fetchEntList(state.page);
            const entList = result[responseField];
            const pageBtns = {prev: !result.prev_page, next: !result.next_page}
            if (entList) {
                setState({...state, entityes: entList, paginatorBtnsDisable: pageBtns})
                // setEnt(entList);
                // setPaginatorBtns(pageBtns);
            }
        };
        fetchData();
    // eslint-disable-next-line
    }, []);

    let listData;
    if (state.entityes) {
        listData = state.entityes.map(item => 
            <div key={item[`${shortName}_id`]} className='entity-list-element'>
                <div className='entity-name'>{item[nameField]}</div>
                <div style={{ paddingRight: '50px' }}>
                    <a href={`/admin/${apiPath}/${item[`${shortName}_id`]}/edit`} className='element-btn'>Изменить</a>
                    <button onClick={() => deleteItem(`/api/admin_panel/${apiPath}/${item[`${shortName}_id`]}/delete`)} className='element-btn'>Удалить</button>
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
                <button disabled={state.paginatorBtnsDisable.prev} onClick={() => updatePage(state.page - 1)}>Prev</button>
                <button disabled={state.paginatorBtnsDisable.next} onClick={() => updatePage(state.page + 1)}>Next</button>
            </div>
        </div>
    </>
}

