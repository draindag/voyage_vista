import React, { useState } from 'react';
import './AddSale.css';

import { useNavigate } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { refreshToken, checkToken } from '../../general/web_ops';
import { setCookieInfo, deleteCookie} from '../../general/cookie_ops';


export default function AddSale() {
    const [name, setName] = useState("");
    const [date, setDate] = useState("");
    const [disc, setDisc] = useState(0);

    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    let headerText = "акции";

    const tryReq = async (token, data) => {
        let response = await fetch("http://127.0.0.1:8000/api/admin_panel/offers/new", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json;charset=utf-8',
                'Authorization': `Bearer ${token}`
            },
            body: data
        });
        return response;
    };

    const sendForm = async () => {
        const data = {"offer_title": name, "end_date": date, "discount_size": disc}
        console.log(data)
        try {
            let token = userData.access_token;
            let check = await checkToken(userData?.access_token)
            if(!check){
                console.log("refresh")
                let refresh = await refreshToken(userData?.refresh_token)
                if(!refresh){
                    deleteCookie();
                    setUserData(null);
                    alert("Авторизируйтесь повторно");
                    navigate("/login");
                    return;
                }
                let newUserData = {access_token: refresh, refresh_token: userData.refresh_token, role: userData.role}
                setCookieInfo(newUserData);
                setUserData(newUserData);
                token = refresh;
            }
            let response = await tryReq(token, JSON.stringify(data))
            if (response.status === 201) {
                alert("Успешно!");
                navigate("/admin/entitylist?name=offers");
            } else {
                let responseData = await response.json()
                let messages = "";
                if (responseData.errors) {
                    let errors = responseData.errors
                    if (errors.email) {
                        messages = messages.concat(`\n- ${errors.email[0]}`)
                    }
                    if (errors.password) {
                        messages = messages.concat(`\n- ${errors.password[0]}`)
                    }
                }
                if (response.message) {
                    messages = messages.concat(`\n${response.message}`)
                }
                alert(`Произошла ошибка при добавлении. ${messages}`);
            }
        } catch (e) {
            alert(`Не удалось. Попробуйте позже`);
        }
    }
    

    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form method='post' action=''>
                <div className='form-container' style={{ justifyContent: "center" }}>
                    <div style={{ width: "600px" }}>
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}
                        onChange={(e)=>{setName(e.target.value)}}></input>
                        <div className='add-left-block'><label>Дата окончания действия</label>
                            <input type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}
                            onChange={(e)=>{setDate(e.target.value)}}></input>
                        </div>
                        <div className='add-left-block'><label>Процент скидки</label>
                            <input type='number' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }} placeholder='%'
                            onChange={(e)=>{setDisc(e.target.value)}}></input>
                        </div>
                    </div>
                </div>
            </form>
            <div className='form-container' style={{ justifyContent: "center" }}>
                    <div className='submit-button-block'>
                        <button className='primary-btn' onClick={() => sendForm()}>Добавить</button>
                    </div>
                </div>
        </div>
    </>

    );
};

