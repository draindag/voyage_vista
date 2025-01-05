import '../../../resources/constants.css';
import './TourPage.css';
import React, { useEffect, useState } from 'react';


import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';

import Serv from '../../../resources/Tour/services.png'
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';
import dayjs from 'dayjs'


export default function TourPage() {

    const { userData, setUserData } = useAuthContext();
    const [state, setState] = useState({});
    const [tab, setTab] = useState(1);
    const { id } = useParams();
    let navigate = useNavigate();

    const callFetch = async () => {
        const response = await fetchData({}, `/api/tours/${id}?page=1`, false);
        console.log(response)
        if (response.data) {
            setState(response.data);
        }
    };

    const isLogin = () => {
        if (userData) {
            return true
        }
        else {
            alert('Войдите в свой профиль')
            navigate('/login')
            return false
        }
    }

    const addToProfile = () => {
        if(isLogin()){
            alert('norm');
        };
    };

    const sendQuestion = () => {
        if(isLogin()){
            alert('norm');
        };
    }

    useEffect(() => {
        callFetch();
        // eslint-disable-next-line 
    }, []);

    let content;
    switch (tab) {
        case 1:
            content = <>
                <div className='tour-page-info-block'>
                    <h1>{state?.tour?.tour_title}</h1>
                    <p>{state?.tour?.tour_text}</p>
                </div>
                <div className='tour-page-price-block'>
                    <p>{`${dayjs(state?.tour?.tour_start_date).format("DD.MM.YY")}-${dayjs(state?.tour?.tour_end_date).format("DD.MM.YY")}`}</p>
                    <img src={Serv}></img>
                    <div>
                        <h1>Цена: {state?.tour?.price_with_discount ? <span>{state?.tour?.tour_price}</span> : null}{state?.tour?.price_with_discount ? state?.tour?.price_with_discount : state?.tour?.tour_price}руб</h1>
                    </div>

                    <div className='btn-block-tour-page'>
                        <button onClick={() => addToProfile()} className='tour-page-button'>Записаться</button>
                    </div>
                </div>
            </>;
            break;
        default:
            content = <>
                <div className='tour-page-info-block'>
                    <h1>{state?.tour?.tour_title}</h1>
                    <textarea className='question-input-area' placeholder='Задайте нам свой вопрос'></textarea>
                    <div className='btn-block-tour-page' style={{ justifyContent: 'start' }}>
                        <button onClick={() => {sendQuestion()}} className='tour-page-button'>Отправить</button>
                    </div>
                </div>

            </>;
            break;
    }

    return (
        <>
            <div className='tour-header'>
                <img src={`/cover_images/${state?.tour?.tour_image}`} alt=''></img>
                <div className='first-tab'>
                    <button onClick={() => setTab(1)} className='angled-corner-button'>Записаться на тур</button>
                </div>
                <div className='second-tab'>
                    <button onClick={() => setTab(2)} className='angled-corner-button'>Q&A</button>
                </div>
            </div>
            <div className='tour-page-container'>
                <div className='tour-page-content'>
                    {content}
                </div>
            </div>

        </>
    );
}



// {
//     "success": true,
//     "tour": {
//       "tour_id": "e8c7c3d4-e23a-4b91-b770-1b884bfc3fda",
//       "tour_title": "Приключенческий тур",
//       "tour_description": "Описание приключенческого тура",
//       "tour_text": "Текст приключенческого тура. Будет очень большим",
//       "tour_price": 1200.5,
//       "price_with_discount": 960.4,
//       "tour_start_date": "2024-06-01",
//       "tour_end_date": "2024-06-10",
//       "tour_image": "flask-backend/webapp/tour_images/e8c7c3d4-e23a-4b91-b770-1b884bfc3fda.png",
//       "category": {
//         "category_id": "123e4567-e89b-12d3-a456-426614174000",
//         "category_title": "Приключения",
//         "category_description": "Описание приключений"
//       },
//       "country": {
//         "country_id": "b0a3a4ce-b5c8-42d9-b23a-d93d768e0c62",
//         "country_name": "Италия",
//         "country_description": "Страна с богатой культурой"
//       },
//       "offers": [
//         {
//           "offer_id": "f1c5a1e2-34bc-4567-89ef-fedcba123456",
//           "offer_title": "Скидка 20%",
//           "discount_size": 20,
//           "end_date": "2024-05-31"
//         }
//       ]
//     },
//     "tour_replies": [
//       {
//         "reply_id": "abcdef01-2345-6789-abcd-ef0123456789",
//         "reply_text": "Это был замечательный тур!",
//         "parent_reply_id": null,
//         "author": {
//           "login": "Пользователь123"
//         },
//         "replies": []
//       },
//       {
//         "reply_id": "abcdef01-2345-6789-abcd-ef0123456790",
//         "reply_text": "Очень понравилось!",
//         "parent_reply_id": null,
//         "author": {
//           "login": "Пользователь456"
//         },
//         "replies": [
//           {
//             "reply_id": "abcdef01-2345-6789-abcd-ef0123456781",
//             "reply_text": "Согласен! Это было незабываемо!",
//             "parent_reply_id": "abcdef01-2345-6789-abcd-ef0123456790",
//             "author": {
//               "login": "Пользователь789"
//             },
//             "replies": []
//           }
//         ]
//       }
//     ],
//     "prev_page": false,
//     "next_page": true
//   }

