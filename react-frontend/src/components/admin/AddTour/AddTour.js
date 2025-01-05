import React, { useState, useRef, useEffect } from 'react';
import './AddTour.css';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuthContext } from '../../general/AuthContext/AuthContext';
import { fetchData, sendData } from '../../general/web_ops';
import { deleteCookie } from '../../general/cookie_ops';

const { v4: uuidv4 } = require('uuid');

export default function AddTour(props) {
    const fileInputRef = useRef(null);

    const { id } = useParams();
    let navigate = useNavigate();
    const { userData, setUserData } = useAuthContext();

    const [state, setState] = useState({
        
        image: null,
        imageToShow: null,
        prevImage: null,
        imageName: "файл не выбран",

        countriesList: [{}],
        categoriesList: [{}],
        offersList: [{}],

        chosenCounty: "",
        chosenCategory: "",
        chosenOffer: "",

        title: "",
        dateStart: "",
        dateEnd: "",
        price: 0,
        shortDesc: "",
        desc: "",
        ent_id: null
    })
    let headerText = "тура";

    console.log(state)

    const sendForm = async () => {
        let method = 'POST';
        let url = `/api/admin_panel/tours/new`;
        const uniqueID = uuidv4();

        console.log(uniqueID)

        let formData = new FormData();
        formData.append(`tour_title`, state.title)
        formData.append(`tour_description`, state.shortDesc)
        formData.append(`tour_text`, state.desc)
        formData.append(`tour_price`, state.price)
        formData.append(`tour_start_date`, state.dateStart)
        formData.append(`tour_end_date`, state.dateEnd)
        formData.append(`category_id`, state.chosenCategory.id)
        // formData.append(`category_id `,  uniqueID)
        formData.append(`country_id`, state.chosenCounty.id)
        if (state.chosenOffer.value !== 'Без акции') {
            formData.append(`offer_id`, state.chosenOffer.id)
        }
        if (props.action === 'upd') {
            method = 'PUT';
            url = `/api/admin_panel/tours/${id}/edit`;
            formData.append(`tour_id`, id);
        }
        else {
            formData.append(`cover_image`, state.image)
        }
        console.log(formData)
        const response = await sendData(userData, url, formData, method, true);
        if (response.action === "ok") {
            console.log(response)
            alert("Успешно!");
            setUserData(response.userData);
            navigate(`/admin/entitylist?name=tours`);
        }
        else {
            if (response.action === "unauth") {
                deleteCookie();
                setUserData(null);
                alert(response.message);
                navigate("/login");
            }
            else {
                // alert(response.message);
            }
        }
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setState({ ...state, image: file, imageToShow: reader.result, imageName: file.name })
            };
            reader.readAsDataURL(file);
        }
    };

    useEffect(() => {
        const callFetch = async () => {
            let response;
            let newState;
            let categories = [{}];
            let countries = [{}];
            let offers = [{}];

            let chosenOfferTmp;
            let chosenCountyTmp;
            let chosenCategoryTmp;

            // Загрузка данных категорий и стран
            response = await fetchData(userData, `/api/categories_all`, false);
            if (response.data) {
                categories = response.data.categories;
                chosenCategoryTmp= { value: categories[0].category_title, id: categories[0].category_id };
            }
            response = await fetchData(userData, `/api/countries_all`, false);
            if (response.data) {
                countries = response.data.countries;
                chosenCountyTmp= { value: countries[0].country_name, id: countries[0].country_id };
            }

            // Загрузка данных акций
            response = await fetchData(userData, `/api/admin_panel/offers_all`, false);
            if (response.data) {
                offers = response.data.special_offers;
                offers.unshift({offer_title: "Без акции", offer_id: ''})
                chosenOfferTmp= { value: offers[0].offer_title, id: offers[0].offer_id };
            }
            if (props?.action === "upd") {
                response = await fetchData(userData, `/api/admin_panel/tours/${id}/edit`);
                if (response.data) {
                    let responseData = response.data.tour;
                    console.log(responseData)
                    let elem = countries.find(item => item.country_id === responseData.country.country_id)
                    chosenCountyTmp= { value: elem?.country_name, id: elem?.country_id };

                    elem = categories.find(item => item.category_id === responseData.category.category_id)
                    chosenCategoryTmp= { value: elem?.category_title, id: elem?.category_id };

                    if(responseData.offers.length > 0){
                        elem = offers.find(item => item.offer_id === responseData.offers[0].offer_id)
                        chosenOfferTmp= { value: elem?.offer_title, id: elem?.offer_id };
                    }

                    console.log(responseData)
                    newState = {
                        ...state,
                        image: `/cover_images/${responseData.tour_image}`,
                        imageToShow: `/cover_images/${responseData.tour_image}`,
                        title: responseData.tour_title,
                        dateStart: responseData.tour_start_date,
                        dateEnd: responseData.tour_start_date,
                        price: responseData.tour_price,
                        shortDesc: responseData.tour_description,
                        desc: responseData.tour_text,
                        ent_id: responseData.tour_id
                    }
                }
                else {
                    if (response.action === "unauth") {
                        deleteCookie();
                        setUserData(null);
                        alert(response.message);
                        navigate("/login");
                    }
                    else {
                        alert(response.message);
                    }
                }
            }
            newState = {
                ...newState,
                countriesList: countries,
                categoriesList: categories,
                offersList: offers,
                chosenOffer: chosenOfferTmp,
                chosenCounty: chosenCountyTmp,
                chosenCategory: chosenCategoryTmp
            }
            setState({ ...state, ...newState })
        }

        callFetch();


        // eslint-disable-next-line    
    }, []);

    let countriesOptions = [];
    state?.countriesList.forEach(elem => {
        countriesOptions.push(
            <option value={elem.country_name}>{elem.country_name}</option>
        );
    });

    let categoriesOptions = [];
    state?.categoriesList.forEach(elem => {
        categoriesOptions.push(
            <option value={elem.category_title}>{elem.category_title}</option>
        );
    });

    let offersOptions = [];
    state?.offersList.forEach(elem => {
        offersOptions.push(
            <option value={elem.offer_title}>{elem.offer_title}</option>
        );
    });


    return (<>
        <div className='add-container'>
            <h2>Добавление {headerText}</h2>
            <form method='post' action=''>
                <div className='form-container'>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Название {headerText}</label></div>
                        <input className='wide-input no-file-input' type='text' placeholder={`Введите название ${headerText}`}
                            value={state.title}
                            onChange={(e) => { setState({ ...state, title: e.target.value }) }}
                        ></input>
                        <div className='add-left-block'><label>Выберите страну</label>
                            <select value={state.chosenCounty.value} style={{ width: "300px", height: "50px", textAlign: "center" }}
                                onChange={(e) => {
                                    console.log(e.target.value)
                                    let elem = state?.countriesList.find(item => item.country_name === e.target.value)
                                    setState({ ...state, chosenCounty: { value: elem?.country_name, id: elem?.country_id } })
                                }}>
                                {countriesOptions}
                            </select>
                        </div>
                        <div className='add-left-block'><label>Выберите категорию</label>
                            <select value={state.chosenCategory.value}
                                style={{ width: "300px", height: "50px", textAlign: "center" }}
                                onChange={(e) => {
                                    console.log(e.target.value)
                                    let elem = state?.categoriesList.find(item => item.category_title === e.target.value)
                                    setState({ ...state, chosenCategory: { value: elem?.category_title, id: elem?.category_id } })
                                }}>
                                {categoriesOptions}
                            </select>
                        </div>
                        <div className='add-left-block'><label>Дата начала тура</label>
                            <input type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}
                                value={state.dateStart}
                                onChange={(e) => { setState({ ...state, dateStart: e.target.value }) }}
                            ></input>
                        </div>
                        <div className='add-left-block'><label>Дата окончания тура</label>
                            <input type='date' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}
                                value={state.dateEnd}
                                onChange={(e) => { setState({ ...state, dateEnd: e.target.value }) }}
                            ></input>
                        </div>
                        <div className='add-left-block'><label>Стоимость тура</label>
                            <input type='number' className='no-file-input' style={{ width: "200px", padding: "0 30px 0 20px" }}
                                value={state.price}
                                placeholder='Введите цену'
                                onChange={(e) => { setState({ ...state, price: e.target.value }) }}
                            ></input>
                        </div>
                    </div>
                    <div>
                        <div className='image-preview'>
                            <img src={state.image ? state.imageToShow : '/admin/Images/cricle_plus.png'} alt=''></img>
                        </div>
                        <div className='add-image-input-block'>
                            <label>Загрузить картинку с компьютера:</label>
                            <div style={{ flexBasis: "100%" }} className='file-input'><button type='button' className='file-choice-btn' onClick={() => fileInputRef.current.click()}>Выберите файл</button><p>{state.imageName}</p></div>
                            <input
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                type="file" accept="image/*" onChange={handleImageChange} />
                        </div>
                    </div>
                </div>
                <div style={{ position: 'relative', top: '-30px' }}>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Краткое описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' style={{ height: "140px" }}
                            placeholder={`Введите описание ${headerText}`}
                            value={state.shortDesc}
                            onChange={(e) => { setState({ ...state, shortDesc: e.target.value }) }}
                        ></textarea>
                    </div>
                    <div>
                        <div style={{ marginBottom: '6px' }}><label>Описание {headerText}</label></div>
                        <textarea className='wide-input hight-input no-file-input' placeholder={`Введите описание ${headerText}`}
                            value={state.desc}
                            onChange={(e) => { setState({ ...state, desc: e.target.value }) }}
                        ></textarea>
                    </div>
                </div>
                <div className='form-container' style={{ justifyContent: "start" }}>
                    <div className='add-left-block'><label>Выберите акцию</label>
                        <select value={state.chosenOffer.value}
                            style={{ width: "300px", height: "50px", textAlign: "center" }}
                            onChange={(e) => {
                                let elem = state?.offersList.find(item => item.offer_title === e.target.value)
                                setState({ ...state, chosenOffer: { value: elem?.offer_title, id: elem?.offer_id } })
                            }}>
                            {offersOptions}
                        </select>
                    </div>
                </div>
            </form>
            <div className='form-container' style={{ justifyContent: "end" }}>
                    <div className='submit-button-block'>
                        <button type='submit' className='primary-btn' onClick={() => sendForm()}>{props.action === "upd" ? "Изменить" : "Добавить"}</button>
                    </div>
                </div>
        </div>
    </>

    );
};

