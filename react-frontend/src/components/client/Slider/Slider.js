import React from 'react';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

import './Slider.css';

import arrowLeft from '../../../resources/Slider/Images/arrow_left.png';
import arrowRight from '../../../resources/Slider/Images/arrow_right.png';


function SampleNextArrow(props) {
    const { onClick } = props;
    return (
        <div className='SampleNextArrow'
        style={{

            display: "block",

            position: "absolute",

            top: "50%",

            right: "-100px", // Позиция по правому краю

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

            left: "-100px", // Позиция по левому краю

            transform: "translateY(-50%)", // Центрирование по вертикали

            zIndex: 1 // Чтобы стрелка была поверх других элементов

        }}
            onClick={onClick}>
            <img src={arrowLeft} alt=''></img>
        </div>
    );
}

export default function SimpleSlider(props) {
    // const [defaultImage, setDefaultImage] = useState({});
    // const settings = {
    //     // className: "center",
    //     // centerMode: true,
    //     // infinite: true,
    //     centerPadding: "0px",
    //     slidesToShow: 4,
    //     speed: 500,
    //     nextArrow: <SampleNextArrow />,
    //     prevArrow: <SamplePrevArrow />,
    //     responsive: [
    //         {
    //             breakpoint: 1890,
    //             settings: {
    //                 slidesToShow: 3,
    //             },
    //         },
    //         {
    //             breakpoint: 1430,
    //             settings: {
    //                 slidesToShow: 2,
    //             },
    //         },
    //     ],
    // };
    const sett = props.settings
    const className = `Slider ${props.main ? "": 'Centered-slider'}`

    return (
        <div className={className}>
            {props.main ? <div style={{ textAlign: 'center' }}>
                <h2 style={{ position: 'relative', top: '100px', fontSize: "50px", fontWeight: 400 }}>Выбери свой тур</h2>
                <p style={{ position: 'relative', top: '100px', fontSize: "32px", fontWeight: 400  }}>Самые востребованные предложения от нашей компании</p>
            </div> : null}
            <Slider {...sett}
                    nextArrow={<SampleNextArrow />}
                    prevArrow={<SamplePrevArrow />}
            >
                {props.sliderObjects}
            </Slider>
        </div>
    );
}

