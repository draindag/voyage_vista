import './ProfilePage.css';
import '../../../resources/constants.css';

import React, { useState, useEffect, useRef } from 'react';


import { useNavigate, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';

export default function ProfilePage() {
    const { userData, setUserData } = useAuthContext();
    const [state, setState] = useState({user: null, favor: [{}], tours: [{}]});
    let navigate = useNavigate();
    console.log(state)
    useEffect(() => {
        const fetchCountry = async () => {
            if(!userData){
                return
            }
            const response = await fetchData(userData, `/api/profile`);
            if (response.data) {
                let data = response.data.user
                setState({
                    user: {login: data.login, email: data.email},
                    favor: data.fav_tours,
                    tours: data.transactions,
                });
                setUserData(response.userData);

                return response;
            }
            else {
                if (response.action === "unauth") {
                    // deleteCookie();
                    // setUserData(null);
                    alert(response.message);
                    // navigate("/login");
                    return null;
                }
                else {
                    alert(response.message);
                    return null;
                }
            }
        }
        fetchCountry();
    }, [userData]);


    let favItems = [];
    let tourItems = [];
    
    // countries.forEach(elem => {
    //     ulElements.push(<li>
    //         <a href={elem.country_id}>{elem.country_name}</a>
    //     </li>)
    // })

    return <>
    <div style={{ height: '200px' }}></div>
        <div>
            <div className='control-panel'>
                <div className='control-panel-head'>
                    <p>{state.user?.login}</p>
                </div>
                <div>
                    <button>ПРОФИЛЬ</button>
                    <button>ИЗБРАННОЕ</button>
                    <button>МОИ ТУРЫ</button>
                </div>
            </div>
            
        </div>
    </>
}

