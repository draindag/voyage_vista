import './AuthPage.css';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import Cookies from 'js-cookie';

export default function AuthPage(props) {
    const location = useLocation();
    console.log(location.pathname)

    const [login, setLogin] = useState("");
    const [validLogin, setValidLogin] = useState(true);
    const [password, setPassword] = useState("");
    const [validPassword, setValidPassword] = useState(true);
    const [email, setEmail] = useState("");
    const [validEmail, setValidEmail] = useState(true);
    const [passwordAgain, setPasswordAgain] = useState("");
    const [validPassAgain, setPassAgain,] = useState(true);

    const {setUserData} = useAuthContext();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let formContent;
    let buttonText;
    let headerText;

    const handleLoginBlur = () => {
        setValidLogin(login.length >= 4)
    }

    const handlePassBlur = () => {
        setValidPassword(password.length >= 5)
    }

    const handleEmailBlur = () => {
        setValidEmail(emailRegex.test(email))
    }

    const handlePassAgainBlur = () => {
        setPassAgain(password === passwordAgain)
    }

    // -----------------------
    const handleEnter = () => {
        let newUserData = {role: login, name: login}
        Cookies.set("userData", JSON.stringify(newUserData), {expires: 7, sameSite: 'strict'})
        setUserData(newUserData);
    }



    if (location.pathname === '/login') {
        headerText = "Вход";
        buttonText = "Войти";

        formContent = <>
            <label>Логин</label>
            <input className={validLogin ? '' : 'invalid-input'}
                title={validLogin ? '' : 'Логин должен иметь не менее 4-х символов'}
                type='text' placeholder='Введите логин'
                onChange={(value) => setLogin(value.target.value)}
            ></input>
            <label>Пароль</label>
            <input className={validPassword ? '' : 'invalid-input'}
                title={validPassword ? '' : 'Пароль должен содержать не менее 5-ти символов'}
                onChange={(value) => setPassword(value.target.value)}
                type='password' placeholder='Введите пароль'></input>
        </>
    }
    else {
        headerText = "Регистрация";
        buttonText = "Зарегистрироваться";
        formContent = <>
            <label>Логин</label>
            <input className={validLogin ? '' : 'invalid-input'}
                title={validLogin ? '' : 'Логин должен иметь не менее 4-х символов'}
                type='text' placeholder='Введите логин'
                onChange={(value) => setLogin(value.target.value)}
                onBlur={handleLoginBlur}
            >
            </input>
            <label>Email</label>
            <input className={validEmail ? '' : 'invalid-input'}
                title={validEmail ? '' : 'Неверный формат электронной почты'}
                type='text' placeholder='Введите Email'
                onChange={(value) => setEmail(value.target.value)}
                onBlur={handleEmailBlur}
            ></input>
            <label>Пароль</label>
            <input className={validPassword ? '' : 'invalid-input'}
                title={validPassword ? '' : 'Пароль должен содержать не менее 5-ти символов'}
                onChange={(value) => setPassword(value.target.value)}
                onBlur={handlePassBlur}
                type='password' placeholder='Введите пароль'></input>
            <label>Повторите пароль</label>
            <input className={validPassAgain ? '' : 'invalid-input'}
                title={validPassAgain ? '' : 'Пароль должен совпадать'}
                onChange={(value) => setPasswordAgain(value.target.value)}
                onBlur={handlePassAgainBlur}
                type='password' placeholder='Введите пароль'></input>
        </>
    }




    return (
        <div className='auth-back'>
            <div style={{ height: "200px" }}></div>
            <div className='container'>
                <h2>{headerText}</h2>
                <div className='auth-form'>
                    <form>
                        {formContent}
                    </form>
                </div>
                <div className='button-block'>
                    <button className='auth-button' onClick={handleEnter}>{buttonText}</button>
                </div>
            </div>

        </div>
    );
}

