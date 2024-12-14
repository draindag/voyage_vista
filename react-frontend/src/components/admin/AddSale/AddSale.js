import React, { useState } from 'react';
import './AddSale.css';


export default function AddSale() {
    const [name, setName] = useState("");
    const [date, setDate] = useState("");
    const [disc, setDisc] = useState(0);
    

    let headerText = "акции";

    

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
                        <button className='primary-btn'>Добавить</button>
                    </div>
                </div>
        </div>
    </>

    );
};

