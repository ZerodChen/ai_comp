import client from './client';

export const getConnections = () => client.get('/connections/');
export const createConnection = (data) => client.post('/connections/', data);
export const getConnection = (id) => client.get(`/connections/${id}`);
export const getConnectionSchema = (id) => client.get(`/connections/${id}/schema`);
