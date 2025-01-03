import './ProfilePage.css';
import '../../../resources/constants.css';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import React, { useState, useEffect, useRef } from 'react';
import TourSlider from './TourSlider';
import { useNavigate, useParams } from 'react-router-dom';




import '../ToursPage/ToursPage.css';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';
import dayjs from 'dayjs'


const tour = {

    tour_image: '0d2b7241-fb36-4154-8fd8-729438486411.png',

    tour_title: 'Приключение на Гавайях',

    tour_start_date: '2025-01-10',

    tour_end_date: '2025-01-20',

    tour_description: 'Незабываемое путешествие на самый красивый остров.',

    country: { country_name: 'США' },

    tour_price: 1000,

    price_with_discount: 800,

}

const toursData = [
    tour, tour, tour, tour


    // Добавьте дополнительные туры здесь

];






export default function ProfilePage() {
    const [state, setState] = useState({ user: null, favor: [{}], tours: [{}] });
    const [tab, setTab] = useState(1)

    const prevUserDataRef = useRef();

    let navigate = useNavigate();
    console.log(state)
    // console.log(tab)


    const { userData, setUserData } = useAuthContext();


    const bigTours = state.tours?.map((item, index) => (
        <div>
            <div className='profile-tour-card'>
                <h1 className='profile-tour-card-h1'>{item.tour_title}</h1>
    
                <div style={{paddingLeft: "66px"}}>
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
                    <div className='profile-tour-card-line-div'>
                        <label className='slide-label'>Стоимость с <br/>учетом скидки:</label>
                        <input className='slide-input' type='text' defaultValue={`${item.price_with_discount}руб`}></input>
                    </div>
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
    



    useEffect(() => {
        const fetchCountry = async () => {
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

        fetchCountry();
    }, [userData]);


    let favItems = [];
    let tourItems = [];

    // countries.forEach(elem => {
    //     ulElements.push(<li>
    //         <a href={elem.country_id}>{elem.country_name}</a>
    //     </li>)
    // })


    let content;
    let name;
    let panelButtons;
    switch (tab) {
        case 1:
            content = <>
                <label className='profile-data-label'>Логин:</label>
                <div>
                    <input className='profile-data-input' type='text' defaultValue={state.user?.login}></input>
                    <button style={{ display: 'inline-block' }}>Изменить</button>
                </div>
                <label className='profile-data-label'>Почта:</label>
                <div>
                    <input className='profile-data-input' type='text' defaultValue={state.user?.email}></input>
                    <button style={{ display: 'inline-block' }}>Изменить</button>
                </div>
                <label className='profile-data-label'>Пароль:</label>
                <div>
                    <input className='profile-data-input' type='password' defaultValue='password'></input>
                    <button style={{ display: 'inline-block' }}>Изменить</button>
                </div>
            </>;
            panelButtons = <>
                <button style={{ backgroundColor: '#5D7EA7' }} onClick={() => { setTab(1) }}>ПРОФИЛЬ</button>
                <button onClick={() => { setTab(2) }}>ИЗБРАННОЕ</button>
                <button onClick={() => { setTab(3) }}>МОИ ТУРЫ</button>
            </>;
            name = 'ПРОФИЛЬ';
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

