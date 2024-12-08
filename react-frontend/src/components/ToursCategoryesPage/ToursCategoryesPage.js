import '../../resources/constants.css';
import './ToursCategoryesPage.css';
import React from 'react';
import SimpleSlider from '../slider/Slider';

import SlideImage from '../../resources/Slider/Images/slideImg.png'
const imageArr = [
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage,
    SlideImage
]

const sliderSettings = {
    className: "center",
    centerMode: true,
    infinite: true,
    centerPadding: "0px",
    slidesToShow: 1,
    speed: 500,
};


export default function ToursCategoryesPage() {

    let sliderObjects = []
    imageArr.forEach(item => {
        sliderObjects.push(<>
            <div className='card-tc'>
                <div>
                    <h1>Зимний отдых</h1>
                    <p>Зимние курорты предлагают уникальные возможности для любителей снега и зимних видов спорта. Здесь можно насладиться горнолыжными склонами, провести время на свежем воздухе и увидеть северное сияние. Эта категория отличается от других тем, что акцент сделан на активном отдыхе в условиях холодного климата. Также зимний отдых часто включает в себя уютный досуг, такие как горячий шоколад и вечерние посиделки у камина.</p>
                </div>
                <div>
                    <img src={item} alt=''></img>
                </div>
            </div>
        </>)
    })

    return (
        <>
            <div className="tours-categoryes-bgpage">
                <p className="tours-categoryes-header-text">Выберите свой тур с<br></br>нами</p>
            </div>
            <SimpleSlider sliderObjects={sliderObjects} settings={sliderSettings}/>

        </>
    );
}

