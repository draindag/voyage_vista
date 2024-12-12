import React, { useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import './AddCountryOrCategory.css';

import PlusImage from '../../../resources/admin/Images/cricle_plus.png'

export default function AddCountryOrCategory() {
    const fileInputRef = useRef(null);
    const [image, setImage] = useState(PlusImage);
    const [imageName, setImageName] = useState('файл не выбран');
    const location = useLocation();
    let pathName = location.pathname.replace("/admin", "").replace("/add", "")

    let headerText;

    if (pathName === '/categories') {
        headerText = "категории"
    }
    else {
        headerText = "страны"
    }

    const handleImageChange = (e) => {
        console.log("ОТСЛОВИЛ")
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
                setImageName(file.name)
            };
            reader.readAsDataURL(file);
        }
    };

    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form>
                <div className='form-container'>
                    <div>
                        <label>Название категории</label>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}></input>
                        <label>Описание категории</label>
                        <textarea className='wide-input hight-input no-file-input' placeholder={`Введите описание ${headerText}`}></textarea>
                    </div>
                    <div>
                        <div className='image-preview'>
                            <img src={image} alt=''></img>
                        </div>
                        <div className='add-image-input-block'>
                            <label>Загрузить картинку с компьютера:</label>
                            <div style={{flexBasis: "100%"}} className='file-input'><button type='button' className='file-choice-btn' onClick={() => fileInputRef.current.click()}>Выберите файл</button><p>{imageName}</p></div>
                            <input 
                            ref={fileInputRef} 
                            style={{display: 'none'}} 
                            type="file" accept="image/*" onChange={handleImageChange} />
                        </div>
                    </div>
                </div>
            </form>
            <div>
                <button className='primary-btn'>Добавить</button>
            </div>
        </div>
    </>

    );
};

