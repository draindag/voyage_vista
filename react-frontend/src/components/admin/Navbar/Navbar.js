import './AdminNavbar.css';
import React from 'react';





export default function Navbar() {
    return <>
        <div className='admnavbar'>
            <div className="header-admnavbar" id="header-navbar">
                <div className="admnavbar-content">
                    <a className='primary-btn' href="/admin/entitylist?name=categories">Категории</a>
                    <a className='primary-btn' href="/admin/entitylist?name=countries"><span>Страны</span></a>
                    <a className='primary-btn' href="/admin/entitylist?name=tours"><span>Туры</span></a>
                    <a className='primary-btn' href="/admin/entitylist?name=offers"><span>Акции</span></a>
                    <a className='primary-btn' href="/admin/moderreg"><span>Добавить пользователя</span></a>
                    <a className='primary-btn' href="/"><span>На сайт</span></a>
                </div>
            </div>
        </div>
    </>
}

