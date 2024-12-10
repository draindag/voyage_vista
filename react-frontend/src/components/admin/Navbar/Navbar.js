import './AdminNavbar.css';
import '../../../resources/constants.css';

import React from 'react';





export default function Navbar() {
    return <>
        <div className='admnavbar'>
            <div className="header-admnavbar" id="header-navbar">
                <div className="admnavbar-content">
                    <a href="/admin/entitylist?name=categories"><span>Категории</span></a>
                    <a href="/admin/entitylist?name=countries"><span>Страны</span></a>
                    <a href="/admin/entitylist?name=tours"><span>Туры</span></a>
                    <a href="/admin/entitylist?name=offers"><span>Акции</span></a>
                    <a href="/admin"><span>Добавить пользователя</span></a>
                    <a href="/"><span>На сайт</span></a>
                </div>
            </div>
        </div>
    </>
}

