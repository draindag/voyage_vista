import React from 'react';
import './ProfileManager.css';
import { Link } from 'react-router';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { deleteCookie } from '../../general/cookie_ops';
import { useNavigate } from 'react-router';

export default function ProfileManager(props) {
    const {userData, setUserData} = useAuthContext();
    const navigate = useNavigate();
    let ulContent;
    if(userData === null){
        ulContent = <><li><Link to='/login'>Войти</Link></li><li><Link to='/reg'>Регистрация</Link></li></>
    }
    else{
        ulContent = <><li><Link to='/profile'>Профиль</Link></li><li><button onClick={()=>{
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

