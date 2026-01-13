import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Trading from './pages/Trading';
import Workflows from './pages/Workflows';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import { Sidebar, Header } from './components/Layout';
import './index.css';

const PrivateRoute = ({ children }) => {
    const isAuthenticated = !!localStorage.getItem('token');
    return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route
                    path="/*"
                    element={
                        <PrivateRoute>
                            <div className="flex min-h-screen bg-[#f8fafd]">
                                <Sidebar />
                                <div className="flex-1 flex flex-col">
                                    <Header />
                                    <main className="p-8 overflow-y-auto">
                                        <Routes>
                                            <Route path="/" element={<Dashboard />} />
                                            <Route path="/trading" element={<Trading />} />
                                            <Route path="/workflows" element={<Workflows />} />
                                        </Routes>
                                    </main>
                                </div>
                            </div>
                        </PrivateRoute>
                    }
                />
            </Routes>
        </Router>
    );
};

export default App;
