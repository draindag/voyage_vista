import './AuthPage.css';
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';


import { setCookieInfo } from '../../general/cookie_ops';

export default function AuthPage() {
    const location = useLocation();
    let navigate = useNavigate();


    const [login, setLogin] = useState("");
    const [validLogin, setValidLogin] = useState(true);
    const [password, setPassword] = useState("");
    const [validPassword, setValidPassword] = useState(true);
    const [email, setEmail] = useState("");
    const [validEmail, setValidEmail] = useState(true);
    const [passwordAgain, setPasswordAgain] = useState("");
    const [validPassAgain, setPassAgain,] = useState(true);

    const {setUserData } = useAuthContext();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let formContent;
    let formBtn;
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


    const handleEnter = async () => {
        const authData = { email: email, password: password }
        const authDataStr = JSON.stringify(authData)
        try {
            let response = await fetch("http://127.0.0.1:8000/api/login", {
                method: 'POST',
                // mode: "no-cors",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                    'Accept': 'application/json;charset=utf-8'
                },
                body: authDataStr
            })
            if (response.status === 200) {
                let responseData = await response.json()
                setCookieInfo(responseData);
                setUserData(responseData);
                console.log(responseData);
                alert("Вы успешно авторизованы!");
                navigate(-1);
            } else {
                let responseData = await response.json()
                let messages = "";
                if (responseData.errors) {
                    let errors = responseData.errors
                    if (errors.email) {
                        messages = messages.concat(`\n- ${errors.email[0]}`)
                    }
                    if (errors.password) {
                        messages = messages.concat(`\n- ${errors.password[0]}`)
                    }
                }
                if (response.message) {
                    messages = messages.concat(`\n${response.message}`)
                }
                alert(`Произошла ошибка при входе.${messages}`);
            }
        } catch (e) {
            alert(`Не удалось авторизоваться. Попробуйте позже`);
        }

    }

    const handleReg = async () => {
        handleLoginBlur()
        handlePassBlur()
        handlePassAgainBlur()
        handleEmailBlur()
        if (!(validEmail && validLogin && validPassword && validPassAgain)) {
            alert("Ошибка в введенных данных")
            return;
        }
        const authData = { login: login, email: email, password: password, password_repeat: passwordAgain }
        const authDataStr = JSON.stringify(authData)
        try {
            let response = await fetch("http://127.0.0.1:8000/api/registration", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                    'Accept': 'application/json;charset=utf-8'
                },
                body: authDataStr
            })
            if (response.status === 201) {
                let responseData = await response.json();
                setCookieInfo(responseData);
                setUserData(responseData);
                alert("Вы успешно зарегестрированы!");
                navigate("/");
            } else {
                let responseData = await response.json()
                let messages = "";
                if (responseData.errors) {
                    let errors = responseData.errors
                    if (errors.email) {
                        messages = messages.concat(`\n- ${errors.email[0]}`)
                    }
                    if (errors.password) {
                        messages = messages.concat(`\n- ${errors.password[0]}`)
                    }
                }
                if (response.message) {
                    messages = messages.concat(`\n${response.message}`)
                }
                alert(`Произошла ошибка при регистрации.${messages}`);
            }
        } catch (e) {
            alert(`Не удалось зарегестрировать. Попробуйте позже`);
        }
    }



    if (location.pathname === '/login') {
        headerText = "Вход";
        buttonText = "Войти";

        formContent = <>
            <label>Почта</label>
            <input className={validLogin ? '' : 'invalid-input'}
                title={validLogin ? '' : 'Логин должен иметь не менее 4-х символов'}
                type='text' placeholder='Введите почту'
                onChange={(value) => setEmail(value.target.value)}
            ></input>
            <label>Пароль</label>
            <input className={validPassword ? '' : 'invalid-input'}
                title={validPassword ? '' : 'Пароль должен содержать не менее 5-ти символов'}
                onChange={(value) => setPassword(value.target.value)}
                type='password' placeholder='Введите пароль'></input>
        </>

        formBtn = <>
            <div className='button-block'>
                <button className='auth-button' onClick={handleEnter}>{buttonText}</button>
            </div>
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
        formBtn = <>
            <div className='button-block'>
                <button className='auth-button' onClick={handleReg}>{buttonText}</button>
            </div>
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
                {formBtn}
            </div>

        </div>
    );
}

