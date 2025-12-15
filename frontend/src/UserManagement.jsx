import React, { useState, useEffect } from 'react';

const UserManagement = () => {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [currentUser, setCurrentUser] = useState(null); // For edit mode
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        rol: 'Bodeguero'
    });
    const [searchTerm, setSearchTerm] = useState('');

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            console.error("No token found, redirecting to login");
            // Optional: navigate('/login');
            // But since this is a component inside Dashboard, maybe Dashboard handles it.
            // For now, let's just log it.
            alert("No hay sesión activa. Por favor inicie sesión nuevamente.");
            return;
        }
        fetchUsers();
    }, [token]);

    // Filter users based on search term
    const filteredUsers = users.filter(user =>
        user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const fetchUsers = async () => {
        if (!token) return;

        console.log("Fetching users with token:", token);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/users/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setUsers(data);
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Estás seguro de eliminar este usuario?')) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            if (response.ok) {
                fetchUsers();
            } else {
                alert('Error al eliminar usuario');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = currentUser
            ? `http://127.0.0.1:8000/api/v1/users/${currentUser.id}/`
            : 'http://127.0.0.1:8000/api/v1/users/';

        const method = currentUser ? 'PUT' : 'POST';

        // Remove password if empty in edit mode
        const dataToSend = { ...formData };
        if (currentUser && !dataToSend.password) {
            delete dataToSend.password;
        }

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
                fetchUsers();
                resetForm();
            } else {
                const errorData = await response.json();
                alert('Error: ' + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error('Error saving user:', error);
        }
    };

    const handleEdit = (user) => {
        setCurrentUser(user);
        setFormData({
            username: user.username,
            email: user.email,
            password: '', // Password empty on edit
            rol: user.rol
        });
        setShowModal(true);
    };

    const resetForm = () => {
        setCurrentUser(null);
        setFormData({ username: '', email: '', password: '', rol: 'Bodeguero' });
        setShowModal(false);
    };

    return (
        <section id="users" className="content-section active">
            <div className="section-header">
                <h1>Gestión de Usuarios</h1>
                <button className="btn btn-primary" onClick={() => { resetForm(); setShowModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Nuevo Usuario
                </button>
            </div>

            <div className="data-table-card">
                <div className="table-header">
                    <div className="search-box">
                        <i className="bi bi-search"></i>
                        <input
                            type="text"
                            placeholder="Buscar usuarios por nombre o email..."
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
                                <th>Email</th>
                                <th>Rol</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredUsers.map(user => (
                                <tr key={user.id}>
                                    <td>#{user.id}</td>
                                    <td>{user.username}</td>
                                    <td>{user.email}</td>
                                    <td>
                                        <span className={`badge ${user.rol === 'Jefe de Bodega' ? 'bg-danger' :
                                            user.rol === 'Bodeguero' ? 'bg-primary' : 'bg-success'
                                            }`}>
                                            {user.rol}
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleEdit(user)}>
                                            <i className="bi bi-pencil"></i>
                                        </button>
                                        <button className="btn btn-sm btn-icon" onClick={() => handleDelete(user.id)}>
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
                                <h5 className="modal-title">{currentUser ? 'Editar Usuario' : 'Nuevo Usuario'}</h5>
                                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
                            </div>
                            <form onSubmit={handleSubmit}>
                                <div className="modal-body">
                                    <div className="mb-3">
                                        <label className="form-label">Nombre de Usuario</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            required
                                            value={formData.username}
                                            onChange={e => setFormData({ ...formData, username: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Email</label>
                                        <input
                                            type="email"
                                            className="form-control"
                                            required
                                            value={formData.email}
                                            onChange={e => setFormData({ ...formData, email: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Contraseña {currentUser && '(Dejar en blanco para mantener)'}</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            required={!currentUser}
                                            value={formData.password}
                                            onChange={e => setFormData({ ...formData, password: e.target.value })}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Rol</label>
                                        <select
                                            className="form-select"
                                            value={formData.rol}
                                            onChange={e => setFormData({ ...formData, rol: e.target.value })}
                                        >
                                            <option value="Bodeguero">Bodeguero</option>
                                            <option value="Jefe de Bodega">Jefe de Bodega</option>
                                            <option value="Autor">Autor</option>
                                        </select>
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

export default UserManagement;
