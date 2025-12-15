import React, { useState, useEffect } from 'react';

const ProductManagement = () => {
    const [products, setProducts] = useState([]);
    const [publishers, setPublishers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [currentProduct, setCurrentProduct] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [formData, setFormData] = useState({
        title: '',
        tipo: 'Libro',
        tamaño: '',
        cantidad: 0,
        editorial: '',
        description: '',
        portada: null // File object
    });

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            alert("No hay sesión activa.");
            return;
        }
        fetchProducts();
        fetchPublishers();
    }, [token]);

    const fetchProducts = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/libros/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setProducts(data);
            }
        } catch (error) {
            console.error('Error fetching products:', error);
        } finally {
            setIsLoading(false);
        }
    };

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
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar este producto?')) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/libros/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                fetchProducts();
            } else {
                alert('Error al eliminar producto');
            }
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = currentProduct
            ? `http://127.0.0.1:8000/api/v1/libros/${currentProduct.id}/`
            : 'http://127.0.0.1:8000/api/v1/libros/';

        const method = currentProduct ? 'PUT' : 'POST';

        // Use FormData for file upload
        const data = new FormData();
        data.append('title', formData.title);
        data.append('tipo', formData.tipo);
        if (formData.tamaño) data.append('tamaño', formData.tamaño);
        data.append('cantidad', formData.cantidad);
        data.append('editorial', formData.editorial);
        data.append('description', formData.description);
        if (formData.portada instanceof File) {
            data.append('portada', formData.portada);
        }

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Token ${token}`
                    // Do NOT set Content-Type header when sending FormData; 
                    // fetch will set it automatically with boundary inside
                },
                body: data
            });

            if (response.ok) {
                setShowModal(false);
                fetchProducts();
                resetForm();
            } else {
                const errorData = await response.json();
                alert('Error: ' + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error('Error saving product:', error);
        }
    };

    const handleEdit = (product) => {
        setCurrentProduct(product);
        setFormData({
            title: product.title,
            tipo: product.tipo,
            tamaño: product.tamaño || '',
            cantidad: product.cantidad,
            editorial: product.editorial, // ID of editorial
            description: product.description,
            portada: null // Don't preload file, user must re-upload if changing
        });
        setShowModal(true);
    };

    const resetForm = () => {
        setCurrentProduct(null);
        setFormData({
            title: '',
            tipo: 'Libro',
            tamaño: '',
            cantidad: 0,
            editorial: '',
            description: '',
            portada: null
        });
        setShowModal(false);
    };

    const filteredProducts = products.filter(p =>
        p.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const getEditorialName = (id) => {
        const ed = publishers.find(p => p.id === id);
        return ed ? ed.name : 'Desconocida';
    };

    return (
        <section id="products" className="content-section active">
            <div className="section-header">
                <h1>Gestión de Productos</h1>
                <button className="btn btn-primary" onClick={() => { resetForm(); setShowModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Nuevo Producto
                </button>
            </div>

            <div className="data-table-card">
                <div className="table-header">
                    <div className="search-box">
                        <i className="bi bi-search"></i>
                        <input
                            type="text"
                            placeholder="Buscar productos..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="table-responsive">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Portada</th>
                                <th>Título</th>
                                <th>Tipo</th>
                                <th>Editorial</th>
                                <th>Stock</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredProducts.map(product => (
                                <tr key={product.id}>
                                    <td>
                                        {product.portada ? (
                                            <img src={product.portada} alt="Portada" style={{ width: '40px', height: '60px', objectFit: 'cover' }} />
                                        ) : (
                                            <div className="bg-light d-flex align-items-center justify-content-center" style={{ width: '40px', height: '60px' }}>
                                                <i className="bi bi-book text-muted"></i>
                                            </div>
                                        )}
                                    </td>
                                    <td>{product.title}</td>
                                    <td>{product.tipo}</td>
                                    <td>{getEditorialName(product.editorial)}</td>
                                    <td>
                                        <span className={`badge ${product.cantidad < 10 ? 'bg-danger' : 'bg-primary'}`}>
                                            {product.cantidad}
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`badge ${product.estadoLibro === 'Publicado' ? 'bg-success' :
                                                product.estadoLibro === 'Denegado' ? 'bg-danger' : 'bg-warning'
                                            }`}>
                                            {product.estadoLibro || 'N/A'}
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleEdit(product)}>
                                            <i className="bi bi-pencil"></i>
                                        </button>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleDelete(product.id)}>
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
                    <div className="modal-dialog modal-lg">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">{currentProduct ? 'Editar Producto' : 'Nuevo Producto'}</h5>
                                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
                            </div>
                            <form onSubmit={handleSubmit}>
                                <div className="modal-body">
                                    <div className="row">
                                        <div className="col-md-6 mb-3">
                                            <label className="form-label">Título</label>
                                            <input
                                                type="text"
                                                className="form-control"
                                                required
                                                value={formData.title}
                                                onChange={e => setFormData({ ...formData, title: e.target.value })}
                                            />
                                        </div>
                                        <div className="col-md-6 mb-3">
                                            <label className="form-label">Tipo</label>
                                            <select
                                                className="form-select"
                                                value={formData.tipo}
                                                onChange={e => setFormData({ ...formData, tipo: e.target.value })}
                                            >
                                                <option value="Libro">Libro</option>
                                                <option value="Revista">Revista</option>
                                                <option value="Enciclopedias">Enciclopedias</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div className="row">
                                        <div className="col-md-6 mb-3">
                                            <label className="form-label">Editorial</label>
                                            <select
                                                className="form-select"
                                                required
                                                value={formData.editorial}
                                                onChange={e => setFormData({ ...formData, editorial: e.target.value })}
                                            >
                                                <option value="">Seleccionar Editorial...</option>
                                                {publishers.map(pub => (
                                                    <option key={pub.id} value={pub.id}>{pub.name}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="col-md-3 mb-3">
                                            <label className="form-label">Cantidad</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                required
                                                value={formData.cantidad}
                                                onChange={e => setFormData({ ...formData, cantidad: e.target.value })}
                                            />
                                        </div>
                                        <div className="col-md-3 mb-3">
                                            <label className="form-label">Tamaño (Páginas)</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={formData.tamaño}
                                                onChange={e => setFormData({ ...formData, tamaño: e.target.value })}
                                            />
                                        </div>
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Descripción</label>
                                        <textarea
                                            className="form-control"
                                            rows="3"
                                            value={formData.description}
                                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                                        ></textarea>
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Portada</label>
                                        <input
                                            type="file"
                                            className="form-control"
                                            accept="image/*"
                                            onChange={e => setFormData({ ...formData, portada: e.target.files[0] })}
                                        />
                                        {currentProduct && currentProduct.portada && (
                                            <div className="form-text">
                                                Actualmente: <a href={currentProduct.portada} target="_blank" rel="noreferrer">Ver Portada</a>. Subir nueva para reemplazar.
                                            </div>
                                        )}
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

export default ProductManagement;
