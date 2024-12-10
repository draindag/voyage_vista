// import './App.css';
import MainPage from './MainPage/MainPage';
import Navbar from './Navbar/Navbar';
import AuthPage from './AuthPage/AuthPage';
import ToursCategoryesPage from './ToursCategoryesPage/ToursCategoryesPage';
import { Route, Routes } from 'react-router';

function ClientApp() {
    return (
        <>
            <Navbar></Navbar>
            <Routes>
                <Route path='/' element={<MainPage></MainPage>}></Route>
                <Route path='/login' element={<AuthPage />}></Route>
                <Route path='/reg' element={<AuthPage />}></Route>
                <Route path='/tours' element={<ToursCategoryesPage></ToursCategoryesPage>}></Route>
            </Routes>
        </>
    );
}

export default ClientApp;
