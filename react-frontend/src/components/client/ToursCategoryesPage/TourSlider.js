import React from 'react';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import './TourSlider.css';

function SampleNextArrow(props) {
    const { onClick } = props;
    return (
        <div className='SampleNextArrow'
        style={{
            display: "block",
            position: "absolute",
            top: "50%",
            right: "-50px", 
            transform: "translateY(-50%)", 
            zIndex: 1 
        }}
            onClick={onClick}>
            <img src={'/Slider/Images/arrow_right.png'} alt=''></img>
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
            left: "-80px", 
            transform: "translateY(-50%)", 
            zIndex: 1 
        }}
            onClick={onClick}>
            <img src={'/Slider/Images/arrow_left.png'} alt=''></img>
        </div>
    );
}

export default function TourSlider(props) {
    const sett = props.settings
    const className = `Slider Centered-slider'}`
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

