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
    let headers =  {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json;charset=utf-8',
        'Authorization': `Bearer ${token}`
    };
    if(token){
        headers = {...headers, 'Authorization': `Bearer ${token}`}
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
    if(form){
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


const sendData = async (userData, url, reqData, method, form = false, needCheck = true) => {
    let result = null;
    let newUser = userData;
    try {
        let token = userData.access_token;
        // console.log("CHECK")
        if(needCheck){
            const check = await checkToken(userData?.access_token)
            if (!check) {
                // console.log("Refresh")
                let refresh = await refreshToken(userData?.refresh_token)
                if (!refresh) {
                    return { data: null, userData: null, message: "Авторизируйтесь повторно", action: "unauth", status: response.status };
                }
                newUser = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role };
            }
        }
        // console.log("SUCCESS to refresh")
        let response = await tryPostReq(token, url, reqData, method, form);
        console.log(result);
        if (response.status === 201 || response.status === 200) {
            result = await response.json()
            return { data: result, userData: newUser, message: "OK", action: "ok" };
        } else {
            return { data: null, userData: newUser, message: "Произошла ошибка при загрузке данных", action: "fail", status: response.status};
        }
    } catch (e) {
        console.log(e)
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except" };
    }
};


const fetchData = async (userData, url, needCheck = true) => {
    let result = null;
    let newUser = userData;
    try {
        let token = userData?.access_token;
        // console.log("CHECK")
        if(needCheck){
            let check = await checkToken(token)
            if (!check) {
                console.log("Refresh")
                let refresh = await refreshToken(userData?.refresh_token)
                if (!refresh) {
                    return { data: null, userData: null, message: "Авторизируйтесь повторно", action: "unauth" };
                }
                newUser = { access_token: refresh, refresh_token: userData.refresh_token, role: userData.role };
            }
        }
        // console.log("SUCCESS to refresh")
        let response = await tryGetReq(token, url);
        console.log(result);
        if (response.status === 200) {
            result = await response.json()
            return { data: result, userData: newUser, message: "OK", action: "ok" };
        } else {
            return { data: null, userData: newUser, message: "Произошла ошибка при загрузке данных", action: "fail", ex: "" };
        }
    } catch (e) {
        return { data: null, userData: null, message: "Не удалось. Попробуйте позже", action: "except", ex: e };
    }
};




export { refreshToken, checkToken, tryGetReq, fetchData, sendData, tryPostReq };