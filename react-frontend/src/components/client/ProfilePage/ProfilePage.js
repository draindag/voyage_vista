import './ProfilePage.css';
import '../../../resources/constants.css';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import React, { useState, useEffect, useRef } from 'react';
import TourSlider from './TourSlider';
import { useNavigate } from 'react-router-dom';


import '../ToursPage/ToursPage.css';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';
import dayjs from 'dayjs'



export default function ProfilePage() {
    const [state, setState] = useState({ user: null, favor: [{}], tours: [{}] });
    const [tab, setTab] = useState(1);
    const [changes, setChanges] = useState(null);

    const [newProfileData, setNewProfileData] = useState({ new_login: '', password: '', email: '', new_password: '' })


    const prevUserDataRef = useRef();

    let navigate = useNavigate();
    console.log(state)
    console.log(newProfileData)

    const { userData, setUserData } = useAuthContext();


    const bigTours = state.tours?.map((item, index) => (
        <div>
            <div className='profile-tour-card'>
                <h1 className='profile-tour-card-h1'>{item.tour_title}</h1>

                <div style={{ paddingLeft: "66px" }}>
                    <div style={{ display: 'flex' }}>
                        <div>
                            <label className='slide-label'>Дата:</label>
                            <input className='slide-input'
                                style={{ width: '244px', marginRight: '130px' }}
                                type='text'
                                defaultValue={`${dayjs(item.tour_start_date).format("DD.MM.YY")}-${dayjs(item.tour_end_date).format("DD.MM.YY")}`}></input>
                        </div>
                        <div>
                            <label className='slide-label'>Страна:</label>
                            <input className='slide-input' style={{ width: '426px' }} type='text' defaultValue={item?.country?.country_name}></input>
                        </div>
                    </div>
                    <div className='profile-tour-card-line-div'>
                        <label className='slide-label'>Стоимость:</label>
                        <input className='slide-input' type='text' defaultValue={`${item.tour_price}руб`}></input>
                    </div>
                    <div className='profile-tour-card-line-div'>
                        <label className='slide-label'>Категория:</label>
                        <input className='slide-input' type='text' defaultValue={item?.category?.category_title}></input>
                    </div>
                    {
                        item.price_with_discount ?
                            <div className='profile-tour-card-line-div'>
                                <label className='slide-label'>Стоимость с <br />учетом скидки:</label>
                                <input className='slide-input' type='text' defaultValue={`${item.price_with_discount}руб`}></input>
                            </div>
                            : null
                    }

                    {/* <div style={{display: 'flex', justifyContent: 'end'}}>
                        <label>Итого</label>
                    </div> */}
                </div>




            </div>
        </div>
    ));

    const smallTour = state.favor?.map((item, index) => (
        <div className='tour-card'>
            <div className='tour-card-image-container'>
                <img src={`/cover_images/${item?.tour_image}`} alt="" />
            </div>
            <div className='tour-card-info-container'>
                <h2>{item?.tour_title}</h2>
                <h3>{`${dayjs(item.tour_start_date).format("DD.MM.YYYY")} - ${dayjs(item.tour_end_date).format("DD.MM.YYYY")}`}</h3>
                <div className='tour-card-info'>
                    <p>{item.tour_description}</p>
                    <p>Страна: {item?.country?.country_name}</p>
                </div>
                <div className='price_block'>
                    {item.price_with_discount ? <span>{item.tour_price}</span> : null}
                    <h1>{item.price_with_discount ? item.price_with_discount : item.tour_price}</h1>
                </div>
            </div>
        </div>
    ));

    const sendProgileEdit = async (type) => {
        let sendedData;
        switch (type) {
            case 'edit_login':
                sendedData = { new_login: newProfileData.new_login, password: newProfileData.password }
                break;
            case 'edit_email':
                sendedData = { email: newProfileData.email, password: newProfileData.password }
                break;
            default:
                sendedData = { old_password: newProfileData.password, new_password: newProfileData.new_password }
                break;
        }
        await sendData(userData, `/api/${type}`, JSON.stringify(sendedData), 'PUT').then(response => {
            if (response.data) {
                let new_user;
                switch (type) {
                    case 'edit_login':
                        new_user = { ...state.user, login: newProfileData.new_login }
                        setUserData({ ...response.userData, access_token: response.data.access_token, refresh_token: response.data.refresh_token });
                        break;
                    case 'edit_email':
                        new_user = { ...state.user, email: newProfileData.email }
                        setUserData(response.userData);
                        break;
                    default:
                        new_user = state.user
                        setUserData(response.userData);
                        // sendedData = { old_password: newProfileData.password, new_password: newProfileData.new_password }
                        break;
                }
                setState({ ...state, user: new_user });
                setChanges(null);
                alert("Успешно!");
            }
            else {
                if (response.action === "unauth") {
                    deleteCookie();
                    setUserData(null);
                    alert(response.message);
                    navigate("/login");
                }
                else {
                    switch (type) {
                        case 'edit_login':
                            alert('Недопустимый логин или неверный пароль');
                            break;
                        case 'edit_email':
                            alert('Недопустимый email или неверный пароль');
                            break;
                        default:
                            alert('Недопустимый новый пароль или неверный старый пароль');
                            break;
                    }
                }
            }
        })


    }


    const fetchProfile = async () => {
        if (!userData) { return };
        console.log(userData)
        const response = await fetchData(userData, `/api/profile`);
        console.log(response)
        if (response.data) {
            let data = response.data.user
            setState({
                user: { login: data.login, email: data.email },
                favor: data.fav_tours,
                tours: data.transactions,
            });
            if (!prevUserDataRef.current || JSON.stringify(prevUserDataRef.current) !== JSON.stringify(userData)) {
                setUserData(response.userData);
            }
            prevUserDataRef.current = userData;
            return;
        }
        else {

            deleteCookie();
            setUserData(null);
            alert(response.message);
            navigate("/login");
            return;

        }
    }


    useEffect(() => {
        fetchProfile();
    // eslint-disable-next-line 
    }, [userData]);


    let content;
    let name;
    let panelButtons;
    switch (tab) {
        case 1:
            switch (changes) {
                case 1:
                    name = 'ИЗМЕНЕНИЕ ЛОГИНА'
                    content = <>
                        <p className='profile-data-label'>Логин:</p>
                        <input id='new-login' className='profile-data-input' type='text'
                            // value={newProfileData.new_login}
                            onChange={(value) => setNewProfileData({ ...newProfileData, new_login: value.target.value })}
                        ></input>
                        <p className='profile-data-label'>Пароль:</p>
                        <input id='confirm-pass' className='profile-data-input' type='password'
                            // value={newProfileData.password}
                            onChange={(value) => setNewProfileData({ ...newProfileData, password: value.target.value })}
                        ></input>
                        <button onClick={() => sendProgileEdit('edit_login')} className='submit-new-profile-button'>Изменить</button>
                    </>

                    break;
                case 2:
                    name = 'ИЗМЕНЕНИЕ ПОЧТЫ'
                    content = <>
                        <label className='profile-data-label'>Почта:</label>
                        <input className='profile-data-input' type='text'
                            // value={newProfileData.email}
                            onChange={(value) => setNewProfileData({ ...newProfileData, email: value.target.value })}
                        ></input>
                        <label className='profile-data-label'>Пароль:</label>
                        <input className='profile-data-input' type='password'
                            // value={newProfileData.password}
                            onChange={(value) => setNewProfileData({ ...newProfileData, password: value.target.value })}
                        ></input>
                        <button onClick={() => sendProgileEdit('edit_email')} className='submit-new-profile-button'>Изменить</button>
                    </>
                    break;
                case 3:
                    name = 'ИЗМЕНЕНИЕ ПАРОЛЯ'
                    content = <>
                        <label className='profile-data-label'>Старый пароль:</label>
                        <input className='profile-data-input' type='text'
                            // value={newProfileData.password}
                            onChange={(value) => setNewProfileData({ ...newProfileData, password: value.target.value })}
                        ></input>
                        <label className='profile-data-label'>Новый пароль:</label>
                        <input className='profile-data-input' type='password'
                            // value={newProfileData.new_password}
                            onChange={(value) => setNewProfileData({ ...newProfileData, new_password: value.target.value })}
                        ></input>
                        <button onClick={() => sendProgileEdit('edit_password')} className='submit-new-profile-button'>Изменить</button>
                    </>
                    break;
                default:
                    name = 'ПРОФИЛЬ';
                    content = <>
                        <p className='profile-data-label'>Логин:</p>
                        <div>
                            <input className='profile-data-input' type='text' defaultValue={state.user?.login}></input>
                            {/* <p className='profile-data-input profile-data-input-p' >{state.user?.login}</p> */}
                            <button className='profile-data-button' style={{ display: 'inline-block' }} onClick={() => { setChanges(1) }}>Изменить</button>
                        </div>
                        <p className='profile-data-label'>Почта:</p>
                        <div>
                            <input className='profile-data-input' type='text' defaultValue={state.user?.email}></input>
                            {/* <p className='profile-data-input profile-data-input-p' >{state.user?.email}</p> */}
                            <button className='profile-data-button' style={{ display: 'inline-block' }} onClick={() => { setChanges(2) }}>Изменить</button>
                        </div>
                        <p className='profile-data-label'>Пароль:</p>
                        <div>
                            <input className='profile-data-input' type='password' defaultValue='password'></input>
                            {/* <p className='profile-data-input profile-data-input-p' >***</p> */}
                            <button className='profile-data-button' style={{ display: 'inline-block' }} onClick={() => { setChanges(3) }}>Изменить</button>
                        </div>
                    </>;
                    break;
            }
            panelButtons = <>
                <button style={{ backgroundColor: '#5D7EA7' }} onClick={() => { setTab(1); setChanges(null); }}>ПРОФИЛЬ</button>
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
            content = state.favor.length > 0 ? <>
                <TourSlider tours={smallTour} settings={{
                    className: "center",
                    centerMode: true,
                    infinite: true,
                    centerPadding: "0px",
                    slidesToShow: 2,
                    speed: 500,
                }} />
            </> : 'Данные отсутствуют';
            name = 'ИЗБРАННОЕ';
            break;
        default:
            panelButtons = <>
                <button onClick={() => { setTab(1) }}>ПРОФИЛЬ</button>
                <button onClick={() => { setTab(2) }}>ИЗБРАННОЕ</button>
                <button style={{ background: '#5D7EA7' }} onClick={() => { setTab(3) }}>МОИ ТУРЫ</button>
            </>;
            content = state.tours.length > 0 ? <>
                <TourSlider tours={bigTours} settings={{
                    className: "center",
                    centerMode: true,
                    infinite: true,
                    centerPadding: "0px",
                    slidesToShow: 1,
                    speed: 500,
                }} />
            </> : 'Данные отсутствуют';
            name = 'МОИ ТУРЫ';
            break;
    }


    return <>
        <div style={{ height: '172px', background: "#5D7EA7", marginBottom: '92px', width: "100%" }}></div>


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
                <h1 className='profile-data-h1 '>{name}</h1>
                <div>
                    {content}

                </div>
            </div>




        </div>
        <div style={{ height: '100px' }}>
            {/* <TourSlider tours={toursData} /> */}
        </div>

    </>
}

