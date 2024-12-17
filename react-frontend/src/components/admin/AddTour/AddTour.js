import React, { useState, useRef, useEffect, useCallback } from 'react';
import './AddTour.css';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken, tryGetReq, fetchData, sendData } from '../../general/web_ops';
import { setCookieInfo, deleteCookie } from '../../general/cookie_ops';

import PlusImage from '../../../resources/admin/Images/cricle_plus.png'

export default function AddTour(props) {
    const fileInputRef = useRef(null);

    const { id } = useParams();
    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    const [state, setState] = useState({ 
        image: null, 
        imageToShow: null, 
        prevImage: null, 
        imageName: "файл не выбран", 
        
        countriesList: null,
        categoriesList: null,
        chosenCounty: "",
        chosenCategory: "",
        
        title: "",
        dateStart: "",
        dateEnd: "",
        price: 0,
        shortDesc: "",
        desc: "", 
        ent_id: null
     })
    let headerText = "тура";

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setState({ ...state, image: file, imageToShow: reader.result, imageName: file.name })
            };
            reader.readAsDataURL(file);
        }
    };



//     "tour": {
//     "tour_id": "a1b2c3d4-e56f-78g9-h0i1-j234k567l890",
//     "tour_title": "Семейный отдых",
//     "tour_description": "Отличный тур для всей семьи",
//     "tour_text": "Полное описание тура...",
//     "tour_price": 850,
//     "price_with_discount": 765,
//     "tour_start_date": "2024-08-01",
//     "tour_end_date": "2024-08-15",
//     "tour_image": "flask-backend/webapp/tour_images/a1b2c3d4-e56f-78g9-h0i1-j234k567l890.png",
//     "category": {
//       "category_id": "123e4567-e89b-12d3-a456-426614174000",
//       "category_title": "Семейные туры",
//       "category_description": "Туры, подходящие для семейного отдыха"
//     },
//     "country": {
//       "country_id": "b0a3a4ce-b5c8-42d9-b23a-d93d768e0c62",
//       "country_name": "Италия",
//       "country_description": "Страна с богатой культурой"
//     },
//     "offers": [
//       {
//         "offer_id": "f1c5a1e2-34bc-4567-89ef-fedcba123456",
//         "offer_title": "Скидка 10%",
//         "discount_size": 10,
//         "end_date": "2024-07-30"
//       }
//     ]
//   }
    useEffect(() => {
        if (props?.action === "upd") {
            const callFetch = async () => {
                const response = await fetchData(userData, `/api/admin_panel/tours/${id}/edit`);
                if (response.data) {
                    let responseData = response.data["asd"];
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
            callFetch();
        }
    }, [props]);


    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form method='post' action=''>
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
                            <select style={{ width: "300px", height: "50px", textAlign: "center" }} onChange={(e) => console.log(e.target.key)}>
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
                            <img src={state.image ? state.imageToShow : PlusImage} alt=''></img>
                        </div>
                        <div className='add-image-input-block'>
                            <label>Загрузить картинку с компьютера:</label>
                            <div style={{ flexBasis: "100%" }} className='file-input'><button type='button' className='file-choice-btn' onClick={() => fileInputRef.current.click()}>Выберите файл</button><p>{state.imageName}</p></div>
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
                </div>
                <div className='form-container' style={{ justifyContent: "end" }}>
                    <div className='submit-button-block'>
                        <button type='submit' className='primary-btn'>Добавить</button>
                    </div>
                </div>
            </form>
        </div>
    </>

    );
};

