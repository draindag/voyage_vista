import React, { createContext, useContext, useEffect, useState} from "react";
import Cookies from "js-cookie";
const AuthContext = createContext();



export const AuthProvider = ({children}) => {

    const [userData, setUserData] = useState({role: "", name: "", token: null, refreshToken: null})

    useEffect(() => {
        const userDataString = Cookies.get("userData");
        if(userDataString){
            setUserData(JSON.parse(userDataString));
        }
    }, []);

    return (
        <AuthContext.Provider value={{userData, setUserData}}>
            {children}
        </AuthContext.Provider>
    );

};

export const useAuthContext = () => {
    return useContext(AuthContext);
}
