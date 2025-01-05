import './Navbar.css';
import React, { useState, useEffect } from 'react';
import ProfileManager from '../ProfileManager/ProfileManager';
import { fetchData } from '../../general/web_ops';


export default function Navbar() {

    const [scrolled, setScrolled] = useState(false);
    const [showProfileManager, setShowProfileManager] = useState(false);

    const [countries, setCountries] = useState([{}]);

    const [showList, setShowList] = useState(false);

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
        const fetchCountry = async () => {
            let response = await fetchData({}, `/api/countries_all`, false);
            if (response.data) {
                setCountries(response.data.countries);
            }
        }

        fetchCountry();
        window.addEventListener('scroll', handleScroll);
        window.addEventListener('resize', handleResize);

        handleResize();

        // Удаляем обработчик при размонтировании компонента
        return () => {
            window.removeEventListener('scroll', handleScroll);
            window.removeEventListener('resize', handleResize);
        };
    // eslint-disable-next-line
    }, []);


    let ulElements = [];

    countries.forEach(elem => {
        ulElements.push(<li>
            <a href={`/tours/${elem.country_id}?type=by-country`}>{elem.country_name}</a>
        </li>)
    })


    let navClasses = `${scrolled ? 'scrolled' : ''} navbar`
    return <>
        <div className={navClasses} id="navbar" style={{ paddingTop: `${paddingTop}px` }}>
            <div className="header-logo">
                <img src={'/Navbar/Images/logo.svg'} alt="" />
                <span style={{ maxWidth: "188px", textWrap: "wrap" }}>Voyage vista</span>
            </div>
            <div className="header-navbar" id="header-navbar" style={{ background: scrolled ? 'none' : 'var(--navbar-background)' }}>
                <div className="navbar-content">
                    <a href="/"><img src={'/Navbar/Images/home.svg'} alt="" /><span>Главная</span></a>
                    {/* <a href="/countryes"><img src={country} alt="" /><span>Страны</span></a> */}
                    <button id='country-button' className='country-button' onClick={() => setShowList(!showList)}><img src={'/Navbar/Images/country.svg'} alt="" /><span>Страны</span></button>
                    <a href="/info"><img src={'/Navbar/Images/tourist.svg'} alt="" /><span>Туристам</span></a>
                    <a href="/contacts"><img src={'/Navbar/Images/contacts.svg'} alt="" /><span>Контактная информация</span></a>
                    <button id='profile-button' className='profile-button' onClick={() => setShowProfileManager(!showProfileManager)}><img src={'/Navbar/Images/personalAccount.svg'} alt="" /><span>Мой кабинет</span></button>
                </div>
            </div>
        </div>
        {showProfileManager ? <ProfileManager onExit={() => { setShowProfileManager(!showProfileManager) }} style={{
            top: `${positions.profile?.bottom + 50}px`,
            left: `${positions.profile?.left}px`,
        }} /> : null}

        {showList ?
            <div className='country-list' style={{
                position: 'fixed',
                top: `${positions.select?.bottom + 50}px`,
                left: `${positions.select?.left}px`,
            }}>
                <ul>
                    {ulElements}
                </ul>
            </div>
            : null}



    </>
}

