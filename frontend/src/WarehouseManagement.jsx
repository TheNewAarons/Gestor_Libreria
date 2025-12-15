import React, { useState, useEffect } from 'react';

const WarehouseManagement = () => {
    const [warehouses, setWarehouses] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [currentWarehouse, setCurrentWarehouse] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [formData, setFormData] = useState({
        nombre: '',
        direction: '',
        tipo_de_contenido: '',
        capacidad: '', // Can be empty/null
        tamaño_bodega: '' // Can be empty/null
    });

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            alert("No hay sesión activa.");
            return;
        }
        fetchWarehouses();
    }, [token]);

    const fetchWarehouses = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/bodegas/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setWarehouses(data);
            }
        } catch (error) {
            console.error('Error fetching warehouses:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar esta bodega?')) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/bodegas/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                fetchWarehouses();
            } else {
                const errorData = await response.json();
                // Backend might return validation error if not empty
                alert('Error: ' + (errorData.detail || JSON.stringify(errorData)));
            }
        } catch (error) {
            console.error('Error deleting warehouse:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = currentWarehouse
            ? `http://127.0.0.1:8000/api/v1/bodegas/${currentWarehouse.id}/`
            : 'http://127.0.0.1:8000/api/v1/bodegas/';

        const method = currentWarehouse ? 'PUT' : 'POST';

        // Clean data: convert empty strings to null for optional integers if needed, 
        // essentially make sure numbers are numbers or null
        const dataToSend = { ...formData };
        if (dataToSend.capacidad === '') delete dataToSend.capacidad;
        if (dataToSend.tamaño_bodega === '') delete dataToSend.tamaño_bodega;

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(dataToSend)
            });

            if (response.ok) {
                setShowModal(false);
                fetchWarehouses();
                resetForm();
            } else {
                const errorData = await response.json();
                alert('Error: ' + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error('Error saving warehouse:', error);
        }
    };

    const handleEdit = (warehouse) => {
        setCurrentWarehouse(warehouse);
        setFormData({
            nombre: warehouse.nombre,
            direction: warehouse.direction,
            tipo_de_contenido: warehouse.tipo_de_contenido,
            capacidad: warehouse.capacidad || '',
            tamaño_bodega: warehouse.tamaño_bodega || ''
        });
        setShowModal(true);
    };

    const resetForm = () => {
        setCurrentWarehouse(null);
        setFormData({
            nombre: '',
            direction: '',
            tipo_de_contenido: '',
            capacidad: '',
            tamaño_bodega: ''
        });
        setShowModal(false);
    };

    const filteredWarehouses = warehouses.filter(w =>
        w.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        w.direction.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <section id="warehouses" className="content-section active">
            <div className="section-header">
                <h1>Gestión de Bodegas</h1>
                <button className="btn btn-primary" onClick={() => { resetForm(); setShowModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Nueva Bodega
                </button>
            </div>

            <div className="data-table-card">
                <div className="table-header">
                    <div className="search-box">
                        <i className="bi bi-search"></i>
                        <input
                            type="text"
                            placeholder="Buscar bodegas..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="table-responsive">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Dirección</th>
                                <th>Contenido</th>
                                <th>Stock</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredWarehouses.map(warehouse => (
                                <tr key={warehouse.id}>
                                    <td>
                                        <div className="d-flex align-items-center">
                                            <div className="icon-circle bg-light me-2">
                                                <i className="bi bi-building text-primary"></i>
                                            </div>
                                            {warehouse.nombre}
                                        </div>
                                    </td>
                                    <td>{warehouse.direction}</td>
                                    <td>{warehouse.tipo_de_contenido}</td>
                                    <td>
                                        <div className="d-flex align-items-center">
                                            <div className="progress flex-grow-1 me-2" style={{ height: '6px', width: '80px' }}>
                                                <div
                                                    className={`progress-bar ${warehouse.nivel_stock > (warehouse.capacidad || 1000) * 0.9 ? 'bg-danger' : 'bg-success'
                                                        }`}
                                                    style={{ width: `${Math.min((warehouse.nivel_stock / (warehouse.capacidad || 100)) * 100, 100)}%` }}
                                                ></div>
                                            </div>
                                            <small>{warehouse.nivel_stock}</small>
                                        </div>
                                    </td>
                                    <td>
                                        <span className={`badge ${warehouse.estado === 'VA' ? 'bg-secondary' :
                                                warehouse.estado === 'OC' ? 'bg-success' : 'bg-warning'
                                            }`}>
                                            {warehouse.estado === 'VA' ? 'Vacío' :
                                                warehouse.estado === 'OC' ? 'Ocupado' : 'Mantenimiento'}
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleEdit(warehouse)}>
                                            <i className="bi bi-pencil"></i>
                                        </button>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleDelete(warehouse.id)}>
                                            <i className="bi bi-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Modal */}
            {showModal && (
                <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">{currentWarehouse ? 'Editar Bodega' : 'Nueva Bodega'}</h5>
                                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
                            </div>
                            <form onSubmit={handleSubmit}>
                                <div className="modal-body">
                                    <div className="mb-3">
                                        <label className="form-label">Nombre</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            required
                                            value={formData.nombre}
                                            onChange={e => setFormData({ ...formData, nombre: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Dirección</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            required
                                            value={formData.direction}
                                            onChange={e => setFormData({ ...formData, direction: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Tipo de Contenido</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            required
                                            placeholder="ej. Libros Escolares"
                                            value={formData.tipo_de_contenido}
                                            onChange={e => setFormData({ ...formData, tipo_de_contenido: e.target.value })}
                                        />
                                    </div>
                                    <div className="row">
                                        <div className="col-md-6 mb-3">
                                            <label className="form-label">Capacidad (Unidades)</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={formData.capacidad}
                                                onChange={e => setFormData({ ...formData, capacidad: e.target.value })}
                                            />
                                        </div>
                                        <div className="col-md-6 mb-3">
                                            <label className="form-label">Tamaño (m²)</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={formData.tamaño_bodega}
                                                onChange={e => setFormData({ ...formData, tamaño_bodega: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancelar</button>
                                    <button type="submit" className="btn btn-primary">Guardar</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
};

export default WarehouseManagement;
