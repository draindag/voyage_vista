import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import './AddCountryOrCategory.css';

import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken, tryGetReq, fetchData, sendData } from '../../general/web_ops';
import { setCookieInfo, deleteCookie } from '../../general/cookie_ops';

import PlusImage from '../../../resources/admin/Images/cricle_plus.png'

export default function AddCountryOrCategory(props) {
    const { id } = useParams();
    const fileInputRef = useRef(null);

    const [state, setState] = useState({ image: null, imageToShow: null, prevImage: null, imageName: "файл не выбран", title: "", desc: "", ent_id: null })

    console.log(state)
    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();
    const location = useLocation();
    let pathName = location.pathname.replace("/admin", "").replace("/add", "")

    let headerText;
    let apiPath;
    let nameField;
    let titleOrName;

    if (pathName.includes("categories")) {
        headerText = "категории";
        apiPath = "categories";
        nameField = "category";
        titleOrName = "title";
    }
    else {
        headerText = "страны";
        apiPath = "countries";
        nameField = "country";
        titleOrName = "name";
    }

    useEffect(() => {
        if (props?.action === "upd") {
            const callFetch = async () => {
                const response = await fetchData(userData, `/api/admin_panel/${apiPath}/${id}/edit`);
                if (response.data) {
                    let responseData = response.data[nameField];
                    let imagePath = responseData[`${nameField}_image`].replace("flask-backend/webapp", "")
                    console.log(response);
                    setState({
                        ...state,
                        title: responseData[`${nameField}_${titleOrName}`],
                        desc: responseData[`${nameField}_description`],
                        ent_id: responseData[`${nameField}_id`],
                        // image: `/${responseData[`${nameField}_image`]}`
                        image: imagePath,
                        imageToShow: imagePath,
                        prevImage: imagePath
                    })
                    // "country": {
                    //     "country_id": "b0a3a4ce-b5c8-42d9-b23a-d93d768e0c62",
                    //     "country_name": "Италия",
                    //     "country_description": "Страна с богатой культурой",
                    //     "country_image": "flask-backend/webapp/cover_images/b0a3a4ce-b5c8-42d9-b23a-d93d768e0c62.png"
                    //   }

                    // "category": {
                    //     "category_id": "123e4567-e89b-12d3-a456-426614174000",
                    //     "category_title": "Семейные туры",
                    //     "category_description": "Туры, подходящие для семейного отдыха",
                    //     "category_image": "flask-backend/webapp/cover_images/123e4567-e89b-12d3-a456-426614174000.png"
                    //   }
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


    const sendForm = async () => {
        let method = 'POST';
        let url = `/api/admin_panel/${apiPath}/new`;

        let formData = new FormData();
        formData.append(`${nameField}_${titleOrName}`, state.title)
        formData.append(`${nameField}_description`, state.desc)
        if (props.action === 'upd') {
            method = 'PUT';
            url = `/api/admin_panel/${apiPath}/${id}/edit`;
            formData.append(`${nameField}_id`, state.ent_id);
            if (state.image != state.prevImage) {
                console.log("ОДИНАКОВЫЕ")
                formData.append(`cover_image`, state.image)
            }
        }
        else{
            formData.append(`cover_image`, state.image)
        }
        console.log(formData)

        // formData = "category_description=asfasfasfas&password=секрет"
        const response = await sendData(userData, url, formData, method, true);
        if (response.data) {
            console.log(response)
            alert("Успешно!");
            navigate(`/admin/entitylist?name=${apiPath}`);
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


    const handleImageChange = (e) => {
        console.log("ОТСЛОВИЛ")
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setState({ ...state, image: file, imageToShow: reader.result, imageName: file.name })
            };
            reader.readAsDataURL(file);
        }
    };

    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form method='post' action=''>
                <div className='form-container'>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`} value={state.title}
                            onChange={(e) => { setState({ ...state, title: e.target.value }) }}
                        ></input>
                        <div style={{ marginBottom: '6px' }}><label>Описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' placeholder={`Введите описание ${headerText}`} value={state.desc}
                            onChange={(e) => { setState({ ...state, desc: e.target.value }) }}
                        ></textarea>
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
            </form>
            <div className='form-container' style={{ justifyContent: "end" }}>
                <div className='submit-button-block'>
                    <button type='submit' className='primary-btn' onClick={() => sendForm()}>Добавить</button>
                </div>
            </div>
        </div>
    </>

    );
};

