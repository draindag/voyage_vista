import '../../../resources/constants.css';
import './ToursCategoryesPage.css';
import React, {useEffect, useState} from 'react';
import TourSlider from './TourSlider';

import '../MainPage/MainPage.css';
import { fetchData } from '../../general/web_ops';

import SlideImage from '../../../resources/Slider/Images/slideImg.png'
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

    const [state, setState] = useState([]);

    let sliderObjects = []
    state.forEach(item => {
        sliderObjects.push(<>
            <div className='card-tc'>
                <div>
                    <h1>{item?.category_title}</h1>
                    <p>{item?.category_description}</p>
                </div>
                <div className='tour-image-container-cat-page'>
                    <img src={`/cover_images/${item.category_image}`}alt=''></img>
                </div>
            </div>
        </>)
    })

    useEffect(() => {
        const callFetch = async () => {
            const response = await fetchData({}, "/api/categories_all", false);
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
            <div className="tours-categoryes-bgpage">
                <p className="tours-categoryes-header-text">Выберите свой тур с<br></br>нами</p>
            </div>
            <div className='container'>
                <TourSlider sliderObjects={sliderObjects} settings={sliderSettings}/>
            </div>
        
        </>
    );
}

