import './AdminApp.css';
import Navbar from './Navbar/Navbar';
import { Route, Routes } from 'react-router';
import { useAuthContext } from '../general/AuthContext/AuthContext';
import EntityList from './List/EntityList';
import AddCategory from './AddCountryOrCategory/AddCountryOrCategory';
import AddTour from './AddTour/AddTour';
import AddSale from './AddSale/AddSale';
import ModeratorRegPage from './ModeratorRegPage/ModeratorRegPage';

function AdminApp() {

    const {userData} = useAuthContext();

    console.log(userData);

    if(userData?.role === "admin"){
    return (
        <>
            <Navbar></Navbar>
            <div style={{ width: '100%', height: '100%'}}>
                <div style={{ height: '110px' }}></div>
                <Routes>
                    <Route path='/' element={<>
                        <div className='container'>
                            <h2>Вы находитесь в панели управления сайтом.</h2>
                            <p>Всякая справочная информация, краткая инструкция, размеры картинок для редактирования и т.п.</p>
                            <p>Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные тексты. Вдали от всех живут они в буквенных домах на берегу Семантика большого языкового океана. Маленький ручеек Даль журчит по всей стране и обеспечивает ее всеми необходимыми правилами. Эта парадигматическая страна, в которой жаренные члены предложения залетают прямо в рот. Даже всемогущая пунктуация не имеет власти над рыбными текстами, ведущими безорфографичный образ жизни. Однажды одна маленькая строчка рыбного текста по имени Lorem ipsum решила выйти в большой мир грамматики. Великий Оксмокс предупреждал ее о злых запятых, диких знаках вопроса и коварных точках с запятой, но текст не дал сбить</p>
                        </div>
                    </>}></Route>
                    <Route path='/moderreg' element={<ModeratorRegPage/>}></Route>
                    <Route path='/entitylist' element={<EntityList/>}></Route>
                    <Route path='/categories/add' element={<AddCategory/>}></Route>
                    <Route path='/categories/:id/delete' element={<>У</>}></Route>
                    <Route path='/categories/:id/edit' element={<>И</>}></Route>
                    <Route path='/countries/add' element={<AddCategory/>}></Route>
                    <Route path='/countries/:id/delete' element={<>У</>}></Route>
                    <Route path='/countries/:id/edit' element={<>И</>}></Route>
                    <Route path='/tours/add' element={<AddTour/>}></Route>
                    <Route path='/tours/:id/delete' element={<>У</>}></Route>
                    <Route path='/tours/:id/edit' element={<>И</>}></Route>
                    <Route path='/offers/add' element={<AddSale/>}></Route>
                    <Route path='/offers/:id/delete' element={<>У</>}></Route>
                    <Route path='/offers/:id/edit' element={<>И</>}></Route>
                </Routes>
            </div>
            
        </>
    );
    }
    else{
        return(<></>)
    }
}

export default AdminApp;
