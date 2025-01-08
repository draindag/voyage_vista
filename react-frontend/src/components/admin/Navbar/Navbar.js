import './AdminNavbar.css';
import React from 'react';
import { Link } from 'react-router';




export default function Navbar() {
    return <>
        <div className='admnavbar'>
            <div className="header-admnavbar" id="header-navbar">
                <div className="admnavbar-content">
                    <Link className='primary-btn' to="/admin/entitylist?name=categories">Категории</Link>
                    <Link className='primary-btn' to="/admin/entitylist?name=countries"><span>Страны</span></Link>
                    <Link className='primary-btn' to="/admin/entitylist?name=tours"><span>Туры</span></Link>
                    <Link className='primary-btn' to="/admin/entitylist?name=offers"><span>Акции</span></Link>
                    <Link className='primary-btn' to="/admin/moderreg"><span>Добавить пользователя</span></Link>
                    <Link className='primary-btn' to="/"><span>На сайт</span></Link>
                </div>
            </div>
        </div>
    </>
}

