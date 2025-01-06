import React from 'react';
import './ProfileManager.css';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { deleteCookie } from '../../general/cookie_ops';
import { useNavigate } from 'react-router';

export default function ProfileManager(props) {
    const {userData, setUserData} = useAuthContext();
    const navigate = useNavigate();
    let ulContent;
    if(userData === null){
        ulContent = <><li><a href='/login'>Войти</a></li><li><a href='/reg'>Регистрация</a></li></>
    }
    else{
        ulContent = <><li><a href='/profile'>Профиль</a></li><li><button onClick={()=>{
            deleteCookie();
            setUserData(null);
            props.onExit();
            navigate('/login');
        }}>Выйти</button></li></>
    }

    return (
        <div className='profile-manager' style={props.style}>
            <ul>
                {ulContent}
            </ul>
        </div>
    );
}

