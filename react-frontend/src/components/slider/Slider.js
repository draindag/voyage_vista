import React from 'react';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

import './Slider.css';

import SlideImage from '../../resources/Slider/Images/slideImg.png'


import arrowLeft from '../../resources/Slider/Images/arrow_left.png';
import arrowRight from '../../resources/Slider/Images/arrow_right.png';



const imageArr = [
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage
]



function SampleNextArrow(props) {
    const { onClick } = props;
    return (
        <div
            style={{ display: "block", position: "relative", top: '-300px', left: "103%" }}
            onClick={onClick}>
            <img src={arrowRight} alt=''></img>
        </div>
    );
}

function SamplePrevArrow(props) {
    const { onClick } = props;
    return (
        <div
            style={{ display: "block", position: "relative", top: '270px', left: "-4%" }}
            onClick={onClick}>
            <img src={arrowLeft} alt=''></img>
        </div>
    );
}



export default function SimpleSlider() {
    // const [defaultImage, setDefaultImage] = useState({});
    const settings = {
        // className: "center",
        // centerMode: true,
        // infinite: true,
        centerPadding: "0px",
        slidesToShow: 4,
        speed: 500,
        nextArrow: <SampleNextArrow />,
        prevArrow: <SamplePrevArrow />,
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



    return (
        <div className="Slider">
            <div style={{ textAlign: 'center' }}>
                <h2 style={{ position: 'relative', top: '100px', fontSize: "50px", fontWeight: 400 }}>Выбери свой тур</h2>
                <p style={{ position: 'relative', top: '100px', fontSize: "32px", fontWeight: 400  }}>Самые востребованные предложения от нашей компании</p>
            </div>
            <Slider {...settings}>
                {imageArr.map((item) => (
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
                ))}
            </Slider>
        </div>
    );
}

