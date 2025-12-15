import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Dashboard.css';
import UserManagement from './UserManagement';
import WarehouseManagement from './WarehouseManagement';
import PublisherManagement from './PublisherManagement';
import ProductManagement from './ProductManagement';

const Dashboard = () => {
    const [activeSection, setActiveSection] = useState('overview');
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const navigate = useNavigate();

    const handleLogout = (e) => {
        e.preventDefault();
        // Implement logout logic here
        navigate('/login');
    };

    const navigateToSection = (sectionId) => {
        setActiveSection(sectionId);
        if (window.innerWidth <= 768) {
            setIsSidebarOpen(false);
        }
    };

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            processFile(file);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const file = e.dataTransfer.files[0];
        if (file) {
            processFile(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const processFile = (file) => {
        const validTypes = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
        if (!validTypes.includes(file.type)) {
            alert("Por favor, selecciona un archivo Excel válido (.xlsx, .xls)");
            return;
        }
        alert(`Archivo "${file.name}" listo para procesar.`);
    };

    const renderContent = () => {
        switch (activeSection) {
            case 'overview':
                return (
                    <section id="overview" className="content-section active">
                        <div className="section-header">
                            <h1>Panel Principal</h1>
                            <p className="text-muted">Bienvenido al sistema de gestión de productos y bodegas</p>
                        </div>

                        {/* Stats Cards */}
                        <div className="row g-4 mb-4">
                            {/* ... Stats Card 1 ... */}
                            <div className="col-md-3">
                                <div className="stat-card">
                                    <div className="stat-icon bg-primary">
                                        <i className="bi bi-box-seam"></i>
                                    </div>
                                    <div className="stat-content">
                                        <h3>1,248</h3>
                                        <p>Total Productos</p>
                                    </div>
                                    <div className="stat-trend positive">
                                        <i className="bi bi-arrow-up"></i> 12%
                                    </div>
                                </div>
                            </div>
                            {/* ... Other Stat Cards ... */}
                            <div className="col-md-3">
                                <div className="stat-card">
                                    <div className="stat-icon bg-success">
                                        <i className="bi bi-building"></i>
                                    </div>
                                    <div className="stat-content">
                                        <h3>8</h3>
                                        <p>Bodegas Activas</p>
                                    </div>
                                    <div className="stat-trend positive">
                                        <i className="bi bi-arrow-up"></i> 2
                                    </div>
                                </div>
                            </div>
                            <div className="col-md-3">
                                <div className="stat-card">
                                    <div className="stat-icon bg-warning">
                                        <i className="bi bi-people"></i>
                                    </div>
                                    <div className="stat-content">
                                        <h3>42</h3>
                                        <p>Usuarios Activos</p>
                                    </div>
                                    <div className="stat-trend positive">
                                        <i className="bi bi-arrow-up"></i> 8%
                                    </div>
                                </div>
                            </div>
                            <div className="col-md-3">
                                <div className="stat-card">
                                    <div className="stat-icon bg-danger">
                                        <i className="bi bi-exclamation-triangle"></i>
                                    </div>
                                    <div className="stat-content">
                                        <h3>15</h3>
                                        <p>Stock Bajo</p>
                                    </div>
                                    <div className="stat-trend negative">
                                        <i className="bi bi-arrow-down"></i> 5
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Module Cards */}
                        <div className="row g-4">
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-people-fill"></i>
                                    </div>
                                    <h3>Gestión de Usuarios</h3>
                                    <p>Administra permisos, roles y accesos del personal</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('users')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-building"></i>
                                    </div>
                                    <h3>Gestión de Bodegas</h3>
                                    <p>Controla ubicaciones, capacidad y estados de bodegas</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('warehouses')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-bookmark-fill"></i>
                                    </div>
                                    <h3>Gestión de Editoriales</h3>
                                    <p>Registra y organiza proveedores y editoriales</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('publishers')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-box-seam"></i>
                                    </div>
                                    <h3>Gestión de Productos</h3>
                                    <p>Crea, edita y consulta el catálogo completo</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('products')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-file-earmark-arrow-up"></i>
                                    </div>
                                    <h3>Importar Productos</h3>
                                    <p>Carga masiva de productos desde archivos Excel</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('import')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6">
                                <div className="module-card">
                                    <div className="module-icon">
                                        <i className="bi bi-file-earmark-arrow-down"></i>
                                    </div>
                                    <h3>Exportar Base de Datos</h3>
                                    <p>Descarga respaldos y reportes del sistema</p>
                                    <button className="btn btn-primary" onClick={() => navigateToSection('export')}>
                                        Acceder <i className="bi bi-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>
                );
            case 'users':
                return <UserManagement />;
            case 'warehouses':
                return <WarehouseManagement />;
            case 'publishers':
                return <PublisherManagement />;
            case 'products':
                return <ProductManagement />;
            case 'import':
                return (
                    <section id="import" className="content-section active">
                        <div className="section-header">
                            <h1>Importar Productos</h1>
                        </div>
                        <div className="import-card">
                            <div className="import-icon">
                                <i className="bi bi-file-earmark-spreadsheet"></i>
                            </div>
                            <h3>Importar desde Excel</h3>
                            <p>Carga masiva de productos desde archivos Excel (.xlsx, .xls)</p>

                            <div
                                className="upload-area"
                                id="uploadArea"
                                onClick={() => document.getElementById('fileInput').click()}
                                onDragOver={handleDragOver}
                                onDrop={handleDrop}
                            >
                                <i className="bi bi-cloud-upload"></i>
                                <p>Arrastra tu archivo aquí o haz clic para seleccionar</p>
                                <input
                                    type="file"
                                    id="fileInput"
                                    accept=".xlsx,.xls"
                                    hidden
                                    onChange={handleFileUpload}
                                />
                                <button className="btn btn-primary mt-3" onClick={(e) => { e.stopPropagation(); document.getElementById('fileInput').click(); }}>
                                    Seleccionar Archivo
                                </button>
                            </div>

                            <div className="mt-4">
                                <a href="#" className="btn btn-outline-secondary">
                                    <i className="bi bi-download"></i> Descargar Plantilla
                                </a>
                            </div>

                            <div className="alert alert-info mt-4">
                                <i className="bi bi-info-circle"></i>
                                <strong>Formato requerido:</strong> El archivo debe contener las columnas: SKU, Nombre, Editorial, Stock, Bodega, Precio
                            </div>
                        </div>
                    </section>
                );
            case 'export':
                return (
                    <section id="export" className="content-section active">
                        <div className="section-header">
                            <h1>Exportar Base de Datos</h1>
                        </div>
                        <div className="row g-4">
                            <div className="col-lg-6">
                                <div className="export-card">
                                    <div className="export-icon">
                                        <i className="bi bi-file-earmark-excel"></i>
                                    </div>
                                    <h3>Exportar a Excel</h3>
                                    <p>Descarga todos los datos en formato Excel (.xlsx)</p>
                                    <button className="btn btn-success">
                                        <i className="bi bi-download"></i> Descargar Excel
                                    </button>
                                </div>
                            </div>
                            <div className="col-lg-6">
                                <div className="export-card">
                                    <div className="export-icon">
                                        <i className="bi bi-database"></i>
                                    </div>
                                    <h3>Respaldo SQL</h3>
                                    <p>Genera un respaldo completo de la base de datos</p>
                                    <button className="btn btn-primary">
                                        <i className="bi bi-download"></i> Descargar SQL
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>
                );
            default:
                return null;
        }
    };

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <div className={`sidebar ${isSidebarOpen ? 'mobile-visible' : ''}`} id="sidebar">
                <div className="sidebar-header">
                    <i className="bi bi-boxes"></i>
                    <span className="sidebar-title">InventoryPro</span>
                </div>

                <nav className="sidebar-nav">
                    <button className={`nav-item ${activeSection === 'overview' ? 'active' : ''}`} onClick={() => navigateToSection('overview')}>
                        <i className="bi bi-grid-fill"></i>
                        <span>Panel Principal</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'users' ? 'active' : ''}`} onClick={() => navigateToSection('users')}>
                        <i className="bi bi-people-fill"></i>
                        <span>Gestión de Usuarios</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'warehouses' ? 'active' : ''}`} onClick={() => navigateToSection('warehouses')}>
                        <i className="bi bi-building"></i>
                        <span>Gestión de Bodegas</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'publishers' ? 'active' : ''}`} onClick={() => navigateToSection('publishers')}>
                        <i className="bi bi-bookmark-fill"></i>
                        <span>Gestión de Editoriales</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'products' ? 'active' : ''}`} onClick={() => navigateToSection('products')}>
                        <i className="bi bi-box-seam"></i>
                        <span>Gestión de Productos</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'import' ? 'active' : ''}`} onClick={() => navigateToSection('import')}>
                        <i className="bi bi-file-earmark-arrow-up"></i>
                        <span>Importar Productos</span>
                    </button>
                    <button className={`nav-item ${activeSection === 'export' ? 'active' : ''}`} onClick={() => navigateToSection('export')}>
                        <i className="bi bi-file-earmark-arrow-down"></i>
                        <span>Exportar Base de Datos</span>
                    </button>
                </nav>

                <div className="sidebar-footer">
                    <button onClick={handleLogout} className="logout-btn">
                        <i className="bi bi-box-arrow-left"></i>
                        <span>Cerrar Sesión</span>
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="main-content">
                {/* Header */}
                <header className="dashboard-header">
                    <button className="menu-toggle" id="menuToggle" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                        <i className="bi bi-list"></i>
                    </button>

                    <div className="header-content">
                        <div className="search-bar">
                            <i className="bi bi-search"></i>
                            <input type="text" placeholder="Buscar..." />
                        </div>

                        <div className="header-actions">
                            <button className="icon-btn">
                                <i className="bi bi-bell"></i>
                                <span className="badge">3</span>
                            </button>

                            <div className="user-menu">
                                <img src="https://ui-avatars.com/api/?name=Admin&background=random" alt="Usuario" className="user-avatar" />
                                <div className="user-info">
                                    <span className="user-name">Jefe de Bodega</span>
                                    <span className="user-role">Administrador</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Content Area */}
                <div className="content-area">
                    {renderContent()}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
