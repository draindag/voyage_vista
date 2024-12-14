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
    if(response.status === 200){
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
    if(response.status === 200){result = true;}
    return result;
}


export {refreshToken, checkToken};