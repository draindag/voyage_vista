import './App.css';
import { Route, Routes, BrowserRouter } from 'react-router';
import ClientApp from './components/client/ClientApp';
import AdminApp from './components/admin/AdminApp';
import { AuthProvider } from './components/general/AuthContext/AuthContext';

function App() {
  return (
    <>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path='/*' element={<ClientApp></ClientApp>}></Route>
            <Route path='/admin/*' element={<AdminApp></AdminApp>}></Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </>
  );
}

export default App;
