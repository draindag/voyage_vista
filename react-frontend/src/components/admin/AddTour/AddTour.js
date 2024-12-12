import React, { useState, useRef } from 'react';
import './AddTour.css';

import PlusImage from '../../../resources/admin/Images/cricle_plus.png'

export default function AddTour() {
    const fileInputRef = useRef(null);
    const [image, setImage] = useState(PlusImage);
    const [imageName, setImageName] = useState('файл не выбран');


    let headerText = "тура";

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
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}></input>
                        <div className='add-left-block'><label>Выберите страну</label>
                            <select style={{ width: "300px", height: "50px", textAlign: "center" }}>
                                <option value='val1'>Val1</option>
                                <option value='val2'>Val2</option>
                            </select>
                        </div>
                        <div className='add-left-block'><label>Выберите категорию</label>
                            <select style={{ width: "300px", height: "50px", textAlign: "center" }}>
                                <option value='val1'>Val1</option>
                                <option value='val2'>Val2</option>
                            </select>
                        </div>
                        <div className='add-left-block'><label>Дата начала тура</label>
                            <input type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}></input>
                        </div>
                        <div className='add-left-block'><label>Дата окончания тура</label>
                            <input type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}></input>
                        </div>
                        <div className='add-left-block'><label>Стоимость тура</label>
                            <input type='number' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }} placeholder='Введите цену'></input>
                        </div>
                    </div>
                    <div>
                        <div className='image-preview'>
                            <img src={image} alt=''></img>
                        </div>
                        <div className='add-image-input-block'>
                            <label>Загрузить картинку с компьютера:</label>
                            <div style={{ flexBasis: "100%" }} className='file-input'><button type='button' className='file-choice-btn' onClick={() => fileInputRef.current.click()}>Выберите файл</button><p>{imageName}</p></div>
                            <input
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                type="file" accept="image/*" onChange={handleImageChange} />
                        </div>
                    </div>
                </div>
                <div style={{ position: 'relative', top: '-30px' }}>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Краткое описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' style={{ height: "140px" }} placeholder={`Введите описание ${headerText}`}></textarea>
                    </div>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' placeholder={`Введите описание ${headerText}`}></textarea>
                    </div>
                    <div className='add-left-block' style={{width: '595px'}}><label>Выберите категорию</label>
                            <select style={{ width: "300px", height: "50px", textAlign: "center" }}>
                                <option value='val1'>Val1</option>
                                <option value='val2'>Val2</option>
                            </select>
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

