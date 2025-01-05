import '../../../resources/constants.css';

import './MainPage.css';
import React, { useEffect, useState } from 'react';
import buttonImg from '../../../resources/MainPage/Images/arrow_tour.png';
import man from '../../../resources/MainPage/Images/man.png';
import girl from '../../../resources/MainPage/Images/girl.png';
import train from '../../../resources/MainPage/Images/Bottom_map.png';
import SimpleSlider from '../Slider/Slider';
import { useAuthContext } from '../../general/AuthContext/AuthContext';

import { fetchData } from '../../general/web_ops';

const settings = {
    // className: "center",
    // centerMode: true,
    // infinite: true,
    centerPadding: "0px",
    slidesToShow: 4,
    speed: 500,
    responsive: [
        {
            breakpoint: 1890,
            settings: {
                slidesToShow: 3,
            },
        },
        {
            breakpoint: 1430,
            settings: {
                slidesToShow: 2,
            },
        },
    ],
};


export default function MainPage() {

    const { userData} = useAuthContext();

    const [state, setState] = useState([]);

    let categCards = [
        <>
            <a href='/tours?type=popular' style={{ textDecoration: "none", }}>
                <div>
                    <div className='card'>
                        <div className='image-container'>
                            <img src={`popular.jpg`} alt="" />
                        </div>
                        <div className='card-container'>
                            <p>Популярные</p>
                        </div>
                    </div>
                </div>
            </a>
        </>,
        <>
            <a href='/tours?type=discount' style={{ textDecoration: "none", }}>
                <div>
                    <div className='card'>
                        <div className='image-container'>
                            <img src={`sales.jpg`} alt="" />
                        </div>
                        <div className='card-container'>
                            <p>Со скидкой</p>
                        </div>
                    </div>
                </div>
            </a>
        </>,
    ];
    state.forEach(item => {
        categCards.push(<>
            <a href={`/tours/${item.category_id}?type=by-categ`} style={{ textDecoration: "none", }}>
            <div>
                <div className='card'>
                    <div className='image-container'>
                        <img src={`/cover_images/${item.category_image}`} alt="" />
                    </div>
                    <div className='card-container'>
                        <p>{item.category_title}</p>
                    </div>
                </div>
            </div>
        </a>
        </>)
    });

    useEffect(() => {
        const callFetch = async () => {
            const response = await fetchData(userData, "/api/categories_all", false);
            console.log(response)
            if (response.data) {
                setState(response.data.categories);
            }
        };
        callFetch();
        // eslint-disable-next-line 
    }, []);

    return (
        <>
            <div className="header-main">

                <p className="first-header-text">Ваше <br></br>идеальное<br></br> путешествие <br></br>начинается здесь!</p>
                <a style={{ textDecoration: 'none' }} href='/tours-categoryes'>
                    <div className="choose-country-button">
                        <span>Выбрать тур</span>
                        <img src={buttonImg} alt="" />
                    </div>
                </a>
            </div>

            <div className='container'>
                <div className='main-desc'>
                    <p className='desc-p'>
                        <span className='span-desc'>Voyage Vista</span>  —  это современное турагентство, специализирующееся
                        на организации путешествий по всему миру.
                        Наша цель — создать для вас незабываемый отдых,
                        который станет источником ярких впечатлений и уникальных моментов.
                        Мы организуем как индивидуальные, так и групповые туры, предлагая широкий спектр направлений и услуг.
                    </p>
                    <img src={man} alt="" />
                </div>
                {/* {sliderObjects} */}
                <SimpleSlider sliderObjects={categCards} settings={settings} main={true} />

                <h1>Почему стоит выбрать нас?</h1>
                <div className='container'>

                    <div className='reasons'>
                        <div className='reason-div'>

                            <div className='reason' style={{ top: "150px" }}>
                                <div className='reason-content'>
                                    <h3>Индивидуальный подход</h3>
                                    <p>Мы подстраиваем туры под ваши пожелания, будь то отдых для всей семьи или романтический уикенд.</p>
                                </div>
                                <h2 style={{ top: '-400px' }}>02</h2>
                            </div>

                        </div>

                        <div className='reason-div'>
                            <div className='reason'>
                                <div className='reason-content'>
                                    <h3>Гибкие условия бронирования</h3>
                                    <p>Предлагаем удобные варианты оплаты и регулярные акции, чтобы сделать путешествие доступнее.</p>
                                </div>
                                <h2 style={{ top: '-400px' }}>01</h2>
                            </div>
                        </div>

                        <div className='reason-div'>
                            <div className='reason' style={{ top: "150px" }}>
                                <div className='reason-content'>
                                    <h3>Доступные цены и уникальные предложения</h3>
                                    <p>Мы предоставляем выгодные условия и часто радуем клиентов специальными предложениями и скидками.</p>
                                </div>
                                <h2 style={{ top: '-450px' }}>04</h2>
                            </div>
                        </div>

                        <div className='reason-div'>
                            <div className='reason'>
                                <div className='reason-content'>
                                    <h3>Проверенные партнеры</h3>
                                    <p>Работаем только с надежными перевозчиками и отелями, чтобы обеспечить максимальный комфорт и безопасность путешествий.</p>
                                </div>
                                <h2 style={{ top: '-440px' }}>03</h2>
                            </div>
                        </div>
                    </div>
                </div >



                <h1>Каждое путешествие — это новая история!</h1>
                <div className='comments'>
                    <div className='comment-container'>
                        <div className='comment'>
                            <div className='comment-header'>
                                <img src={girl} alt="" />
                                <h3>Имя Фамилия</h3>
                            </div>
                            <div className='comment-content'>
                                <p>
                                    Я всегда мечтала о путешествии в Италию, но не знала, с чего начать.
                                    Обратилась в Voyage Vista по рекомендации подруги.
                                    Консультант помогла мне выбрать маршрут, который включал не только знаменитые города,
                                    но и менее известные, но невероятно красивые места. Мы побывали в Риме, Венеции и на Сицилии.
                                    Каждый день был наполнен новыми впечатлениями. Оперативная поддержка по всем вопросам и удобный
                                    трансфер сделали наше путешествие еще более комфортным. Единственный минус — на некоторые экскурсии
                                    хотелось бы больше времени, но это уже вопрос личных предпочтений. В целом, это был лучший отпуск в моей жизни!
                                </p>
                            </div>
                            <div style={{ height: "40px" }}></div>
                        </div>
                    </div>
                    <div className='comment-container'>
                        <div className='comment'>
                            <div className='comment-header'>
                                <img src={girl} alt="" />
                                <h3>Имя Фамилия</h3>
                            </div>
                            <div className='comment-content'>
                                <p>
                                    Пользовались услугами Voyage Vista для организации свадебного путешествия на Мальдивы.
                                    Все было просто прекрасно! Спасибо за отличный сервис!
                                </p>
                            </div>
                            <div style={{ height: "40px" }}></div>
                        </div>
                    </div>
                    <div className='comment-container'>
                        <div className='comment'>
                            <div className='comment-header'>
                                <img src={girl} alt="" />
                                <h3>Имя Фамилия</h3>
                            </div>
                            <div className='comment-content'>
                                <p>
                                    С друзьями мы решили отправиться в активный отдых в Грузии. Обратились в Voyage Vista, и это
                                    было правильное решение. Нам подобрали идеальный маршрут, который включал походы в горах, сплав
                                    по реке и экскурсии по Тбилиси. Все детали были продуманы: от трансфера до размещения. Одним из
                                    плюсов была возможность адаптировать программу под наши желания. Были небольшие задержки с
                                    трансфером в один из дней, но менеджеры оперативно решили вопрос и предложили нам компенсацию в
                                    виде бесплатной экскурсии. В целом, очень позитивный опыт, и мы планируем обратиться снова!
                                </p>
                            </div>
                            <div style={{ height: "40px" }}></div>
                        </div>
                    </div>
                </div>
            </div>

            <img src={train} style={{ width: '100%' }} alt='Poezd LOL'></img>


        </>
    );
}

