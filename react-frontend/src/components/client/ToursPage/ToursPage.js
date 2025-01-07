import './ToursPage.css';
import React, { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';
import dayjs from 'dayjs'

export default function ToursPage() {
    const { id } = useParams();
    const { userData, setUserData } = useAuthContext();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const name = queryParams.get('type');
    let navigate = useNavigate();

    let path;

    let headerImg = `/cover_images/${id}.png`;

    switch (name) {
        case 'by-categ':
            path = `/api/tours/categories/${id}`;
            break;
        case 'by-country':
            path = `/api/tours/countries/${id}`;
            break;
        case 'discount':
            path = `/api/tours/special_offers`;
            headerImg = '/MainPage/Images/sales.jpg';
            break;
        default:
            path = '/api/tours/popular';
            headerImg = '/MainPage/Images/popular.jpg';
            break;
    }

    const [state, setState] = useState({
        tours_list: [],
        page: 1,
        fav_tours_list: []
    });

    console.log(state)

    useEffect(() => {
        const callFetch = async () => {
            const response = await fetchData(userData, path, false);
            let profileResponse = { data: null }
            if (userData) {
                profileResponse = await fetchData(userData, `/api/profile`);
                console.log(profileResponse.data)
            }
            console.log(response)
            if (response.data && (!userData || profileResponse?.data)) {
                let fav_tours;
                if (userData && profileResponse) {
                    fav_tours = response.data.tours.map(item => profileResponse.data.user.fav_tours.some(obj => obj.tour_id === item.tour_id))
                }
                else {
                    fav_tours = response.data.tours.map(() => false)
                }
                setState({ ...state, tours_list: response.data.tours, fav_tours_list: fav_tours });
            }
        };
        callFetch();
        // eslint-disable-next-line 
    }, [userData]);

    const favorReq = async (type, id, index) => {
        if (!userData) {
            alert("Требуется авторизация");
            navigate("/login");
            return;
        }

        let method;
        let url;
        if (!type) {
            method = 'POST';
            url = `/api/tours/${id}/to_favourite`;
        }
        else {
            method = "DELETE"
            url = `/api/tours/${id}/out_of_favourite`;
        }
        const response = await sendData(userData, url, JSON.stringify(""), method);
        if (response.data) {
            alert("Успешно!");
            const newFavList = [...state.fav_tours_list];
            newFavList[index] = !newFavList[index];
            setState({ ...state, fav_tours_list: newFavList });
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

    }

    let toursCards = [];
    if (state.tours_list.length > 0) {
        state.tours_list?.forEach((item, index) => {
            toursCards.push(
                <>
                    <div>
                        <a href={`/tour-page/${item.tour_id}`}>
                            <div className='tour-card'>
                                <div className='tour-card-image-container'>
                                    <img src={`/cover_images/${item.tour_image}`} alt="" />
                                </div>
                                <div className='tour-card-info-container'>
                                    <h2>{item.tour_title}</h2>
                                    <h3>{`${dayjs(item.tour_start_date).format("DD.MM.YYYY")} - ${dayjs(item.tour_end_date).format("DD.MM.YYYY")}`}</h3>
                                    <div className='tour-card-info'>
                                        <p>{item.tour_description}</p>
                                        <p>Страна: {item.country.country_name}</p>
                                    </div>
                                    <div className='price_block'>
                                        {item.price_with_discount ? <span>{item.tour_price}</span> : null}
                                        <h1>{item.price_with_discount ? item.price_with_discount : item.tour_price}</h1>
                                    </div>
                                </div>
                            </div>
                        </a>
                        <button
                            onClick={async () => await favorReq(state.fav_tours_list[index], item.tour_id, index)}
                            className={!state.fav_tours_list[index] ? 'to-favor-btn' : 'un-favor-btn'}></button>
                    </div>

                </>
            )
        })
    }
    else{
        toursCards.push(<>Туров пока нет! Зайдите позже.</>)
    }
    return (
        <>
            <div className="tours-header">
                <img alt='' src={headerImg}></img>
                <div className='triangle-back'></div>
            </div>
            <div className='tours-container'>
                {toursCards}
            </div>
        </>
    );
}

