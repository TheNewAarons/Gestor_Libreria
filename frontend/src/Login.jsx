import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; // Ensure Bootstrap is imported
import './Login.css';

const Login = () => {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const togglePassword = () => {
        setShowPassword(!showPassword);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        console.log("Login attempt", { email, password });

        try {
            // Updated to use the correct local API endpoint
            const response = await fetch('http://127.0.0.1:8000/api/v1/auth/api-token-auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.non_field_errors || "Error al iniciar sesión");
            }

            const data = await response.json();
            console.log("Login successful:", data);

            // Store token and user info
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify({
                id: data.user_id,
                email: data.email,
                rol: data.rol
            }));

            // Redirect to dashboard
            navigate('/dashboard');

        } catch (error) {
            console.error("Login error:", error);
            alert(error.message || "Error de conexión con el servidor");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-container">
                {/* Left side - Login Form */}
                <div className="login-side">
                    <div className="login-content">
                        {/* Logo and Brand */}
                        <div className="brand-header">
                            <div className="brand-logo">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M16.5 9.4 7.55 4.24" />
                                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                                    <polyline points="3.29 7 12 12 20.71 7" />
                                    <line x1="12" x2="12" y1="22" y2="12" />
                                </svg>
                            </div>
                            <span className="brand-name">WarehousePro</span>
                        </div>

                        {/* Title */}
                        <div className="login-header">
                            <h1>Bienvenido de nuevo</h1>
                            <p>Ingresa tus credenciales para acceder al sistema de gestión</p>
                        </div>

                        {/* Login Form */}
                        <form id="loginForm" className="login-form" onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label htmlFor="email" className="form-label">Correo electrónico</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    id="email"
                                    placeholder="usuario@empresa.com"
                                    required
                                    autoComplete="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>

                            <div className="mb-3">
                                <label htmlFor="password" className="form-label">Contraseña</label>
                                <div className="password-input-wrapper position-relative">
                                    <input
                                        type={showPassword ? "text" : "password"}
                                        className="form-control"
                                        id="password"
                                        placeholder="Ingresa tu contraseña"
                                        required
                                        autoComplete="current-password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                    <button
                                        type="button"
                                        className="password-toggle btn btn-link position-absolute top-50 end-0 translate-middle-y text-decoration-none text-muted"
                                        onClick={togglePassword}
                                        aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
                                        style={{ zIndex: 5, paddingRight: '12px' }}
                                    >
                                        {showPassword ? (
                                            <svg className="eye-off-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
                                                <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
                                                <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
                                                <line x1="2" x2="22" y1="2" y2="22" />
                                            </svg>
                                        ) : (
                                            <svg className="eye-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                                                <circle cx="12" cy="12" r="3" />
                                            </svg>
                                        )}
                                    </button>
                                </div>
                            </div>

                            <div className="form-options d-flex justify-content-between align-items-center mb-4">
                                <div className="form-check">
                                    <input type="checkbox" className="form-check-input" id="remember" />
                                    <label className="form-check-label" htmlFor="remember">Recordarme</label>
                                </div>
                                <button type="button" className="btn btn-link p-0 text-decoration-none forgot-password">¿Olvidaste tu contraseña?</button>
                            </div>

                            <button type="submit" className="btn btn-primary w-100 btn-submit d-flex justify-content-center align-items-center gap-2" disabled={isLoading}>
                                {isLoading ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        <span>Iniciando sesión...</span>
                                    </>
                                ) : (
                                    <span className="btn-text">Iniciar sesión</span>
                                )}
                            </button>
                        </form>

                        {/* Help Text */}
                        <div className="help-text text-center mt-4">
                            <p className="mb-1 text-muted">¿Problemas para acceder?</p>
                            <button type="button" className="btn btn-link p-0 text-decoration-none contact-admin">Contacta al administrador</button>
                        </div>
                    </div>
                </div>

                {/* Right side - Feature Showcase */}
                <div className="feature-side">
                    <div className="grid-pattern"></div>
                    <div className="feature-content">
                        <div className="feature-header mb-5">
                            <h2>Gestiona tu inventario con eficiencia</h2>
                            <p>Control total de productos, bodegas y movimientos en tiempo real. Optimiza tu operación logística con herramientas profesionales.</p>
                        </div>

                        <div className="features-list">
                            <div className="feature-item">
                                <div className="feature-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M16.5 9.4 7.55 4.24" />
                                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                                        <polyline points="3.29 7 12 12 20.71 7" />
                                        <line x1="12" x2="12" y1="22" y2="12" />
                                    </svg>
                                </div>
                                <div className="feature-text">
                                    <h3>Control de Inventario</h3>
                                    <p>Seguimiento en tiempo real de todos tus productos</p>
                                </div>
                            </div>

                            <div className="feature-item">
                                <div className="feature-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <rect width="7" height="9" x="3" y="3" rx="1" />
                                        <rect width="7" height="5" x="14" y="3" rx="1" />
                                        <rect width="7" height="9" x="14" y="12" rx="1" />
                                        <rect width="7" height="5" x="3" y="16" rx="1" />
                                    </svg>
                                </div>
                                <div className="feature-text">
                                    <h3>Múltiples Bodegas</h3>
                                    <p>Administra inventario en diferentes ubicaciones</p>
                                </div>
                            </div>

                            <div className="feature-item">
                                <div className="feature-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <line x1="12" x2="12" y1="20" y2="10" />
                                        <line x1="18" x2="18" y1="20" y2="4" />
                                        <line x1="6" x2="6" y1="20" y2="16" />
                                    </svg>
                                </div>
                                <div className="feature-text">
                                    <h3>Reportes Detallados</h3>
                                    <p>Analítica avanzada para tomar mejores decisiones</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
