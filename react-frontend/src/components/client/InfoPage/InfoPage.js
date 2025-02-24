import './InfoPage.css';
import React from 'react';

export default function InfoPage() {
    return (
        <>
            <div className='info'>
                <div style={{ height: '200px' }}></div>

                <div className='info-container'>
                    <div>
                        <div className='info-card'>
                            <h2>1. До поездки</h2>
                            <p>Выяснить, позволяет ли состояние здоровья ехать в конкретную страну
                                Изучить традиции страны, политическую, экологическую и инфекционную обстановку
                                Узнать как можно больше о флоре и фауне страны – ядовитые растения, змеи, насекомые
                                Планировать сроки поездки – учитывая время на адаптацию
                                Заранее узнать адрес посольства РФ
                                Уточнить, какие банковские карточки работают в стране пребывания, при необходимости поменять деньги
                                Заранее сообщить родным сроки своей поездки
                                Не забыть застраховать багаж
                                Узнать порядок пребывания в конкретной стране несовершеннолетних – он может отличаться от России</p>
                        </div>
                        <div className='info-card'>
                            <h2>2. Аптечка</h2>
                            <p> Лейкопластыри, бинт, ватные диски <br />
                                Йод<br />
                                Средство от расстройства<br />
                                Болеутоляющие средства<br />
                                Антигистаминные средства<br />
                                Средства от простуды<br />
                                Средства по необходимости (от укусов насекомых, солнцезащитный крем и т.п.)</p>
                        </div>
                    </div>
                    <div>
                        <div className='info-card'>
                            <h2>3. Безопасный отдых</h2>
                            <p>Не оставлять детей одних!
                                Пищу принимать только в тех местах, где можно гарантировать ее качество
                                Пить исключительно бутилированную воду
                                Мыть фрукты тоже бутилированной водой, а лучше – шпарить кипятком
                                Быть осторожней с местной кухней
                                Не следует купаться в море по ночам
                                Не нужно слишком много рассказывать своим попутчикам
                                Избегать услуг частного такси
                                Не употреблять алкоголь в малознакомой компании
                                Не забыть каждый раз оставлять ключи от номера на ресепшене
                                При утере документов сразу же получить свидетельство на возвращение. Оно действительно 15 дней</p>
                        </div>
                        <div className='info-card'>
                            <h2>4. Не забыть</h2>
                            <p>Загранпаспорта всех членов семьи<br />
                                Ксерокопии документов<br />
                                Билеты<br />
                                Туристический ваучер<br />
                                Медицинский страховой полис<br />
                                Необходимые медикаменты (постоянно принимаемые лекарства, средства от укачивания, раствор для линз и т.п.)<br />
                                Мобильный телефон и зарядное устройство к нему<br />
                                Деньги и банковские карты<br />
                                Ключи<br />
                                Не забыть дома выключить газ, воду, свет, электроприборы</p>
                        </div>
                    </div>
                </div>

                <div className='info-card' style={{ margin: 'auto' }}>
                    <h2>5. Чтобы отдых был в радость, не забыть</h2>
                    <p>Блокнот для ведения путевых заметок и записи интересностей<br />
                        Фотоаппарат или Видеокамеру<br />
                        Зарядные устройства для гаджетов<br />
                        Флэш-карту</p>
                </div>
                <div style={{ position: 'relative', top: '-900px', textAlign: "center"}}>
                    <h1 >Памятка<br/>туристу</h1>
                </div>


            </div>
        </>
    );
}

