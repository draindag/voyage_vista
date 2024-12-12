import React from 'react';
import './AddSale.css';



export default function AddSale() {

    let headerText = "акции";

    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form>
                <div className='form-container' style={{ justifyContent: "center" }}>
                    <div style={{ width: "600px" }}>
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

