import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import './AddCountryOrCategory.css';

import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken, tryGetReq, fetchData } from '../../general/web_ops';
import { setCookieInfo, deleteCookie } from '../../general/cookie_ops';

import PlusImage from '../../../resources/admin/Images/cricle_plus.png'

export default function AddCountryOrCategory(props) {
    const { id } = useParams();
    const fileInputRef = useRef(null);
    const [image, setImage] = useState(PlusImage);

    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    const [imageName, setImageName] = useState('файл не выбран');
    const location = useLocation();
    let pathName = location.pathname.replace("/admin", "").replace("/add", "")

    let headerText;
    let apiPath;

    if (pathName.includes("categories")) {
        headerText = "категории"
        apiPath = "categories"
    }
    else {
        headerText = "страны"
        apiPath = "countries"
    }

    const fetchDataA = useCallback(async () => {
        let result = null;
        try {
            let token = userData.access_token;
            console.log("CHECK")
            let check = await checkToken(userData?.access_token)
            if (!check) {
                console.log("Refresh")
                let refresh = await refreshToken(userData?.refresh_token)
                if (!refresh) {
                    deleteCookie();
                    setUserData(null);
                    alert("Авторизируйтесь повторно");
                    navigate("/login");
                    return result;
                }
                let newUserData = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role }
                setCookieInfo(newUserData);
                setUserData(newUserData);
                token = refresh;
            }
            console.log("SUCCESS to refresh")
            let response = await tryGetReq(token, `/api/admin_panel${pathName}/${props.id}/edit`);
            console.log(result);
            if (response.status === 200) {
                result = await response.json()
            } else {
                alert(`Произошла ошибка при загрузке данных.`);
            }
            return result;
        } catch (e) {
            alert(`Не удалось. Попробуйте позже`);
            return result;
        }

    }, [userData, navigate, setUserData, pathName, props]); // зависимости, если есть

    useEffect(() => {
        if(props?.action === "upd"){
            const callFetch = async () => {
                const response = await fetchData(userData, `/api/admin_panel/${apiPath}/${id}/edit`);
                if (response.data) {
                    console.log(response)
                    return response;
                }
                else {
                    if (response.action === "unauth") {
                        deleteCookie();
                        setUserData(null);
                        alert(response.message);
                        navigate("/login");
                        return null;
                    }
                    else {
                        alert(response.message);
                        return null;
                    }
                }

            };
            callFetch();
        }
    }, [props])


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
            <form method='post' action=''>
                <div className='form-container'>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}></input>
                        <div style={{ marginBottom: '6px' }}><label>Описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' placeholder={`Введите описание ${headerText}`}></textarea>
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

