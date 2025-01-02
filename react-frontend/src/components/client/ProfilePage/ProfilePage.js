import './ProfilePage.css';
import '../../../resources/constants.css';

import React, { useState, useEffect, useRef } from 'react';


import { useNavigate, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';


export default function ProfilePage() {
    const { userData, setUserData } = useAuthContext();
    const [state, setState] = useState({ user: null, favor: [{}], tours: [{}] });

    const [tab, setTab] = useState(1)

    let navigate = useNavigate();
    console.log(state)
    console.log(tab)
    useEffect(() => {
        const fetchCountry = async () => {
            if (!userData) {
                return
            }
            const response = await fetchData(userData, `/api/profile`);
            if (response.data) {
                let data = response.data.user
                setState({
                    user: { login: data.login, email: data.email },
                    favor: data.fav_tours,
                    tours: data.transactions,
                });
                setUserData(response.userData);

                return response;
            }
            else {
                if (response.action === "unauth") {
                    // deleteCookie();
                    // setUserData(null);
                    alert(response.message);
                    // navigate("/login");
                    return null;
                }
                else {
                    alert(response.message);
                    return null;
                }
            }
        }
        fetchCountry();
    }, [userData]);


    let favItems = [];
    let tourItems = [];

    // countries.forEach(elem => {
    //     ulElements.push(<li>
    //         <a href={elem.country_id}>{elem.country_name}</a>
    //     </li>)
    // })

    let panelButtons;
    switch (tab) {
        case 1:
            panelButtons = <>
                <button style={{ backgroundColor: '#5D7EA7' }} onClick={() => { setTab(1) }}>ПРОФИЛЬ</button>
                <button onClick={() => { setTab(2) }}>ИЗБРАННОЕ</button>
                <button onClick={() => { setTab(3) }}>МОИ ТУРЫ</button>
            </>;
            break;
        case 2:
            panelButtons = <>
                <button onClick={() => { setTab(1) }}>ПРОФИЛЬ</button>
                <button style={{ background: '#5D7EA7' }} onClick={() => { setTab(2) }}>ИЗБРАННОЕ</button>
                <button onClick={() => { setTab(3) }}>МОИ ТУРЫ</button>
            </>;
            break;
        default:
            panelButtons = <>
                <button onClick={() => { setTab(1) }}>ПРОФИЛЬ</button>
                <button onClick={() => { setTab(2) }}>ИЗБРАННОЕ</button>
                <button style={{ background: '#5D7EA7' }} onClick={() => { setTab(3) }}>МОИ ТУРЫ</button>
            </>;
            break;
    }

    return <>
        <div style={{ height: '172px', background: "#5D7EA7", marginBottom: '92px' }}></div>
        <div className='profile-container'>
            <div className='control-panel'>
                <div className='control-panel-head'>
                    <p>{state.user?.login}</p>
                </div>
                <div>
                    {panelButtons}
                </div>
            </div>

            <div className='profile-data'>
                <h1>ПРОФИЛЬ</h1>
                <div>
                    <label>Логин:</label>
                    <div>
                        <input type='text' value={state.user?.login}></input>
                        <button style={{ display: 'inline-block' }}>Изменить</button>
                    </div>
                    <label>Почта:</label>
                    <div>
                        <input type='text' value={state.user?.email}></input>
                        <button style={{ display: 'inline-block' }}>Изменить</button>
                    </div>
                    <label>Пароль:</label>
                    <div>
                        <input type='password' value='password'></input>
                        <button style={{ display: 'inline-block' }}>Изменить</button>
                    </div>

                </div>
            </div>

        </div>
    </>
}

