import '../../../resources/constants.css';

import './ToursPage.css';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import SlideImage from '../../../resources/Slider/Images/slideImg.png'
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData } from '../../general/web_ops';
import dayjs from 'dayjs'

const imageArr = [
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage
]


export default function ToursPage() {
    const { id } = useParams();
    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const name = queryParams.get('type');

    let path;

    switch (name) {
        case 'by-categ':
            path = `/api/tours/categories/${id}`;
            break;
        case 'by-country':
            path = `/api/tours/categories/${id}`;
            break;
        default:
            path = '/api/tours/popular';
            break;
    }

    const [state, setState] = useState({
        tours_list: [],
        page: 1
    });

    console.log(state)

    useEffect(() => {
        const callFetch = async () => {
            const response = await fetchData(userData, path, false);
            console.log(response)
            if (response.data) {
                setState({ ...state, tours_list: response.data.tours });
            }
        };
        callFetch();
        // eslint-disable-next-line 
    }, []);

    let toursCards = [];
    state.tours_list.forEach(item => {
        toursCards.push(
            <>
                <div className='tour-card'>
                    <div className='tour-card-image-container'>
                        <img src={`/cover_images/${item.tour_image}`} alt="" />
                    </div>
                    <div className='tour-card-info-container'>
                        <h2>{item.tour_title}</h2>
                        <h3>{`${ dayjs(item.tour_start_date).format("DD.MM.YYYY") } - ${dayjs(item.tour_end_date).format("DD.MM.YYYY")}`}</h3>
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
            </>
        )
    })


    let sliderObjects = []
    imageArr.forEach(item => {
        sliderObjects.push(<>
            <div>
                <div className='card'>
                    <div>
                        <img src={item} alt="" />
                    </div>
                    <div className='card-container'>
                        <p>Text</p>
                    </div>
                </div>
            </div>
        </>)
    })
    return (
        <>
            <div className="tours-header">
                <div className='triangle-back'></div>
                {/* <p className="first-header-text">Ваше <br></br>идеальное<br></br> путешествие <br></br>начинается здесь!</p>
                <a style={{ textDecoration: 'none' }} href='/tours'>
                    <div className="choose-country-button">
                        <span>Выбрать тур</span>
                        <img src={buttonImg} alt="" />
                    </div>
                </a> */}
            </div>
            <div className='tours-container'>
                    {toursCards}
            </div>
        </>
    );
}

