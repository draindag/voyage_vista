import Cookies from 'js-cookie';

const deleteCookie = () => {
    Cookies.remove('userData');
};

const getCookieInfo = () => {
    return Cookies.get("userData");
};

const setCookieInfo = (userData) => {
    Cookies.set("userData", JSON.stringify(userData), { expires: 1, sameSite: 'strict' })
};

export { deleteCookie, getCookieInfo, setCookieInfo };
