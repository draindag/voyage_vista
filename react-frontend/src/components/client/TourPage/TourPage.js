import '../../../resources/constants.css';
import './TourPage.css';
import React, { useEffect, useState } from 'react';


import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';

import Serv from '../../../resources/Tour/services.png'

import Arrow from '../../../resources/Tour/arrow_down.png'
import ArrowLeft from '../../../resources/Tour/arrow_left.png'


import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';
import dayjs from 'dayjs'


export default function TourPage() {

    const { userData, setUserData } = useAuthContext();
    const [state, setState] = useState({});

    const [visible, setVisible] = useState([]);

    const [page, setPage] = useState(1);

    const [reply_text, setReply] = useState("");


    const [tab, setTab] = useState(1);
    const { id } = useParams();
    let navigate = useNavigate();


    const callFetch = async (page = 1) => {
        const response = await fetchData({}, `/api/tours/${id}?page=${page}`, false);
        console.log(response)
        if (response.data) {
            setState(response.data);
            setVisible(response.data.tour_replies.map(() => false));
        }
    };

    const send = async (url, data, method) => {
        const response = await sendData(userData, url, JSON.stringify(data), method);
        if (response.data) {
            console.log(response)
            alert("Успешно!");
            callFetch(page);
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

    const handleToggle = (index) => {

        const newVisibleItems = [...visible];

        newVisibleItems[index] = !newVisibleItems[index];

        setVisible(newVisibleItems);

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
        if (isLogin()) {
            const result = window.confirm("Подтвердите действие");
            if (result) {
                send(`/api/tours/${id}/payment`, { acceptance: true }, 'POST');
            }
        };
    };

    const sendRepl = (parent = null) => {
        if (isLogin()) {
            const result = window.confirm("Подтвердите действие");
            if (result) {
                let data;
                if (parent) {
                    data = { reply_text: reply_text, parent_reply_id: parent }
                }
                else {
                    data = { reply_text: reply_text }
                }
                send(`/api/tours/${id}/add_reply`, data, 'POST');
            }
        };
    };

    const newPage = async (page) => {
        setPage(page);
        setState({...state, prev_page: false, next_page: false})
        callFetch(page);
    }

    useEffect(() => {
        callFetch();
        // eslint-disable-next-line 
    }, []);

    let content;
    let paginator = null;
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

            paginator = <>
                <div
                    className={!(state.prev_page || state.next_page) ? 'hidden-class' : 'tour-page-paginator'}
                // className='tour-page-paginator'
                >
                    <button disabled={!state.prev_page} onClick={()=>newPage(page-1)}><img src={ArrowLeft} alt=''></img></button>
                    <div className='paginator-cur-page'>{page}</div>
                    <button disabled={!state.next_page} onClick={()=>newPage(page+1)}><img className='next-img' src={ArrowLeft} alt=''></img></button>
                </div>
            </>

            let qAndABlock = [];


            state.tour_replies.forEach((elem, index) => {


                let answerBlock = null;
                if (elem.replies.length > 0) {
                    answerBlock = <>
                        <div className='answer'>
                            <div className='show-answer'>
                                <h3>ОТВЕТ</h3>
                                <button className='show-answer-btn'
                                    onClick={() => handleToggle(index)}>
                                    <img className={!visible[index] ? 'image-flip' : ""} src={Arrow} alt=''></img>
                                </button>
                            </div>
                            <p className={!visible[index] ? 'hidden-class' : ""}>{elem.replies[0].reply_text}</p>
                        </div>
                    </>
                }
                if (userData?.role === "moderator" && !answerBlock) {
                    answerBlock = <>
                        <div className='answer'>
                            <div className='show-answer'>
                                <h3>ОТВЕТИТЬ</h3>
                                <button className='show-answer-btn'
                                    onClick={() => handleToggle(index)}>
                                    <img className={!visible[index] ? 'image-flip' : ""} src={Arrow} alt=''></img>
                                </button>
                            </div>
                            <textarea
                                onChange={(val) => setReply(val.target.value)}
                                className={!visible[index] ? 'hidden-class answ-input' : "answ-input"}></textarea>
                            <div style={{ display: 'flex', justifyContent: 'end' }}>
                                <button
                                    onClick={() => { sendRepl(elem.reply_id) }}
                                    className={!visible[index] ? 'hidden-class answ-input' : "answ-button"}>Ответить</button>
                            </div>
                        </div>
                    </>
                }



                qAndABlock.push(<>
                    <div className='question'>
                        <h3>{elem.author.login}</h3>
                        <p>{elem.reply_text}</p>
                    </div>
                    {answerBlock}
                </>);

            })

            content = <>
                <div className='tour-page-info-block'>
                    <h1>{state?.tour?.tour_title}</h1>
                    {
                        userData?.role === "moderator" ?
                            null :
                            <>
                                <textarea onChange={(val) => setReply(val.target.value)}
                                    className='question-input-area' placeholder='Задайте нам свой вопрос'></textarea>
                                <div className='btn-block-tour-page' style={{ justifyContent: 'start' }}>
                                    <button onClick={() => { sendRepl() }} className='tour-page-button'>Отправить</button>
                                </div>
                            </>
                    }
                </div>
                <div className='tour-page-quest-block'>
                    {qAndABlock}
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
                {paginator}
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

