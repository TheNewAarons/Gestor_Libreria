import React, { useState, useEffect } from 'react';

const PublisherManagement = () => {
    const [publishers, setPublishers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [currentPublisher, setCurrentPublisher] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [formData, setFormData] = useState({
        name: '',
        address: '',
        phone: ''
    });

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            alert("No hay sesión activa.");
            return;
        }
        fetchPublishers();
    }, [token]);

    const fetchPublishers = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/editoriales/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setPublishers(data);
            }
        } catch (error) {
            console.error('Error fetching publishers:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar esta editorial?')) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/editoriales/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                fetchPublishers();
            } else {
                const errorData = await response.json();
                // Most likely "No se puede eliminar..." verification error
                alert('Error: ' + (errorData[0] || JSON.stringify(errorData)));
            }
        } catch (error) {
            console.error('Error deleting publisher:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = currentPublisher
            ? `http://127.0.0.1:8000/api/v1/editoriales/${currentPublisher.id}/`
            : 'http://127.0.0.1:8000/api/v1/editoriales/';

        const method = currentPublisher ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                setShowModal(false);
                fetchPublishers();
                resetForm();
            } else {
                const errorData = await response.json();
                alert('Error: ' + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error('Error saving publisher:', error);
        }
    };

    const handleEdit = (publisher) => {
        setCurrentPublisher(publisher);
        setFormData({
            name: publisher.name,
            address: publisher.address,
            phone: publisher.phone || ''
        });
        setShowModal(true);
    };

    const resetForm = () => {
        setCurrentPublisher(null);
        setFormData({
            name: '',
            address: '',
            phone: ''
        });
        setShowModal(false);
    };

    const filteredPublishers = publishers.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.address.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <section id="publishers" className="content-section active">
            <div className="section-header">
                <h1>Gestión de Editoriales</h1>
                <button className="btn btn-primary" onClick={() => { resetForm(); setShowModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Nueva Editorial
                </button>
            </div>

            <div className="data-table-card">
                <div className="table-header">
                    <div className="search-box">
                        <i className="bi bi-search"></i>
                        <input
                            type="text"
                            placeholder="Buscar editoriales..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="table-responsive">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nombre</th>
                                <th>Dirección</th>
                                <th>Teléfono</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredPublishers.map(publisher => (
                                <tr key={publisher.id}>
                                    <td>#{publisher.id}</td>
                                    <td>
                                        <div className="d-flex align-items-center">
                                            <div className="icon-circle bg-light me-2">
                                                <i className="bi bi-bookmark text-primary"></i>
                                            </div>
                                            {publisher.name}
                                        </div>
                                    </td>
                                    <td>{publisher.address}</td>
                                    <td>{publisher.phone || 'N/A'}</td>
                                    <td>
                                        <span className="badge bg-success">Activa</span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleEdit(publisher)}>
                                            <i className="bi bi-pencil"></i>
                                        </button>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleDelete(publisher.id)}>
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
                                <h5 className="modal-title">{currentPublisher ? 'Editar Editorial' : 'Nueva Editorial'}</h5>
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
                                            value={formData.name}
                                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Dirección</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            required
                                            value={formData.address}
                                            onChange={e => setFormData({ ...formData, address: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Teléfono</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={formData.phone}
                                            onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                        />
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

export default PublisherManagement;
