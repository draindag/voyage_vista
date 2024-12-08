import React from 'react';
import './AuthPage.css';



export default function AuthPage(props) {
    const type = props.type



    let ulContent;


    if (type === null) {
        ulContent = <><li><a href='/login'>Войти</a></li><li><a href='/reg'>Регистрация</a></li></>
    }
    else {
        ulContent = <><li><a href='/profile'>Профиль</a></li><li><a href='/'>Выйти</a></li></>
    }

    return (
        <div className='auth-back'>
            <div style={{ height: "200px" }}></div>
            <div className='container'>
                <div className='auth-form'>
                    <form>
                        <label>asfasf</label>
                        <input type='text'></input>
                        <label>asfasf</label>
                        <input type='text'></input>
                        <label>asfasf</label>
                        <input type='text'></input>
                        <label>asfasf</label>
                        <input type='text'></input>
                    </form>
                </div>
            </div>

        </div>
    );
}

