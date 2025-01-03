import React from 'react';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

import './TourSlider.css';

import arrowLeft from '../../../resources/Slider/Images/arrow_left.png';
import arrowRight from '../../../resources/Slider/Images/arrow_right.png';


const tour =     {

    tour_image: 'image1.jpg',

    tour_title: 'Приключение на Гавайях',

    tour_start_date: '2025-01-10',

    tour_end_date: '2025-01-20',

    tour_description: 'Незабываемое путешествие на самый красивый остров.',

    country: { country_name: 'США' },

    tour_price: 1000,

    price_with_discount: 800,

}

const toursData = [
    tour, tour, tour

    // Добавьте дополнительные туры здесь

];


function SampleNextArrow(props) {
    const { onClick } = props;
    return (
        <div className='SampleNextArrow'
            style={{
                display: "block",
                position: "absolute",
                top: "51%",
                right: "-60px", // Позиция по правому краю
                transform: "translateY(-50%)", // Центрирование по вертикали
                zIndex: 1 // Чтобы стрелка была поверх других элементов
            }}
            onClick={onClick}>
            <img src={arrowRight} alt=''></img>
        </div>
    );
}

function SamplePrevArrow(props) {
    const { onClick } = props;
    return (
        <div
            style={{

                display: "block",
                position: "absolute",
                top: "50%",
                left: "-80px", // Позиция по левому краю
                transform: "translateY(-50%)", // Центрирование по вертикали
                zIndex: 1 // Чтобы стрелка была поверх других элементов

            }}
            onClick={onClick}>
            <img src={arrowLeft} alt=''></img>
        </div>
    );
}

export default function TourSlider(props) {
    const sett = props.settings;
    const className = `Slider Centered-slider'}`

    return (
        <div className={className}>
            <Slider {...sett}
                nextArrow={<SampleNextArrow />}
                prevArrow={<SamplePrevArrow />}
            >
                {/* {props.tours.map((item, index) => (
                    <div>
                        <div className='profile-tour-card'>
                            <h1></h1>
                            <div>
                                <div>
                                    <label>asfasf</label>
                                    <input type='text'></input>
                                </div>
                                <div>
                                    <label>asfasf</label>
                                    <input type='text'></input>
                                </div>
                            </div>
                        </div>
                    </div>
                ))} */}
                {props.tours}
            </Slider>
        </div>
    );
}

