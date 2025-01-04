import '../../../resources/constants.css';
import './TourPage.css';
import React, {useEffect, useState} from 'react';

import { fetchData } from '../../general/web_ops';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';


export default function TourPage() {

    const { userData, setUserData } = useAuthContext();
    const [state, setState] = useState({});
    const { id } = useParams();

    useEffect(() => {
        const callFetch = async () => {
            const response = await fetchData(userData, `/api/tours/${id}?page=1`);
            console.log(response)
            if (response.data) {
                setState(response.data);
            }
        };  
        if(userData){
            callFetch();
        }
        
        // eslint-disable-next-line 
    }, [userData]);

    return (
        <>
            <div className='tour-header'>
                <img src={`/cover_images/${state?.tour?.tour_image}`}alt=''></img>
                <div className='first-tab'>

                </div>
                <div className='second-tab'>
                        
                </div>
            </div>
        </>
    );
}



// {
//     "success": true,
//     "tour": {
//       "tour_id": "e8c7c3d4-e23a-4b91-b770-1b884bfc3fda",
//       "tour_title": "Приключенческий тур",
//       "tour_description": "Описание приключенческого тура",
//       "tour_text": "Текст приключенческого тура. Будет очень большим",
//       "tour_price": 1200.5,
//       "price_with_discount": 960.4,
//       "tour_start_date": "2024-06-01",
//       "tour_end_date": "2024-06-10",
//       "tour_image": "flask-backend/webapp/tour_images/e8c7c3d4-e23a-4b91-b770-1b884bfc3fda.png",
//       "category": {
//         "category_id": "123e4567-e89b-12d3-a456-426614174000",
//         "category_title": "Приключения",
//         "category_description": "Описание приключений"
//       },
//       "country": {
//         "country_id": "b0a3a4ce-b5c8-42d9-b23a-d93d768e0c62",
//         "country_name": "Италия",
//         "country_description": "Страна с богатой культурой"
//       },
//       "offers": [
//         {
//           "offer_id": "f1c5a1e2-34bc-4567-89ef-fedcba123456",
//           "offer_title": "Скидка 20%",
//           "discount_size": 20,
//           "end_date": "2024-05-31"
//         }
//       ]
//     },
//     "tour_replies": [
//       {
//         "reply_id": "abcdef01-2345-6789-abcd-ef0123456789",
//         "reply_text": "Это был замечательный тур!",
//         "parent_reply_id": null,
//         "author": {
//           "login": "Пользователь123"
//         },
//         "replies": []
//       },
//       {
//         "reply_id": "abcdef01-2345-6789-abcd-ef0123456790",
//         "reply_text": "Очень понравилось!",
//         "parent_reply_id": null,
//         "author": {
//           "login": "Пользователь456"
//         },
//         "replies": [
//           {
//             "reply_id": "abcdef01-2345-6789-abcd-ef0123456781",
//             "reply_text": "Согласен! Это было незабываемо!",
//             "parent_reply_id": "abcdef01-2345-6789-abcd-ef0123456790",
//             "author": {
//               "login": "Пользователь789"
//             },
//             "replies": []
//           }
//         ]
//       }
//     ],
//     "prev_page": false,
//     "next_page": true
//   }

