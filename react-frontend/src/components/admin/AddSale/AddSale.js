import React, { useState, useEffect } from 'react';
import './AddSale.css';

import { useNavigate, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';


export default function AddSale(props) {
    const { id } = useParams();
    const [state, setState] = useState({ offer_id: "", offer_title: "", discount_size: 0, end_date: "" });
    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    let headerText = "акции";
    console.log(state);


    useEffect(() => {
        if (props?.action === "upd") {
            const callFetch = async () => {
                const response = await fetchData(userData, `/api/admin_panel/offers/${id}/edit`);
                if (response.data) {
                    console.log(response)
                    let data = response.data.special_offer
                    setState({
                        offer_id: data.offer_id,
                        offer_title: data.offer_title,
                        discount_size: data.discount_size,
                        end_date: data.end_date
                    });
                    setUserData(response.userData);

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
    // eslint-disable-next-line
    }, [])

    const sendForm = async () => {
        let data;
        let url;
        let method;
        if (props?.action === "upd") {
            data = { "offer_title": state.offer_title, "end_date": state.end_date, "discount_size": state.discount_size, "offer_id": state.offer_id }
            url = `/api/admin_panel/offers/${id}/edit`
            method = 'PUT';
        }
        else {
            data = { "offer_title": state.offer_title, "end_date": state.end_date, "discount_size": state.discount_size }
            url = '/api/admin_panel/offers/new'
            method = "POST";
        }
        const response = await sendData(userData, url, JSON.stringify(data), method);
        if (response.data) {
            console.log(response)
            setUserData(response.userData);
            alert("Успешно!");
            navigate("/admin/entitylist?name=offers");
        }
        else {
            if (response.action === "unauth") {
                deleteCookie();
                setUserData(null);
                alert(response.message);
                navigate("/login");
            }
            else {
                let logMess = `${response.message}\n${JSON.stringify(response.log)}`
                alert(logMess);
            }
        }
    }


    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form method='post' action=''>
                <div className='form-container' style={{ justifyContent: "center" }}>
                    <div style={{ width: "600px" }}>
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input value={state.offer_title} className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}
                            onChange={(e) => { setState({ ...state, offer_title: e.target.value }) }}></input>
                        <div className='add-left-block'><label>Дата окончания действия</label>
                            <input value={state.end_date} type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}
                                onChange={(e) => { setState({ ...state, end_date: e.target.value }) }}></input>
                        </div>
                        <div className='add-left-block'><label>Процент скидки</label>
                            <input value={state.discount_size} type='number' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }} placeholder='%'
                                onChange={(e) => { setState({ ...state, discount_size: e.target.value }) }}></input>
                        </div>
                    </div>
                </div>
            </form>
            <div className='form-container' style={{ justifyContent: "center" }}>
                <div className='submit-button-block'>
                    <button className='primary-btn' onClick={() => sendForm()}>{props.action === 'upd' ? "Изменить" : "Добавить"}</button>
                </div>
            </div>
        </div>
    </>

    );
};

