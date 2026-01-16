import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Trading from './pages/Trading';
import Workflows from './pages/Workflows';
import Settings from './pages/Settings';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Layout from './components/Layout';
import ThreeVisualizer from './components/ThreeVisualizer';
import './index.css';

const PrivateRoute = ({ children }) => {
    const isAuthenticated = !!localStorage.getItem('token');
    return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
    return (
        <Router>
            {/* Ambient 3D Background */}
            <ThreeVisualizer />

            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route
                    path="/*"
                    element={
                        <PrivateRoute>
                            <Routes>
                                <Route element={<Layout />}>
                                    <Route path="/" element={<Dashboard />} />
                                    <Route path="/trading" element={<Trading />} />
                                    <Route path="/workflows" element={<Workflows />} />
                                    <Route path="/settings" element={<Settings />} />
                                </Route>
                            </Routes>
                        </PrivateRoute>
                    }
                />
            </Routes>
        </Router>
    );
};

export default App;
