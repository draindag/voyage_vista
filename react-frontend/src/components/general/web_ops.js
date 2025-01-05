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
    let headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json;charset=utf-8',
        'Authorization': `Bearer ${token}`
    };
    if (token) {
        headers = { ...headers, 'Authorization': `Bearer ${token}` }
    }
    let response = await fetch(`http://127.0.0.1:8000${url}`, {
        method: 'GET',
        headers: headers
    });
    return response;
};


const tryPostReq = async (token, url, reqData, method, form = false) => {
    console.log(`${method} запрос для`);
    console.log(reqData);

    let headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json;charset=utf-8',
        'Authorization': `Bearer ${token}`
    }
    if (form) {
        headers = {
            // 'Content-Type': 'multipart/form-data;charset=utf-8',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`,

        }
    }
    let response = await fetch(`http://127.0.0.1:8000${url}`, {
        method: method,
        headers: headers,
        body: reqData
    });
    return response;
};

const refresh = async (userData) => {
    let res = await checkToken(userData?.access_token);
    if (!res) {
        let resp = await refreshToken(userData?.refresh_token)
        if (!resp) {
            return null;
        }
        let result = { access_token: resp, refresh_token: userData.refresh_token, role: userData.role }
        return result;
    }
    else {
        return userData
    }
}

const formAnswer = (res, status, userData, type = 1) => {
    if (type !== 1) {
        return { data: null, userData: null, message: "Авторизируйтесь повторно", action: "unauth", status: 401 };
    }
    if (status === 200 || status === 201) {
        return { data: res, userData: userData, message: "OK", action: "ok" };
    } else {
        return { data: null, userData: userData, message: "Произошла ошибка при загрузке данных", action: "fail", ex: "" };
    }
}


const sendData = async (userData, url, reqData, method, form = false, needCheck = true) => {
    try {
        let newUser = userData;
        console.log(`Токен начала ${newUser.access_token}`)
        if (needCheck) {
            let refreshResult = await refresh(userData);
            if (!refreshResult) {
                return formAnswer(null, 0, null, 2)
            }
            else {
                newUser = refreshResult;
            }
        }
        console.log(`Токен факт ${newUser.access_token}`)
        const response = await tryPostReq(newUser.access_token, url, reqData, method, form);
        const content = await response.json();
        return formAnswer(content, response.status, newUser)
    } catch (e) {
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except" };
    }
};


const fetchData = async (userData, url, needCheck = true) => {
    try {
        let newUser = userData;
        console.log(`Токен начала ${newUser.access_token}`)
        if (needCheck) {
            let refreshResult = await refresh(userData);
            if (!refreshResult) {
                return formAnswer(null, 0, null, 2)
            }
            else {
                newUser = refreshResult;
            }
        }
        console.log(`Токен факт ${newUser.access_token}`)
        const response = await tryGetReq(newUser.access_token, url);
        const content = await response.json();
        console.log(content);
        return formAnswer(content, response.status, newUser)
    } catch (e) {
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except", ex: e };
    }
};




export { refreshToken, checkToken, tryGetReq, fetchData, sendData, tryPostReq };