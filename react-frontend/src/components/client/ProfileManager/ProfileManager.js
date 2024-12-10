import React from 'react';
import './ProfileManager.css';



export default function ProfileManager(props) {
    let ulContent;
    const jwt = props.jwt
    if(jwt === null){
        ulContent = <><li><a href='/login'>Войти</a></li><li><a href='/reg'>Регистрация</a></li></>
    }
    else{
        ulContent = <><li><a href='/profile'>Профиль</a></li><li><a href='/'>Выйти</a></li></>
    }

    return (
        <div className='profile-manager'>
            <ul>
                {ulContent}
            </ul>
        </div>
    );
}

