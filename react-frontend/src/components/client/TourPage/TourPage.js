import './TourPage.css';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
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
        const response = await fetchData(null, `/api/tours/${id}?page=${page}`, false);
        if (response.data) {
            setState(response.data);
            setVisible(response.data.tour_replies.map(() => false));
        }
    };

    const send = async (url, data, method) => {
        const response = await sendData(userData, url, JSON.stringify(data), method);
        if (response.data) {
            alert("Успешно!");
            callFetch(page);
            setUserData(response.userData);
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
        setState({ ...state, prev_page: false, next_page: false })
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
                    <img src={'/Tour/services.png'} alt=''></img>
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
                    <button disabled={!state.prev_page} onClick={() => newPage(page - 1)}><img src={'/Tour/arrow_left.png'} alt=''></img></button>
                    <div className='paginator-cur-page'>{page}</div>
                    <button disabled={!state.next_page} onClick={() => newPage(page + 1)}><img className='next-img' src={'/Tour/arrow_left.png'} alt=''></img></button>
                </div>
            </>

            let qAndABlock = [];
            if (state.tour_replies.length === 0) {
                qAndABlock = "Будьте первым, кто оставит отзыв!"
            }
            state.tour_replies.forEach((elem, index) => {


                let delBtn = userData?.role === "moderator" ?
                    <>
                        <button className='del-btn'
                            onClick={() => {
                                let conf = window.confirm("Вы уверены, что хотите удалить комментарий?")
                                if (conf) {
                                    send(`/api/tours/replies/${elem.reply_id}/delete`, "", 'DELETE')
                                }
                            }}>Удалить</button>
                    </>
                    : null;


                let answerBlock = null;
                if (elem.replies.length > 0) {
                    answerBlock = <>
                        <div className='answer'>
                            <div className='show-answer'>
                                <h3>ОТВЕТ</h3>
                                <button className='show-answer-btn'
                                    onClick={() => handleToggle(index)}>
                                    <img className={!visible[index] ? 'image-flip' : ""} src={'/Tour/arrow_down.png'} alt=''></img>
                                </button>
                                {delBtn}
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
                                    <img className={!visible[index] ? 'image-flip' : ""} src={'/Tour/arrow_down.png'} alt=''></img>
                                </button>
                                {delBtn}
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
