import { deleteCookie } from "./cookie_ops";
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import { useAuthContext } from "./AuthContext/AuthContext";

const refreshToken = async (token) => {
    let response = await fetch("http://127.0.0.1:8000/api/refresh", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`
        },
    });
    let result = null;
    if (response.status === 200) {
        result = await response.json()
        result = result.access_token
    }
    return result;
}

const checkToken = async (token) => {
    let response = await fetch("http://127.0.0.1:8000/api/check_token", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`
        },
    });
    let result = false;
    if (response.status === 200) { result = true; }
    return result;
}

const tryGetReq = async (token, url) => {
    let response = await fetch(`http://127.0.0.1:8000${url}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`
        },
    });
    return response;
};


const tryPostReq = async (token, url, reqData, method) => {
    console.log(`${method} запрос для`);
    console.log(reqData);
    let response = await fetch(`http://127.0.0.1:8000${url}`, {
        method: method,
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`
        },
        body: reqData
    });
    return response;
};


const sendData = async (userData, url, reqData, method) => {
    let result = null;
    let newUser = userData;
    try {
        let token = userData.access_token;
        console.log("CHECK")
        let check = await checkToken(userData?.access_token)
        if (!check) {
            console.log("Refresh")
            let refresh = await refreshToken(userData?.refresh_token)
            if (!refresh) {
                return { data: null, userData: null, message: "Авторизируйтесь повторно", action: "unauth" };
            }
            newUser = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role };
        }
        console.log("SUCCESS to refresh")
        let response = await tryPostReq(token, url, reqData, method);
        console.log(result);
        if (response.status === 201 || response.status === 200) {
            result = await response.json()
            return { data: result, userData: newUser, message: "OK", action: "ok" };
        } else {
            return { data: null, userData: newUser, message: "Произошла ошибка при загрузке данных", action: "fail" };
        }
    } catch (e) {
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except" };
    }
};


const fetchData = async (userData, url) => {
    let result = null;
    let newUser = userData;
    try {
        let token = userData.access_token;
        console.log("CHECK")
        let check = await checkToken(userData?.access_token)
        if (!check) {
            console.log("Refresh")
            let refresh = await refreshToken(userData?.refresh_token)
            if (!refresh) {
                return { data: null, userData: null, message: "Авторизируйтесь повторно", action: "unauth" };
            }
            newUser = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role };
        }
        console.log("SUCCESS to refresh")
        let response = await tryGetReq(token, url);
        console.log(result);
        if (response.status === 200) {
            result = await response.json()
            return { data: result, userData: newUser, message: "OK", action: "ok" };
        } else {
            return { data: null, userData: newUser, message: "Произошла ошибка при загрузке данных", action: "fail" };
        }
    } catch (e) {
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except" };
    }
};




export { refreshToken, checkToken, tryGetReq, fetchData, sendData, tryPostReq };