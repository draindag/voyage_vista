import './Navbar.css';
import '../../../resources/constants.css';

import React, { useState, useEffect } from 'react';
import ProfileManager from '../ProfileManager/ProfileManager';


import home from '../../../resources/Navbar/Images/home.svg';
import contacts from '../../../resources/Navbar/Images/contacts.svg';
import tourist from '../../../resources/Navbar/Images/tourist.svg';
import personalAccount from '../../../resources/Navbar/Images/personalAccount.svg';
import country from '../../../resources/Navbar/Images/country.svg';
import logo from '../../../resources/Navbar/Images/logo.svg';


export default function Navbar() {
    const [scrolled, setScrolled] = useState(false);
    const [showProfileManager, setShowProfileManager] = useState(false);
    const [paddingTop, setPaddingTop] = useState(30);
    const handleScroll = () => {
        const scrollTop = window.scrollY;
        if (scrollTop > 30) {
            setScrolled(true);
            setPaddingTop(0);
        } else {
            setScrolled(false);
            setPaddingTop(30 - scrollTop);
        }
    };


    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        // Удаляем обработчик при размонтировании компонента
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);




    let navClasses = `${scrolled? 'scrolled': ''} navbar`
    return <>
            <div className={navClasses} id="navbar" style={{ paddingTop: `${paddingTop}px` }}>
                <div className="header-logo">
                    <img src={logo} alt="" />
                    <span style={{maxWidth: "188px", textWrap: "wrap"}}>Voyage vista</span>
                </div>
                <div className="header-navbar" id="header-navbar" style={{background: scrolled ? 'none' : 'var(--navbar-background)'}}>
                    <div className="navbar-content">
                        <a href="/"><img src={home} alt="" /><span>Главная</span></a>
                        <a href="/countryes"><img src={country} alt="" /><span>Страны</span></a>
                        <a href="/tourist"><img src={tourist} alt=""/><span>Туристам</span></a>
                        <a href="/contacts"><img src={contacts} alt="" /><span>Контактная информация</span></a>
                        <button onClick={() => setShowProfileManager(!showProfileManager)}><img src={personalAccount} alt="" /><span>Мой кабинет</span></button>
                    </div>
                </div>
            </div>
            {showProfileManager ? <ProfileManager jwt={null}/> : null}
    </>
}

