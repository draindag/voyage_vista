import './Navbar.css';
import '../../../resources/constants.css';

import React, { useState, useEffect, useRef } from 'react';
import ProfileManager from '../ProfileManager/ProfileManager';


import home from '../../../resources/Navbar/Images/home.svg';
import contacts from '../../../resources/Navbar/Images/contacts.svg';
import tourist from '../../../resources/Navbar/Images/tourist.svg';
import personalAccount from '../../../resources/Navbar/Images/personalAccount.svg';
import country from '../../../resources/Navbar/Images/country.svg';
import logo from '../../../resources/Navbar/Images/logo.svg';


export default function Navbar() {
    const countrySelect = useRef(null);

    const [scrolled, setScrolled] = useState(false);
    const [showProfileManager, setShowProfileManager] = useState(false);
    const [paddingTop, setPaddingTop] = useState(30);

    const [positions, setPositions] = useState({ select: null, profile: null })

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

    const handleResize = () => {
        const profile = document.querySelector('.profile-button').getBoundingClientRect();
        const select = document.querySelector('.country-button').getBoundingClientRect();
        setPositions({ select: select, profile: profile });
    }


    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        window.addEventListener('resize', handleResize);
        handleResize();
        // Удаляем обработчик при размонтировании компонента
        return () => {
            window.removeEventListener('scroll', handleScroll);
            window.removeEventListener('resize', handleResize);
        };
    }, []);




    let navClasses = `${scrolled ? 'scrolled' : ''} navbar`
    return <>
        <div className={navClasses} id="navbar" style={{ paddingTop: `${paddingTop}px` }}>
            <div className="header-logo">
                <img src={logo} alt="" />
                <span style={{ maxWidth: "188px", textWrap: "wrap" }}>Voyage vista</span>
            </div>
            <div className="header-navbar" id="header-navbar" style={{ background: scrolled ? 'none' : 'var(--navbar-background)' }}>
                <div className="navbar-content">
                    <a href="/"><img src={home} alt="" /><span>Главная</span></a>
                    {/* <a href="/countryes"><img src={country} alt="" /><span>Страны</span></a> */}
                    <button id='country-button' className='country-button' onClick={() => countrySelect.current.click()}><img src={country} alt="" /><span>Страны</span></button>
                    <select
                        style={{ display: 'none' }}
                        ref={countrySelect}
                    >
                        <option>asfasfasf</option>
                    </select>
                    <a href="/tourist"><img src={tourist} alt="" /><span>Туристам</span></a>
                    <a href="/contacts"><img src={contacts} alt="" /><span>Контактная информация</span></a>
                    <button id='profile-button' className='profile-button' onClick={() => setShowProfileManager(!showProfileManager)}><img src={personalAccount} alt="" /><span>Мой кабинет</span></button>
                </div>
            </div>
        </div>
        {showProfileManager ? <ProfileManager onExit={() => { setShowProfileManager(!showProfileManager) }} style={{
            position: 'absolute',
            top: `${positions.profile?.bottom+50}px`,
            left: `${positions.profile?.left}px`,
        }} /> : null}
    </>
}

