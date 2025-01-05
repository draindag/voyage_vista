import MainPage from './MainPage/MainPage';
import Navbar from './Navbar/Navbar';
import AuthPage from './AuthPage/AuthPage';
import ToursCategoryesPage from './ToursCategoryesPage/ToursCategoryesPage';
import { Route, Routes } from 'react-router';
import ToursPage from './ToursPage/ToursPage';
import InfoPage from './InfoPage/InfoPage';
import ProfilePage from './ProfilePage/ProfilePage';
import TourPage from './TourPage/TourPage';

function ClientApp() {
    return (
        <>
            <Navbar></Navbar>
            <Routes>
                <Route path='/' element={<MainPage></MainPage>}></Route>
                <Route path='/login' element={<AuthPage />}></Route>
                <Route path='/reg' element={<AuthPage />}></Route>
                <Route path='/info' element={<InfoPage />}></Route>
                <Route path='/profile' element={<ProfilePage />}></Route>
                <Route path='/tours-categoryes' element={<ToursCategoryesPage></ToursCategoryesPage>}></Route>
                <Route path='/tours' element={<ToursPage />}></Route>
                <Route path='/tours/:id' element={<ToursPage />}></Route>
                <Route path='/tour-page/:id' element={<TourPage />}></Route>
                
            </Routes>
        </>
    );
}

export default ClientApp;
