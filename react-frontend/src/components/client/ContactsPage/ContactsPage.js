import './ContactsPage.css';
import React from 'react';

export default function ContactsPage() {
    return (
        <>
            <div style={{ height: '172px', background: "#5D7EA7", marginBottom: '64px', width: "100%" }}></div>
            <div className='contacts-container'>
                <div className='contacts-text-block'>
                    <h1>Контакты</h1>
                    <div>
                        <p className='contacts-bt'>Телефон:</p>
                        <p className='contacts-st'>+7 (495) 123-45-67</p>
                    </div>
                    <div>
                        <p className='contacts-bt'>Электронная почта:</p>
                        <p className='contacts-st'>info@puteshestvuisnamy.ru</p>
                    </div>
                    <div>
                        <p className='contacts-bt'>Адрес:</p>
                        <p className='contacts-st'>Москва, ул. Туристическая, 15, офис 5</p>
                    </div>
                    <div>
                        <p className='contacts-bt'>Часы работы:</p>
                    </div>
                    <div>
                        <div>
                            <p className='contacts-bt date-p'>Пн-Пт:</p>
                            <p className='contacts-st date-p'>09:00 - 18:00</p>
                        </div>
                        <div>
                            <p className='contacts-bt date-p'>Сб:</p>
                            <p className='contacts-st date-p'>10:00 - 15:00</p>
                        </div>
                        <div>
                            <p className='contacts-bt date-p'>Вс:</p>
                            <p className='contacts-st date-p'>выходной</p>
                        </div>
                    </div>
                </div>
                <div className='contacts-page-block'>
                    <img src='/Contacts/ofice.png' alt=''></img>
                </div>
            </div>
        </>
    );
}

