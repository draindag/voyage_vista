import './App.css';
import {Route, Routes, BrowserRouter} from 'react-router';
import ClientApp from './components/client/ClientApp';
import AdminApp from './components/admin/AdminApp';

function App() {
  return (
    <>
        <BrowserRouter>
          <Routes>
            <Route path='/*' element={<ClientApp></ClientApp>}></Route>
            <Route path='/admin/*' element={<AdminApp></AdminApp>}></Route>
          </Routes>
        </BrowserRouter>
    </>
  );
}

export default App;
