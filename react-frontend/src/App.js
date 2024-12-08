import './App.css';
import MainPage from './components/MainPage/MainPage';
import Navbar from './components/Navbar/Navbar';
import ToursCategoryesPage from './components/ToursCategoryesPage/ToursCategoryesPage';
import {Route, Routes, BrowserRouter} from 'react-router';
import AuthPage from './components/AuthPage/AuthPage';

function App() {
  return (
    <>
      <Navbar></Navbar>
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<MainPage></MainPage>}></Route>
            <Route path='/login' element={<AuthPage/>}></Route>
            <Route path='/reg' element={<AuthPage/>}></Route>
            <Route path='/tours' element={<ToursCategoryesPage></ToursCategoryesPage>}></Route>
          </Routes>
        </BrowserRouter>

    </>
  );
}

export default App;
